from inspect import trace
import sys
import socket
import struct
from tempfile import TemporaryFile
import threading
import time
import traceback

def thread_debug(msg):
    thread = str(threading.currentThread().getName())
    print(f'{thread}, {msg}')

class Peer:
    def __init__(self, serverport, serverhost, debug=False):
        self.serverport = serverport
        self.serverhost = serverhost
        
        self.my_id = f'{serverhost}:{serverport}'
        self.debug = debug
        
        self.peerlock = threading.Lock()

        self.peers = {}
        self.shutdown = False
        self.handlers = {}
        self.router = None


    def __debug(self, msg):
        thread_debug(msg)

    def make_server_socket(self, port, backlog=5):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind('', port)
        s.listen(backlog)
        return s

    def __handle_peer(self, client_socket):
        self.__debug( 'New child ' + str(threading.currentThread().getName()) )
        self.__debug( 'Connected ' + str(client_socket.getpeername()) )

        host, port = client_socket.getpeername()
        peer_conn = PeerConnection(None, host, port, client_socket, debug=False)

        try:
            msg_type, msg_data = peer_conn.recv_data()
            if msg_type: msg_type = msg_type.upper()
            if msg_type not in self.handlers:
                self.__debug('Not handled: %s: %s', (msg_type, msg_data))
            else:
                self.__debug( 'Handling peer msg: %s: %s' % (msg_type, msg_data) )
            self.handlers[ msg_type ]( peer_conn, msg_data )
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
        
        self.__debug( 'Disconnecting ' + str(client_socket.getpeername()) )
        peer_conn.close()


    def add_handler(self, msg_type, handler):
        assert len(msg_type) ==  4
        self.handlers[msg_type] = handler

    
    def add_router(self, router):
        self.router = router

    def add_peer(self, peer_id, host, port):
        if peer_id not in self.peers:
            self.peers[peer_id] = (host, int(port))
            return True
        else:
            return False
    
    def get_peer(self, peer_id):
        assert peer_id in self.peers
        return self.peers[peer_id]
    
    def remove_peer(self, peer_id):
        if peer_id in self.peers:
            del self.peers[peer_id]
        
    def add_peer_at(self, loc, peer_id, host, port):
        self.peers[loc] = (peer_id, host, int(port))
    
    def get_peer_at(self, loc):
        if loc not in self.peers:
            return None
        return self.peers[loc]

    def remove_peer_at(self, loc):
        self.remove_peer(loc)
    
    def get_peer_ids(self):
        return self.peers.keys()
    
    def number_of_peers(self):
        return len(self.peers)
        
    def send_to_peer(self, peer_id, msg_type, msg_data, wait_reply=True):
        if self.router:
            next_pid, host, port = self.router(peer_id)
        if not self.router or not next_pid:
            self.__debug(f'Unabel to route %{msg_type} to %{peer_id}')
            return None
        return self.connect_and_send (host, port, msg_type, msg_data,
                                      pid=next_pid,
                                      wait_reply=wait_reply)

    def connect_and_send(self, host, port, msg_type, msg_data, pid=None, wait_reply=True):
        msg_reply = []
        try:
            peer_conn = PeerConnection(pid, host, port, debug=self.debug)
            peer_conn.send_data(msg_type, msg_data)
            self.__debug(f'Sent {pid}: {msg_type}')

            if wait_reply:
                one_reply = peer_conn.recv_data()
                while (one_reply != (None, None)):
                    msg_reply.append(one_reply)
                    self.__debug(f'Got reply {pid}: {str(msg_reply)}')
                    one_reply = peer_conn.recv_data()
                peer_conn.close()
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
            
        return msg_reply

    def check_live_peers(self):
        to_delete = []
        for pid in self.peers:
            is_connected = False
            try:
                self.__debug(f'Check live {pid}')
                host, port = self.peers[pid]
                peer_conn = PeerConnection(pid, host, port, debug=self.debug)
                peer_conn.send_data('PING', '')
                is_connected = True
            except:
                to_delete(pid)
                if is_connected:
                    peer_conn.close()

        self.peerlock.acquire()
        try:
            for pid in to_delete:
                if pid in self.peers:
                    del self.peers[pid]
        finally:
            self.peerlock.release()

    def main_loop(self):
        s = self.make_server_socket(self.serverport)
        s.settimeout(2)
        self.__debug(f'Server started: {self.serverhost}, {self.serverport}')

        while not self.shutdown:
            try:
                self.__debug('Listening for connections...')  
                client_socket, client_addr = s.accept()
                client_socket.settimeout(None)

                t = threading.Thread(target = self.__handle_peer, args = [ client_socket ])
                t.start()
            except KeyboardInterrupt:
                print('KeyboardInterrupt: stopping mainloop')
                self.shutdown = True
            except:
                if self.debug:
                    traceback.print_exc()
                continue
        
        self.__debug('Main loop exiting')
        s.close()

class PeerConnection:
    def __init__(self, peer_id, host, port, socket=None, debug=False):
        self.id = peer_id
        self.debug = debug

        if not socket:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host, int(port)))
        else:
            self.s = socket
        
        # ik weet nog niet wat dit doet lol
        self.sd = self.s.makefile('rw', 0)
    
    def __make_msg(self, msg_type, msg_data):
        msg_len = len(msg_data)
        msg = struct.pack("!4sL%ds",msg_len, msg_type, msg_len, msg_data)
        return msg

    def __debug(self, msg):
        if self.debut:
            thread_debug(msg)

    def send_data(self, msg_type, msg_data):
        try:
            msg = self.__make_msg(msg_type, msg_data)
            self.sd.write(msg)
            self.sd.flush()
        except KeyboardInterrupt:
            raise
        except:
            if self.debut:
                traceback.print_exc()
                return False
        return True
    
    def recv_data(self):
        try:
            msgtype = self.sd.read( 4 )
            if not msgtype: return (None, None)
            
            lenstr = self.sd.read( 4 )
            msglen = int(struct.unpack( "!L", lenstr )[0])
            msg = ""

            while len(msg) != msglen:
                data = self.sd.read( min(2048, msglen - len(msg)) )
                if not len(data):
                    break
                msg += data
            if len(msg) != msglen:
                return (None, None)

        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
                return (None, None)

        return ( msgtype, msg )

    def close(self):
        self.s.close()
        self.s = None
        self.sd = None

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
