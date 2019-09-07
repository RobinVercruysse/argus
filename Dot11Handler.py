from scapy.layers.dot11 import *
from wirelesswatch.dot11 import *


class Dot11Handler:
    def __init__(self, callback):
        self.callback = callback
        self.handlers = {
            0: {  # management
                0: self.handle_asso_req,
                1: self.handle_asso_resp,
                2: self.handle_reasso_req,
                3: self.handle_reasso_resp,
                4: self.handle_probe_req,
                5: self.handle_probe_resp,
                8: self.handle_beacon,
                9: self.handle_atim,
                10: self.handle_disas,
                11: self.handle_auth,
                12: self.handle_deauth,
                13: self.handle_action
            },
            1: {  # control
                5: self.handle_ndp_announcement,
                8: self.handle_block_ack_request,
                9: self.handle_block_ack,
                11: self.handle_rts,
                12: self.handle_cts,
                13: self.handle_ack
            },
            2: {  # data
                0: self.handle_data,
                4: self.handle_data,
                8: self.handle_data
            },
            3: {  # reserved

            }
        }
        self.beacon_senders = {}
        self.devices = {}
        self.probe_requests = {}
        self.probe_responses = {}
        self.block_ack_requests = []
        self.block_acks = []
        self.disassociations = []
        self.actions = []
        self.reassocation_responses = []

    def handle_packet(self, packet: Packet):
        if not packet.haslayer(Dot11FCS) or not packet.haslayer(RadioTap):
            return
        packet_type = packet.type
        packet_subtype = packet.subtype
        if packet_type in self.handlers:
            if packet_subtype in self.handlers[packet_type]:
                self.handlers[packet_type][packet_subtype](packet)
            else:
                packet.show()
                print('Unknown packet subtype ' + str(packet_type) + ':' + str(packet_subtype))
                #raise Exception('Unknown packet subtype ' + str(packet_subtype) +
                #                ' for packet type ' + str(packet_type))
        else:
            packet.show()
            print('Unknown packet type ' + str(packet_type))
            #raise Exception('Unknown packet type ' + str(packet_type))

    def handle_asso_req(self, packet: Packet):
        # TODO implement
        raise NotImplementedError()

    def handle_asso_resp(self, packet: Packet):
        # TODO implement
        raise NotImplementedError()

    def handle_reasso_req(self, packet: Packet):
        # TODO implement
        raise NotImplementedError()

    def handle_reasso_resp(self, packet: Packet):
        # TODO inspect
        self.reassocation_responses.append(ReassocationResponse(packet.addr1, packet.addr2))

    def handle_probe_req(self, packet: Packet):
        if not packet.haslayer(Dot11ProbeReq):
            packet.show()
            raise Exception('Probe request without Dot11ProbeReq layer :(')
        target = packet.addr1
        sender = packet.addr2
        probe = packet.info
        if sender not in self.probe_requests:
            self.probe_requests[sender] = []
        self.probe_requests[sender].append(ProbeRequest(target, sender, probe))
        self.log_frame(sender, packet[RadioTap])

    def handle_probe_resp(self, packet: Packet):
        if not packet.haslayer(Dot11ProbeResp):
            packet.show()
            raise Exception('Probe response without Dot11ProbeResp layer :(')
        sender = packet.addr2
        if sender not in self.probe_responses:
            self.probe_responses[sender] = ProbeResponse(receiver=packet.addr1, sender=sender, ssid=packet.info)
        self.log_frame(sender, packet[RadioTap])

    def handle_beacon(self, packet: Packet):
        mac = packet.addr2
        ssid = str(packet.info)
        if mac not in self.beacon_senders:
            self.beacon_senders[mac] = BeaconSender(mac, ssid)
        self.beacon_senders[mac].count += 1
        self.log_frame(mac, packet[RadioTap])

    def handle_atim(self, packet: Packet):
        # TODO implement
        raise NotImplementedError()

    def handle_disas(self, packet: Packet):
        # TODO inspect
        if not packet.haslayer(Dot11Disas):
            packet.show()
            raise Exception('Disassocation without Dot11Disas layer :(')
        self.disassociations.append(Disassociation(packet.addr1, packet.addr2, packet.reason))

    def handle_auth(self, packet: Packet):
        # TODO implement
        print('auth')

    def handle_deauth(self, packet: Packet):
        # TODO implement
        raise NotImplementedError()

    def handle_action(self, packet: Packet):
        # TODO figure out if packet contains interesting info, contains scapy.packet.Raw layer with "load" field
        self.actions.append(Action(packet.addr1, packet.addr2, packet.load))

    def handle_ndp_announcement(self, packet: Packet):
        # TODO implement
        print('ndp announcement')

    def handle_block_ack_request(self, packet: Packet):
        # TODO figure out if packet contains interesting info, contains scapy.packet.Raw layer with "load" field
        self.block_ack_requests.append(BlockAckRequest(packet.addr1, packet.addr2, packet.load))

    def handle_block_ack(self, packet: Packet):
        # TODO figure out if packet contains interesting info, contains scapy.packet.Raw layer with "load" field
        self.block_acks.append(BlockAck(packet.addr1, packet.addr2, packet.load))

    def handle_ack(self, packet: Packet):
        # TODO figure out if packet contains interesting info
        receiver = packet.addr1

    def handle_rts(self, packet: Packet):
        # TODO figure out if packet contains interesting info
        addr1 = packet.addr1
        addr2 = packet.addr2

    def handle_cts(self, packet: Packet):
        # TODO figure out if packet contains interesting info
        receiver = packet.addr1
        # if mac not in self.devices:
        #     self.devices[mac] = Device(mac)
        # self.devices[mac].spot_count += 1

    def handle_data(self, packet: Packet):
        # TODO figure out interesting data from data frames
        addr1 = packet.addr1
        addr2 = packet.addr2

    def log_frame(self, mac, radiotap: RadioTap):
        if mac not in self.devices:
            self.devices[mac] = Device(mac)
        self.devices[mac].frame_count += 1
        timestamp = radiotap.time
        signal = -1
        if hasattr(radiotap, 'dBm_AntSignal'):
            signal = radiotap.dBm_AntSignal
        signal_entry = SignalEntry(timestamp, signal)
        self.devices[mac].signal_entries.append(signal_entry)
        self.callback(mac, signal_entry)
        # x = np.linspace(0, 6*np.pi, 100)
        #        y = np.sin(x)
        #        fig = plt.figure()
        #        ax = fig.add_subplot(111)
        #        line1, = ax.plot(x, y, 'r-')
        #        #plt.xlabel('time')
        #        #plt.ylabel('signal strength')
        #        #plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
        #        for phase in np.linspace(0, 10*np.pi, 500):
        #            line1.set_ydata(np.sin(x + phase))
        #            fig.canvas.draw()
        #            fig.canvas.flush_events()
