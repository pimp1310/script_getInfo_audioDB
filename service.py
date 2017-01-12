
# while not xbmc.abortRequested and not SomeReasonIWantToStopFor:
    # do(myThing)
    
    
# RunScript(serveice.whatever)

# xbmcaddon.Addon(id) 



# yes, that was what I meant.
# Maybe it is possible, maybe xbmcaddon.Addon(id) will get you the instance if exists. 

# Meanwhile I am considering if it is possible to use xbmcaddon.Addon(id).setsetting. 
# I have not used it before but it may take care of this.

# If you have an addon with a service and a program extension.

# Where the service do:
# while (not xbmc.abortRequested and xbmcaddon.Addon(id).getSetting("service_enabled") == "true"


# and the program have a button that do
# xbmcaddon.Addon(id).setSetting("service_enabled", "false") 


# I cant test it right now...






# A service is just a regular addon that can be run at either startup or login. If you don't have a while loop, the service addon will exit just like any other addon.

# I think the best way to manage state is by an addon setting which is not visible to the user. The you can call getSetting and setSetting to manage state. Then check that setting in each iteration of your while loop. If the setting is false, exit the while loop and the service addon will die. To start it again, call RunPlugin('plugin://service.whatever.mynameis/?key=value')

# Any addon can call any other addon's getSetting and setSetting methods








# SOCKETS

# Echo server program
import socket

HOST = '127.0.0.1'
PORT = 50100
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(1024)
    if not data: break
    conn.sendall(data)
conn.close()



select([sock],[],[],0) 



# Echo client program
import socket

HOST = '127.0.0.1'    # The remote host
PORT = 50100              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('Hello, world')
data = s.recv(1024)
s.close()
print 'Received', repr(data)