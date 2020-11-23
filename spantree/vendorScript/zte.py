import json
import socket
import telnetlib
import time
import re
import sys
import logging

# logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
logging.basicConfig(filename="zteLast.log", filemode="w", level=logging.DEBUG)


def genONTDict(lin):
    dictz = {
        "id": lin[0],
        "1490rx": lin[1],
        "1310tx": lin[2],
        "1310rx": lin[3],
        "1550rx": lin[4],
        "Temp": None,
        "Volt": None,
        "Current": None,
    }
    return dictz


def quitsys():
    tn.write(b"qu\n")
    tn.read_until(b":")
    tn.write(b"y\n")
    logging.info("quitted")
    time.sleep(1)
    tn.write(b"q\n")
    tn.close()
    return


def merger(t1, t2, t3, t4):
    return list(t1) + [t2[1], t3[1], t4[1]]


# Error code list
# 0 NO ERRORS
# 1 UNSPECIFIC ERROR
# 2 TIMEOUT
# 3 NOT EXIST
# 4 BAD COMMAND
# 5 UNAUTHORIZED
# 6 RESERVED
# 7 RESERVED

# sys.argv = [sys.argv[0], "10.239.187.4", "1/1/1"]

# Step 1: Arguments format checking
if len(sys.argv) != 3:
    logging.critical("Incomplete args")
    exit(4)

ip = sys.argv[1]
fsp = sys.argv[2]
fspList = fsp.strip().split("/")

if len(fspList) != 3:
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
    tn = telnetlib.Telnet(ip, 0, 20)
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

j = tn.expect([b"Username:", b"unreachable", b"timed out"], timeout=3)
logging.info(j)

if j[0] == 1:
    tn.write(b"q\n")
    logging.error("SAM-BB: Host unreachable")
    tn.close()
    exit(2)
elif j[0] == -1 or j[0] == 2:
    tn.write("\x03".encode("ascii"))
    tn.write(b"q\n")
    logging.error("SAM-BB: Timeout, Connection closed")
    tn.close()
    exit(2)
else:
    logging.info("SAM-BB: Accessing OLT")
    pass

tn.write(USER2 + b"\n")
tn.read_until(b"Password:")
tn.write(PW2 + b"\n")
j = tn.expect([b">", b"authentication failed"], timeout=4)
logging.info(j)
if j[0] == 1:
    tn.write("\x03".encode("ascii"))
    tn.write(b"q\n")
    logging.error("SAM-BB:Username or password invalid")
    exit(5)
elif j[0] == -1:
    tn.write("\x03".encode("ascii"))
    tn.write(b"q\n")
    logging.error("SAM-BB:Timeout, Connection closed")
    exit(2)
logging.info("OLT: Access Granted")
# 3 Initial something

tn.write(b"en\nzxr10\n")
tn.write(b"ter len 0\n")
time.sleep(0.5)
tn.read_very_eager()

logging.info(
    "Reading olt tx power (1490tx) of F/S/P:"
    + fspList[0]
    + " "
    + fspList[1]
    + " "
    + fspList[2]
)
tn.write(
    (
        "show pon power olt-tx gpon-olt_"
        + fspList[0]
        + "/"
        + fspList[1]
        + "/"
        + fspList[2]
        + "\n"
    ).encode("ascii")
)
cmpout = tn.expect(
    [b"------\r\n", b"Invalid input", b"###########", b"##########"], timeout=10
)
# print (cmpout)
if cmpout[0] == 1:
    logging.critical("OLT: Invalid input")
    quitsys()
    exit(2)
elif cmpout[0] == -1:
    logging.critical("OLT: Unspecific error")
    quitsys()
    exit(1)
else:
    z = tn.read_until(b"\r\n")
    # print('#####',z)
    txpw = z.decode("ascii").split()[1].rstrip("(dbm)")
    # print(txpw)

logging.info(
    "Reading ont rx (1490rx) power F/S/P:"
    + fspList[0]
    + " "
    + fspList[1]
    + " "
    + fspList[2]
)
tn.write(
    (
        "show pon power onu-rx gpon-olt_"
        + fspList[0]
        + "/"
        + fspList[1]
        + "/"
        + fspList[2]
        + "\n"
    ).encode("ascii")
)
cmpout = tn.expect(
    [b"------\r\n", b"Invalid input", b"No related information to show", b"##########"],
    timeout=10,
)

logging.info(cmpout)

if cmpout[0] == 1:
    logging.critical("OLT: Invalid input")
    quitsys()
    exit(2)
elif cmpout[0] == -1:
    print(cmpout)
    logging.critical("OLT: Unspecific error")
    quitsys()
    exit(1)
