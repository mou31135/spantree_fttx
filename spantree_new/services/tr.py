# -*- coding: utf-8 -*-

import time
import sys
import os
import datetime
import requests
import cx_Oracle
import multiprocessing as mp
import json
import subprocess


def findZTEifindex(gp):
  arr = [
    ['1/1/1','268501248'],
    ['1/1/2','268501504'],
    ['1/1/3','268501760'],
    ['1/1/4','268502016'],
    ['1/1/5','268502272'],
    ['1/1/6','268502528'],
    ['1/1/7','268502784'],
    ['1/1/8','268503040'],
    ['1/1/9','268503296'],
    ['1/1/10','268503552'],
    ['1/1/11','268503808'],
    ['1/1/12','268504064'],
    ['1/1/13','268504320'],
    ['1/1/14','268504576'],
    ['1/1/15','268504832'],
    ['1/1/16','268505088'],
    ['1/2/1','268566784'],
    ['1/2/2','268567040'],
    ['1/2/3','268567296'],
    ['1/2/4','268567552'],
    ['1/2/5','268567808'],
    ['1/2/6','268568064'],
    ['1/2/7','268568320'],
    ['1/2/8','268568576'],
    ['1/2/9','268568832'],
    ['1/2/10','268569088'],
    ['1/2/11','268569344'],
    ['1/2/12','268569600'],
    ['1/2/13','268569856'],
    ['1/2/14','268570112'],
    ['1/2/15','268570368'],
    ['1/2/16','268570624'],
    ['1/3/1','268632320'],
    ['1/3/2','268632576'],
    ['1/3/3','268632832'],
    ['1/3/4','268633088'],
    ['1/3/5','268633344'],
    ['1/3/6','268633600'],
    ['1/3/7','268633856'],
    ['1/3/8','268634112'],
    ['1/3/9','268634368'],
    ['1/3/10','268634624'],
    ['1/3/11','268634880'],
    ['1/3/12','268635136'],
    ['1/3/13','268635392'],
    ['1/3/14','268635648'],
    ['1/3/15','268635904'],
    ['1/3/16','268636160'],
    ['1/4/1','268697856'],
    ['1/4/2','268698112'],
    ['1/4/3','268698368'],
    ['1/4/4','268698624'],
    ['1/4/5','268698880'],
    ['1/4/6','268699136'],
    ['1/4/7','268699392'],
    ['1/4/8','268699648'],
    ['1/4/9','268699904'],
    ['1/4/10','268700160'],
    ['1/4/11','268700416'],
    ['1/4/12','268700672'],
    ['1/4/13','268700928'],
    ['1/4/14','268701184'],
    ['1/4/15','268701440'],
    ['1/4/16','268701696'],
    ['1/5/1','268763392'],
    ['1/5/2','268763648'],
    ['1/5/3','268763904'],
    ['1/5/4','268764160'],
    ['1/5/5','268764416'],
    ['1/5/6','268764672'],
    ['1/5/7','268764928'],
    ['1/5/8','268765184'],
    ['1/5/9','268765440'],
    ['1/5/10','268765696'],
    ['1/5/11','268765952'],
    ['1/5/12','268766208'],
    ['1/5/13','268766464'],
    ['1/5/14','268766720'],
    ['1/5/15','268766976'],
    ['1/5/16','268767232'],
    ['1/6/1','268828928'],
    ['1/6/2','268829184'],
    ['1/6/3','268829440'],
    ['1/6/4','268829696'],
    ['1/6/5','268829952'],
    ['1/6/6','268830208'],
    ['1/6/7','268830464'],
    ['1/6/8','268830720'],
    ['1/6/9','268830976'],
    ['1/6/10','268831232'],
    ['1/6/11','268831488'],
    ['1/6/12','268831744'],
    ['1/6/13','268832000'],
    ['1/6/14','268832256'],
    ['1/6/15','268832512'],
    ['1/6/16','268832768'],
    ['1/7/1','268894464'],
    ['1/7/2','268894720'],
    ['1/7/3','268894976'],
    ['1/7/4','268895232'],
    ['1/7/5','268895488'],
    ['1/7/6','268895744'],
    ['1/7/7','268896000'],
    ['1/7/8','268896256'],
    ['1/7/9','268896512'],
    ['1/7/10','268896768'],
    ['1/7/11','268897024'],
    ['1/7/12','268897280'],
    ['1/7/13','268897536'],
    ['1/7/14','268897792'],
    ['1/7/15','268898048'],
    ['1/7/16','268898304'],
    ['1/8/1','268960000'],
    ['1/8/2','268960256'],
    ['1/8/3','268960512'],
    ['1/8/4','268960768'],
    ['1/8/5','268961024'],
    ['1/8/6','268961280'],
    ['1/8/7','268961536'],
    ['1/8/8','268961792'],
    ['1/8/9','268962048'],
    ['1/8/10','268962304'],
    ['1/8/11','268962560'],
    ['1/8/12','268962816'],
    ['1/8/13','268963072'],
    ['1/8/14','268963328'],
    ['1/8/15','268963584'],
    ['1/8/16','268963840'],
    ['1/9/1','269025536'],
    ['1/9/2','269025792'],
    ['1/9/3','269026048'],
    ['1/9/4','269026304'],
    ['1/9/5','269026560'],
    ['1/9/6','269026816'],
    ['1/9/7','269027072'],
    ['1/9/8','269027328'],
    ['1/9/9','269027584'],
    ['1/9/10','269027840'],
    ['1/9/11','269028096'],
    ['1/9/12','269028352'],
    ['1/9/13','269028608'],
    ['1/9/14','269028864'],
    ['1/9/15','269029120'],
    ['1/9/16','269029376'],
    ['1/12/1','269222144'],
    ['1/12/2','269222400'],
    ['1/12/3','269222656'],
    ['1/12/4','269222912'],
    ['1/12/5','269223168'],
    ['1/12/6','269223424'],
    ['1/12/7','269223680'],
    ['1/12/8','269223936'],
    ['1/12/9','269224192'],
    ['1/12/10','269224448'],
    ['1/12/11','269224704'],
    ['1/12/12','269224960'],
    ['1/12/13','269225216'],
    ['1/12/14','269225472'],
    ['1/12/15','269225728'],
    ['1/12/16','269225984'],
    ['1/13/1','269287680'],
    ['1/13/2','269287936'],
    ['1/13/3','269288192'],
    ['1/13/4','269288448'],
    ['1/13/5','269288704'],
    ['1/13/6','269288960'],
    ['1/13/7','269289216'],
    ['1/13/8','269289472'],
    ['1/13/9','269289728'],
    ['1/13/10','269289984'],
    ['1/13/11','269290240'],
    ['1/13/12','269290496'],
    ['1/13/13','269290752'],
    ['1/13/14','269291008'],
    ['1/13/15','269291264'],
    ['1/13/16','269291520'],
    ['1/14/1','269353216'],
    ['1/14/2','269353472'],
    ['1/14/3','269353728'],
    ['1/14/4','269353984'],
    ['1/14/5','269354240'],
    ['1/14/6','269354496'],
    ['1/14/7','269354752'],
    ['1/14/8','269355008'],
    ['1/14/9','269355264'],
    ['1/14/10','269355520'],
    ['1/14/11','269355776'],
    ['1/14/12','269356032'],
    ['1/14/13','269356288'],
    ['1/14/14','269356544'],
    ['1/14/15','269356800'],
    ['1/14/16','269357056'],
    ['1/15/1','269418752'],
    ['1/15/2','269419008'],
    ['1/15/3','269419264'],
    ['1/15/4','269419520'],
    ['1/15/5','269419776'],
    ['1/15/6','269420032'],
    ['1/15/7','269420288'],
    ['1/15/8','269420544'],
    ['1/15/9','269420800'],
    ['1/15/10','269421056'],
    ['1/15/11','269421312'],
    ['1/15/12','269421568'],
    ['1/15/13','269421824'],
    ['1/15/14','269422080'],
    ['1/15/15','269422336'],
    ['1/15/16','269422592'],
    ['1/16/1','269484288'],
    ['1/16/2','269484544'],
    ['1/16/3','269484800'],
    ['1/16/4','269485056'],
    ['1/16/5','269485312'],
    ['1/16/6','269485568'],
    ['1/16/7','269485824'],
    ['1/16/8','269486080'],
    ['1/16/9','269486336'],
    ['1/16/10','269486592'],
    ['1/16/11','269486848'],
    ['1/16/12','269487104'],
    ['1/16/13','269487360'],
    ['1/16/14','269487616'],
    ['1/16/15','269487872'],
    ['1/16/16','269488128'],
    ['1/17/1','269549824'],
    ['1/17/2','269550080'],
    ['1/17/3','269550336'],
    ['1/17/4','269550592'],
    ['1/17/5','269550848'],
    ['1/17/6','269551104'],
    ['1/17/7','269551360'],
    ['1/17/8','269551616'],
    ['1/17/9','269551872'],
    ['1/17/10','269552128'],
    ['1/17/11','269552384'],
    ['1/17/12','269552640'],
    ['1/17/13','269552896'],
    ['1/17/14','269553152'],
    ['1/17/15','269553408'],
    ['1/17/16','269553664'],
    ['1/18/1','269615360'],
    ['1/18/2','269615616'],
    ['1/18/3','269615872'],
    ['1/18/4','269616128'],
    ['1/18/5','269616384'],
    ['1/18/6','269616640'],
    ['1/18/7','269616896'],
    ['1/18/8','269617152'],
    ['1/18/9','269617408'],
    ['1/18/10','269617664'],
    ['1/18/11','269617920'],
    ['1/18/12','269618176'],
    ['1/18/13','269618432'],
    ['1/18/14','269618688'],
    ['1/18/15','269618944'],
    ['1/18/16','269619200'],
    ['1/19/1','269680896'],
    ['1/19/2','269681152'],
    ['1/19/3','269681408'],
    ['1/19/4','269681664'],
    ['1/19/5','269681920'],
    ['1/19/6','269682176'],
    ['1/19/7','269682432'],
    ['1/19/8','269682688'],
    ['1/19/9','269682944'],
    ['1/19/10','269683200'],
    ['1/19/11','269683456'],
    ['1/19/12','269683712'],
    ['1/19/13','269683968'],
    ['1/19/14','269684224'],
    ['1/19/15','269684480‬'],
    ['1/19/16','269684736']
  ]

  for x in arr:
    if x[0] == str(gp):
      return x[1]
