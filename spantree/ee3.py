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


class ParameterErr(Exception):
    pass


# Convert toolkits
def readoneONTStatus(input):
    # print(input)
    lst = input.split()
    #  F/ S/P   ONT         SN         Control     Run      Config   Match    Protect
    return [int(lst[2]), str(lst[5]), str(lst[6]), str(lst[7])]


def readoneONTOpticsInfo(input):
    lst = input.split()
    # ONT  Rx power    Tx power    OLT Rx ONT  Temperature  Voltage     Current
    lstm = [None if a == "-" else float(a) for a in lst]
    lstm[0] = int(lstm[0])
    return lstm


def convertDataToDict(input):
    dictz = {"id": input[0],
            "RunState": input[1],
            "ConfigState": input[2],
            "MatchState": input[3],
            "1490rx": input[4],
            "1310tx": input[5],
            "1310rx": input[6],
            "1550rx": None,
            "Temp": input[7],
            "Volt": input[8],
            "Current": input[9]
            }
    return dictz


# sys.argv = [sys.argv[0], "10.238.168.46", "0/0/0"]


# format checking
if (len(sys.argv) != 3):
    print("Invalid arguments number")
    exit(4)

ip = sys.argv[1]
fsp = sys.argv[2]
fspList = fsp.strip().split("/")

if ((len(fspList) != 3)):
    print("Bad command format")
    exit(4)

# IP = OLT'S IP ADDRESS
# FSP = FRME/SLOT/PORT

# ARRAY
ontlistSecond = []
tempList2On = []
tempListoff = []

grandONTlist = []

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
    print("Timeout!!!!")
    exit(2)
else:
    pass
    # print("Telnet connect established ")

tn.read_until(b"Unauthorized")
#print("Accessing SAM-BB")
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


#tn.read_until(b">>User name:")
tn.write(USER2 + b"\n")
tn.read_until(b"password:")
tn.write(PW2 + b"\n")

time.sleep(2)
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

tn.read_very_eager()
# ###############################################
time.sleep(0.5)
tn.write(b"\n")
time.sleep(0.5)
oltIDraw = tn.read_very_eager().decode("ascii").strip()
oltID = oltIDraw.rstrip(">")
tn.write(b"en\nundo sm\nscr\n")
time.sleep(1)
tn.read_very_eager()

try:
    tn.write(('display ont info ' + fspList[0] + ' ' + fspList[1] + ' ' + fspList[2] + ' all | count\n').encode('ascii'))
    time.sleep(2)
    z = tn.expect([b"CTRL_C to break\r\n",b"Parameter error"])
    if (z[0] == 1):
        print("Parameter error")
        raise ParameterErr
    linecount = tn.read_very_eager().decode("ascii").strip()
    if (linecount.split()[2]) == u"1.":
        raise NoBoardError
except NoBoardError:
    print("No board exist or no ONT on this port " + sys.argv[2])
    tn.read_very_eager()
    tn.write(b'q\ny\nq\n')
    time.sleep(0.5)
    exit(3)
except ParameterErr:
    print("Parameter error on command: "+ 'display ont info ' + fspList[0] + ' ' + fspList[1] + ' ' + fspList[2] + ' all')
    tn.write(b'q\ny\nq\n')
    time.sleep(0.5)
    exit(3)
else:
    pass


tn.write(('display ont info ' + fspList[0] + ' ' + fspList[1] + ' ' + fspList[2] + ' all | include online\n').encode(
    'ascii'))
time.sleep(2)
tn.read_until(b"CTRL_C to break\r\n")

raw = tn.read_very_eager().decode("ascii")
tmp = raw.split("\r\n")
for l in tmp[:-3]:
    l = l.strip()
    # print(readoneONTStatus(l))
    tempList2On.append(readoneONTStatus(l))

tn.read_very_eager()

tn.write(('display ont info ' + fspList[0] + ' ' + fspList[1] + ' ' + fspList[2] + ' all | include offline\n').encode(
    'ascii'))
