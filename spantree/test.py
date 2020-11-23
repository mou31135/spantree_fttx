import json
import time
x = {"ID":1,
     "RunState":"online",
     "ConfigState":"normal",
     "MatchState":"match",
     "1490rx":-18.00,
     "1310tx":2.00,
     "1310rx":-18.00,
     "Temp":60,
     "Volt":3.30,
     "Current":15}
y = {"ID":2,
     "RunState":"online",
     "ConfigState":"normal",
     "MatchState":"match",
     "1490rx":None,
     "1310tx":2.00,
     "1310rx":-18.00,
     "Temp":None,
     "Volt":3.30,
     "Current":15}
z = [x,y]
time.sleep(2)
print(json.dumps(z,sort_keys = True))