#end findZTEifindex

def getData(res):
    #VENDOR,OLT_IP,GPON_PORT,ONU_ID,TELEPHONE_NUMBER
    olt_ip = res[1]
    onuid = res[3]
    TELEPHONE_NUMBER = res[4]
    state = ""

    try:
        if res[0].upper() == "HUAWEI":
            gp = res[2].split('/')

            F = gp[0]
            S = gp[1]
            P = gp[2]

            ifindex = (125*(2**25))+(int(S)*(2**13))+(int(P)*(2**8))

            #onoff
            p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 8 -t 7 -c public123 '+str(olt_ip)+' 1.3.6.1.4.1.2011.6.128.1.1.2.46.1.15.'+str(ifindex)+'.'+onuid,shell=True,stdout=subprocess.PIPE)
            time.sleep(1)
            p.kill()

            output = p.communicate()
            output = output[0].decode("utf-8").strip()

            t = output.split('= INTEGER: ')

            try:
                status = t[1].replace(' ', '')
            except:
                return [TELEPHONE_NUMBER,'-','-','-','-','-','-']

            if int(status) == 1:
                state = "online"
                #1490
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 8 -t 7 -c public123 '+str(olt_ip)+' 1.3.6.1.4.1.2011.6.128.1.1.2.51.1.4.'+str(ifindex)+'.'+onuid,shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                _1490 = float(int(t[1].replace(' ', ''))/100)

                #1550
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 8 -t 7 -c public123 '+str(olt_ip)+' 1.3.6.1.4.1.2011.6.128.1.1.2.51.1.7.'+str(ifindex)+'.'+onuid,shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                _1550 = float(int(t[1].replace(' ', ''))/100)

                if _1550 > 21474836:
                    _1550 = '-'

                #1310
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 8 -t 7 -c public123 '+str(olt_ip)+' 1.3.6.1.4.1.2011.6.128.1.1.2.51.1.3.'+str(ifindex)+'.'+onuid,shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                _1310 = float(int(t[1].replace(' ', ''))/100)

                #1310
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 8 -t 7 -c public123 '+str(olt_ip)+' 1.3.6.1.4.1.2011.6.128.1.1.2.51.1.2.'+str(ifindex)+'.'+onuid,shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                _1310R = float(int(t[1].replace(' ', ''))/100)

                #distance
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 8 -t 7 -c public123 '+str(olt_ip)+' 1.3.6.1.4.1.2011.6.128.1.1.2.46.1.20.'+str(ifindex)+'.'+onuid,shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                dist = t[1].replace(' ', '')

                return [TELEPHONE_NUMBER,state,_1490,_1550,_1310,dist,_1310R]
            else:
                state = "offline"
                return [TELEPHONE_NUMBER,state,'-','-','-','-','-']

        elif res[0].upper() == "ZTE":
            #onoff
            gp2 = res[2]

            gp = res[2].split('/')
            F = int(gp[0])
            S = int(gp[1])
            P = int(gp[2])

            if_no = 1;#fix
            if_no1 = 2;#fix

            ifindex = findZTEifindex(gp2)

            if ifindex == None:
                return [TELEPHONE_NUMBER,'-','-','-','-','-']

            p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 5 -t 8 -c public '+olt_ip+' 1.3.6.1.4.1.3902.1012.3.28.2.1.4.'+str(ifindex)+'.'+str(onuid),shell=True,stdout=subprocess.PIPE)
            time.sleep(1.5)
            p.kill()

            output = p.communicate()
            output = output[0].decode("utf-8").strip()

            t = output.split('= INTEGER: ')

            try:
                status = t[1].replace(' ', '')
            except:
                return [TELEPHONE_NUMBER,'-','-','-','-','-']

            if int(status) == 3:
                state = "online"

                ifindex = (int((if_no<<28)) + int(((if_no1 -1)<<24)) + int(((F)<<16))+int((S)<<8)+int(P))
                #1490
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 5 -t 8 -c public '+olt_ip+' 1.3.6.1.4.1.3902.1082.500.20.2.2.2.1.10.'+str(ifindex)+'.'+str(onuid),shell=True,stdout=subprocess.PIPE)
                time.sleep(1.5)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                if int(t[1]) > 15000 and int(t[1]) < 65535:
                    _1490 = round(float((int(t[1])-65535)* 0.002 - 30),2)
                elif int(t[1])  < 15000:
                    _1490 = round(float(int(t[1])* 0.002 - 30),2)
                else:
                    _1490 = "0"

                #1550
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 5 -t 8 -c public '+olt_ip+' 1.3.6.1.4.1.3902.1082.500.20.2.5.3.1.8.'+str(ifindex)+'.'+str(onuid),shell=True,stdout=subprocess.PIPE)
                time.sleep(1.5)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                _1550 = int(t[1])-30

                #1310
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 5 -t 8 -c public '+olt_ip+' 1.3.6.1.4.1.3902.1082.500.20.2.2.2.1.14.'+str(ifindex)+'.'+str(onuid),shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                _1310 = round((int(t[1])*0.002)-30,2)

                #distance
                ifindex = findZTEifindex(gp2)
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 5 -t 8 -c public '+olt_ip+' 1.3.6.1.4.1.3902.1012.3.11.4.1.2.'+str(ifindex)+'.'+str(onuid),shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                dist = t[1]

                return [TELEPHONE_NUMBER,state,_1490,_1550,_1310,dist]

            else:
                state = "offline"
                return [TELEPHONE_NUMBER,state,'-','-','-','-']

        elif res[0].upper() == "DASAN":
            #onoff
            gp = res[2].split('/')

            p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c public '+str(olt_ip)+' 1.3.6.1.4.1.6296.101.23.3.1.1.2.'+str(gp[2])+'.'+str(onuid),shell=True,stdout=subprocess.PIPE)
            time.sleep(1)
            p.kill()

            output = p.communicate()
            output = output[0].decode("utf-8").strip()

            t = output.split('= INTEGER: ')

            try:
                status = t[1].replace(' ', '')
            except:
                return [TELEPHONE_NUMBER,'-','-','-','-','-']

            if int(status) == 2:
                state = "online"
                #1490
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c public '+str(olt_ip)+' 1.3.6.1.4.1.6296.101.23.3.1.1.16.'+str(gp[2])+'.'+str(onuid),shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                _1490 = round(int(t[1])/10,3)

                #1550
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c public '+str(olt_ip)+' 1.3.6.1.4.1.6296.101.23.6.8.1.1.9.'+str(gp[2])+'.'+str(onuid)+'.1',shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                _1550 = t[1]

                #1310
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c public '+str(olt_ip)+' 1.3.6.1.4.1.6296.101.23.6.6.1.1.19.'+str(gp[2])+'.'+str(onuid)+'.1',shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= STRING: "')

                _1310 = round(float(t[1].replace('"','')),3)

                #distance
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c public '+str(olt_ip)+' 1.3.6.1.4.1.6296.101.23.3.1.1.10.'+str(gp[2])+'.'+str(onuid),shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                dist = t[1]

                return [TELEPHONE_NUMBER,state,_1490,_1550,_1310,dist]
            else:
                state = "offline"
                return [TELEPHONE_NUMBER,state,'-','-','-','-']

        elif res[0].upper() == "GCOM":
            #onoff
            return [TELEPHONE_NUMBER,'-','-','-','-','-']
            gp = res[2].split('/')

            p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c public '+str(olt_ip)+' 1.3.6.1.4.1.13464.1.14.2.4.1.1.1.6.'+str(gp[1])+'.'+str(gp[2])+'.'+str(onuid),shell=True,stdout=subprocess.PIPE)
            time.sleep(1)
            p.kill()

            output = p.communicate()
            output = output[0].decode("utf-8").strip()

            t = output.split('= INTEGER: ')

            try:
                status = t[1].replace(' ', '')
            except:
                return [TELEPHONE_NUMBER,'-','-','-','-','-']

            if int(status) == 1:
                state = "online"

                #1490
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c public '+str(olt_ip)+' 1.3.6.1.4.1.13464.1.14.2.4.1.4.1.5.'+str(gp[1])+'.'+str(gp[2])+'.'+str(onuid),shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= STRING: "')

                _1490 = t[1].replace('"','')

                #1550
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c public '+str(olt_ip)+' 1.3.6.1.4.1.13464.1.14.2.4.1.4.1.9.'+str(gp[1])+'.'+str(gp[2])+'.'+str(onuid),shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= STRING: "')

                _1550 = t[1].replace('"','')

                #1310
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c public '+str(olt_ip)+' 1.3.6.1.4.1.13464.1.14.2.4.1.4.1.6.'+str(gp[1])+'.'+str(gp[2])+'.'+str(onuid),shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= STRING: "')

                _1310 = t[1].replace('"','')

                #distance
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c public '+str(olt_ip)+' 1.3.6.1.4.1.13464.1.14.2.4.1.1.1.7.'+str(gp[1])+'.'+str(gp[2])+'.'+str(onuid),shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= STRING: "')

                dist = t[1].replace('"','')

                return [TELEPHONE_NUMBER,state,_1490,_1550,_1310,dist]
            else:
                state = "offline"
                return [TELEPHONE_NUMBER,state,'-','-','-','-']
        elif res[0].upper() == "RAISECOM":
            gp = res[2].split('/')

            if len(str(gp[2])) < 2:
                port = "0"+str(gp[2])
            else:
                port = str(gp[2])

            if len(str(onuid)) < 2:
                onuid = "0"+str(onuid)
            else:
                onuid = str(onuid)

            #onoff
            p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c public '+str(olt_ip)+' 1.3.6.1.4.1.8886.18.3.6.3.1.1.17.'+str(gp[1])+str(port)+str(onuid)+'001',shell=True,stdout=subprocess.PIPE)
            time.sleep(1)
            p.kill()

            output = p.communicate()
            output = output[0].decode("utf-8").strip()

            t = output.split('= INTEGER: ')

            try:
                status = t[1].replace(' ', '')
            except:
                return [TELEPHONE_NUMBER,'-','-','-','-','-']

            if int(status) > 0:
                state = "online"
                #1490
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c public '+str(olt_ip)+' 1.3.6.1.4.1.8886.18.3.6.3.1.1.16.'+str(gp[1])+str(port)+str(onuid)+'001',shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                _1490 = round((int(t[1])-15000)/500,3)

                #1550
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c public '+str(olt_ip)+' 1.3.6.1.4.1.8886.18.3.6.10.1.1.8.'+str(gp[1])+str(port)+str(onuid)+'001',shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                _1550 = t[1]

                #1310
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c public '+str(olt_ip)+' 1.3.6.1.4.1.8886.18.3.6.3.1.1.17.'+str(gp[1])+str(port)+str(onuid)+'001',shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                _1310 = round((int(t[1])-15000)/500,3)

                #distance
                vif = "0001"
                slot = bin(int(gp[1]))[2:]
                slot = slot.rjust(5,"0")
                pon_port = bin(int(gp[2]))[2:]
                pon_port = pon_port.rjust(6,"0")
                onuid = bin(int(onuid))[2:]
                onuid = onuid.rjust(16,"0")
                big_onu_id = int(vif+slot+"0"+pon_port+onuid,2)

                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c public '+str(olt_ip)+' 1.3.6.1.4.1.8886.18.3.1.3.1.1.16.'+str(big_onu_id),shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                dist = t[1]

                return [TELEPHONE_NUMBER,state,_1490,_1550,_1310,dist]
            else:
                state = "offline"
                return [TELEPHONE_NUMBER,state,'-','-','-','-']

        elif res[0].upper() == "FIBERHOME":
            gp = res[2].split('/')

            ifindex = (int(gp[1])*33554432)+(int(gp[2])*524288)+(int(onuid)*256)
            #onoff
            p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c adsl '+str(olt_ip)+' 1.3.6.1.4.1.5875.800.3.81.1.1.11.'+str(gp[1])+'.'+str(gp[2])+'.'+onuid,shell=True,stdout=subprocess.PIPE)
            time.sleep(1)
            p.kill()

            output = p.communicate()
            output = output[0].decode("utf-8").strip()

            t = output.split('= INTEGER: ')

            try:
                status = t[1].replace(' ', '')
            except:
                return [TELEPHONE_NUMBER,'-','-','-','-','-']

            if int(status) == 1:
                state = "online"
                #1490
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c adsl '+str(olt_ip)+' 1.3.6.1.4.1.5875.800.3.9.3.3.1.6.'+str(ifindex),shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                _1490 = int(t[1])/100

                #1550
                _1550 = "-"

                #1310
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c adsl '+str(olt_ip)+' 1.3.6.1.4.1.5875.800.3.9.3.3.1.7.'+str(ifindex),shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                _1310 = int(t[1])/100

                #distance
                p = subprocess.Popen('/usr/bin/snmpwalk -v2c -r 3 -t 8 -c adsl '+str(olt_ip)+' 1.3.6.1.4.1.5875.800.3.9.6.1.1.1.'+str(ifindex),shell=True,stdout=subprocess.PIPE)
                time.sleep(1)
                p.kill()

                output = p.communicate()
                output = output[0].decode("utf-8").strip()

                t = output.split('= INTEGER: ')

                dist = t[1]

                return [TELEPHONE_NUMBER,state,_1490,_1550,_1310,dist]
            else:
                state = "offline"
                return [TELEPHONE_NUMBER,state,'-','-','-','-']
    except:
        return [TELEPHONE_NUMBER,'-','-','-','-','-']

