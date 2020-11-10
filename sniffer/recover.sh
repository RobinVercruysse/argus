#!/bin/bash
ip link set $1 down
iwconfig $1 mode managed
ip link set $1 up