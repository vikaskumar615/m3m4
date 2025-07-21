import os
import re
import requests
import psutil
import time

def seconds_elapsed():
    return time.time() - psutil.boot_time()

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])

    return uptime_seconds

def download(name):
    url = "http://oracle1.lalbox.tech/amz/flipkart/"+name
    response = requests.get(url).content
    if response != None and len(response)!=0 and response.find(b"/lander")==-1 and response.find(b"DOCTYPE")==-1:
        with open(name, 'wb') as f:
            f.write(response)
        
def start():
    download("mydatabase.db")
    download("saved_and_blocked.txt")
    download("blocked.txt")
    download("main2links.txt")
    print("All files downloaded")

if __name__ == '__main__':
    start()