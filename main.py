import base64
import concurrent.futures
import random
import time
import uuid
from multiprocessing.pool import ThreadPool
from urllib.request import Request, urlopen
import logging
from logging.handlers import RotatingFileHandler
import traceback
import gzip
import re
import json
import datetime
import pytz
import urllib.parse
import ssl
import requests
import asyncio
import aiohttp

from requests.packages import urllib3
import os
if os.name=="nt123":
    import httpx
else:
    from curl_cffi import requests
import block
import urllib

#pip install curl_cffi --upgrade

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.ERROR)
handler = RotatingFileHandler("log.txt", maxBytes=10000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def random_useragent(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
        if random.randrange(num):
            continue
        line = aline

    list = line.split("->")
    return list[2].strip()

def myasyncsend(telegramurl):
    try:
        header = {}
        header.update([("accept-language", "en-US,en;q=0.9")])
        header.update([("accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3")])
        header.update([("accept-encoding", "gzip, deflate")])
        header.update([("User-Agent", "Mozilla/5.0 (Linux; Android 8.1.0; ASUS_X00TD Build/OPM1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/102.0.5005.78 Mobile Safari/537.36")])

        asyncio.run(async_request(telegramurl, headers=header, proxies="", timeout=15, verify=False))
    except:
        return

async def async_request(url, headers, proxies, timeout, verify):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, proxy=proxies, timeout=timeout, ssl=verify) as resp:
            response = await resp.text()
            if response.find("Bad Request") != -1:
                logger.error(url + "\r\n" + response)
            print(response)

def deletesavedtext(filename):
    try:
        f = open("donotsave.txt", "r+")
        get_contents = f.read().strip()
        f.close()
    except FileNotFoundError:
        f = open("donotsave.txt", "w+")
        get_contents = f.read().strip()
        f.close()

    textfound = 0
    if get_contents == "" or get_contents == None:
        return
    else:
        try:
            with open(filename, "r") as w:
                lines = w.readlines()
            with open(filename, "w+") as w:
                for line in lines:
                    if get_contents not in line:
                        w.write(line)
                    else:
                        textfound = 1
            if textfound == 1:
                telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=-1001590697850&disable_notification=1&parse_mode=HTML&text=" + urllib.parse.quote("IN " + filename + " " + get_contents + " lines cleared")
                myasyncsend(telegramurl)

        except Exception as e:
            print(str(e))

def checkblocklist(name, total, listingid):
    try:
        with open("blocked.txt", "r") as text_fileh:
            text_file = text_fileh.read().strip(",")
        blocked = text_file.split(',')

        name = name.lower().strip()
        namearray = name.strip(",").strip("(").strip(")").split(" ")

        bloc=0
        reason = ""
        for word in namearray:
            word = word.strip(",").strip("(").strip(")").strip(".")
            for bla in blocked:
                bprice = None
                if bla.find("=") != -1:
                    bwop = bla.split("=")
                    bla = bwop[0]
                    bprice = bwop[1]
                if listingid.lower() == bla.lower():
                    bloc = 1
                    word = bla
                    #print("blocked " + bla + " in " + listingid)
                    break
                if bla.find(" ") != -1 and name.lower().find(bla.lower()) != -1 and reason.find(bla)==-1:
                    bloc = 1
                    word = bla
                    #print("blocked " + bla + " in " + name)
                    break
                if bla.lower() == word.lower() and bla != "" and word != "":
                    bloc = 1
                    #print("blocked " + word + " in " + name)
                    break
            if bloc == 1:
                packof = re.search("pack of (\d+)(\s|,|\)|$)", name.lower())
                if bprice != None and bprice!='':
                    packoftotal=total
                    if packof!=None and packof[1]!=None and packof[1]!='' and packof[1]!="1":
                        packoftotal = int(total)/int(packof[1])
                    if float(bprice) >= float(total) or float(bprice) >= float(packoftotal):
                        bloc = 0
                    reason = bla + "=" + str(bprice)
                else:
                    reason = bla
                if bloc == 1:
                    break
            else:
                bla = None

        del text_file
        del blocked
        del namearray
        return bloc, reason
    except Exception as e:
        logger.error("blocklist" + str(e))
        logger.error(traceback.format_exc())
        return 0,None


def checkforname(filename):
    names = ["men","man","women","woman","cloth","bulb"]
    for nam in names:
        if filename.find(nam) != -1:
            return True
    return False

def loadlinks(data):
    try:
        with open("main2links.txt") as f_in:
            jsonarray = json.loads(f_in.read())
            url = jsonarray[data]
            return url
    except Exception as e:
        logger.error("loadlinks" + str(e))
        logger.error(traceback.format_exc())
        return None

def checkout_start(html1, name, urls, listingid, cp, mrp, discount, filename, pid):
    falsealert = 0
    try:
        orname = urllib.parse.quote(name[:30])
        params = []
        pool = ThreadPool(80)
        for z in urls:
            params.append([z, listingid, cp, mrp, discount, filename, orname, pid])
        results = pool.imap_unordered(fetch_url, params)
        try:
            for url, html, error in results:
                print("%r fetched" % (url))
                if html.find("Currently out of stock") != -1 or html.find(
                        "Item not available for purchase") != -1:
                    falsealert = 1
        except:
            pass
        pool.terminate()
        pool.join()
        block.block(filename)

        if not os.path.exists('logggs'):
            os.makedirs('logggs')
        with open("logggs/"+listingid+".html", "w+") as w:
            w.write(name+"\n"+str(cp)+"\n"+str(mrp)+"\n"+str(discount)+"\n"+filename+"\n"+str(html1.encode('utf-8')))

    except Exception as e:
        logger.error("checkout_start" + str(e))
        logger.error(traceback.format_exc())
    return falsealert


def fetch_url(params):
    try:
        url = params[0]
        listingid = params[1]
        price = str(params[2])
        mrp = str(params[3])
        discount = str(params[4])
        filename = params[5]
        name = params[6]
        pid = params[7]
        print("going to checkout " + listingid)
        uclient = Request(url + "&itemid=" + listingid + "&maxe=" + price + "&filename=" + filename + "&mrp=" + mrp + "&discount=" + discount + "&pid=" + pid + "&name=" + name)


        uclient.add_header("User-Agent",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
        uclient.add_header("Accept", "*/*")
        uclient.add_header("Accept-Language", "en-GB,en-US;q=0.9,en;q=0.8")
        uclient.add_header("Accept-Encoding", "gzip, deflate")
        uclient.add_header("Connection", "keep-alive")
        response = urlopen(uclient, timeout=60)

        if response.info().get('Content-Encoding') == 'gzip':
            html = gzip.decompress(response.read()).decode('utf8')
        elif response.info().get('Content-Encoding') == 'deflate':
            html = response.read().decode('utf8')
        else:
            html = response.read().decode('utf8')

        return listingid, html, None
    except Exception as e:
        return listingid, "null", e


def checkstatus(url, listingid):
    data = '{"pageUri":"' + url + '","pageType":"PRODUCTPAGE_' + url + '","locationContext":{"pincode":null},"pageContext":{"pageNumber":1,"paginatedFetch":false,"paginationContextMap":{},"trackingContext":{"context":{"eVar61":""}}}}'
    binary_data = data.encode('utf-8')

    myurl = "https://www.flipkart.com/api/4/page/fetch?reqhash=2243276226&usePrefetch=true&prefetchKey=PRODUCTPAGE_" + urllib.parse.quote(
        url) + "&cacheFirst=false"
    uclient = Request(myurl, data=binary_data)

    uclient.add_header("user-agent",
                       "Mozilla/5.0 (Linux; Android 7.1.1; Lenovo K8 Plus) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36")
    uclient.add_header("Accept", "*/*")
    uclient.add_header("Content-Type", "application/json")
    uclient.add_header("X-user-agent",
                       "Mozilla/5.0 (Linux; Android 7.1.1; Lenovo K8 Plus) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36 FKUA/msite/0.0.1/msite/Mobile")
    uclient.add_header("Accept-Encoding", "gzip, deflate")
    uclient.add_header("Cookie", "SN=VI268E3765C793420081708A88F08F54D9.TOK5B26758624B94EBC948BE3BB4D7FB4AC.1658325269.LI; S=d1t15YD8/Pz8/OT8/P18/P10/P4r/TRmB9cwf8QljgKmmqPz6W6fkV1QsCE3mTYqhaEqYftry5GCn76fn4pd8jl9Exg==")

    try:
        response = urlopen(uclient, timeout=10)
    except Exception as e:
        # print(filename + " : " + str(e))
        return False

    if response.info().get('Content-Encoding') == 'gzip':
        html = gzip.decompress(response.read()).decode('utf8')
    elif response.info().get('Content-Encoding') == 'deflate':
        html = response.read().decode('utf8')
    else:
        html = response.read().decode('utf8')

    jsonarray = json.loads(html)

    status = jsonarray["RESPONSE"]["pageData"]["pageContext"]["trackingDataV2"].get("productStatus", "IN_STOCK")
    lid = jsonarray["RESPONSE"]["pageData"]["pageContext"].get("listingId", "")
    if status.lower().find("out of stock") != -1:
        return True
    elif status.lower().find("out of stock") == -1 and lid != listingid:
        return True
    else:
        return False


def flipkart_parse(filename, telegram, force, myurl, res_queue, stop_not_assured=False, s=None):
    chatid = "-1001356446279"
    d = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    date = d.strftime("%d-%m-%y")
    hour = d.hour

    urls = Purls = loadlinks("urls")
    NPurls = loadlinks("NPurls")
    Nighturls = loadlinks("Nighturls")
    takehighriskurls = loadlinks("takehighriskurls")
    notassuredurls = loadlinks("notassuredurls")

    if hour >= 2 and hour <= 6:
        urls = Nighturls

    try:
        f = open("checkout.txt", "r+")
        get_contents_1 = f.read()
        f.close()
    except FileNotFoundError:
        f = open("checkout.txt", "w+")
        get_contents_1 = f.read()
        f.close()

    if get_contents_1.find("true") != -1 or get_contents_1.find("yes") != -1 or get_contents_1.find("1") != -1:
        urls = NPurls = []
    elif get_contents_1.find("nponly") != -1:
        urls = NPurls
    elif get_contents_1.find("plusonly") != -1:
        NPurls = urls

    if get_contents_1.find("codonly") != -1:
        temmp = []
        for sss in urls:
            temmp.append(sss.replace("phonepe=yes", "cod=yes"))
        urls = temmp
        temmp = []
        for sss in NPurls:
            temmp.append(sss.replace("phonepe=yes", "cod=yes"))
        NPurls = temmp
    elif get_contents_1.find("gvonly") != -1:
        temmp = []
        for sss in urls:
            temmp.append(sss.replace("phonepe=yes", "gv=yes"))
        urls = temmp
        temmp = []
        for sss in NPurls:
            temmp.append(sss.replace("phonepe=yes", "gv=yes"))
        NPurls = temmp
    elif get_contents_1.find("gpayonly") != -1:
        temmp = []
        for sss in urls:
            temmp.append(sss.replace("phonepe=yes", "gpay=yes"))
        urls = temmp
        temmp = []
        for sss in NPurls:
            temmp.append(sss.replace("phonepe=yes", "gpay=yes"))
        NPurls = temmp

    text_file = open("blocked.txt", "r")
    text_file = text_file.read().strip(",")
    blocked = text_file.split(',')

    try:
        f = open(filename, "r+")
        get_contents = f.read()
        f.close()
    except FileNotFoundError:
        f = open(filename, "w+")
        get_contents = f.read()
        f.close()
        telegram = "off"

    if hour == 3 or hour == 4:
        try:
            if os.path.exists("template_"+filename) and date not in get_contents:
                print("template found.... copying to " + filename)
                with open("template_"+filename, 'r') as source:
                    content = source.read()
                with open(filename, 'w+') as destination:
                    destination.write(date + "\r\n" + content)
            elif date not in get_contents:
                f = open(filename, "w+")
                f.write(date + "\r\n")
                f.close()
        except Exception as e:
            print("template cant be copied: " + str(e))

        telegram = "off"

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

    # myurl = myurl + "&p%5B%5D=facets.availability%255B%255D%3DInclude%2BOut%2Bof%2BStock"

    filtersafe = 99999

    try:
        filtersafe = re.search("facets.price_range.to%3D(.*?)(?=&|$)", myurl)
        filtersafe = int(filtersafe[1])
    except Exception as e:
        filtersafe = 99999

    if myurl.find("Flipkart%2BAssured")!=-1:
        myurl = myurl.replace("Flipkart%2BAssured", "F-Assured")

    if myurl.find("Plus+%28FAssured%29")!=-1:
        myurl = myurl.replace("Plus+%28FAssured%29", "F-Assured")

    if myurl.find("Plus%2B%2528FAssured%2529")!=-1:
        myurl = myurl.replace("Plus%2B%2528FAssured%2529", "F-Assured")

    try:
        header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "sec-ch-ua-mobile":"?0",
        "sec-ch-ua-platform":"\"Windows\"",
        "Upgrade-Insecure-Requests":"1",
        "Sec-Fetch-Site":"none",
        "Sec-Fetch-Mode":"navigate",
        "Origin": "https://www.flipkart.com",
        "Referer": "https://www.flipkart.com",
        "Sec-Fetch-User":"?1",
        "Sec-Fetch-Dest":"document",
        "Accept-Language":"en-GB,en;q=0.9", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding":"gzip, deflate, br"}

        try:
            if filename.find("grocery")!=-1:
                with open("cookie.txt") as fff:
                    cokie=fff.readlines()
                #header["Cookie"]=cokie[2].strip()

            with open("cookie.txt") as fff:
                cokie=fff.readlines()
            #header["Cookie"]=cokie[2].strip()
        except Exception as e:
            print(filename + " : cookie " + str(e))
            return

        l = list(header.items())
        random.shuffle(l)
        d_shuffled = dict(l)

        try:
            if os.name=="nt123":
                try:
                    #proxies = {"http://": "http://127.0.0.1:8888", "https://": "http://127.0.0.1:8888"}
                    proxies = {}
                    r = httpx.get(myurl, headers=d_shuffled, verify=False, proxies=proxies)
                except Exception as e:
                    r = httpx.get(myurl, headers=d_shuffled, verify=False, proxies=proxies)
            else:
                proxies = {"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888"}
                proxies = {}
                impersonations = ["chrome99_android","firefox147","chrome116","safari260","chrome146","edge101","safari260_ios","firefox135"]
                try:
                    r = requests.get(myurl, headers=d_shuffled, proxies=proxies, verify=False, impersonate=random.choice(impersonations))
                except:
                    r = requests.get(myurl, headers=d_shuffled, proxies=proxies, verify=False, impersonate="chrome110")

            html=r.text
            if r.status_code>=400:
                print(filename + " -> " + str(r.status_code) + " error")
                res_queue.put(str('{0:<35} 529 Error'.format(filename)))
                return

            if html.find("recaptcha")!=-1:
                print("recaptcha")
                return

        except Exception as e:
            print(filename + " : " + str(e))
            if str(e).find("404") != -1:
                flilename = "failed.txt"
                try:
                    fl = open(flilename, "r+")
                    get_contentsfl = fl.read()
                    fl.close()
                except FileNotFoundError:
                    fl = open(flilename, "w+")
                    get_contentsfl = fl.read()
                    fl.close()

                if date not in get_contentsfl:
                    telegramurl = "https://api.telegram.org/bot1311880981:AAG9eM_c62lH5ITjMp_OzR7Klp40e3urnjA/sendMessage?chat_id=" + chatid + "&parse_mode=HTML&text=" + urllib.parse.quote(
                        "<b>" + filename + " => Content Not Found</b> \n Flipkart dead.")
                    myasyncsend(telegramurl)

                    fl = open(flilename, "w+")
                    fl.write(date + "\r\n")
                    fl.close()
            return
    except Exception as e:
        print(filename + " : " + str(e))
        return

    try:
        if html.find("\"isLoggedIn\":false") != -1:
            telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=-1001590697850&parse_mode=HTML&text=" + urllib.parse.quote(
            "ACC LOGOUT \nL-(" + filename + ")")
            #myasyncsend(telegramurl)
    except Exception as e:
        print(str(e))

    ratwro = html

    try:
        mat = re.search("__INITIAL_STATE__ = (.*?)};", html)
        if mat:
            mat = mat[1] + "}"
        else:
            mat = re.search("{\"abExperiments\":.*}", html)
            mat = str(mat[0])
    except Exception as e:
        if html.find("Lot of rush for the best offers") == -1:
            fl = open("new_ex.html", "w+")
            fl.write(date + "\r\n" + str(e) + "\r\n" + myurl + "\r\n" + html)
            fl.close()
        print(filename + " -> Unknown page found.")
        return

    jsonarray = json.loads(mat)
    #jsonarray = copy.deepcopy(json.loads(mat))

    numberofresults = 0
    checkoutpro = 0
    pages = jsonarray["pageDataV4"]["page"]["data"].get("10003", "")
    totalproducts = jsonarray["pageDataV4"]["browseMetadata"].get("totalProducts", "")

    appliedfilter = 10000
    try:
        filterapplied = re.search(",\"appliedFilterCount\":(.*?),", html)
        appliedfilter = int(filterapplied[1])
    except Exception as e:
        appliedfilter = 10000

    fakepage=False
    try:
        suburl = re.search("https://www.flipkart.com(.*?)\?", myurl)
        suburl = suburl[1]
        if html.find(suburl)==-1:
            fakepage=True
    except Exception as e:
        return

    filterinlinks = re.findall("facets.(.*?)%3D", myurl)
    filterinlink = len(set(filterinlinks))
    if filterinlinks.count("price_range.from") == 1:
        filterinlink -= 1
    if myurl.find("facets.serviceability") != -1:
        filterinlink -= 1

    if appliedfilter == 0:
        telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=" + chatid + "&parse_mode=HTML&text=" + urllib.parse.quote(
            "<b>W-(" + filename + ") \n FILTER 0. \n"+str(totalproducts)+" products</b>")
        #myasyncsend(telegramurl)
        return

    if appliedfilter < filterinlink:
        telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=" + chatid + "&parse_mode=HTML&text=" + urllib.parse.quote(
            "<b>W-(" + filename + ") \n FILTER mismatch. \n"+str(appliedfilter)+" filters. "+str(totalproducts)+" products</b>")
        #myasyncsend(telegramurl)

    if fakepage == True and totalproducts>60:
        telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=" + chatid + "&parse_mode=HTML&text=" + urllib.parse.quote(
            "<b>W-(" + filename + ") \n FakePage detected. \n"+str(totalproducts)+" products</b>")
        myasyncsend(telegramurl)
        if not os.path.exists('logggs'):
            os.makedirs('logggs')
        with open("logggs/fakepage_"+str(random.randint(1, 100))+".html", "w+") as w:
            w.write(myurl+"\n"+filename+"\n"+str(html.encode('utf-8')))
        return

    # print(pages)

    d = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    currenttime = d.strftime("%H:%M:%S")

    #process only top 20 results
    limitonresults = 0

    for val1 in pages:
        try:
            for val2 in val1["widget"]["data"]["products"]:
                if 'adInfo' in val2:
                    continue
                limitonresults += 1
                if limitonresults > 20 and filename.find("grocery") == -1 and filename.find("mob") == -1 and filename.find("lap") == -1 and filename.find("tv") == -1 and filename.lower().find("ac_") == -1:
                    break
                val = val2["productInfo"]["value"]
                availability = val["availability"].get("displayState", "NO_AVAILABLE_LISTING")
                name = val["titles"].get("title", "").encode('ascii', 'ignore').decode('utf-8')
                name = str(name).strip()
                newname = val["titles"].get("newTitle", "").encode('ascii', 'ignore').decode('utf-8')
                newname = str(newname).strip()
                if name.find(newname)==-1 and newname != "":
                    name += " " + newname
                subtitle = val["titles"].get("coSubtitle", "").encode('ascii', 'ignore').decode('utf-8')
                if subtitle!="":
                    name += " \n " +  str(subtitle).strip()

                if name.lower().find("refurbished")!=-1 or name.lower().find("(refurbished)")!=-1:
                    continue

                if filename.find("grocery")!=-1:
                    availability = val["availability"].get("displayState", "ok")
                    mrp = str(val["pricing"]["prices"][0].get("value", "0"))
                    cp = str(val["pricing"]["prices"][1].get("value", "0"))
                    delcharge = "0"
                    ruflink = val["baseUrl"]
                    ruflink = "https://www.flipkart.com" + ruflink
                    listingid = val.get("listingId", "")
                    pid = val.get("id", "")
                    discount = int(val["pricing"].get("totalDiscount", "0"))
                    sellertype = "F_ASSURED"
                    chatid = "-1001775370994"
                else:
                    mrp = str(val["pricing"]["prices"][0].get("value", "0"))
                    try:
                        cp = str(val["pricing"]["prices"][1].get("value", "0"))
                    except Exception as e:
                        cp = mrp

                    cp1 = 0
                    try:
                        if len(val["pricing"]["prices"]) > 2:
                            for valll in val["pricing"]["prices"]:
                                if valll["priceType"] == "FSP":
                                    cp1 = valll.get("decimalValue", "0")
                                    break
                    except:
                        cp1 = 0
                    if float(cp) < float(cp1):
                        cp = str(cp1)
                    delcharge = "0"
                    discount = round((float(mrp) - float(cp)) * 100 / float(mrp))
                    #ruflink = val["smartUrl"].replace("dl.flipkart.com/dl", "www.flipkart.com")
                    ruflink = val["baseUrl"]
                    ruflink = "https://www.flipkart.com"+ruflink
                    listingid = val.get("listingId", "")
                    pid = val.get("id", "")

                    if pid!="" and listingid!="" and "LST"+pid[0:3] not in listingid:
                        print("false results. pid lid not matching - " + pid + "  " + listingid)
                        continue

                    sellertype = ""

                    try:
                        chatid = "-1001775370994"
                        sellertype = val["productCardTagDetails"][0].get("type", "")
                        if sellertype == "FOOD_PREFERENCE" or sellertype == "GROCERY":
                            continue
                    except Exception as e:
                        sellertype = "<strike>Not Assured</strike>"
                        chatid = "-1001356446279"
                        #continue

                docheckout = True

                total = float(cp) + float(delcharge)
                if total >= 500 and NPurls != None and Purls !=None:
                    urls = NPurls + Purls

                bypass_list = ['peter england', 'nutraj', 'Happilo', 'pepe', 'louis', 'jockey', 'kurlon', 'bata', 'raymond', 'allen', 'nike', 'puma', 'adidas', 'reebok', 'sketchers', 'cooper']
                bypassto = [ele for ele in bypass_list if(ele in name.lower())]

                if sellertype != "F_ASSURED" or float(cp) > filtersafe: # or appliedfilter < filterinlink:
                    if force == 1:
                        docheckout = True
                        urls = NPurls
                    elif bypassto == True and (float(cp) < 300 or float(discount)>70):
                        docheckout = True
                        urls = Purls
                    elif float(discount) > 85 and float(cp) < 1500 and stop_not_assured==False:
                        docheckout = True
                        urls = notassuredurls
                    elif float(discount) >= 95 and stop_not_assured==False:
                        docheckout = True
                        urls = notassuredurls
                    else:
                        docheckout = False
                        urls = NPurls
                else:
                    docheckout = True

                if total < 500 and sellertype == "F_ASSURED":
                    urls = Purls

                if ruflink.find(listingid) == -1:
                    link = ruflink + "&lid=" + listingid + "&sattr[]=size&st=size&affExtParam2=" + base64.b64encode(str(int(float(cp))).encode()).decode('ascii')
                else:
                    link = ruflink + "&sattr[]=size&st=size&affExtParam2=" + base64.b64encode(str(int(float(cp))).encode()).decode('ascii')

                #shopsylink = link.replace("www.flipkart.com", "dl.shopsy.in/dl/deal/p")


                # print(name + " , " + mrp + " , " + cp + " , " + str(discount) + " , " + listingid + " , " + link + "\n")

                numberofresults += 1
                bloc = 0
                word = ""

                if availability == "NO_AVAILABLE_LISTING" or availability == "TEMP_DISCONTINUED" or cp == "":
                    print("availability")
                    continue

                if get_contents.count(name + " => " + availability) > 3:
                    #print(">20")
                    continue

                params = []
                blockedword = ""
                falsealert = 0

                nameavail_cond=False
                permanentsaved = {}
                if (get_contents and name + " => " + availability not in get_contents):
                    permanentsaved = block.select(listingid)
                    nameavail_cond=True

                permanentbypassed = "False"
                if listingid in permanentsaved and float(cp) >= (float(permanentsaved[listingid])*0.9):
                    enter = False
                elif listingid in permanentsaved and float(cp) < (float(permanentsaved[listingid])*0.9):
                    enter = True
                    permanentbypassed = permanentsaved[listingid]
                else:
                    enter = True

                if get_contents and enter:
                    if nameavail_cond or (filename.find("grocery")==-1 and float(cp) < 50 and sellertype == "F_ASSURED"):
                        f = open(filename, "a+")
                        str1 = currenttime + " => " + name + " => " + availability + " => " + mrp + " => " + cp + " => " + listingid + "\n"
                        f.write(str1)
                        f.close()

                        bloc, word = checkblocklist(name, total, listingid)

                        blockedpackof = ["rubber","Placemat","Silicone","Hook","Extender","bra","panty","band","cover","girls","women","Holder","Ponytail","Wipes","Plant","Saree","Storage","Monster","Saikara"]
                        if bloc == 1 and word != "" and word != None and word.find("=") != -1:
                            if word.lower().find("pack of") == -1 and word.lower().find("lst") == -1 and name.lower().find("pack of") != -1:
                                packof = re.search("pack of (\d+)(\s|,|\)|$)", name.lower())
                                for item in blockedpackof:
                                    if name.lower().find(item.lower()) != -1:
                                        packof = "nevercheckout"
                                        break
                                if packof == None or packof != "nevercheckout" and packof[1] != "1" and packof[1] != "2":
                                    word += " unblocked by packof"
                                    bloc = 0
                                    docheckout = True

                        if bloc == 0 and word != "" and word != None:
                            name = name + " [" + word + "]"


                        if telegram != "off" and availability != "OUT_OF_STOCK" and listingid in get_contents:
                            if (checkstatus(link, listingid)):
                                availability = "OUT_OF_STOCK"


                        #if float(cp) > 40 and checkforname(filename) == True and force != 1:
                        #    docheckout = False

                        specialforce = False
                        if force == 1 and discount < 70:
                            if filename.find("mob") != -1 or filename.lower().find("tab") != -1 or filename.find("lap") != -1 or filename.find("tv") != -1 or filename.lower().find("ac_") != -1:
                                specialforce = True

                        if recheckforcommand(filename):
                            docheckout = False

                        telegramsent = False

                        if bloc == 1 and docheckout == True:
                            #print("blocked " + word)
                            if force == 1 or discount > 90 or float(cp) < 60 or mrp == cp and (hour <= 3 or hour >= 7) :
                                #Blocked text sent only 5 times in telegram for lifetime and then permanent block
                                if controlspam(name,cp,listingid) == True:
                                    continue
                                if telegram != "off":
                                    telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id="+ chatid +"&disable_notification=1&parse_mode=HTML&text=" + urllib.parse.quote(
                                        word + "\nL-(" + filename + ") " + currenttime + " => " + name + " - " + listingid + "\n " + mrp + " =>\n" + cp + " + " + delcharge + " Rs.\n" + str(
                                    discount) + " %\n " + availability + "\n" + sellertype + " @mausa_bot" + "\n" + link)
                                    myasyncsend(telegramurl)
                                    telegramsent = True
                            blockedword = word
                            docheckout = False

                        if filename.find("grocery")!=-1:
                            docheckout = False

                        '''
                        with open(filename + str(random.randint(1, 1000)) + ".html", "w+", encoding="utf-8") as f1:
                            f1.write(html)
                        '''

                        if (total <= 20000 or discount >= 50) and telegram != "off" and docheckout == True and availability != "OUT_OF_STOCK":

                            if ((discount >= 97 and float(cp) < 20) or float(cp) < 20) and sellertype == "F_ASSURED" and listingid not in get_contents:
                                telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=-1001590697850&parse_mode=HTML&text=" + urllib.parse.quote(
                                    "<b>L-(" + filename + ")[1] " + currenttime + "</b> => " + name + " - " + listingid + "\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n" + str(
                                        discount) + " %\n " + availability + "\n" + sellertype + " @mausa_bot" + "\n" + link)
                                myasyncsend(telegramurl)
                                if text_file.find(listingid.lower()) == -1:
                                    falsealert = checkout_start(html, name, urls, listingid, cp, mrp, discount, filename, pid)
                                    checkoutpro = 1

                            elif discount >= 90 and total <= 100:
                                telegramurl = "https://api.telegram.org/bot1311880981:AAG9eM_c62lH5ITjMp_OzR7Klp40e3urnjA/sendMessage?chat_id=-1001590697850&parse_mode=HTML&text=" + urllib.parse.quote(
                                    "<b>L-(" + filename + ")[2] " + currenttime + "</b> => " + name + " - " + listingid + "\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n" + str(
                                        discount) + " %\n " + availability + "\n" + sellertype + " @mausa_bot" + "\n" + link)
                                myasyncsend(telegramurl)
                                falsealert = checkout_start(html, name, urls, listingid, cp, mrp, discount, filename, pid)
                                checkoutpro = 1

                            elif discount >= 96 or float(cp) < 70:
                                telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=-1001590697850&parse_mode=HTML&text=" + urllib.parse.quote(
                                    "<b>L-(" + filename + ")[3] " + currenttime + "</b> => " + name + " - " + listingid + "\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n" + str(
                                        discount) + " %\n " + availability + "\n" + sellertype + " @mausa_bot" + "\n" + link)
                                myasyncsend(telegramurl)
                                falsealert = checkout_start(html, name, urls, listingid, cp, mrp, discount, filename, pid)
                                checkoutpro = 1

                            elif float(cp) >= 1999 and float(cp) <= 2001 and discount < 10:
                                telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=-1001590697850&parse_mode=HTML&text=" + urllib.parse.quote(
                                    "<b>L-(" + filename + ")[4] " + currenttime + "</b> => " + name + " - " + listingid + "\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n" + str(
                                        discount) + " %\n " + availability + "\n" + sellertype + " @mausa_bot" + "\n" + link)
                                myasyncsend(telegramurl)
                                falsealert = checkout_start(html, name, takehighriskurls, listingid, cp, mrp, discount, filename, pid)
                                checkoutpro = 1

                            elif discount >= 70 and force == 1:
                                telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=-1001590697850&parse_mode=HTML&text=" + urllib.parse.quote(
                                    "<b>L-(" + filename + ")[5] " + currenttime + "</b> => " + name + " - " + listingid + "\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n" + str(
                                        discount) + " %\n " + availability + "\n" + sellertype + " @mausa_bot" + "\n" + link)
                                myasyncsend(telegramurl)
                                falsealert = checkout_start(html, name, urls, listingid, cp, mrp, discount, filename, pid)
                                checkoutpro = 1

                            elif specialforce == True and force == 1:
                                telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=-1001590697850&parse_mode=HTML&text=" + urllib.parse.quote(
                                    "<b>L-(" + filename + ")[6] " + currenttime + "</b> => " + name + " - " + listingid + "\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n" + str(
                                        discount) + " %\n " + availability + "\n" + sellertype + " @mausa_bot" + "\n" + link)
                                myasyncsend(telegramurl)
                                falsealert = checkout_start(html, name, takehighriskurls, listingid, cp, mrp, discount, filename, pid)
                                checkoutpro = 1

                            elif discount >= 90 or total < 70 or mrp == cp or mrp == "" or mrp == "0":
                                telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=-1001590697850&parse_mode=HTML&text=" + urllib.parse.quote(
                                    "<b>L-(" + filename + ")[7] " + currenttime + "</b> => " + name + " - " + listingid + "\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n" + str(
                                        discount) + " %\n " + availability + "\n" + sellertype + " @mausa_bot" + "\n" + link)
                                myasyncsend(telegramurl)
                                falsealert = checkout_start(html, name, urls, listingid, cp, mrp, discount, filename, pid)
                                checkoutpro = 1

                            elif discount >= 85 and total < 500:
                                telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=-1001590697850&parse_mode=HTML&text=" + urllib.parse.quote(
                                    "<b>L-(" + filename + ")[8] " + currenttime + "</b> => " + name + " - " + listingid + "\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n" + str(
                                        discount) + " %\n " + availability + "\n" + sellertype + " @mausa_bot" + "\n" + link)
                                myasyncsend(telegramurl)
                                falsealert = checkout_start(html, name, notassuredurls, listingid, cp, mrp, discount, filename, pid)
                                checkoutpro = 1

                        elif telegram != "off" and filename.find("grocery")!=-1 and (discount >= 70 or total<=15)  and availability != "OUT_OF_STOCK":
                            telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=-1001590697850&parse_mode=HTML&disable_notification=1&text=" + urllib.parse.quote(
                                "<b>L-(" + filename + ") grocery nocheckout \n " + currenttime + "</b> => " + name + " - " + listingid + "\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n" + str(
                                    discount) + " %\n " + availability + "\n" + sellertype + " @mausa_bot" + "\n" + link)
                            myasyncsend(telegramurl)
                        elif telegram != "off" and filename.find("grocery")==-1 and bloc==0 and (discount > 80 or mrp == "" or mrp == cp or mrp == "0" or total <= 100 or
                                                   (float(mrp) < float(cp) + 101)) and availability != "OUT_OF_STOCK":
                            telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=-1001590697850&parse_mode=HTML&disable_notification=1&text=" + urllib.parse.quote(
                                "<b>L-(" + filename + ") checkout stopped \n " + currenttime + "</b> => " + name + " - " + listingid + "\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n" + str(
                                    discount) + " %\n " + availability + "\n" + sellertype + " @mausa_bot" + "\n" + link)
                            myasyncsend(telegramurl)
                        elif telegram != "off" and bloc==0 and (discount >= 50 or mrp == "") and force == 1 and availability != "OUT_OF_STOCK":
                            telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=-1001590697850&parse_mode=HTML&disable_notification=1&text=" + urllib.parse.quote(
                                "<b>L-(" + filename + ") checkout stopped \n " + currenttime + "</b> => " + name + " - " + listingid + "\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n" + str(
                                    discount) + " %\n " + availability + "\n" + sellertype + " @mausa_bot" + "\n" + link)
                            myasyncsend(telegramurl)


                        if permanentbypassed != "False":
                            telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=-1001590697850&parse_mode=HTML&text=" + urllib.parse.quote(
                                "permanent bypassed " + str(permanentbypassed) + "\nL-(" + filename + ") " + currenttime + " => " + name + " - " + listingid + "\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n" + str(
                                    discount) + " %\n " + availability + "\n" + sellertype + " @mausa_bot" + "\n" + link)
                            myasyncsend(telegramurl)





                            '''
                            fa = open(str(uuid.uuid4()) + ".html", "w+", encoding="utf-8")
                            fa.write(ratwro)
                            fa.flush()
                            fa.close()
                            '''

                        if telegramsent==False and checkoutpro == 1 and falsealert != 1:
                            checkoutpro = 0

                            telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=" + chatid + "&parse_mode=HTML&text=" + urllib.parse.quote(
                                "<b>L-(" + filename + ") " + currenttime + "</b> => " + name + " - " + listingid + "\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n" + str(
                                    discount) + " %\n " + availability + "\n" + sellertype + " @mausa_bot" + "\n" + link)
                            myasyncsend(telegramurl)

                            #logthehtml(filename, html)


                            if recheckforcommand(filename):
                                urls = NPurls = []
                            text_file = open("blocked.txt", "r")
                            text_file = text_file.read().strip(",")
                            blocked = text_file.split(',')

                        elif telegramsent==False and telegram != "off" and (discount > 80 or mrp == "" or mrp == cp or mrp == "0" or total <= 100 or
                                                                          (float(mrp) < float(cp) + 101)) and availability != "OUT_OF_STOCK":
                            telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=" + chatid + "&parse_mode=HTML&text=" + urllib.parse.quote(
                                "<b>L-(" + filename + ") " + currenttime + "</b> => " + name + " - " + listingid + "\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n" + str(
                                    discount) + " %\n " + availability + "\n" + sellertype + " @mausa_bot" + "\n" + link)
                            myasyncsend(telegramurl)

                        elif telegramsent==False and telegram != "off" and (
                                discount >= 50 or mrp == "") and force == 1 and availability != "OUT_OF_STOCK":
                            telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=" + chatid + "&parse_mode=HTML&text=" + urllib.parse.quote(
                                "<b>L-(" + filename + ") " + currenttime + "</b> => " + name + " - " + listingid + "\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n" + str(
                                    discount) + " %\n " + availability + "\n" + sellertype + " @mausa_bot" + "\n" + link)
                            myasyncsend(telegramurl)



                        '''
                        if docheckout == False and (discount >= 60 or mrp == "" or float(cp) < 80) and availability != "OUT_OF_STOCK":
                            telegramurl = "https://api.telegram.org/bot1311880981:AAG9eM_c62lH5ITjMp_OzR7Klp40e3urnjA/sendMessage?chat_id=-1001590697850&parse_mode=HTML&text=" + urllib.parse.quote(
                                "<b>WEB-(" + filename + ") " + currenttime + "</b> => " + name + " - " + listingid + " =>\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n => (" + str(
                                    discount) + " %) =>\n " + availability + "\nBlocked reason = " + blockedword + "\n" + sellertype + "\n" + link)
                            myasyncsend(telegramurl)
                        '''
                        '''
                        elif telegram != "off" and name + " => " + availability not in get_contents and (discount > 70 or total < 70) and availability == "OUT_OF_STOCK":
                            telegramurl = "https://api.telegram.org/bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI/sendMessage?chat_id=-939189614&parse_mode=HTML&text=" + urllib.parse.quote(
                                "<b>mob_p_OOS-(" + filename + ") " + currenttime + "</b> => " + name + " - " + listingid + " =>\n " + mrp + " =>\n <b>" + cp + " + " + delcharge + " Rs.</b>\n => (" + str(
                                    discount) + " %) =>\n " + availability + "\n" + link)
                            uclient = Request(telegramurl)
                            response = urlopen(uclient, timeout=30)


                        if falsealert == 1:
                            f.write(str1)
                            f.write(str1)
                            f.write(str1)
                            f.write(str1)
                            f.write(str1)
                        '''

                else:
                    if nameavail_cond or not get_contents:
                        str1 = currenttime + " => " + name + " => " + availability + " => " + mrp + " => " + cp + " => " + listingid + "\n"
                        f = open(filename, "a+")
                        if nameavail_cond:
                            f.write(str1)
                            f.write(str1)
                            f.write(str1)
                        f.write(str1)
                        f.close()
            deletesavedtext(filename) #check if command for deletion of product to be checkout again
        except KeyError:
            pass
        except Exception as e:
            # print(str(e))
            logger.error(filename + "\r\n" + listingid + "\r\n" + name + str(e))
            logger.error(traceback.format_exc())
            pass

    # print("[%s] W - {0:<25s}%s -> Results = %d" %(currenttime, filename, numberofresults))
    print('[{0:<6}] {1:<35} {2:<4}|{3:>3} Results'.format(currenttime, filename, totalproducts, numberofresults))
    try:
        res_queue.put(str('[{0:<6}] {1:<35} {2:<4}|{3:>3} Results'.format(currenttime, filename, totalproducts, numberofresults)))
    except Exception as e:
        print(str(e))

    del jsonarray
    del html
    del pages
    del get_contents
    return



