import logging

fsfsdfsdfsdfdsfsdfsdsdf
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.basicConfig(filename='app.log', filemode='w', level=logging.DEBUG)
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