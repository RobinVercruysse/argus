from scapy.layers.dot11 import *
from wirelesswatch.model import Spot


class Dot11Handler:
    @staticmethod
    def build_spot(channel: int, packet: Packet):
        if not packet.haslayer(Dot11FCS) or not packet.haslayer(RadioTap):
            return None
        packet_type = packet.type
        packet_subtype = packet.subtype
        radiotap = packet[RadioTap]
        time = radiotap.time
        signal = None
        if hasattr(radiotap, 'dBm_AntSignal'):
            signal = radiotap.dBm_AntSignal
        if signal is None:
            signal = 0
        transmitter_name = None
        if packet_type == 0 and packet_subtype == 5:
            # probe response
            transmitter_name = packet.info
        elif packet_type == 0 and packet_subtype == 8:
            # beacon
            transmitter_name = packet.info
        if packet.addr1 != 'ff:ff:ff:ff:ff:ff':
            receiver = packet.addr1
        else:
            receiver = None
        return Spot(packet.addr2, receiver, signal, time, packet_type, packet_subtype, channel, transmitter_name)
