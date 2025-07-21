import sqlite3
from urllib.request import Request, urlopen
import logging
from logging.handlers import RotatingFileHandler
import traceback
import gzip
import re
import json
import ssl
import inspect
import shutil
import urllib
import requests
import os

ssl._create_default_https_context = ssl._create_unverified_context
'''
http_proxy = "http://127.0.0.1:8888"
https_proxy = "https://127.0.0.1:8888"

proxyDict = {
    "http": http_proxy,
    "https": https_proxy,
}

proxy_support = urllib.request.ProxyHandler(proxyDict)
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)
'''

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.ERROR)
handler = RotatingFileHandler("log.txt", maxBytes=10000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def block(foldername):
    #checkstop(foldername)
    try:
        filename = "blocked.txt"
        try:
            f = open(filename, "r+")
            get_contents = f.read()
            f.close()
        except FileNotFoundError:
            f = open(filename, "w+")
            get_contents = f.read()
            f.close()

        try:
            #url = "https://api.telegram.org/bot923259452:AAG1tBRBM7PIIYUL1g789IP4tBMgsI8uOJg/getUpdates?offset=-1"
            telegramurl = "http://rdptv.lalbox.tech/fkwebhook/fkcommands.php"

            header = {}
            header.update([("upgrade-insecure-requests", "1")])
            header.update([("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.32 Safari/537.36")])
            header.update([("accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3")])

            try:
                r = requests.get(telegramurl, headers=header, proxies={"http": "", "https": ""}, timeout=15, verify=False)
            except Exception as e:
                return
        except:
            return

        try:
            messages = r.json()
            del r
        except Exception as e:
            return

        #messages = json.loads(html)
        #for val2 in messages["result"]:
        for message in messages:
            if message!="message":
                continue
            else:
                message = messages
            try:
                text = message["message"].get("text", "")
            except Exception:
                return

            if text.find("/block") != -1:

                text = text.replace("/block", "")
                text = text.replace("@mausa_bot", "")
                text = text.strip()

                frm = inspect.stack()[1]
                mod = inspect.getmodule(frm[0])
                #print(os.path.basename(mod.__file__))

                if text.lower().find("=")!=-1:
                    firstpart=text.lower().split("=")[0]
                else:
                    firstpart=text.lower()

                if get_contents.find("," + firstpart + "=") != -1:
                    get_contents = re.sub(firstpart + "=(.*?),","", get_contents)
                    fa = open(filename, "w+")
                    fa.write(get_contents)
                    fa.close()

                f = open(filename, "a+")

                if get_contents.find("," + text.lower()) == -1 and get_contents.find("," + text.lower() + ",") == -1:
                    if text == "@mausa_bot":
                        return
                    else:
                        url = "https://api.telegram.org/bot923259452:AAG1tBRBM7PIIYUL1g789IP4tBMgsI8uOJg/sendMessage?chat_id=-1001590697850&disable_notification=1&parse_mode=HTML&text=" + urllib.parse.quote(foldername + " <b>Blocked keyword " + text + "</b>")

                    f.write(',' + text.lower())
                    uclient=Request(url)

                    uclient.add_header("User-Agent",
                                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
                    uclient.add_header("Accept", "*/*")
                    uclient.add_header("Accept-Language",
                                       "en-GB,en-US;q=0.9,en;q=0.8")
                    uclient.add_header("Accept-Encoding", "gzip, deflate")
                    uclient.add_header("Connection", "keep-alive")
                    try:
                        response=urlopen(uclient, timeout=120)
                    except Exception as e:
                        pass


                f.close()

            elif text.find("/remove") != -1:
                text = text.replace("/remove", "")
                text = text.replace("@mausa_bot", "")
                text = text.strip()

                frm = inspect.stack()[1]
                mod = inspect.getmodule(frm[0])
                # print(os.path.basename(mod.__file__))

                if get_contents.find("," + text.lower()) != -1 and text != "" and text != None:
                    get_contents = get_contents.replace("," + text.lower(), "")
                    if text == "@mausa_bot":
                        return
                    else:
                        url = "https://api.telegram.org/bot923259452:AAG1tBRBM7PIIYUL1g789IP4tBMgsI8uOJg/sendMessage?chat_id=-1001590697850&disable_notification=1&parse_mode=HTML&text=" + urllib.parse.quote(
                            foldername + " <b>removed keyword " + text.lower() + "</b>")

                    fa = open(filename, "w+")
                    fa.write(get_contents)
                    fa.close()
                    uclient = Request(url)

                    uclient.add_header("User-Agent",
                                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
                    uclient.add_header("Accept", "*/*")
                    uclient.add_header("Accept-Language",
                                       "en-GB,en-US;q=0.9,en;q=0.8")
                    uclient.add_header("Accept-Encoding", "gzip, deflate")
                    uclient.add_header("Connection", "keep-alive")
                    response = urlopen(uclient, timeout=120)

            elif text.find("/stopcheckout") != -1:
                text = text.replace("/stopcheckout", "")
                text = text.replace("@mausa_bot", "")
                text = text.strip()

                frm = inspect.stack()[1]
                mod = inspect.getmodule(frm[0])
                # print(os.path.basename(mod.__file__))

                try:
                    f = open("checkout.txt", "r+")
                    get_contents = f.read()
                    f.close()
                except FileNotFoundError:
                    f = open("checkout.txt", "w+")
                    get_contents = f.read()
                    f.close()

                if get_contents.find(text) != -1:
                    continue

                f = open("checkout.txt", "w+")
                f.write(text)
                f.close()

                url = "https://api.telegram.org/bot923259452:AAG1tBRBM7PIIYUL1g789IP4tBMgsI8uOJg/sendMessage?chat_id=-1001590697850&disable_notification=1&parse_mode=HTML&text=" + urllib.parse.quote(
                        "<b>" + foldername + " AutoCheckout stop</b> = "+text+" !! \n\n To stop keywords - true,yes,1,nponly,plusonly,codonly")

                uclient = Request(url)

                uclient.add_header("User-Agent",
                                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
                uclient.add_header("Accept", "*/*")
                uclient.add_header("Accept-Language",
                                   "en-GB,en-US;q=0.9,en;q=0.8")
                uclient.add_header("Accept-Encoding", "gzip, deflate")
                uclient.add_header("Connection", "keep-alive")
                response = urlopen(uclient, timeout=120)

            elif text.find("/donotsave") != -1:
                text = text.replace("/donotsave", "")
                text = text.replace("@mausa_bot", "")
                text = text.strip()

                frm = inspect.stack()[1]
                mod = inspect.getmodule(frm[0])
                # print(os.path.basename(mod.__file__))

                try:
                    f = open("donotsave.txt", "r+")
                    get_contents = f.read()
                    f.close()
                except FileNotFoundError:
                    f = open("donotsave.txt", "w+")
                    get_contents = f.read()
                    f.close()

                if text == "" and text == None:
                    text = "ghjghhjkhkjh"

                if get_contents.find(text) != -1 and text != "" and text != None:
                    return
                else:
                    f = open("donotsave.txt", "w+")
                    f.write(text)
                    f.close()

            elif text.find("/permanent") != -1:
                if message["message"]["reply_to_message"]==None:
                    return
                text = message["message"]["reply_to_message"].get("text", "")
                temp = re.search("lid=(.*?)&", text)
                lid = temp[1].strip()
                temp = re.search("([\d\.,]*?) \+ 0", text)
                price = temp[1].strip()
                temp = re.search("\((.*?)\)(.*?)", text)
                filename = temp[1].strip()
                temp = re.search("=> (.*?)(?= - LST)", text)
                name = temp[1].strip()
                operation = insert(lid, price, filename, name)

                '''
                if operation=="success":
                    frm = inspect.stack()[1]
                    mod = inspect.getmodule(frm[0])
                    # print(os.path.basename(mod.__file__))

                    
                    url = "https://api.telegram.org/bot923259452:AAG1tBRBM7PIIYUL1g789IP4tBMgsI8uOJg/sendMessage?chat_id=-1001590697850&disable_notification=1&parse_mode=HTML&text=" + urllib.parse.quote(
                        "<b>" + foldername + " " + lid + " </b> saved in DB. !!")

                    uclient = Request(url)
                    uclient.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
                    uclient.add_header("Accept", "*/*")
                    uclient.add_header("Accept-Language", "en-GB,en-US;q=0.9,en;q=0.8")
                    uclient.add_header("Accept-Encoding", "gzip, deflate")
                    uclient.add_header("Connection", "keep-alive")
                    response = urlopen(uclient, timeout=120)
                    '''

            elif text.find("/permanentdelete") != -1:
                text = message["message"]["reply_to_message"].get("text", "")
                temp = re.search("lid=(.*?)&", text)
                lid = temp[1].strip()
                temp = re.search("([\d\.,]*?) \+ 0", text)
                price = temp[1].strip()
                temp = re.search("\((.*?)\)(.*?)", text)
                filename = temp[1].strip()
                temp = re.search("=> (.*?)(?= - LST)", text)
                name = temp[1].strip()
                operation = delete(lid)

                '''
                if operation=="success":
                    frm = inspect.stack()[1]
                    mod = inspect.getmodule(frm[0])
                    # print(os.path.basename(mod.__file__))

                    
                    url = "https://api.telegram.org/bot923259452:AAG1tBRBM7PIIYUL1g789IP4tBMgsI8uOJg/sendMessage?chat_id=-1001590697850&disable_notification=1&parse_mode=HTML&text=" + urllib.parse.quote(
                        "<b>" + foldername + " " + lid + " </b> saved in DB. !!")

                    uclient = Request(url)
                    uclient.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
                    uclient.add_header("Accept", "*/*")
                    uclient.add_header("Accept-Language", "en-GB,en-US;q=0.9,en;q=0.8")
                    uclient.add_header("Accept-Encoding", "gzip, deflate")
                    uclient.add_header("Connection", "keep-alive")
                    response = urlopen(uclient, timeout=120)
                    '''

        del get_contents
        return
    except Exception as e:
        print(str(e))
        logger.error("block" + str(e))
        logger.error(traceback.format_exc())
        return

def remove_dups():
    try:
        f = open("blocked.txt", "r")
        text1 = f.read()
        text1 = text1.rstrip(",")
        f.close()

        res = []
        str = ""
        res.append(set(text1.split(",")))
        for i in res[0]:
            str += i + ","

        if len(text1)+1 != len(str):
            f = open("blocked.txt", "w+")
            f.write(str)
            f.close()

        del text1
        return
    except Exception as e:
        print(str(e))
        logger.error("remove_dups" + str(e))
        logger.error(traceback.format_exc())
        return None

def checkstop(foldername):
    try:
        f = open("checkout.txt", "r")
        get_contents_1 = f.read()
        f.close()


        if get_contents_1.find("true") != -1 or get_contents_1.find("yes") != -1 or get_contents_1.find("1") != -1:
            url = "https://api.telegram.org/bot923259452:AAG1tBRBM7PIIYUL1g789IP4tBMgsI8uOJg/sendMessage?chat_id=-1001590697850&disable_notification=1&parse_mode=HTML&text=" + urllib.parse.quote(
                "<b>" + foldername + " \n Checkout stopped!\n URGENT MESSAGE</b>")

            uclient = Request(url)

            uclient.add_header("User-Agent",
                               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
            uclient.add_header("Accept", "*/*")
            uclient.add_header("Accept-Language",
                               "en-GB,en-US;q=0.9,en;q=0.8")
            uclient.add_header("Accept-Encoding", "gzip, deflate")
            uclient.add_header("Connection", "keep-alive")
            response = urlopen(uclient, timeout=120)
    except Exception as e:
        print(str(e))
        logger.error("checkstop" + str(e))
        logger.error(traceback.format_exc())
        return None

def insert(lid,price,filename,name):
    try:
        createtable()
        conn = sqlite3.connect("mydatabase.db")
        cus = conn.cursor()

        try:
            res = select(lid)
            if lid in res and float(price) == float(res[lid]):
                return "failed"
            cus.execute("INSERT INTO permanent VALUES(?,?,?,?)", (lid, float(price), filename, name))
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            conn.commit()
            conn.close()
            update(lid=lid, filename=filename, price=price, name=name)

        return "success"
    except Exception as e:
        print(str(e))
        logger.error("insert" + str(e))
        logger.error(traceback.format_exc())
        return None

def update(lid="", price=99999, name="", filename=""):
    try:
        conn = sqlite3.connect("mydatabase.db")
        cus = conn.cursor()

        cus.execute("""Update permanent set price = ?, name = ?, filename=? where lid = ?""", (float(price), name, filename, lid))

        conn.commit()
        conn.close()
        return
    except Exception as e:
        print(str(e))
        logger.error("update" + str(e))
        logger.error(traceback.format_exc())
        return None

def delete(lid=""):
    try:
        conn = sqlite3.connect("mydatabase.db")
        cus = conn.cursor()

        cus.execute("DELETE FROM permanent WHERE lid=?", (lid,))

        conn.commit()
        conn.close()
        return
    except Exception as e:
        print(str(e))
        logger.error("delete" + str(e))
        logger.error(traceback.format_exc())
        return None

def select(lid="",filename=""):
    try:
        conn = sqlite3.connect("mydatabase.db")
        cus = conn.cursor()
        rows=[]
        #cus.execute("SELECT * FROM amazon WHERE filename = ? and asin=?", (filename, asin,))
        if lid!="" and filename=="":
            cus.execute("SELECT lid, price FROM permanent where lid=?", (lid,))
        elif lid=="" and filename!="":
            cus.execute("SELECT lid, price FROM permanent where filename=?", (filename,))
        elif lid!="" and filename!="":
            cus.execute("SELECT lid, price FROM permanent where lid=? and filename=?", (lid,filename,))
        else:
            cus.execute("SELECT lid, price FROM permanent")

        for i in cus:
            rows.append(i)

        results = {}
        for row in rows:
            results[row[0]] = row[1]
        conn.commit()
        cus.close()
        conn.close()

        #listToStr = ' '.join([str(elem) for elem in results])
        del conn
        del cus
        return results
    except Exception as e:
        print(str(e))
        logger.error("select" + str(e))
        logger.error(traceback.format_exc())
        return None

def createtable():
    try:
        conn = sqlite3.connect("mydatabase.db")
        cus = conn.cursor()
        cus.execute("""CREATE TABLE IF NOT EXISTS permanent (
        lid text NOT NULL,
        price real DEFAULT 99999,
        filename text,
        name text,
        PRIMARY KEY (lid)
        )""")

        conn.commit()
        conn.close()
        return
    except Exception as e:
        print(str(e))
        logger.error("createtable" + str(e))
        logger.error(traceback.format_exc())
        return None



if __name__ == '__main__':
    createtable()
    block("testing..")
    remove_dups()
