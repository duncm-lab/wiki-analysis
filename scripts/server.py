#! /usr/bin/env python3
# Serves the data_processing module functions for remote execution
import os
from multiprocessing.managers import BaseManager
from app.data_processing import filter_main
import socket


server_ip = socket.gethostbyname(socket.gethostname())
server_port = 8900


class DataProcessingManager(BaseManager):
    pass


DataProcessingManager.register('filter_main', callable=lambda: filter_main())
DataProcessingManager.register('cpu_count', proxytype=int,
                               callable=lambda: os.cpu_count())
manager = DataProcessingManager(address=(server_ip, server_port),
                                authkey=b'processing')
server = manager.get_server()

if __name__ == '__main__':
    print(f'Multiprocessing Server {server_ip}:{server_port}')
    server.serve_forever()