#end getData
if __name__ == "__main__":

    team = sys.argv[1]

    olt_n = sys.argv[1]
    l1_n =  sys.argv[2]
    l2_n =  sys.argv[3]


    con = cx_Oracle.connect(
        "cmtsusr/pwdcmts@10.50.25.76/NQIDB",encoding="UTF-8", nencoding="UTF-8"
    )

    cur = con.cursor()

    if l2_n.upper() != 'ALL':
        sql = "select circuit,olt_vendor as vendor,olt_ip,gpon_port,onu_id,olt_name,SPLITTER_L1,SPLITTER_L2 from app_circuit_profile@DBL_FDSDB where olt_name=:1 and SPLITTER_L1 = :2  and SPLITTER_L2 = :3 "
        cur.execute(sql,{'1':olt_n,'2':l1_n,'3':l2_n})
        tres = cur.fetchall()


    elif l1_n.upper() != "ALL":
        sql = "select circuit,olt_vendor as vendor,olt_ip,gpon_port,onu_id,olt_name,SPLITTER_L1,SPLITTER_L2 from app_circuit_profile@DBL_FDSDB where olt_name=:1 and SPLITTER_L1 = :2 "
        cur.execute(sql,{'1':olt_n,'2':l1_n})
        tres = cur.fetchall()


    else:
        sql = "select circuit,olt_vendor as vendor,olt_ip,gpon_port,onu_id,olt_name,SPLITTER_L1,SPLITTER_L2 from app_circuit_profile@DBL_FDSDB where olt_name=:1  "
        cur.execute(sql,{'1':olt_n})
        tres = cur.fetchall()




    # close cursor
    cur.close()

    # close DB
    con.close()

    new_arr = []
    for x in tres:
        #VENDOR,OLT_IP,GPON_PORT,ONU_ID,TELEPHONE_NUMBER
        new_arr.append([x[1],x[2],x[3],x[4],x[0]])


    # print(json.dumps(new_arr))

    worker = mp.cpu_count()
    pool = mp.Pool(processes=int(worker*15))
    res = pool.map(getData,new_arr)
    pool.close()

    new_tres = []
    for x in tres:
        for y in res :
            if str(x[0]) == str(y[0]):
                a = {}

                a["CIRCUIT"] = x[0]
                a["OLT_VENDOR"] = x[1]
                a["ONU_ID"] = x[4]
                a["OLT_NAME"] = x[5]
                a["L1_SPLITTER"] = x[6]
                a["L2_SPLITTER"] = x[7]
                a["OLT_IP"] = x[2]
                a["GRON_PORT"] = x[3]
                a["STATUS"] = y[1]
                a["1490RX"] = y[2]
                a["1550RX"] = y[3]
                a["1310TX"] = y[4]
                a["DISTANCE"] = y[5]

                new_tres.append(a)
        #end for y
    #end for x


    print(json.dumps(new_tres))

#end if__main__
