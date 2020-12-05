#!/usr/bin/env python3
# pylint: disable=all
import socket
from multiprocessing.managers import BaseManager
from app.config_loader import load_config


def is_open(addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(addr)
        s.close()
        return True
    except ConnectionRefusedError:
        return False


def available_servers():
    servers = load_config('processing_servers')
    avail = [tuple(i) for i in servers if is_open(tuple(i))]
    if not avail:
        raise RuntimeError('No servers available')
    return avail


class DataProcessingManager(BaseManager):
    pass


DataProcessingManager.register('cpu_count')
DataProcessingManager.register('filter_main')


def connect_servers():
    """
    Connect to all available running server instances
    :return:
    """
    avail = available_servers()
    connections = []
    for i in avail:
        connections.append(DataProcessingManager(address=i, authkey=b'processing'))

    for c in connections:
        c.connect()

    return connections
