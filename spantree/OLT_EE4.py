import json
import socket
import telnetlib
import time
import re
import sys
import logging

logging.basicConfig(stream=sys.stderr, level=logging.ERROR)


def genONTDict(input):
    dictz = {"id": int(input[0]),
             "RunState": input[3],
             "ConfigState": input[4],
             "MatchState": input[5],
             "1490rx": None,
             "1310tx": None,
             "1310rx": None,
             "Temp": None,
             "Volt": None,
             "Current": None
             }
    return dictz


def addOpticaldataONTDict(dictz, input):
    if dictz['id'] != int(input[0]):
        logging.error("Wat")
        return dictz
    dictz['1490rx'] = None if input[1] == '-' else float(input[1])
    dictz['1310tx'] = None if input[2] == '-' else float(input[2])
    dictz['1310rx'] = None if input[3] == '-' else float(input[3])
    dictz['Temp'] = None if input[4] == '-' else float(input[4])
    dictz['Volt'] = None if input[5] == '-' else float(input[5])
    dictz['Current'] = None if input[6] == '-' else float(input[6])

    logging.debug("Dict edited")

    return dictz


# Error code list
# 0 NO ERRORS
# 1 UNSPECIFIC ERROR
# 2 TIMEOUT
# 3 NOT EXIST
# 4 BAD COMMAND
# 5 UNAUTHORIZED
# 6 RESERVED
# 7 RESERVED

# sys.argv = [sys.argv[0], "10.238.3.3", "0/1/1"]

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
    tn = telnetlib.Telnet(HOST1, 0, 2)
    logging.info("Telnet to " + HOST1)
except socket.timeout:
    logging.critical("Connection timeout!")
    exit(2)
except socket.error:
    logging.critical("Error During Telnet")
else:
    logging.info("Telnet connection established")
    pass

tn.read_until(b"Unauthorized")
logging.info("Accessing SAM-BB")
tn.read_until(b"login: ")
tn.write(USER1 + b"\n")
tn.read_until(b"Password: ")
tn.write(PW1 + b"\n")
tn.read_until(b"Broadband Gateway")
logging.info("SAM-BB: Access granted")
tn.read_until(b"Enter IP address [press q/Q to quit]: ")
tn.write(OLTHOST + b'\n')

j = tn.expect([b'User name:', b'unreachable', b'timed out'], timeout=3)
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
    logging.info("SAM-BB: Accessing OLT")
    pass

tn.write(USER2 + b"\n")
tn.read_until(b"password:")
tn.write(PW2 + b"\n")
j = tn.expect([b'Huawei', b'invalid'], timeout=4)
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
oltID = oltIDraw.rstrip(">")
logging.debug("OLT ID IS :" + oltID)
tn.write(b"en\nundo sm\nscr\n")
time.sleep(.5)
tn.read_very_eager()

# 4 READ OLT GENERAL STATUS-----------------------------------------------

logging.info("Reading General ont infos with F/S/P:" + fspList[0] + ' ' + fspList[1] + ' ' + fspList[2])
tn.write(('display ont info ' + fspList[0] + ' ' + fspList[1] + ' ' + fspList[2] + ' all\n').encode('ascii'))
cprout = tn.expect([b'--------', b'Parameter error', b'Failure:', b'no ONT'], timeout=10)
if cprout[0] == 1:
    logging.error("OLT: Parameter error")
    tn.write(b'q\ny\nq\n')
    tn.close()
    exit(3)
elif cprout[0] == 2:
    err = tn.read_very_eager()
    logging.error("OLT: Failure:" + err.decode('ascii'))
    tn.write(b'q\ny\nq\n')
    tn.close()
    exit(3)
elif cprout[0] == -1:
    logging.error("Unspecific caught error")
    tn.write(b'q\ny\nq\n')
    tn.close()
    exit(1)
elif cprout[0] == 3:
    logging.error("There is no ONT")
    tn.write(b'q\ny\nq\n')
    tn.close()
    exit(3)

oltgenraw = tn.read_until(b"F/S/P   ONT-ID   Description")
oltgenList = oltgenraw.decode('ascii').split('\n')
oltgenList = [i.strip()[9:].split() for i in oltgenList]
processed = oltgenList[4:-2]

ONTLIST = [genONTDict(i) for i in processed]

time.sleep(0.5)
tn.read_very_eager()

tn.write(b"config\n")
tn.write(('int gpon ' + fspList[0] + '/' + fspList[1] + '\n').encode('ascii'))

# Read OLT Values

tn.write(b"display port state 0 | include TX power\n")
s = tn.expect(['\\(dBm\\)'.encode('ascii')], timeout=5)

if s[0] == -1:
    logging.error("No TX Data found!")
    oltpwN = None
else:
    oltpw = tn.read_until(b"\n")
    oltpwN = float(oltpw.decode('ascii').strip())
tn.read_very_eager()

# Read ONT Optical status
tn.write(("display ont optical-info " + fspList[2] + " all\n").encode('ascii'))
cprout = tn.expect([b'--------', b'Parameter error', b'Failure:', b'information does not exist'], timeout=10)
if cprout[0] == 1:
    logging.error("OLT: Parameter error")
    tn.write(b'ret\nq\ny\nq\n')
    tn.close()
    exit(3)
elif cprout[0] == 2:
    err = tn.read_very_eager()
    logging.error("OLT: Failure:" + err.decode('ascii'))
    tn.write(b'ret\nq\ny\nq\n')
    tn.close()
    exit(3)
elif cprout[0] == -1:
    logging.error("Unspecific caught error")
    tn.write(b'ret\nq\ny\nq\n')
    tn.close()
    exit(1)
elif cprout[0] == 3:
    logging.warning("No online ONTs")
else:
    z = tn.read_until(b"config-if-gpon")
    # print(z.decode('ascii').split('\r\n'))
    ontopticinf = z.decode('ascii').split('\r\n')[4:-3]
    ontopticinf = [e.split() for e in ontopticinf]

    # print(ONTLIST)
    # print(ontopticinf)  # ONT-Optic-Info
    logging.info("editing dict")

    for d in ONTLIST:
        for l in ontopticinf:
            if d['id'] == int(l[0]):
                d = addOpticaldataONTDict(d, l)
                break

time.sleep(.5)
tn.read_very_eager()

OutDict = {"OLT_ID": oltID,
           "1490tx": oltpwN,
           "portID": int(fspList[2]),
           "ONTs": ONTLIST}

print(json.dumps(OutDict, indent=4))

tn.write(b'ret\nq\ny\nq\n')
tn.close()
