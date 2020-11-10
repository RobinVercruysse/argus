class Device:
    def __init__(self, mac):
        self.mac = mac
        self.frame_count = 0
        self.signal_entries = []


class SignalEntry:
    def __init__(self, timestamp, signal):
        self.timestamp = timestamp
        self.signal = signal


class BeaconSender:
    def __init__(self, mac, ssid):
        self.mac = mac
        self.ssid = ssid
        self.count = 0


class ProbeRequest:
    def __init__(self, target, sender, probe):
        self.target = target
        self.sender = sender
        self.probe = probe


class ProbeResponse:
    def __init__(self, receiver, sender, ssid):
        self.receiver = receiver
        self.sender = sender
        self.ssid = ssid


class BlockAckRequest:
    def __init__(self, addr1, addr2, load):
        self.addr1 = addr1
        self.addr2 = addr2
        self.load = load


class BlockAck:
    def __init__(self, addr1, addr2, load):
        self.addr1 = addr1
        self.addr2 = addr2
        self.load = load


class Disassociation:
    def __init__(self, addr1, addr2, reason):
        self.addr1 = addr1
        self.addr2 = addr2
        self.reason = reason


class Action:
    def __init__(self, addr1, addr2, load):
        self.addr1 = addr1
        self.addr2 = addr2
        self.load = load


class ReassocationResponse:
    def __init__(self, addr1, addr2):
        self.addr1 = addr1
        self.addr2 = addr2
