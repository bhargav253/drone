import socket   #for sockets
import XboxController
import sys
import time

#tests
if __name__ == '__main__':

    #generic call back
    def controlCallBack(xboxControlId, value):
        print "Control Id = {}, Value = {}".format(xboxControlId, value)

    #specific callbacks for the left thumb (X & Y)
    def leftThumbX(value):    
        msg = 'LX,' + str(value) + ";"
        s.sendall(msg)

    def leftThumbY(value):
        msg = 'LY,' + str(value) + ";"
        s.sendall(msg)

    def rightThumbX(value):
        msg = 'RX,' + str(value) + ";"
        s.sendall(msg)

    def rightThumbY(value):
        msg = 'RY,' + str(value) + ";"
        s.sendall(msg)

    def aTrigger(value):
        msg = 'AT,' + str(value) + ";"
        s.sendall(msg)

    def bTrigger(value):
        msg = 'BT,' + str(value) + ";"
        s.sendall(msg)
    
    #setup xbox controller, set out the deadzone and scale, also invert the Y Axis (for some reason in Pygame negative is up - wierd! 
    xboxCont = XboxController.XboxController(controlCallBack, deadzone = 30, scale = 100, invertYAxis = True)

    #setup the left thumb (X & Y) callbacks
    xboxCont.setupControlCallback(xboxCont.XboxControls.LTHUMBX, leftThumbX)
    xboxCont.setupControlCallback(xboxCont.XboxControls.LTHUMBY, leftThumbY)
    xboxCont.setupControlCallback(xboxCont.XboxControls.RTHUMBX, rightThumbX)
    xboxCont.setupControlCallback(xboxCont.XboxControls.RTHUMBY, rightThumbY)
    xboxCont.setupControlCallback(xboxCont.XboxControls.A, aTrigger)
    xboxCont.setupControlCallback(xboxCont.XboxControls.B, bTrigger)

    try:
        #create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        sys.exit();
    
    print 'Socket Created'
        
    host = '192.168.1.191'
    port = 8787

    #Connect to remote server
    s.connect((host , port))

    print 'Socket Connected to ' + host

    try:
        #start the controller
        xboxCont.start()
        print "xbox controller running"
        while True:
            time.sleep(1)

    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"
    
    except socket.error:
        print "socket error"

    #error        
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
        
    finally:
        #stop the controller
        xboxCont.stop()
        s.close()