time.sleep(1)
tn.read_until(b"CTRL_C to break\r\n")
raw2 = tn.read_very_eager().decode("ascii")
tmp2 = raw2.split("\r\n")
# print(raw2)
for l in tmp2[:-2]:
    l = l.strip()
    tempListoff.append(readoneONTStatus(l))
# tn.interact()
tn.read_very_eager()

tn.write(b"config\n")
tn.write(('int gpon ' + fspList[0] + '/' + fspList[1] + '\n').encode('ascii'))
tn.read_very_eager().decode("ascii")
tn.write(("display ont optical-info " + fspList[2] + " all | count\n").encode('ascii'))
time.sleep(3)
tn.read_until(b"CTRL_C to break")
count = tn.read_very_eager().decode("ascii")
oinf2 = re.findall(r'\d+', count)
rcount = oinf2[0]
ontcount = int(rcount) - 5

# print('Getting ONTs Information')
tn.write(("display ont optical-info " + fspList[2] + " all\n").encode('ascii'))
# print(tn.read_very_eager().decode("ascii"))
time.sleep(2)
for i in range(0, 5):
    tn.read_until(b"\n")
for i in range(0, int(rcount) - 5):
    rawstr = tn.read_until(b"\n").decode("ascii")
    z = readoneONTOpticsInfo(rawstr)
    ontlistSecond.append(z)

tn.read_very_eager()

tn.write(b"display port state 0 | include TX power\n")
time.sleep(2)
tn.read_until(b"CTRL_C to break\r\n")
oltTXPWR = tn.read_until(b"\n").decode("ascii").strip()
tn.read_very_eager()

oltpower = oltTXPWR.split()[2]

#print("OLT TX power: " + oltpower)

if len(tempList2On) != len(ontlistSecond):
    raise Exception("Mismatched table len")
for i in range(len(tempList2On)):
    z = tempList2On[i] + ontlistSecond[i][1:]
    # print(z)
    grandONTlist.append(z)
for i in tempListoff:
    grandONTlist.append(i + [None] * 6)
grandONTlist.sort()

'''
print("-" * 80)
print('{:<3s}{:>9s}{:>9s}{:>9s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}'.format("ID", "RunState", "Conf-ST", "Match-ST",
                                                                            "1490rx", "1310tx",
                                                                            "1310rx", "Temp", "Volt", "mAmp"))
for i in grandONTlist:
    if i[4] != None:
        print(
            '{:<3d}{:>9s}{:>9s}{:>9s}{:>8.2f}{:>8.2f}{:>8.2f}{:>8d}{:>8.2f}{:>8d}'.format(i[0], i[1], i[2], i[3], i[4],
                                                                                          i[5], i[6], int(i[7]), i[8],
                                                                                          int(i[9])))
    elif i[6] != None:
        print('{:<3d}{:>9s}{:>9s}{:>9s}{:>8s}{:>8s}{:>8.2f}{:>8s}{:>8s}{:>8s}'.format(i[0], i[1], i[2], i[3], "NONE",
                                                                                      "NONE", i[6], "NONE", "NONE",
                                                                                      "NONE"))
    else:
        print('{:<3d}{:>9s}{:>9s}{:>9s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}'.format(i[0], i[1], i[2], i[3], "NONE",
                                                                                    "NONE", "NONE", "NONE", "NONE",
                                                                                    "NONE"))
print("-" * 80)
'''

ontListJson = [convertDataToDict(x) for x in grandONTlist]
grandDict = {"OLT_ID": oltID,
             "1490tx:": float(oltpower),
             "portID": int(fspList[2]),
             "ONTs": ontListJson}

print(json.dumps(grandDict))

tn.write(b"return\n")
time.sleep(0.2)
tn.write(b"quit\n")
tn.read_until(b"Are you sure to log out? (y/n)[n]:")
tn.write(b"y\n")

time.sleep(0.2)
tn.read_until(b"Enter IP address [press q/Q to quit]: ")
tn.write(b"q\n")

time.sleep(0.2)
tn.read_very_eager().decode("ascii").strip()
tn.close()

# print("Done")
