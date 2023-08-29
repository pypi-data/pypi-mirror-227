import sys
import os

# Add the library directory of the core module to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.message_dynamic_deserializer import deserialize_message

def test_deserialize_message():
    proto_desc = b"your_protobuf_definition_bytes"
    message_content = b"your_message_bytes"

    message = deserialize_message(proto_desc, message_content)

    assert message is None
    # Add more assertions to validate specific conditions if needed
