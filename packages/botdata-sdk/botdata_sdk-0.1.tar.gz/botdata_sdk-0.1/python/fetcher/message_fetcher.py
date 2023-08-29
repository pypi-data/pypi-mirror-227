def fetch_message(record_id, timestamp, message_alignment_option, channel):
    """
    Given record_id, timestamp, message_alignment_option, channel, the function will return channel and message binary data

    Args:
        record_id (int): record identification, it's the Cyber recorder's start time
        timestamp (int): the timestamp of message to fetch message, the timestamp to lookup is message's published timestamp
        channel (string): channel full name
        message_alignment_option (string): EXACT_TIMESTAMP is to lookup by exact time
            or MAX_TIMESTAMP is to lookup last published timestamp close to request time

    Returns:
        proto_desc (bytes): protobuf definition in bytes
        published_time (int): message publish time
        received_time (int): message received time by recorder
        message_content (bytes): message in bytes
    """
    proto_desc = None
    published_time = None
    received_time = None
    message_content = None

    return proto_desc, published_time, received_time, message_content
