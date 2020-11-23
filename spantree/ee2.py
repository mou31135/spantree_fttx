import getpass
import sys
import socket
import telnetlib
import time
import re


# Class definition
class ONT:
    def __init__(self, id, runstate, configstate, matchingstate, rx1490, tx1310, rx1310, temp, volt, current):
        self.runstate = runstate
        self.configstate = configstate
        self.matchingstate = matchingstate
        self.id = id
        self.rx1490 = rx1490
        self.tx1310 = tx1310
        self.rx1310 = rx1310
        self.temp = temp
        self.volt = volt
        self.current = current

    def __lt__(self, other):
        return self.id < other.id

    def __str__(self):
        return "An ONT with ID: " + str(self.id)

    def showONTinfo(self):
        print(self.id, self.runstate, self.configstate, self.matchingstate, self.rx1490, self.tx1310, self.rx1310,
              self.temp, self.volt, self.current)


class OLTport:
    ontlist = []

    def __init__(self, id, tx1490, temp, voltage, current):
        self.id = id
        self.tx1490 = tx1490
        self.temp = temp
        self.voltage = voltage
        self.current = current

    def addONT(self, ont):
        self.ontlist.append(ont)

    def printall(self):
        print("List of all ONT")
        for i in self.ontlist:
            print(i)


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


a = ONT(1, "on", "N", "M", -20.0, 2.0, -20.0, 50, 2.0, 2.0)
b = ONT(5, "off", "I", "I", None, None, None, None, 2.0, 2.0)
c = OLTport(0, 2.1, 50, 2, 2)
c.addONT(a)
c.addONT(b)

j = readoneONTStatus(" 0/ 0/0    7  48575443078FB19C  active      online   normal   mismatch no \r\n")
print(j)
print(readoneONTOpticsInfo("    6  -19.35      2.34        -21.25      68           3.300       21        \r\n"))
print(readoneONTOpticsInfo("    7  -           -           -20.92      -            -           -         "))

print("class test done!")
print('#' * 50)

# oa = input("please specific OLT's ip addr: ")
oa = "10.238.168.46"
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
OLTHOST = oa.encode("utf-8")
USER2 = b"Natt237@clls"
PW2 = b"Faii1/iam"

# Login#
try:
    tn = telnetlib.Telnet(HOST1, 0, 2)
except socket.timeout:
    print("Timeout!!!!")
    exit(2)
else:
    print("Telnet connect established ")

tn.read_until(b"Unauthorized")
print("Accessing SAM-BB")
tn.read_until(b"login: ")
tn.write(USER1 + b"\n")
tn.read_until(b"Password: ")
tn.write(PW1 + b"\n")
print("Logined to SAM-BB")
tn.read_until(b"Broadband Gateway")
print("Access granted")
tn.read_until(b"Enter IP address [press q/Q to quit]: ")
tn.write(OLTHOST + b'\n')
tn.read_until(b">>User name:")
tn.write(USER2 + b"\n")
tn.read_until(b"password:")
tn.write(PW2 + b"\n")
print("Logging into OLT")
tn.read_until(b"\n")
print("OLT Done")
time.sleep(1)
tn.read_very_eager().decode("ascii")
# #########################################

# #############Basic information display#############
print("#" * 30)
tn.write(b"\n")
time.sleep(0.5)
oltID = tn.read_very_eager().decode("ascii").strip()
print("OLT's ID is: " + oltID.rstrip(">"))
tn.write(b"en\nundo sm\nscr\n")
time.sleep(1)
tn.read_very_eager()

tn.write(b'display ont info 0 0 0 all | include online\n')
time.sleep(2)
tn.read_until(b"CTRL_C to break\r\n")

raw = tn.read_very_eager().decode("ascii")
tmp = raw.split("\r\n")
for l in tmp[:-3]:
    l = l.strip()
    print(readoneONTStatus(l))
    tempList2On.append(readoneONTStatus(l))

print(tn.read_very_eager())

