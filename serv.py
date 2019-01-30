import socket
import sys
 
HOST = '192.168.43.45'   # Symbolic name meaning all available interfaces
PORT = 8888              # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
try:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'
 
#wait to accept a connection - blocking call
conn, addr = s.accept()
 
#display client information
print 'Connected with ' + addr[0] + ':' + str(addr[1])

while 1:
    try:
        data = conn.recv(4096)
        print "recvd " + data
        rep = "got " + data
        conn.sendall(rep)

    except socket.error:
        print "socket error"
        break

    except KeyboardInterrupt:
        print "User cancelled"
        break

    except:
        print "some other error"
        break

conn.close()
s.close()
sys.exit()
