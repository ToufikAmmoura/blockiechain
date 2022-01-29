import socket
import sys
import threading
import time
import traceback

def thread_debug(msg):
    thread = str(threading.currentThread().getName())
    print(f'{thread}, {msg}')

class Peer:
    def __init__(self, serverport, serverhost):
        self.serverport = serverport
        self.serverhost = serverhost
        
        self.peers = {}
        self.shutdown = False

    def __debug(self, msg):
        thread_debug(msg)

    def make_server_socket(self, port, backlog):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind('', port)
        s.listen(backlog)
        return s

    def add_peer(self, peer_id, host, port):
        if peer_id not in self.peers:
            self.peers[peer_id] = (host, int(port))
            return True
        else:
            return False
        
    def main_loop(self):
        s = self.make_server_socket(self.serverport)
        s.settimeout(2)
        self.__debug(f'Server started: {self.serverhost}, {self.serverport}')

        while not self.shutdown:
            try:
                self.__debug('Listening for connections...')  
                client_socket, client_addr = s.accept()
                client_socket.settimeout(None)

                t = threading.Thread(target = self.__handlepeer, args = [ client_socket ])
                t.start()
            except KeyboardInterrupt:
                print('KeyboardInterrupt: stopping mainloop')
                self.shutdown = True
            except:
                traceback.print_exc()
                continue
        
        self.__debug('Main loop exiting')
        s.close()

# def server():
#     serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     serv.bind(('0.0.0.0', 8080))
#     serv.listen(5)
#     while True:
#         conn, addr = serv.accept()
#         from_client = b''
#         while True:
#             data = conn.recv(4096)
#             if not data: break
#             from_client += data
#             print(from_client.decode())
#             conn.send("I am SERVER".encode())
#         conn.close()
#         print('client disconnected')
    
# def client(message):
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect(('0.0.0.0', 8080))
#     client.send(message.encode())
#     from_server = client.recv(4096)
#     client.close()
#     print(from_server.decode())

# if __name__ == "__main__":
#     task = sys.argv[1]
#     if task == 'client':
#         message = sys.argv[2]
#         client(message)
#     else:
#         server()
