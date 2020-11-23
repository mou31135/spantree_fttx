import logging

#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.basicConfig(filename='test.log', filemode='w', level=logging.DEBUG)
logging.info('IMPORTING....')
import json
logging.info('IMP:Json')
import socket
logging.info('IMP:Socket')
import telnetlib
logging.info('IMP:Telnet')
import time
logging.info('IMP:Time')
import re
logging.info('IMP:Regex')
import sys
logging.info('IMP:System')

logging.info('Module Done!')

def genONTDict(lin):
    dictz = {"id": lin[0],
             "1490rx": lin[1],
             "1310tx": lin[2],
             "1310rx": lin[3],
             "1550rx": lin[4],
             "Temp": lin[5],
             "Volt": lin[6],
             "Current": lin[7]
             }
    return dictz

def quitsys():
    tn.write(b'q\n')
    tn.read_until(b':')
    tn.write(b'y\n')
    logging.info('quitted')
    time.sleep(1)
    tn.write(b'q\n')
    logging.info('Quitted from SAM-BB')
    tn.close()
    return


def chkint(inz):
     return (None if inz == '-' else int(inz))

def chkfloat(inz):
    return (None if inz == '-' else float(inz))

logging.info('INITIALIZING')

# Error code list
# 0 NO ERRORS
# 1 UNSPECIFIC ERROR
# 2 TIMEOUT
# 3 NOT EXIST
# 4 BAD COMMAND
# 5 UNAUTHORIZED
# 6 RESERVED
# 7 RESERVED

#sys.argv = [sys.argv[0], "10.238.3.3", "0/1/2"]

# Step 1: Arguments format checking
if len(sys.argv) != 3:
    logging.critical("Incomplete args")
    exit(4)

ip = sys.argv[1]
fsp = sys.argv[2]
fspList = fsp.strip().split("/")

if ((len(fspList) != 3)):
    logging.critical("bad Frame/Slot/Port Format")
    exit(4)

# Step 2: Telnet ------------------------------------------
logging.info(ip)
# TELNET1
HOST1 = "10.50.64.182"
USER1 = b"natt237"
PW1 = b"Stamp@123"

# TELNET2
OLTHOST = ip.encode("ascii")
USER2 = b"Natt237@clls"
# USER2 = b"Tuperine"
PW2 = b"Faii1/iam"

try:
    tn = telnetlib.Telnet(ip, 0, 30)
    logging.info("Telnet to " + ip)
except socket.timeout:
    logging.critical("Connection timeout!")
    exit(2)
except socket.error:
    logging.critical("Error During Telnet")
else:
    logging.info("Telnet connection established")
    pass

# tn.read_until(b"Unauthorized")
# logging.info("Accessing SAM-BB")
# tn.read_until(b"login: ")
# tn.write(USER1 + b"\n")
# tn.read_until(b"Password: ")
# tn.write(PW1 + b"\n")
# tn.read_until(b"Broadband Gateway")
# logging.info("SAM-BB: Access granted")
# tn.read_until(b"Enter IP address [press q/Q to quit]: ")
# tn.write(OLTHOST + b'\n')
j = tn.expect([b": ", b"Unreachable", b"Timeout"], timeout=3)
logging.info(j)
if j[0] == 1:
    tn.write(b"q\n")
    logging.error("SAM-BB: Host unreachable")
    tn.close()
    exit(2)
elif j[0] == -1 or j[0] == 2:
    tn.write('\x03'.encode('ascii'))
    tn.write(b"q\n")
    logging.error("SAM-BB: Timeout, Connection closed")
    tn.close()
    exit(2)
else:
    logging.info("SAM-BB: Accessing OLT: " + ip)
    pass

tn.write(USER2 + b"\n")
tn.read_until(b"Password:")
tn.write(PW2 + b"\n")
j = tn.expect([b'\r\n', b'invalid'], timeout=4)
logging.info(j)
if j[0] == 1:
    tn.write('\x03'.encode('ascii'))
    tn.write(b"q\n")
    logging.error("SAM-BB:Username or password invalid")
    exit(5)
elif (j[0] == -1):
    tn.write('\x03'.encode('ascii'))
    tn.write(b"q\n")
    logging.error("SAM-BB:Timeout, Connection closed")
    exit(2)


time.sleep(0.5)
logging.info("OLT: Access Granted")
tn.read_very_eager()
# 3 GET OLT ID AND ENABLE-------------------------------------------------
tn.write(b"\n")
time.sleep(0.5)
oltIDraw = tn.read_very_eager().decode("ascii").strip()
oltID = oltIDraw.rstrip("#")
logging.debug("OLT ID IS :" + oltID)
tn.write(b"en\nundo sm\nscr\n")
time.sleep(.5)
tn.read_very_eager()

# 4 READ OLT GENERAL STATUS-----------------------------------------------

