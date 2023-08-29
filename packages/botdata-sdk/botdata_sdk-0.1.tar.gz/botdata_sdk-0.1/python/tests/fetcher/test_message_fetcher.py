import sys
import os

# Add the library directory of the core module to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fetcher.message_fetcher import fetch_message

def test_fetch_message_exact_timestamp():
    record_id = 123
    timestamp = 1629511200
    message_alignment_option = "EXACT_TIMESTAMP"
    channel = "example_channel"

    proto_desc, published_time, received_time, message_content = fetch_message(record_id, timestamp, message_alignment_option, channel)

    assert proto_desc is None
    assert published_time is None
    assert received_time is None
    assert message_content is None
    # Add more assertions to validate specific conditions if needed

def test_fetch_message_max_timestamp():
    record_id = 456
    timestamp = 1631000000
    message_alignment_option = "MAX_TIMESTAMP"
    channel = "another_channel"

    proto_desc, published_time, received_time, message_content = fetch_message(record_id, timestamp, message_alignment_option, channel)

    assert proto_desc is None
    assert published_time is None
    assert received_time is None
    assert message_content is None
    # Add more assertions to validate specific conditions if needed
