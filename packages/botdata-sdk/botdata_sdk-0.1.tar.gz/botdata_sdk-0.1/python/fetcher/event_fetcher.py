import copy

def fetch_events_by_record(record_id, event_name, begin_time, end_time):
    """
    Get list of events from event table by querying event_name with a timespan of event published time.
    This query specify event happened on a single record_id

    Args:
        event_name (string): event name
        begin_time (int): the begin time of timespan towards event published_time
        end_time (int): the end time of timespan towards event published_time

    Returns:
        events (list[dict]): a list of event records
    """
    event_dict = {
          "event_id": None,
          "record_id": None,
          "event_type": None,
          "event_name": None,
          "event_start_time": None,
          "event_end_time": None,
          "context": None,
    }
    another_event_dict = copy.deepcopy(event_dict)

    event_dicts = []
    event_dicts.append(event_dict)
    event_dicts.append(another_event_dict)
    return event_dicts

def fetch_events(event_name, begin_time, end_time):
    """
    Get list of events from event table by querying event_name with a timespan of event published time.
    This query doens't specify record_id

    Args:
        event_name (string): event name
        begin_time (int): the begin time of timespan towards event published_time
        end_time (int): the end time of timespan towards event published_time

    Returns:
        events (list[dict]): a list of event records
    """
    event_dict = {
          "event_id": None,
          "record_id": None,
          "event_type": None,
          "event_name": None,
          "event_start_time": None,
          "event_end_time": None,
          "context": None,
    }
    another_event_dict = copy.deepcopy(event_dict)

    event_dicts = []
    event_dicts.append(event_dict)
    event_dicts.append(another_event_dict)
    return event_dicts
