from datetime import datetime
from typing import List


class Spot:
    def __init__(self, transmitter: str, receiver: str, sig: int, time: datetime, frame_type: int, frame_subtype: int, channel: int, transmitter_name: str):
        self.transmitter: str = transmitter
        self.receiver: str = receiver
        self.sig: int = sig
        self.time: datetime = time
        self.frame_type: int = frame_type
        self.frame_subtype: int = frame_subtype
        self.channel: int = channel
        self.transmitter_name: str = transmitter_name


class Station:
    def __init__(self, mac: str):
        self.mac: str = mac
        self.names: List[str] = [mac]
        self.spots: List[Spot] = []
