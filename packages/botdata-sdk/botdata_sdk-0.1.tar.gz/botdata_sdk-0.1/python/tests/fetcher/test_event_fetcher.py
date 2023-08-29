import sys
import os

# Add the library directory of the core module to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fetcher.event_fetcher import fetch_events_by_record, fetch_events

def test_fetch_events_by_record():
    record_id = 123
    event_name = "example_event"
    begin_time = 1629511200
    end_time = 1631000000

    events = fetch_events_by_record(record_id, event_name, begin_time, end_time)

    assert len(events) == 2
    assert events[0]["record_id"] == None
    assert events[0]["event_name"] == None
    # Add more assertions to validate specific conditions if needed

def test_fetch_events():
    event_name = "example_event"
    begin_time = 1629511200
    end_time = 1631000000

    events = fetch_events(event_name, begin_time, end_time)

    assert len(events) == 2
    assert events[0]["event_name"] == None
    # Add more assertions to validate specific conditions if needed
