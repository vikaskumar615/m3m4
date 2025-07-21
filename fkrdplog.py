import os
import re
import requests
import json
import pytz
from datetime import datetime
import time

filename = ''
path = "./"


def gettimeofoutput():
    try:
        global filename
        alltimes = re.findall('\[(.*?)\]', open(path + filename).read())
        first = datetime.strptime(alltimes[0], '%H:%M:%S')
        last = datetime.strptime(alltimes[-1], '%H:%M:%S')
        timediff = last - first
        timediff = int(timediff.total_seconds())
        return timediff
    except Exception as e:
        print(str(e))
        return None


def reboot():
    os.system("reboot")
    return


def getavgresults(last=10):
    try:
        global filename
        with open(path + filename, 'r') as f:
            data = f.readlines()

        data = data[-last:]
        avg = sum = 0
        for i in data:
            sum = sum + int(i)
        avg = sum // last
        return str(avg)
    except Exception as e:
        print(str(e))
        return None


def getlastupdate():
    try:
        global filename
        lasttime = os.path.getmtime(path + filename)
        timezone = pytz.timezone("Asia/Kolkata")
        dateTime = datetime.fromtimestamp(lasttime).astimezone(
            timezone).strftime('%d-%m-%y %H:%M')
        return dateTime
    except Exception as e:
        print(str(e))
        return None


def getservername():
    try:
        global filename
        if os.path.isfile("servername.txt") == False:
            with open(path + filename) as f:
                data = f.read()
            res = re.search('(MA|W)[\s]*-[\s]*(.*?)/', data)
            with open("servername.txt", "w") as f:
                f.write(res[2])
                name = res[2].strip()
        else:
            with open('servername.txt') as f:
                name = f.read().strip()
        return name
    except Exception as e:
        print(str(e))
        return None


def getipinfo():
    try:
        ip_details = {}
        try:
            response = requests.get(
                "https://ip-info.ff.avast.com/v2/info").content.decode()
            jsondata = json.loads(response)
            ip_details["ip"] = jsondata["ip"]
            ip_details["country"] = jsondata["country"]
            ip_details["city"] = jsondata["city"]
        except Exception as e:
            try:
                response = requests.get(
                    "https://napps-2.com/v1/helpers/ips/insights").content.decode()
                jsondata = json.loads(response)
                ip_details["ip"] = jsondata["ip"]
                ip_details["country"] = jsondata["country"]
                ip_details["city"] = jsondata["city"]
            except Exception as e:
                try:
                    response = requests.get(
                        "http://ipwho.is/").content.decode()
                    jsondata = json.loads(response)
                    ip_details["ip"] = jsondata["ip"]
                    ip_details["country"] = jsondata["country_code"]
                    ip_details["city"] = jsondata["city"]
                except Exception as e:
                    response = requests.get(
                        "http://api.db-ip.com/v2/free/self/").content.decode()
                    jsondata = json.loads(response)
                    ip_details["ip"] = jsondata["ipAddress"]
                    ip_details["country"] = jsondata["countryCode"]
                    ip_details["city"] = jsondata["city"]
                #response = requests.get("http://ip-api.com/json/").content.decode()

        return ip_details
    except Exception as e:
        print("IP fetch Exception")
        print(str(e))
        return None


def updatetoserver(servername=""):
    try:
        global filename
        filename = servername.strip("/") + "_output.txt"

        try:
            with open(servername.strip("/")+"_lastupdatesent.txt", 'r') as f:
                lasttime = f.read().strip()
                if int(time.time()) - int(lasttime) < 300:
                    return
        except:
            pass
        data = {
            "server": servername,
            "ip": getipinfo(),
            "modification_time": getlastupdate(),
            "consumed_time": gettimeofoutput()
        }

        post = json.dumps(data)
        print(post)
        url = "http://rdptv.lalbox.tech/rdplog/update1.php"
        response = requests.post(url, data=post).content.decode()
        with open(servername.strip("/")+"_lastupdatesent.txt", 'w') as f:
            f.write(str(int(time.time())))

        if response.find("updatefile") != -1:
            jsondata = json.loads(response)
            link = jsondata["link"]
            path = jsondata["pathname"]
            r = requests.get(link)
            with open(path, 'wb') as f:
                f.write(r.content)
        if response.find("\"reboot\":\"yes\"") != -1:
            reboot()
        return
    except Exception as e:
        print(str(e))
        return None


if __name__ == '__main__':
    updatetoserver("oracle3pk")
    print(getlastupdate())
    print(gettimeofoutput())
