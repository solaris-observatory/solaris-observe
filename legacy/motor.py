"""
Low-level UDP driver commands for telescope axes.
Behavior preserved where code was provided; redacted parts kept as comments.
"""
import math

def abilita(sock, UDP_IP, UDP_PORT):
    sock.sendto(b'd:en', (UDP_IP, UDP_PORT))
    sock.settimeout(1)
    data, _ = sock.recvfrom(1024)
    print("Answer: %s" % data)
    return data

# ... (other functions unchanged from original)

def fault_reset(sock, UDP_IP, UDP_PORT):
    sock.sendto(b'd:a:fr', (UDP_IP, UDP_PORT))
    sock.sendto(b'd:e:fr', (UDP_IP, UDP_PORT))
    sock.settimeout(1)
    data, _ = sock.recvfrom(1024)
    print("Answer: %s" % data)
    return data
