import copy

def fetch_segments(record_id, begin_time, end_time, storage_type="DATA_CENTER"):
    """
    Given record_id, timespan of published time. The function returns any segment file that containers any message that were published within the timespan
    If storage_type == "S3" then it will look for s3 path
    If storage_type == "DATA_CENTER" then it will look for data center storage path

    Args:
        record_id (int): record identification, it's the Cyber recorder's start time
        begin_time (int): the begin time of timespan towards message published_time
        end_time (int): the end time of timespan towards message published_time
        storage_type (string): "S3" or "DATA_CENTER"

    Returns:
        segment_dicts (list[dict]): a list of segment files
    """
    segment_dict = {
          "segment_id": None,
          "segment_path": None,
    }
    another_segment_dict = copy.deepcopy(segment_dict)

    segment_dicts = []
    segment_dicts.append(segment_dict)
    segment_dicts.append(another_segment_dict)
    return segment_dicts
