import sys
import os

# Add the library directory of the core module to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fetcher.segment_fetcher import fetch_segments

def test_fetch_segments():
    record_id = 123
    begin_time = 1629511200
    end_time = 1631000000
    storage_type = "DATA_CENTER"

    segments = fetch_segments(record_id, begin_time, end_time, storage_type)

    assert len(segments) == 2
    assert segments[0]["segment_id"] is None
    assert segments[0]["segment_path"] is None
    # Add more assertions to validate specific conditions if needed
