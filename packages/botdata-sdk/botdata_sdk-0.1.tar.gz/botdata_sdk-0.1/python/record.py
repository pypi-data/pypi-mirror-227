from protobuf.grpc_generated.botdata_pb2 import Record, SingleMessage, Frame, Segment, Channel, Event
from protobuf.grpc_generated.botdata_pb2 import FrameList, SegmentList, EventList, MessageList

from fetcher.message_fetcher import fetch_message
from fetcher.event_fetcher import fetch_events_by_record
from fetcher.segment_fetcher import fetch_segments

def get_message(self,
                timestamp,
                channel_name,
                message_alignment_option="MAX_TIMESTAMP"
                ):
    """
    Get a message by the timestamp, channel, and query option,

    Args:
        timestamp (int): the timestamp of message to fetch message
        channel (string): channel full name
        message_alignment_option (string): EXACT_TIMESTAMP is to lookup by exact time
            or MAX_TIMESTAMP is to lookup last published timestamp close to request time

    Returns:
        message (SingleMessage)
    """
    proto_desc, published_time, received_time, message_content = fetch_message(
        self.record_id,
        timestamp,
        message_alignment_option,
        channel_name
        )

    channel = Channel(
        name=channel_name,
        message_type="",
        proto_desc=proto_desc
    )

    message = SingleMessage(
        channel=channel,
        received_time=received_time,
        published_time=published_time,
        content=message_content
    )

    return message

def iterate_messages(self,
                     channel_list,
                     begin_time,
                     end_time,
                     sampler="FREQUENCY_SAMPLER"
                     ):
    """
    Get an iterator of messages by providing the channel_list, and the timespan in the record.
    A sampler method is also provided to use for different sampling algorithm

    Args:
        channel_list (list[string]): channel full name
        begin_time (int): the begin time of timespan towards message published_time
        end_time (int): the end time of timespan towards message published_time
        sampler (string): FREQUENCY_SAMPLER is to sampling by certain frequency e.g. 50hz -> every 20ms
            or DEBUG_SAMPLER is to lookup messages with exact published time per channel

    Returns:
        message (Message): iterator of messages
    """
    if sampler == 'FREQUENCY_SAMPLER':
        step = int(2e7)
        timestamp_list = [ts for ts in range(begin_time, end_time, step)]

    for channel in channel_list:
        for timestamp in timestamp_list:
            message = self.get_message(timestamp, channel, message_alignment_option="MAX_TIMESTAMP")
            yield message

def list_messages(self,
                  channel_list,
                  begin_time,
                  end_time,
                  sampler="FREQUENCY_SAMPLER"
                  ):
    """
    Get a list message by providing the channel_list, and the timespan in the record.
    A sampler method is also provided to use for different sampling algorithm

    Args:
        channel_list (list[string]): channel full name
        begin_time (int): the begin time of timespan towards message published_time
        end_time (int): the end time of timespan towards message published_time
        sampler (string): FREQUENCY_SAMPLER is to sampling by certain frequency e.g. 50hz -> every 20ms
            or DEBUG_SAMPLER is to lookup messages with exact published time per channel

    Returns:
        message_list (MessageList)
    """
    if sampler == 'FREQUENCY_SAMPLER':
        step = int(2e7)
        timestamp_list = [ts for ts in range(begin_time, end_time, step)]

    message_list = MessageList()
    for channel in channel_list:
        for timestamp in timestamp_list:
            message = self.get_message(timestamp, channel, message_alignment_option="MAX_TIMESTAMP")
            message_list.message_list.append(message)

    return message_list

def get_frame(self,
              channel_list,
              callback_time,
              ):
    """
    Get a frame of messages (per channel) by providing the channel_list, and the callback time in the record.

    Args:
        channel_list (list[string]): channel full name
        callback_time (int): the callback time for the frame

    Returns:
        frame (Frame)
    """
    message_list = MessageList()
    frame = Frame(
        callback_time=callback_time,
        message_list=message_list
    )

    for channel in channel_list:
        message = self.get_message(callback_time, channel, message_alignment_option="MAX_TIMESTAMP")
        message_list.message_list.append(message)
    return frame

def iterate_frames(self,
                channel_list,
                callback_time_list
                ):
    """
    Get an iterator frames with callback time list in the record, where each frame has messages (per channel) by providing the channel_list.
    The expected output is a list of frame objects, the length of list is same as the list of callback time

    Args:
        channel_list (list[string]): channel full name
        callback_time_list (list[int]): a list of the callback time for the each frame
        lazy_fetch (bool): True means returning an iterator, False means returning a frame_list (FrameList) object

    Returns:
        frame (Frame): iterator of frame
    """
    for callback_time in callback_time_list:
        frame = self.get_frame(channel_list, callback_time)
        yield frame


def list_frames(self,
                channel_list,
                callback_time_list
                ):
    """
    Get an iterator frames with callback time list in the record, where each frame has messages (per channel) by providing the channel_list.
    The expected output is a list of frame objects, the length of list is same as the list of callback time

    Args:
        channel_list (list[string]): channel full name
        callback_time_list (list[int]): a list of the callback time for the each frame
        lazy_fetch (bool): True means returning an iterator, False means returning a frame_list (FrameList) object

    Returns:
        frame_list (FrameList)
    """
    frame_list = FrameList()
    for callback_time in callback_time_list:
        frame = self.get_frame(channel_list, callback_time)
        frame_list.frame_list.append(frame)
    return frame_list

def list_segments(self,
                  begin_time,
                  end_time):
    """
        In the same record_id, find all segments within timespan of published time.
        The function returns any segment file that containers any message that were published within the timespan
        If record.storage_type == "S3" then it will look for s3 path
        If record.storage_type == "DATA_CENTER" then it will look for data center storage path

    Args:
        begin_time (int): the begin time of timespan towards message published_time
        end_time (int): the end time of timespan towards message published_time

    Returns:
        segment_list (SegmentList)
    """

    segment_dicts = fetch_segments(self.record_id, begin_time, end_time, self.storage_type)
    print(segment_dicts)
    segment_list = SegmentList()
    for segment_dict in segment_dicts:
        segment = Segment(
            segment_id=segment_dict["segment_id"],
            segment_path=segment_dict["segment_path"]
        )
        segment_list.segment_list.append(segment)

    return segment_list

def list_events(self,
                event_name,
                begin_time,
                end_time):
    """
    Get a list of events associated with the record by providing the event_name, and timespan

    Args:
        event_name (string): the event_name
        begin_time (int): the begin time of timespan towards event published_time
        end_time (int): the end time of timespan towards event published_time

    Returns:
        event_list (EventList)
    """

    event_dicts =  fetch_events_by_record(self.record_id, event_name, begin_time, end_time)

    event_list = EventList()
    for event_dict in event_dicts:
        event = Event(
            event_id=event_dict["event_id"],
            event_type=event_dict["event_type"],
            event_name=event_dict["event_name"],
            event_start_time=event_dict["event_start_time"],
            event_end_time=event_dict["event_end_time"],
            context=event_dict["context"]
        )
        event_list.event_list.append(event)

    return event_list

# Attach the custom method to the generated message class
Record.get_message = get_message
Record.list_messages = list_messages
Record.iterate_messages = iterate_messages
Record.get_frame = get_frame
Record.list_frames = list_frames
Record.iterate_frames = iterate_frames
Record.list_segments = list_segments
Record.list_events = list_events
