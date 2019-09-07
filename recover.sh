#!/bin/bash
ip link set wlp3s0 down
iwconfig wlp3s0 mode managed
ip link set wlp3s0 up
service network-manager restart