elif cmpout[0] == 2:
    logging.warning("OLT: No onu on this port)")
    jsondict = {"1490tx": None if txpw == "N/A" else float(txpw), "ONTs": []}
    jsonout = json.dumps(jsondict, indent=4)
    print(jsonout)
    quitsys()
    exit(0)

else:
    zraw = tn.read_until(b"#")
    ont1490rx = zraw.decode("ascii").replace(":", " ").split("\r\n")
    logging.info("SAM-BB: Accessing OLT")
    logging.info(ont1490rx)
    z = ont1490rx[:-1]
    z = [i.split() for i in z]
    zi = [(i[1], i[2].strip("(dbm)")) for i in z]
    onurxlist = [(int(i[0]), (None if i[1] == "N/A" else float(i[1]))) for i in zi]
    # print(onurxlist)

logging.info(
    "Reading ont tx (1310tx) power F/S/P:"
    + fspList[0]
    + " "
    + fspList[1]
    + " "
    + fspList[2]
)
tn.write(
    (
        "show pon power onu-tx gpon-olt_"
        + fspList[0]
        + "/"
        + fspList[1]
        + "/"
        + fspList[2]
        + "\n"
    ).encode("ascii")
)
cmpout = tn.expect(
    [b"------\r\n", b"Invalid input", b"###########", b"##########"], timeout=10
)
if cmpout[0] == 1:
    logging.critical("OLT: Invalid input")
    quitsys()
    exit(2)
elif cmpout[0] == -1:
    logging.critical("OLT: Unspecific error")
    print(cmpout)
    quitsys()
    exit(1)
else:
    zraw = tn.read_until(b"#")
    ont1310tx = zraw.decode("ascii").replace(":", " ").split("\r\n")
    z = ont1310tx[:-1]
    z = [i.split() for i in z]
    zi = [(i[1], i[2].strip("(dbm)")) for i in z]
    onutxlist = [(int(i[0]), (None if i[1] == "N/A" else float(i[1]))) for i in zi]
    # print(onutxlist)

logging.info(
    "Reading olt rx (1310rx) power F/S/P:"
    + fspList[0]
    + " "
    + fspList[1]
    + " "
    + fspList[2]
)
tn.write(
    (
        "show pon power olt-rx gpon-olt_"
        + fspList[0]
        + "/"
        + fspList[1]
        + "/"
        + fspList[2]
        + "\n"
    ).encode("ascii")
)
cmpout = tn.expect(
    [b"------\r\n", b"Invalid input", b"###########", b"##########"], timeout=10
)
if cmpout[0] == 1:
    logging.critical("OLT: Invalid input")
    quitsys()
    exit(2)
elif cmpout[0] == -1:
    logging.critical("OLT: Unspecific error")
    print(cmpout)
    quitsys()
    exit(1)
else:
    zraw = tn.read_until(b"#")
    ont1310rx = zraw.decode("ascii").replace(":", " ").split("\r\n")
    z = ont1310rx[:-1]
    z = list(filter(None, z))
    z = [i.split() for i in z]
    zi = [(i[1], i[2].strip("(dbm)")) for i in z]
    oltrxlist = [(int(i[0]), (None if "no" in i[1] else float(i[1]))) for i in zi]

onuIDlist = []

for i in onurxlist:
    onuIDlist.append(i[0])

onuTVlist = []

for i in onuIDlist:
    logging.info("Reading: " + str(i))
    tn.write(
        (
            "show gpon remote-onu interface video-ani gpon-onu_"
            + fspList[0]
            + "/"
            + fspList[1]
            + "/"
            + fspList[2]
            + ":"
            + str(i)
            + "\n"
        ).encode("ascii")
    )
    cmpout = tn.expect(
        [b"Optical signal level:", b"Invalid input", b"###########", b"##########"],
        timeout=1,
    )
    if cmpout[0] == 1:
        logging.critical("OLT: Invalid input")
        quitsys()
        exit(2)
    elif cmpout[0] == -1:
        print(cmpout)
        logging.critical("OLT: Unspecific error")
        quitsys()
        exit(1)
    else:
        zr = tn.read_until(b"\r\n")
        tvv = zr.decode("ascii").strip().strip("(dBm)")
        tvv = None if tvv == "N/A" else float(tvv)
        tn.read_until(b"#")
        onuTVlist.append((i, tvv))

grandList = list(map(merger, onurxlist, onutxlist, oltrxlist, onuTVlist))

dictlist = list(map(genONTDict, grandList))

jsondict = {"1490tx": float(txpw), "ONTs": dictlist}
jsonout = json.dumps(jsondict, indent=4)
print(jsonout)

quitsys()
