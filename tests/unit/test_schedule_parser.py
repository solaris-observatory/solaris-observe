from solaris_observe.core import schedule

def test_parse_schedule():
    result = schedule.parse_schedule('dummy.lis')
    assert 'file' in result
