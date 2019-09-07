from scapy.all import *
from sys import argv
from scapy.layers.bluetooth import *
from scapy.layers.dot11 import *
from Dot11Handler import Dot11Handler
from wirelesswatch.dot11 import SignalEntry

devices = {}
linemap = {}


def enter_monitor_mode(p_interface: str):
    os.system(
        'service network-manager stop && '
        'ip link set ' + p_interface + ' down && '
        'iwconfig ' + p_interface + ' mode monitor && '
        'ip link set ' + p_interface + ' up')


def handle_bt_packet(p_packet: HCI_Hdr):
    if p_packet.haslayer(HCI_LE_Meta_Advertising_Reports):
        reports = p_packet[HCI_LE_Meta_Advertising_Reports].reports
        report: HCI_LE_Meta_Advertising_Report
        for report in reports:
            mac = report.addr
            if mac not in devices:
                devices[mac] = []
                print('New device spotted: ' + mac)

interface = argv[1]
if os.geteuid() != 0:
    print('Run as root')
    exit(-1)

# bt = BluetoothHCISocket(0)
# bt.sr(HCI_Hdr()/HCI_Command_Hdr()/HCI_Cmd_LE_Set_Scan_Parameters(type=1))
# bt.sr(HCI_Hdr()/HCI_Command_Hdr()/HCI_Cmd_LE_Set_Scan_Enable(enable=True, filter_dups=False))
# bt.sniff(prn=handle_bt_packet)
enter_monitor_mode(interface)






fig = plt.figure()
ax = fig.add_subplot(111)
fig.canvas.draw()
plt.show(block=False)


def signal_callback(mac: str, signal_entry: SignalEntry):
    if mac not in linemap:
        line, = ax.plot([], [])
        line.set_label(mac)
        fig.legend()
        linemap[mac] = [[], [], line]
    xdata = linemap[mac][0]
    ydata = linemap[mac][1]
    xdata.append(signal_entry.timestamp)
    ydata.append(signal_entry.signal)
    line = linemap[mac][2]
    line.set_xdata(xdata)
    line.set_ydata(ydata)
    linemap[mac][0] = xdata
    linemap[mac][1] = ydata
    ax.relim()
    ax.autoscale_view(True, True, True)
    fig.canvas.draw()
    fig.canvas.flush_events()


dot11handler = Dot11Handler(signal_callback)


def handle_packet(p_packet: Packet):
    dot11handler.handle_packet(p_packet)


channel = 1
#for channel in range(1, 14):
while True:
    print('sniffing channel ' + str(channel))
    os.system('iwconfig ' + interface + ' channel ' + str(channel))
    sniff(timeout=5, prn=handle_packet, iface=interface)