logging.info("Reading General ont infos with F/S/P:" + fspList[0] + ' ' + fspList[1] + ' ' + fspList[2])
tn.write(('display ont info ' + fspList[0] + ' ' + fspList[1] + ' ' + fspList[2] + ' all\n').encode('ascii'))
cprout = tn.expect([b'\r\n', b'Parameter error', b'Failure:', b'no ONT'], timeout=10)
logging.info(cprout)
logging.info(cprout[1])


if cprout[0] == 1:
    logging.error("OLT: Parameter error")
    quitsys()
    exit(3)
elif cprout[0] == 2:
    err = tn.read_very_eager()
    logging.error("OLT: Failure:" + err.decode('ascii'))
    quitsys()
    exit(3)
elif cprout[0] == -1:
    logging.error("Unspecific caught error")
    quitsys()
    exit(1)
elif cprout[0] == 3:
    logging.error("There is no ONT")
    quitsys()
    exit(3)
#
ontIDlist = []

oltgenraw = tn.read_until(b"",30)
logging.info(oltgenraw)
oltgenList = oltgenraw.decode('ascii').split('\n')
oltgenList = [i.strip()[9:].split() for i in oltgenList]
processed = oltgenList[4:-2]
logging.info(oltgenList)

#
# #print(processed)
#
# ontIDlist = [i[0] for i in processed]
#
# tn.read_until(b'#')
#
# tn.write(b"config\n")
#
# tn.write(('int gpon ' + fspList[0] + '/' + fspList[1] + '\n').encode('ascii'))
#
# # Read OLT Values
#
# tn.write(b"display port state 0 | include TX power\n")
# s = tn.expect(['\\(dBm\\)'.encode('ascii')], timeout=5)
#
# if s[0] == -1:
#     logging.error("No TX Data found!")
#     oltpwN = None
# else:
#     oltpw = tn.read_until(b"\n")
#     oltpwN = float(oltpw.decode('ascii').strip())
# logging.debug("OLT Tx power: "+ str(oltpwN))
# tn.read_until(b'#')
#
# # Read ONT Optical status
# ontDataList = []
#
# for i in ontIDlist:
#     logging.debug("Getting olt optical status of: " + i)
#     tn.write(("display ont optical-info " + fspList[2] + " " + i + "\n").encode('ascii'))
#     cprout = tn.expect([b'--------', b'Parameter error', b'is not online', b'does not exist'], timeout=10)
#     if cprout[0] == 2:
#         logging.warning("OLT:Ont "+ i +" is not online")
#         tn.read_until(b'#')
#         data = [int(i)] + [None] * 7
#         #print(data)
#         ontDataList.append(genONTDict(data))
#     elif cprout[0] == 1:
#         logging.error("OLT: Parameter error")
#         tn.write(b'ret\nq\ny\nq\n')
#         tn.close()
#         exit(3)
#     elif cprout[0] == 3:
#         logging.error("ONT does not exist")
#         tn.close()
#         exit(3)
#     elif cprout[0] == -1:
#         logging.error("Unspecific caught error")
#         tn.write(b'ret\nq\ny\nq\n')
#         tn.close()
#         exit(1)
#     else:
#         tn.read_until(b'Rx optical power(dBm)')
#         rxa = tn.read_until(b'\r\n').decode('ascii').replace(':','').strip()
#         rxal = rxa.split(',')
#         if len(rxal) != 0:
#             rxa = rxal[0]
#         else:
#             rxa = rxal[0]
#         tn.read_until(b'Tx optical power(dBm)')
#         txa = tn.read_until(b'\r\n').decode('ascii').replace(':','').strip()
#         tn.read_until(b'Laser bias current(mA)')
#         cur = tn.read_until(b'\r\n').decode('ascii').replace(':','').strip()
#         tn.read_until(b'Temperature(C)')
#         temp = tn.read_until(b'\r\n').decode('ascii').replace(':','').strip()
#         tn.read_until(b'Voltage(V)')
#         vol = tn.read_until(b'\r\n').decode('ascii').replace(':','').strip()
#         tn.read_until(b'OLT Rx ONT optical power(dBm) ')
#         olt_rx = tn.read_until(b'\r\n').decode('ascii').replace(':','').strip()
#         rxe = olt_rx.split(',')
#         if len(rxe) != 0:
#             olt_rx = rxe[0]
#         else:
#             olt_rx = rxe[0]
#         tn.read_until(b'CATV Rx optical power(dBm)')
#         rx_tv = tn.read_until(b'\r\n').decode('ascii').replace(':','').strip()
#         tn.read_until(b'#')
#         data = [int(i),chkfloat(rxa),chkfloat(txa),chkfloat(olt_rx),chkfloat(rx_tv),chkint(temp),chkfloat(vol),chkint(cur)]
#         #print(data)
#         ontDataList.append(genONTDict(data))
#
# #print(ontDataList)
#
# # Convert to json and send to output

OutDict = {"1490tx": oltpwN,
           "ONTs": ontDataList
               }

print(json.dumps(OutDict, indent=4))

tn.write(b'ret\nq\ny\nq\n')
tn.close()
