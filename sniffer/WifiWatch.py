from scapy.all import *
from sys import argv
# from scapy.layers.bluetooth import *
from scapy.layers.dot11 import *
from Dot11Handler import Dot11Handler
from wirelesswatch.persistence import PersistenceController
from wirelesswatch.model import Spot


if os.geteuid() != 0:
    print('Run as root')
    exit(-1)
interface = argv[1]
persistenceController = PersistenceController(mysql_user=argv[2], mysql_password=argv[3], rabbitmq_user=argv[4], rabbitmq_password=argv[5])
# devices = {}
linemap = {}


def enter_monitor_mode(p_interface: str):
    os.system(
        'ip link set ' + p_interface + ' down && '
        'iwconfig ' + p_interface + ' mode monitor && '
        'ip link set ' + p_interface + ' up')


# def handle_bt_packet(p_packet: HCI_Hdr):
#     if p_packet.haslayer(HCI_LE_Meta_Advertising_Reports):
#         reports = p_packet[HCI_LE_Meta_Advertising_Reports].reports
#         report: HCI_LE_Meta_Advertising_Report
#         for report in reports:
#             mac = report.addr
#             if mac not in devices:
#                 devices[mac] = []
#                 print('New device spotted: ' + mac)



# bt = BluetoothHCISocket(0)
# bt.sr(HCI_Hdr()/HCI_Command_Hdr()/HCI_Cmd_LE_Set_Scan_Parameters(type=1))
# bt.sr(HCI_Hdr()/HCI_Command_Hdr()/HCI_Cmd_LE_Set_Scan_Enable(enable=True, filter_dups=False))
# bt.sniff(prn=handle_bt_packet)
enter_monitor_mode(interface)






# fig = plt.figure()
# ax = fig.add_subplot(111)
# fig.canvas.draw()
# plt.show(block=False)
current_channel = 0


def packet_callback(p_packet: Packet):
    spot: Spot = Dot11Handler.build_spot(current_channel, p_packet)
    if spot is None:
        return
    persistenceController.spot(spot)
    # if spot.transmitter is None or spot.sig == 0:
    #     return
    # if spot.transmitter not in linemap:
    #     line, = ax.plot([], [])
    #     line.set_label(spot.transmitter)
    #     fig.legend()
    #     linemap[spot.transmitter] = [[], [], line]
    # xdata = linemap[spot.transmitter][0]
    # ydata = linemap[spot.transmitter][1]
    # xdata.append(spot.time)
    # ydata.append(spot.sig)
    # line = linemap[spot.transmitter][2]
    # line.set_xdata(xdata)
    # line.set_ydata(ydata)
    # linemap[spot.transmitter][0] = xdata
    # linemap[spot.transmitter][1] = ydata
    # ax.relim()
    # ax.autoscale_view(True, True, True)
    # fig.canvas.draw()
    # fig.canvas.flush_events()


while True:
    for current_channel in range(1, 14):
        print('sniffing channel ' + str(current_channel))
        os.system('iwconfig ' + interface + ' channel ' + str(current_channel))
        sniff(timeout=None, prn=packet_callback, iface=interface)
