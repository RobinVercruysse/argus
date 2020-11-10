from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel
from sys import argv
from pickle import loads
from scapy.all import plt
from wirelesswatch.model import Spot
from networkx import Graph, draw_networkx, draw, draw_networkx_labels, spring_layout
from matplotlib import figure, axes, pyplot

linemap = {}
fig: figure.Figure = plt.figure('Argus')
# ax: axes.Axes = fig.add_subplot(122)
# ax2: axes.Axes = fig.add_subplot(121)
ax: axes.Axes = fig.add_subplot(111)
canvas: figure.FigureCanvasBase = fig.canvas
canvas.draw()
plt.show(block=False)
username = argv[1]
password = argv[2]
connection = BlockingConnection(ConnectionParameters(
    host='::1',
    credentials=PlainCredentials(username=username, password=password)
))
channel: BlockingChannel = connection.channel()
channel.queue_declare(queue='spots', durable=True)
graph = Graph()
spots = []
names = {}


def callback(ch, method, properties, body: bytearray):
    spot: Spot = loads(body)
    if spot.transmitter is None or spot.sig == 0 and spot.receiver is not None:
        return
    # if spot.transmitter in names and spot.transmitter_name is not None and names[spot.transmitter] == spot.transmitter:
    #     names[spot.transmitter] = spot.transmitter_name.decode('UTF-8')
    # if spot.receiver is not None:
    #     if not graph.has_node(spot.transmitter):
    #         graph.add_node(spot.transmitter)
    #         if spot.transmitter_name is not None:
    #             names[spot.transmitter] = spot.transmitter_name.decode('UTF-8')
    #         else:
    #             names[spot.transmitter] = spot.transmitter
    #     if not graph.has_node(spot.receiver):
    #         graph.add_node(spot.receiver)
    #         names[spot.receiver] = spot.receiver
    #     graph.add_edge(u_of_edge=spot.transmitter, v_of_edge=spot.receiver)
    #     pos = spring_layout(graph)
    #     draw(G=graph, ax=ax2, pos=pos)
    #     draw_networkx_labels(G=graph, ax=ax2, labels=names, pos=pos)
    spots.append(spot)

    if len(spots) % 50 == 0:
        for spot in spots:
            graph.add_node(spot.transmitter)
            graph.add_node(spot.receiver)
        # graph.update(edges=[(spot.transmitter, spot.receiver) for spot in spots])
        draw_networkx(G=graph, with_labels=True, ax=ax)
        pyplot.show(block=False)
        canvas.draw()
        canvas.flush_events()
        spots.clear()
    #     draw_networkx(G=graph, with_labels=True)
    #     update_signal_ax()
    # canvas.draw()
    # canvas.flush_events()

    print(str(len(channel._pending_events)))


def update_signal_ax():
    for spot in spots:
        if spot.transmitter not in linemap:
            line, = ax.plot([], [])
            line.set_label(spot.transmitter)
            fig.legend()
            linemap[spot.transmitter] = [[], [], line]
        xdata = linemap[spot.transmitter][0]
        ydata = linemap[spot.transmitter][1]
        xdata.append(spot.time)
        ydata.append(spot.sig)
        line = linemap[spot.transmitter][2]
        line.set_xdata(xdata)
        line.set_ydata(ydata)
        linemap[spot.transmitter][0] = xdata
        linemap[spot.transmitter][1] = ydata
    ax.relim()
    ax.autoscale_view(True, True, True)
    spots.clear()


channel.basic_consume(queue='spots', on_message_callback=callback, auto_ack=True)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
