import socket   #for sockets
import sys

try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
print 'Socket Created'

host = '192.168.0.33'
port = 8810

#Connect to remote server
s.connect((host , port))

print 'Socket Connected to ' + host

while 1:
    try:
        msg = raw_input("> ")
        s.sendall(msg)
        rep = s.recv(4096)
        print rep

    except socket.error:
        print "socket error"
        break

    except KeyboardInterrupt:
        print "User cancelled"
        break

    except:
        print "some other error"
        break
