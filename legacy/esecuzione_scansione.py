"""
Execute schedule scans using serpentine RA rows at (effectively) fixed Dec.
This preserves the original behavior as closely as possible.
"""
import numpy as np
import time, pytz, sys, os, socket
import motor as drive
import convertitore_schedule as sched
from datetime import datetime, timedelta

LOCATION = 'TG'
UDP_IP = "192.168.1.5"
UDP_PORT = 1700
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Logging setup
t_now = datetime.now(pytz.UTC)
date_dir = 'LOGdir/' + str(t_now.strftime('%Y-%m-%d')) + '/'
if not os.path.isdir(date_dir):
    os.makedirs(date_dir)
log_name = 'log_' + str(t_now.strftime('%Y-%m-%dT%Hh%Mm%Ss')) + '.txt'
log_path = os.path.join(date_dir, log_name)
filelog = open(log_path, 'w')
filelog.write('N | DATETIME | POS-RAA | POS-DEC | POS-AZ | POS-EL | '
              'GIRI-AZ | GIRI-EL | VEL-AZ | VEL-EL\n')

# Load schedule
filename = sys.argv[1]
sched.schedule_to_matrix(filename)

# Initial approach to the first point (kept as in original spirit)
declination = sched.dec_0 + sched.offset_dec[0] - sched.delta_dec / 2
raascension = (sched.raa_0 + (sched.offset_raa[0] - sched.delta_raa / 2)
               / np.cos(np.radians(declination)))
el_deg, az_deg = sched.radec_to_elaz(raascension, declination, t_now, LOCATION)
giri_el_0 = 2668 - (90 - el_deg) * 100
giri_az_0 = (180 - 180 - 10 - 5 - 0.5 - 0.5 - (az_deg - 70)) * 100 + 3955

def drive_setup(waiting_seconds=30):
    print('\t1.1. Removing brakes and enabling motors')
    drive.brakes_remove(sock, UDP_IP, UDP_PORT)
    drive.abilita(sock, UDP_IP, UDP_PORT)
    print('\t1.2. Setting initial velocities')
    v_el = str(20000000)
    v_az = str(25000000)
    drive.set_velel(sock, UDP_IP, UDP_PORT, v_el)
    drive.set_velaz(sock, UDP_IP, UDP_PORT, v_az)
    print('\t1.3. Moving to first point')
    drive.mva_el(sock, UDP_IP, UDP_PORT, giri_el_0)
    drive.mva_az(sock, UDP_IP, UDP_PORT, giri_az_0)
    print('\t1.4. Sleeping to complete slew\n')
    time.sleep(waiting_seconds)

drive_setup()

print('Starting scans ...\n\n')
t_slew = 1
for i in range(sched.n_scan):
    print('Scan', str(i+1)+'/'+str(sched.n_scan), '\t',
          datetime.now(pytz.UTC).strftime('%Hh%Mm%Ss'))

    obs_time = datetime.now(pytz.UTC) + timedelta(seconds=t_slew)
    if i % 2 == 0:
        declination = sched.dec_0 + sched.offset_dec[i] - sched.delta_dec / 2
        raascension = (sched.raa_0 + (sched.offset_raa[i] - sched.delta_raa/2)
                       / np.cos(np.radians(declination)))
    else:
        declination = sched.dec_0 + sched.offset_dec[i] + sched.delta_dec / 2
        raascension = (sched.raa_0 + (sched.offset_raa[i] + sched.delta_raa/2)
                       / np.cos(np.radians(declination)))

    el_deg, az_deg = sched.radec_to_elaz(raascension, declination,
                                         obs_time, LOCATION)

    v_el = str(20000000)
    v_az = str(20000000)
    drive.set_velel(sock, UDP_IP, UDP_PORT, v_el)
    drive.set_velaz(sock, UDP_IP, UDP_PORT, v_az)

    giri_el_0 = 2668 - (90 - el_deg) * 100
    giri_az_0 = (180 - 180 - 10 - 5 - 0.5 - 0.5 - (az_deg - 70)) * 100 + 3955
    drive.mva_el(sock, UDP_IP, UDP_PORT, giri_el_0)
    drive.mva_az(sock, UDP_IP, UDP_PORT, giri_az_0)

    filelog.write(str(i+1) + ' | ' + str(obs_time.strftime('%Hh%Mm%Ss')) +
                  ' | ' + str(raascension) + ' | ' + str(declination) +
                  ' | ' + str(az_deg) + ' | ' + str(el_deg) + ' | ' +
                  str(giri_az_0) + ' | ' + str(giri_el_0) + ' | ' +
                  str(v_az) + ' | ' + str(v_el) + '\n')

    print('Waiting slew ...')
    time.sleep(t_slew)
    time.sleep(1)

    obs_time = datetime.now(pytz.UTC) + timedelta(seconds=sched.t_scan)
    if i % 2 == 0:
        declination = sched.dec_0 + sched.offset_dec[i] + sched.delta_dec / 2
        raascension = (sched.raa_0 + (sched.offset_raa[i] + sched.delta_raa/2)
                       / np.cos(np.radians(declination)))
    else:
        declination = sched.dec_0 + sched.offset_dec[i] - sched.delta_dec / 2
        raascension = (sched.raa_0 + (sched.offset_raa[i] - sched.delta_raa/2)
                       / np.cos(np.radians(declination)))

    el_deg, az_deg = sched.radec_to_elaz(raascension, declination,
                                         obs_time, LOCATION)

    giri_el_1 = 2668 - (90 - el_deg) * 100
    giri_az_1 = (180 - 180 - 10 - 5 - 0.5 - 0.5 - (az_deg - 70)) * 100 + 3955
    delta_giri_el = abs(giri_el_1 - giri_el_0)
    delta_giri_az = abs(giri_az_1 - giri_az_0)

    v_el = str(int(delta_giri_el * 8.544 * 10000 * 2 * np.pi / sched.t_scan))
    v_az = str(int(delta_giri_az * 8.544 * 10000 * 2 * np.pi / sched.t_scan))

    drive.set_velel(sock, UDP_IP, UDP_PORT, v_el)
    drive.set_velaz(sock, UDP_IP, UDP_PORT, v_az)
    drive.mva_el(sock, UDP_IP, UDP_PORT, giri_el_1)
    drive.mva_az(sock, UDP_IP, UDP_PORT, giri_az_1)

    filelog.write(str(i+1) + ' | ' + str(obs_time.strftime('%Hh%Mm%Ss')) +
                  ' | ' + str(raascension) + ' | ' + str(declination) +
                  ' | ' + str(az_deg) + ' | ' + str(el_deg) + ' | ' +
                  str(giri_az_1) + ' | ' + str(giri_el_1) + ' | ' +
                  str(v_az) + ' | ' + str(v_el) + '\n')

    print('Waiting scan ...\n')
    time.sleep(sched.t_scan)
    time.sleep(2)

sock.close()
filelog.close()