def telegram_send(telegramurl):
    try:
        uclient = Request(telegramurl)
        response = urlopen(uclient, timeout=30)

        if response.info().get('Content-Encoding') == 'gzip':
            html = gzip.decompress(response.read()).decode('utf8')
        elif response.info().get('Content-Encoding') == 'deflate':
            html = response.read().decode('utf8')
        else:
            html = response.read().decode('utf8')

        if html.find("\"ok\":true") == -1:
            f = open("telegramerrors.txt", "a+")
            f.write("\n" + telegramurl + "\n" + html + "\n")
            f.close()

            telegramurl = telegramurl.replace("bot630455540:AAHtnLN2YFEzDpiVWeZBInQ_nlsPCpFzNEI", "bot923259452:AAG1tBRBM7PIIYUL1g789IP4tBMgsI8uOJg")
            uclient = Request(telegramurl)
            response = urlopen(uclient, timeout=30)
        return response
    except Exception as e:
        '''f1 = open('exceptions.txt', 'a+')
        f1.write("\r\n ------------------------- \r\n" + telegramurl + "\r\n" + str(e) + "\r\n")
        f1.close()'''
        return ""

def logthehtml(filename, htmldata):
    with open(filename + str(random.randint(1, 1000)) + ".html", "w+", encoding="utf-8") as f1:
        f1.write(htmldata)

def recheckforcommand(filename):
    block.block(filename)
    try:
        f = open("checkout.txt", "r+")
        get_contents_1 = f.read()
        f.close()
    except FileNotFoundError:
        f = open("checkout.txt", "w+")
        get_contents_1 = f.read()
        f.close()

    if get_contents_1.find("true") != -1 or get_contents_1.find("yes") != -1 or get_contents_1.find("1") != -1:
        return True
    else:
        return False

def controlspam(name,cp,listingid):
    try:
        try:
            f = open("saved_and_blocked.txt", "r+")
            get_contents_1 = f.read()
            f.close()
        except FileNotFoundError:
            f = open("saved_and_blocked.txt", "w+")
            get_contents_1 = f.read()
            f.close()

        if get_contents_1.count(name + "->" + listingid + "=>" + str(cp)) > 2:
            return True
        else:
            f = open("saved_and_blocked.txt", "a+")
            f.write(name + "->" + listingid + "=>" + str(cp) + "\n")
            f.close()
            return False
    except:
        return False

