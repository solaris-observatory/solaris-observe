from solaris_observe.runner import schedule_runner

def test_run_schedule_sim():
    schedule_runner.run_schedule('dummy.lis', driver='sim')
