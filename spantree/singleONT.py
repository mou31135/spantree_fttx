import json
import socket
import telnetlib
import time
import re
import sys

class NoBoardError(Exception):
    pass


class NoONTError(Exception):
    pass


class BadCommandException(Exception):
    pass

# format checking
if (len(sys.argv) != 4):
    print("Invalid arguments")
    exit(4)

ip = sys.argv[1]
fsp = sys.argv[2]
fspList = fsp.strip().split("/")
ontID = sys.argv[3]

if ((len(fspList) != 3)):
    print("Bad command format")
    exit(4)

# IP = OLT'S IP ADDRESS
# FSP = FRME/SLOT/PORT
# ONTID 

# TELNET1
HOST1 = "10.50.64.182"
USER1 = b"natt237"
PW1 = b"Stamp@123"

# TELNET2
OLTHOST = ip.encode("ascii")
USER2 = b"Natt237@clls"
#USER2 = b"Tuperine"
PW2 = b"Faii1/iam"

# Login#
try:
    tn = telnetlib.Telnet(HOST1, 0, 2)
except socket.timeout:
    print("First Host Timeout!!!!")
    exit(2)
except socket.error:
    print("An error occoured during telnet.")
    exit(2)
else:
    pass
    # print("Telnet connect established ")

tn.read_until(b"login: ")
tn.write(USER1 + b"\n")
tn.read_until(b"Password: ")
tn.write(PW1 + b"\n")
tn.read_until(b"Broadband Gateway")
#print("Access granted")
tn.read_until(b"Enter IP address [press q/Q to quit]: ")
tn.write(OLTHOST + b'\n')

time.sleep(2)
j = tn.expect([b'User name:',b'unreachable',b'timed out'],timeout = 2)
#print(j)

if(j[0] == 1):
    tn.read_very_eager()
    tn.write(b"q\n")
    print("SAM-BB:Host unreachable")
    exit(2)
elif(j[0] == -1 or j[0] == 2):
    tn.write('\x03'.encode('ascii'))
    tn.write(b"q\n")
    print("SAM-BB:Timeout, Connection closed")
    exit(2)
else:
    #print("IP OK")
    pass


tn.write(USER2 + b"\n")
tn.read_until(b"password:")
tn.write(PW2 + b"\n")

time.sleep(1)
j = tn.expect([b'Huawei',b'invalid'],timeout = 2)
#print(j)
if(j[0] == 1):
    tn.write('\x03'.encode('ascii'))
    tn.write(b"q\n")
    print("SAM-BB:Username or password invalid")
    exit(5)
elif(j[0] == -1):
    tn.write('\x03'.encode('ascii'))
    tn.write(b"q\n")
    print("SAM-BB:Timeout, Connection closed")
    exit(2)

tn.read_very_eager().decode("ascii")
# ###############################################

tn.write(b"en\nundo sm\nscr\n")
time.sleep(1)
tn.read_very_eager()

tn.write(b"config\n")
tn.write(('int gpon ' + fspList[0] + '/' + fspList[1] + '\r\n').encode('ascii'))
gponst = tn.expect([b'config-if-gpon-',b'Failure:'],timeout = 1)
#print(gponst)
tn.read_very_eager()


if(gponst[0] == 1):
    print("OLT:This board does not exist")
    
    tn.write(b"return\n")
    time.sleep(0.2)
    tn.write(b"q\n")
    tn.read_until(b"Are you sure to log out? (y/n)[n]:")
    tn.write(b"y\n")
    time.sleep(0.2)
    tn.read_until(b"Enter IP address [press q/Q to quit]: ")
    tn.write(b"q\n")
    time.sleep(0.2)
    tn.close()
    exit(3)
    
tn.read_very_eager()
time.sleep(1)

tn.write(('display ont optical-info '+fspList[2]+' '+ontID+' | include Rx optical\r\n').encode('ascii'))
tn.read_eager()
time.sleep(1)
j = tn.expect([b'CATV Rx optical power'],timeout = 1)
time.sleep(0.5)
if(j[0] == -1):
    
    print("OLT:The ONT does not exist")
    tn.close()
    exit(3)
    
else:
    info = tn.read_until(b"\r\n")
    infos =info.strip().split()
    outJSON = {"1550rx":float(infos[2])}
    print(json.dumps(outJSON))

    tn.write(b"return\n")
    time.sleep(0.2)
    tn.write(b"q\n")
    tn.read_until(b"Are you sure to log out? (y/n)[n]:")
    tn.write(b"y\n")
    time.sleep(0.2)
    tn.read_until(b"Enter IP address [press q/Q to quit]: ")
    tn.write(b"q\n")
    time.sleep(0.2)
    tn.close()
    exit(0)
    