tn.write(b'display ont info 0 0 0 all | include offline\n')
time.sleep(1)
tn.read_until(b"CTRL_C to break\r\n")
raw2 = tn.read_very_eager().decode("ascii")
tmp2 = raw2.split("\r\n")
# print(raw2)
for l in tmp2[:-2]:
    l = l.strip()
    print(readoneONTStatus(l))
    tempListoff.append(readoneONTStatus(l))
# tn.interact()
tn.read_very_eager()

tn.write(b"config\n")
tn.write(b"int gpon 0/0\n")
tn.read_very_eager().decode("ascii")
tn.write(b"display ont optical-info 0 all | count\n")
time.sleep(3)
tn.read_until(b"CTRL_C to break")
count = tn.read_very_eager().decode("ascii")
oinf2 = re.findall(r'\d+', count)
rcount = oinf2[0]
ontcount = int(rcount) - 5

print('Getting ONTs Information')
tn.write(b"display ont optical-info 0 all\n")
# print(tn.read_very_eager().decode("ascii"))
time.sleep(2)
for i in range(0, 5):
    tn.read_until(b"\n")
for i in range(0, int(rcount) - 5):
    rawstr = tn.read_until(b"\n").decode("ascii")
    z = readoneONTOpticsInfo(rawstr)
    print(z)
    ontlistSecond.append(z)

lowDbl = [e for e in ontlistSecond if e[1] <= -27.0]
lowDbcount = len(lowDbl)

print("ONT low singal (<= -27dB) count: " + str(lowDbcount) + "/" + str(ontcount))
if lowDbcount > 0:
    print("ONT with low signals is/are: ")
    print([int(e[0]) for e in lowDbl])
else:
    print("Every ONTs are working properly")

tn.read_very_eager()

tn.write(b"display port state 0 | include TX power\n")
time.sleep(2)
tn.read_until(b"CTRL_C to break\r\n")
oltTXPWR = tn.read_until(b"\n").decode("ascii").strip()
tn.read_very_eager()

print("OLT TX power: " + oltTXPWR)

print("-" * 50)
if len(tempList2On) != len(ontlistSecond):
    raise Exception("Mismatched table len")
for i in range(len(tempList2On)):
    z = tempList2On[i]+ontlistSecond[i][1:]
    #print(z)
    grandONTlist.append(z)
for i in tempListoff:
    grandONTlist.append(i + [None]*6)
grandONTlist.sort()
print("-" * 80)
print('{:<3s}{:>9s}{:>9s}{:>9s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}'.format("ID","RunState","Conf-ST","Match-ST","1490rx","1310tx",
                                                                            "1310rx","Temp","Volt","mAmp"))
for i in grandONTlist:
    if i[4] != None:
        print('{:<3d}{:>9s}{:>9s}{:>9s}{:>8.2f}{:>8.2f}{:>8.2f}{:>8d}{:>8.2f}{:>8d}'.format(i[0],i[1],i[2],i[3],i[4],i[5],i[6],int(i[7]),i[8],int(i[9])))
    elif i[6] != None:
        print('{:<3d}{:>9s}{:>9s}{:>9s}{:>8s}{:>8s}{:>8.2f}{:>8s}{:>8s}{:>8s}'.format(i[0],i[1],i[2],i[3],"NONE","NONE",i[6],"NONE","NONE","NONE"))
    else:
        print('{:<3d}{:>9s}{:>9s}{:>9s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}'.format(i[0],i[1],i[2],i[3],"NONE","NONE","NONE","NONE","NONE","NONE"))

print("_" * 80)

print("#" * 30)
tn.write(b"return\n")
time.sleep(1)
# print("quitting olt")
tn.write(b"quit\n")
tn.read_until(b"Are you sure to log out? (y/n)[n]:")
tn.write(b"y\n")

time.sleep(1)
# print("OLT Quitted")
tn.read_until(b"Enter IP address [press q/Q to quit]: ")
tn.write(b"q\n")

time.sleep(0.1)
print(tn.read_very_eager().decode("ascii").strip())
tn.close()

print("Done")
