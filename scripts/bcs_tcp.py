import socket
import time
class connection:
    
    # initializer creates socket and binds to powell messenger port
    def __init__(self, tcp_addr, tcp_port, timeout):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.connect((tcp_addr,tcp_port))
        self.my_socket.settimeout(timeout)
        
    def ver(self):
        print("v0.1")
        
    def test(self):
        self.my_socket.sendall('ListCommands\r\n'.encode())
        print(self.my_socket.recv(8192).decode("utf-8"))
        
    def __getattr__(self, name):
        return lambda *argv : self.callTCP(name, argv)
    
    def stringify(self, argv):
        return '(' + ','.join([str(arg) for arg in argv]) + ')'
        
    def callTCP(self, name, argv):
        cmd = name.replace('_'," ") + self.stringify(argv)
        #print("Calling BCS function:",cmd)
        self.sendToSocket(cmd)
        return self.read()

    def sendToSocket(self,cmd):
        cmd+='\r\n'
        self.my_socket.sendall(cmd.encode())

    def wait_for_scan(self, timeout=1000000):
        if (timeout < 1):
            timeout = 1000000
        count = 0
        rscan = 'None'
        while ('None' in rscan) and (count < 2):
            self.my_socket.sendall('RunningScan\r\n'.encode())
            rscan = self.my_socket.recv(8192).decode("utf-8")
            time.sleep(1)
            count += 1
        while not('None' in rscan):
            self.my_socket.sendall('RunningScan\r\n'.encode())
            rscan = self.my_socket.recv(8192).decode("utf-8")
            time.sleep(1)
            count += 1
            if(count >= timeout):
                return False
        return True

    def read(self):
        #print("Reading. Waiting for data ...")
        rd = ''
        try:
            rd = self.my_socket.recv(8192).decode("utf-8")
            #print("Done. Got :"+rd+":")
        except:
            pass
        return rd