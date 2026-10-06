import datetime
import random
import logging
import threading
from logging.handlers import RotatingFileHandler
import traceback
from threading import Thread
import os
from os import path
import psutil
import sys
from multiprocessing import Process,Queue
import time
import pytz
from fkrdplog import updatetoserver
import gc
import extrafiles
extrafiles.start()
from mainmob import flipkart_parse
from block import block
from os import system, name

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.ERROR)
handler = RotatingFileHandler("log.txt", maxBytes=10000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

foldername = "m4_hkpri2/"
if not os.path.exists(foldername):
    os.mkdir(foldername)


def creation_time(path_to_file):
    current = time.time()
    try:
        return current-float(os.path.getctime(path_to_file))
    except Exception as e:
        print(str(e))
        return 0

def pcmemory():
    pid = os.getpid()
    py = psutil.Process(pid)
    memoryUse = py.memory_info()[0] / 2. ** 20  # memory use in GB...I think
    print('memory use:', round(memoryUse, 2), "MB")
    if memoryUse > 300:
        os.system("python " + __file__)
        print("Restarting memory usage exceeds ...........")
        sys.exit()

def dowork():
    arr = []
    res_queue = Queue()

    arr.append(['routers_700.txt', 0, False,'https://www.flipkart.com/computers/network-components/routers/pr?sid=6bo%2F70k%2F2a2&otracker=nmenu_sub_Electronics_0_Routers&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D700'])
    arr.append(['appleipads_20k.txt', 0, False,'https://www.flipkart.com/tablets/~apple-ipads/pr?sid=tyy%2Chry&otracker=nmenu_sub_Electronics_0_Apple+iPads&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D20000'])
    arr.append(['ssd_1500.txt', 0, False,'https://www.flipkart.com/computers/storage/ssd/pr?sid=6bo%2Cjdy%2Cdus&otracker=categorytree&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.brand%255B%255D%3DWD&p[]=facets.brand%255B%255D%3DSAMSUNG&p[]=facets.brand%255B%255D%3DSeagate&p[]=facets.brand%255B%255D%3DKINGSTON&p[]=facets.brand%255B%255D%3DHP&p[]=facets.brand%255B%255D%3DWESTERN%2BDIGITAL&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D1500'])
    arr.append(['tablet_5k.txt', 0, False,'https://www.flipkart.com/tablets/pr?sid=hry&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&otracker=categorytree&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D5000&p%5B%5D=facets.discount_range_v1%255B%255D%3D40%2525%2Bor%2Bmore'])
    arr.append(['remotetoys_100.txt', 0, False,'https://www.flipkart.com/toys/toy-vehicles/remote-control-toys/pr?sid=tng%2C56a%2Cfq8&otracker=categorytree&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D100'])
    arr.append(['gamingconsole_50p.txt', 0, False,'https://www.flipkart.com/gaming/gaming-consoles/pr?sid=4rr%2Cx1m&fm=neo%2Fmerchandising&iid=M_6a232d0b-37ce-40a3-a6da-b9e4bcb0a1ef_1_372UD5BXDFYS_MC.E8WPY497D45H&otracker=hp_rich_navigation_2_1.navigationCard.RICH_NAVIGATION_Electronics%7EGaming%7EGaming%2BConsoles_E8WPY497D45H&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_2_L2_view-all&cid=E8WPY497D45H&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DSONY&p%5B%5D=facets.brand%255B%255D%3DMICROSOFT&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore'])
    arr.append(['dslr_10k.txt', 0, False,'https://www.flipkart.com/cameras/dslr~type/pr?sid=jek%2Cp31&otracker=nmenu_sub_Electronics_0_DSLR+%26+Mirrorless&otracker=nmenu_sub_Electronics_0_DSLR+%26+Mirrorless&otracker=nmenu_sub_Electronics_0_DSLR+%26+Mirrorless&p[]=facets.discount_range_v1%255B%255D%3D30%2525%2Bor%2Bmore&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D10000'])
    arr.append(['fansbrand_disc50.txt', 1, False,'https://www.flipkart.com/fan/pr?sid=j9e%2Cabm%2Clbz&otracker=categorytree&sort=price_asc&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.brand%255B%255D%3DCrompton&p[]=facets.brand%255B%255D%3DBAJAJ&p[]=facets.brand%255B%255D%3DSyska&p[]=facets.brand%255B%255D%3DFlipkart%2BSmartBuy&p[]=facets.brand%255B%255D%3DOrient%2BElectric&p[]=facets.brand%255B%255D%3DLUMINOUS&p[]=facets.brand%255B%255D%3DHindware&p[]=facets.brand%255B%255D%3DHALONIX&p[]=facets.brand%255B%255D%3DSansui&p[]=facets.brand%255B%255D%3DUSHA&p[]=facets.brand%255B%255D%3DAtomberg&p[]=facets.brand%255B%255D%3DHAVELLS&p[]=facets.brand%255B%255D%3DV-Guard&p[]=facets.brand%255B%255D%3DKenstar&p[]=facets.brand%255B%255D%3DSymphony&p[]=facets.brand%255B%255D%3DHavells%2BStandard&p[]=facets.brand%255B%255D%3DRussell%2BHobbs&p[]=facets.brand%255B%255D%3DHavells%2BElectrical&p[]=facets.brand%255B%255D%3Dpolycab&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D2000'])
    arr.append(['fansbrand_1200.txt', 1, False,'https://www.flipkart.com/fan/pr?sid=j9e%2Cabm%2Clbz&otracker=categorytree&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D1200&p[]=facets.brand%255B%255D%3DCrompton&p[]=facets.brand%255B%255D%3DBAJAJ&p[]=facets.brand%255B%255D%3DSyska&p[]=facets.brand%255B%255D%3DFlipkart%2BSmartBuy&p[]=facets.brand%255B%255D%3DOrient%2BElectric&p[]=facets.brand%255B%255D%3DLUMINOUS&p[]=facets.brand%255B%255D%3DHindware&p[]=facets.brand%255B%255D%3DHALONIX&p[]=facets.brand%255B%255D%3DSansui&p[]=facets.brand%255B%255D%3DUSHA&p[]=facets.brand%255B%255D%3DAtomberg&p[]=facets.brand%255B%255D%3DHAVELLS&p[]=facets.brand%255B%255D%3DV-Guard&p[]=facets.brand%255B%255D%3DKenstar&p[]=facets.brand%255B%255D%3DSymphony&p[]=facets.brand%255B%255D%3DHavells%2BStandard&p[]=facets.brand%255B%255D%3DRussell%2BHobbs&p[]=facets.brand%255B%255D%3DHavells%2BElectrical&p[]=facets.brand%255B%255D%3Dpolycab&p[]=facets.type%255B%255D%3DCeiling'])
    arr.append(['coolers_disc5000.txt', 1, False,'https://www.flipkart.com/air-coolers/pr?sid=j9e%2Cabm%2C52j&marketplace=FLIPKART&otracker=product_breadCrumbs_Air+Coolers&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D5000'])
    arr.append(['coolers_4000brands.txt', 1, False,'https://www.flipkart.com/air-coolers/pr?sid=j9e%2Cabm%2C52j&marketplace=FLIPKART&otracker=product_breadCrumbs_Air+Coolers&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DHindware&p%5B%5D=facets.brand%255B%255D%3DSymphony&p%5B%5D=facets.brand%255B%255D%3DCrompton&p%5B%5D=facets.brand%255B%255D%3DThomson&p%5B%5D=facets.brand%255B%255D%3DMAHARAJA%2BWHITELINE&p%5B%5D=facets.brand%255B%255D%3DFlipkart%2BSmartBuy&p%5B%5D=facets.brand%255B%255D%3DSansui&p%5B%5D=facets.brand%255B%255D%3DUSHA&p%5B%5D=facets.brand%255B%255D%3DVoltas&p%5B%5D=facets.brand%255B%255D%3DHAVELLS&p%5B%5D=facets.brand%255B%255D%3DOrient%2BElectric&p%5B%5D=facets.brand%255B%255D%3DBAJAJ&p%5B%5D=facets.brand%255B%255D%3DKenstar&p%5B%5D=facets.brand%255B%255D%3DBlue%2BStar&p%5B%5D=facets.brand%255B%255D%3DV-Guard&p%5B%5D=facets.brand%255B%255D%3DSinger&p%5B%5D=facets.brand%255B%255D%3DSURYA&p%5B%5D=facets.brand%255B%255D%3DONIDA&p%5B%5D=facets.brand%255B%255D%3DHindware%2BSnowcrest&p%5B%5D=facets.brand%255B%255D%3DRussell%2BHobbs&p%5B%5D=facets.brand%255B%255D%3DVenus&p%5B%5D=facets.brand%255B%255D%3DSunflame&p%5B%5D=facets.brand%255B%255D%3DDesert&p%5B%5D=facets.brand%255B%255D%3Dsymphony%2Blimited&p%5B%5D=facets.brand%255B%255D%3DVoltass&p%5B%5D=facets.brand%255B%255D%3DPolycab&p%5B%5D=facets.brand%255B%255D%3DLifelong&p%5B%5D=facets.brand%255B%255D%3DKENSTARR&p%5B%5D=facets.brand%255B%255D%3DKELVINATER&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D5000'])
    arr.append(['RObrand_disc4000.txt', 1, False,'https://www.flipkart.com/water-purifiers/pr?sid=j9e%2Cabm%2Ci45&marketplace=FLIPKART&otracker=product_breadCrumbs_Water+purifiers&sort=price_asc&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.brand%255B%255D%3DAquaguard&p[]=facets.brand%255B%255D%3DPureit&p[]=facets.brand%255B%255D%3DHindware&p[]=facets.brand%255B%255D%3DBlue%2BStar&p[]=facets.brand%255B%255D%3DLG&p[]=facets.brand%255B%255D%3DKENT&p[]=facets.brand%255B%255D%3DLIVPURE&p[]=facets.brand%255B%255D%3DHAVELLS&p[]=facets.brand%255B%255D%3DV-Guard&p[]=facets.brand%255B%255D%3DMarQ%2Bby%2BFlipkart&p[]=facets.brand%255B%255D%3DFaber&p[]=facets.brand%255B%255D%3DEUREKA%2BFORBES&p[]=facets.brand%255B%255D%3DAO%2BSmith&p[]=facets.brand%255B%255D%3DPrestige&p[]=facets.brand%255B%255D%3DMidea&p[]=facets.brand%255B%255D%3DEureka%2BForbes%2BSure%2BFrom%2BAquaguard&p[]=facets.brand%255B%255D%3DEureka%2BForbes%2BLtd&p[]=facets.brand%255B%255D%3DEureka%2BForbes%2BAquasure%2Bfrom%2BAquaguard&p[]=facets.brand%255B%255D%3DCarrier%2BMidea&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D4000'])
    arr.append(['ac_disc_21k.txt', 1, False,'https://www.flipkart.com/air-conditioners/pr?sid=j9e%2Cabm%2Cc54&marketplace=FLIPKART&otracker=product_breadCrumbs_Air+Conditioners&sort=price_asc&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D21000'])
    arr.append(['ac_20k.txt', 1, False,'https://www.flipkart.com/air-conditioners/pr?sid=j9e%2Cabm%2Cc54&marketplace=FLIPKART&otracker=product_breadCrumbs_Air+Conditioners&sort=price_asc&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D20000'])
    arr.append(['fridge_8000.txt', 1, False,'https://www.flipkart.com/refrigerators/pr?sid=j9e%2Cabm%2Chzg&marketplace=FLIPKART&otracker=product_breadCrumbs_Refrigerators&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D8000'])
    arr.append(['fridge_disc10000.txt', 1, False,'https://www.flipkart.com/refrigerators/pr?sid=j9e%2Cabm%2Chzg&marketplace=FLIPKART&otracker=product_breadCrumbs_Refrigerators&sort=price_asc&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D10000'])
    arr.append(['WashingMc_5000.txt', 1, False,'https://www.flipkart.com/washing-machines/pr?sid=j9e%2Cabm%2C8qx&marketplace=FLIPKART&otracker=product_breadCrumbs_Washing+Machines&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D5000'])
    arr.append(['ironbrand_250.txt', 1, False,'https://www.flipkart.com/iron/pr?sid=j9e%2Cabm%2Ca0u&marketplace=FLIPKART&otracker=product_breadCrumbs_Irons&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.brand%255B%255D%3DPHILIPS&p%5B%5D=facets.brand%255B%255D%3DBAJAJ&p%5B%5D=facets.brand%255B%255D%3DUSHA&p%5B%5D=facets.brand%255B%255D%3DFlipkart%2BSmartBuy&p%5B%5D=facets.brand%255B%255D%3DPanasonic&p%5B%5D=facets.brand%255B%255D%3DOrient%2BElectric&p%5B%5D=facets.brand%255B%255D%3DMAHARAJA%2BWHITELINE&p%5B%5D=facets.brand%255B%255D%3DHAVELLS&p%5B%5D=facets.brand%255B%255D%3DCrompton&p%5B%5D=facets.brand%255B%255D%3DSyska&p%5B%5D=facets.brand%255B%255D%3DMorphy%2BRichards&p%5B%5D=facets.brand%255B%255D%3DWipro&p%5B%5D=facets.brand%255B%255D%3DInalsa&p%5B%5D=facets.brand%255B%255D%3DPrestige&p%5B%5D=facets.brand%255B%255D%3DTefal&p%5B%5D=facets.brand%255B%255D%3DMURPHY&p%5B%5D=facets.brand%255B%255D%3DKenstar&p%5B%5D=facets.brand%255B%255D%3DPigeon&p%5B%5D=facets.brand%255B%255D%3DBlack%2B%2526%2BDecker&p%5B%5D=facets.brand%255B%255D%3DSinger&p%5B%5D=facets.brand%255B%255D%3DSansui&p%5B%5D=facets.brand%255B%255D%3DORPAT&p%5B%5D=facets.brand%255B%255D%3Dcello&p%5B%5D=facets.brand%255B%255D%3DRussell%2BHobbs&p%5B%5D=facets.brand%255B%255D%3DMAHARAJA&p%5B%5D=facets.brand%255B%255D%3DSunflame&p%5B%5D=facets.brand%255B%255D%3DPolycab&p%5B%5D=facets.brand%255B%255D%3DPhillips&p%5B%5D=facets.brand%255B%255D%3DMorphy%2BRichard&p%5B%5D=facets.brand%255B%255D%3DORIENT&p%5B%5D=facets.brand%255B%255D%3DButterfly&p%5B%5D=facets.brand%255B%255D%3DEVEREADY&p%5B%5D=facets.brand%255B%255D%3DBOROSIL&p%5B%5D=facets.brand%255B%255D%3DBLACK%252BDECKER&p%5B%5D=facets.brand%255B%255D%3DBLACK%2BDECKER&p%5B%5D=facets.brand%255B%255D%3DBillion&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D250'])
    arr.append(['geyserbrand_1500.txt', 1, False,'https://www.flipkart.com/water-geysers/pr?sid=j9e%2Cabm%2Cbfm&marketplace=FLIPKART&otracker=product_breadCrumbs_Water+Geysers&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.brand%255B%255D%3DHindware&p[]=facets.brand%255B%255D%3DCrompton&p[]=facets.brand%255B%255D%3DV-Guard&p[]=facets.brand%255B%255D%3DAO%2BSmith&p[]=facets.brand%255B%255D%3DBAJAJ&p[]=facets.brand%255B%255D%3DVenus&p[]=facets.brand%255B%255D%3DHAVELLS&p[]=facets.brand%255B%255D%3DOrient%2BElectric&p[]=facets.brand%255B%255D%3DUSHA&p[]=facets.brand%255B%255D%3DPolycab&p[]=facets.brand%255B%255D%3DHaier&p[]=facets.brand%255B%255D%3DKenstar&p[]=facets.brand%255B%255D%3DFaber&p[]=facets.brand%255B%255D%3DMorphy%2BRichards&p[]=facets.brand%255B%255D%3DMAHARAJA%2BWHITELINE&p[]=facets.brand%255B%255D%3DHindware%2BAtlantic&p[]=facets.brand%255B%255D%3DSunflame&p[]=facets.brand%255B%255D%3DSansui&p[]=facets.brand%255B%255D%3DFlipkart%2BSmartBuy&p[]=facets.brand%255B%255D%3DButterfly&p[]=facets.brand%255B%255D%3DPanasonic&p[]=facets.brand%255B%255D%3DInalsa&p[]=facets.brand%255B%255D%3DEVEREST&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D1500'])
    arr.append(['freezer_5000.txt', 1, False,'https://www.flipkart.com/home-kitchen/home-appliances/freezer-chests/pr?sid=j9e%2Cabm%2Cix6&marketplace=FLIPKART&otracker=product_breadCrumbs_Freezer+Chests&sort=price_asc&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D5000'])
    arr.append(['vaccdisc_1000.txt', 1, False,'https://www.flipkart.com/vacuum-cleaners/pr?sid=j9e%2Cabm%2Cul2&sort=price_asc&hpid=z_Ol7LGAxswe2kARyu-e6ap7_Hsxr70nj65vMAAFKlc%3D&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InZhbHVlQ2FsbG91dCI6eyJtdWx0aVZhbHVlZEF0dHJpYnV0ZSI6eyJrZXkiOiJ2YWx1ZUNhbGxvdXQiLCJpbmZlcmVuY2VUeXBlIjoiVkFMVUVfQ0FMTE9VVCIsInZhbHVlcyI6WyJVcCB0byA2NSUgT2ZmIl0sInZhbHVlVHlwZSI6Ik1VTFRJX1ZBTFVFRCJ9fSwiaGVyb1BpZCI6eyJzaW5nbGVWYWx1ZUF0dHJpYnV0ZSI6eyJrZXkiOiJoZXJvUGlkIiwiaW5mZXJlbmNlVHlwZSI6IlBJRCIsInZhbHVlIjoiVkNMRlBEM1ZUVzM1REhKRiIsInZhbHVlVHlwZSI6IlNJTkdMRV9WQUxVRUQifX0sInRpdGxlIjp7Im11bHRpVmFsdWVkQXR0cmlidXRlIjp7ImtleSI6InRpdGxlIiwiaW5mZXJlbmNlVHlwZSI6IlRJVExFIiwidmFsdWVzIjpbIlZhY3V1bSBDbGVhbmVycyJdLCJ2YWx1ZVR5cGUiOiJNVUxUSV9WQUxVRUQifX19fX0%3D&fm=neo%2Fmerchandising&iid=M_20ff712d-de95-48cf-92f9-062e1f4d47f8_31.U3FROAW98UWL&ppt=clp&ppn=tvs-and-appliances-new-clp-store&ssid=kdcd51c94qijmbr41676890455896&otracker=clp_omu_Up%2Bto%2B70%2525%2BOff_5_31.dealCard.OMU_tvs-and-appliances-new-clp-store_tvs-and-appliances-new-clp-store_U3FROAW98UWL_19&otracker1=clp_omu_PINNED_neo%2Fmerchandising_Up%2Bto%2B70%2525%2BOff_NA_dealCard_cc_5_NA_view-all_19&cid=U3FROAW98UWL&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D2000&p%5B%5D=facets.brand%255B%255D%3DDyson&p%5B%5D=facets.brand%255B%255D%3DMi&p%5B%5D=facets.brand%255B%255D%3DEUREKA%2BFORBES&p%5B%5D=facets.brand%255B%255D%3DBlack%2B%2526%2BDecker&p%5B%5D=facets.brand%255B%255D%3DKENT&p%5B%5D=facets.brand%255B%255D%3DPrestige&p%5B%5D=facets.brand%255B%255D%3DPanasonic&p%5B%5D=facets.brand%255B%255D%3DILIFE&p%5B%5D=facets.brand%255B%255D%3DPHILIPS&p%5B%5D=facets.brand%255B%255D%3DECOVACS&p%5B%5D=facets.brand%255B%255D%3DFlipkart%2BSmartBuy&p%5B%5D=facets.brand%255B%255D%3D360&p%5B%5D=facets.brand%255B%255D%3Drealme%2BTechLife&p%5B%5D=facets.brand%255B%255D%3DBLACK%252BDECKER&p%5B%5D=facets.brand%255B%255D%3DTP-Link&p%5B%5D=facets.brand%255B%255D%3DSinger&p%5B%5D=facets.brand%255B%255D%3DPhilips%2BSpeedPro%2BCordless%2BStick%2Bvacuum%2Bcleaner%2B-%2BFC6723%252F01&p%5B%5D=facets.brand%255B%255D%3DHaier&p%5B%5D=facets.brand%255B%255D%3DForbes&p%5B%5D=facets.brand%255B%255D%3DBOSCH&p%5B%5D=facets.brand%255B%255D%3DSAMSUNG&p%5B%5D=facets.brand%255B%255D%3DProscenic&p%5B%5D=facets.brand%255B%255D%3DInalsa&p%5B%5D=facets.brand%255B%255D%3DAGARO&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore'])
    arr.append(['inverterbattery_5000.txt', 1, False,'https://www.flipkart.com/home-kitchen/home-appliances/inverters-and-accessories/inverter-batteries/pr?sid=j9e%2Cabm%2Cve9%2Chlv&otracker=categorytree&sort=price_asc&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D5000'])
    arr.append(['roomheater_500.txt', 1, False,'https://www.flipkart.com/room-heaters/pr?sid=j9e%2Cabm%2Cxie&otracker=categorytree&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D500'])
    arr.append(['airfryers_disc2000.txt', 1, False,'https://www.flipkart.com/air-fryers/pr?sid=j9e%2Cm38%2Cj1e&otracker=categorytree&sort=price_asc&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D2000'])
    arr.append(['juicermixerbrand_disc1500.txt', 1, False,'https://www.flipkart.com/home-kitchen/kitchen-appliances/mixer-juicer-grinder/pr?sid=j9e%2Cm38%2C7ek&otracker=categorytree&sort=price_asc&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.brand%255B%255D%3DButterfly&p%5B%5D=facets.brand%255B%255D%3DBAJAJ&p%5B%5D=facets.brand%255B%255D%3DPrestige&p%5B%5D=facets.brand%255B%255D%3DPreethi&p%5B%5D=facets.brand%255B%255D%3DBOSCH&p%5B%5D=facets.brand%255B%255D%3DPHILIPS&p%5B%5D=facets.brand%255B%255D%3DWONDERCHEF&p%5B%5D=facets.brand%255B%255D%3DFaber&p%5B%5D=facets.brand%255B%255D%3DUSHA&p%5B%5D=facets.brand%255B%255D%3DSUJATA&p%5B%5D=facets.brand%255B%255D%3DMAHARAJA%2BWHITELINE&p%5B%5D=facets.brand%255B%255D%3DHAVELLS&p%5B%5D=facets.brand%255B%255D%3DPanasonic&p%5B%5D=facets.brand%255B%255D%3DCrompton&p%5B%5D=facets.brand%255B%255D%3DMorphy%2BRichards&p%5B%5D=facets.brand%255B%255D%3DOrient%2BElectric&p%5B%5D=facets.brand%255B%255D%3DPigeon&p%5B%5D=facets.brand%255B%255D%3DV-Guard&p%5B%5D=facets.brand%255B%255D%3DKENT&p%5B%5D=facets.brand%255B%255D%3DKenstar&p%5B%5D=facets.brand%255B%255D%3DMAHARAJA&p%5B%5D=facets.brand%255B%255D%3DInalsa&p%5B%5D=facets.brand%255B%255D%3DFlipkart%2BSmartBuy&p%5B%5D=facets.brand%255B%255D%3DBOROSIL&p%5B%5D=facets.brand%255B%255D%3DSansui&p%5B%5D=facets.brand%255B%255D%3DSinger&p%5B%5D=facets.brand%255B%255D%3DTefal&p%5B%5D=facets.brand%255B%255D%3DNutriPro&p%5B%5D=facets.brand%255B%255D%3DCrompton%2BGreaves&p%5B%5D=facets.brand%255B%255D%3DAGARO&p%5B%5D=facets.brand%255B%255D%3DORPAT&p%5B%5D=facets.brand%255B%255D%3DEVEREADY&p%5B%5D=facets.brand%255B%255D%3DThomson&p%5B%5D=facets.brand%255B%255D%3DAtomberg&p%5B%5D=facets.brand%255B%255D%3DBlack%2B%2526%2BDecker&p%5B%5D=facets.brand%255B%255D%3DORIENT&p%5B%5D=facets.brand%255B%255D%3DPigeon%2Bby%2BStovekraft&p%5B%5D=facets.brand%255B%255D%3DRussell%2BHobbs&p%5B%5D=facets.brand%255B%255D%3DAsus&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1500'])
    arr.append(['handblender_500.txt', 0, False,'https://www.flipkart.com/hand-blenders/pr?sid=j9e%2Cm38%2Cu7m&otracker=categorytree&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.brand%255B%255D%3DPHILIPS&p%5B%5D=facets.brand%255B%255D%3DKENT&p%5B%5D=facets.brand%255B%255D%3DInalsa&p%5B%5D=facets.brand%255B%255D%3DFlipkart%2BSmartBuy&p%5B%5D=facets.brand%255B%255D%3DMAHARAJA%2BWHITELINE&p%5B%5D=facets.brand%255B%255D%3DUSHA&p%5B%5D=facets.brand%255B%255D%3DORPAT&p%5B%5D=facets.brand%255B%255D%3DBAJAJ&p%5B%5D=facets.brand%255B%255D%3DPrestige&p%5B%5D=facets.brand%255B%255D%3DMorphy%2BRichards&p%5B%5D=facets.brand%255B%255D%3DWONDERCHEF&p%5B%5D=facets.brand%255B%255D%3DBlack%2B%2526%2BDecker&p%5B%5D=facets.brand%255B%255D%3DBOROSIL&p%5B%5D=facets.brand%255B%255D%3DHAVELLS&p%5B%5D=facets.brand%255B%255D%3DSinger&p%5B%5D=facets.brand%255B%255D%3DORBIT&p%5B%5D=facets.brand%255B%255D%3DCrompton&p%5B%5D=facets.brand%255B%255D%3Dcello&p%5B%5D=facets.brand%255B%255D%3DOrient%2BElectric&p%5B%5D=facets.brand%255B%255D%3DBLACK%252BDECKER&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D500'])
    arr.append(['induction_1000.txt', 0, False,'https://www.flipkart.com/induction-cooktops/pr?sid=j9e%2Cm38%2C575&otracker=categorytree&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.brand%255B%255D%3DPrestige&p%5B%5D=facets.brand%255B%255D%3DPigeon&p%5B%5D=facets.brand%255B%255D%3DPHILIPS&p%5B%5D=facets.brand%255B%255D%3DUSHA&p%5B%5D=facets.brand%255B%255D%3DLifelong&p%5B%5D=facets.brand%255B%255D%3DBAJAJ&p%5B%5D=facets.brand%255B%255D%3DButterfly&p%5B%5D=facets.brand%255B%255D%3DHAVELLS&p%5B%5D=facets.brand%255B%255D%3DFlipkart%2BSmartBuy&p%5B%5D=facets.brand%255B%255D%3DV-Guard&p%5B%5D=facets.brand%255B%255D%3Dcello&p%5B%5D=facets.brand%255B%255D%3DOrient%2BElectric&p%5B%5D=facets.brand%255B%255D%3DMorphy%2BRichards&p%5B%5D=facets.brand%255B%255D%3DKENT&p%5B%5D=facets.brand%255B%255D%3DCrompton&p%5B%5D=facets.brand%255B%255D%3DWONDERCHEF&p%5B%5D=facets.brand%255B%255D%3DMAHARAJA%2BWHITELINE&p%5B%5D=facets.brand%255B%255D%3DKenstar&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1000'])
    arr.append(['chimney_4000.txt', 1, False,'https://www.flipkart.com/chimney/pr?sid=j9e%2Cm38%2Ctgz&otracker=categorytree&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D4000'])
    arr.append(['oven_4000.txt', 1, False,'https://www.flipkart.com/microwave-ovens/pr?sid=j9e%2Cm38%2Co49&otracker=categorytree&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D4000'])
    arr.append(['foodprocessor_disc2000.txt', 1, False,'https://www.flipkart.com/food-processors/pr?sid=j9e%2Cm38%2Crj3&otracker=categorytree&sort=price_asc&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.brand%255B%255D%3DMorphy%2BRichards&p[]=facets.brand%255B%255D%3DInalsa&p[]=facets.brand%255B%255D%3DPrestige&p[]=facets.brand%255B%255D%3DBAJAJ&p[]=facets.brand%255B%255D%3DButterfly&p[]=facets.brand%255B%255D%3Dcello&p[]=facets.brand%255B%255D%3DMAHARAJA%2BWHITELINE&p[]=facets.brand%255B%255D%3DMORPHY&p[]=facets.brand%255B%255D%3DKENT&p[]=facets.brand%255B%255D%3DSansui&p[]=facets.brand%255B%255D%3DPHILIPS&p[]=facets.brand%255B%255D%3DSinger&p[]=facets.brand%255B%255D%3DUSHA&p[]=facets.brand%255B%255D%3DWONDERCHEF&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D2000'])
    arr.append(['gasstove_disc1200.txt', 1, False,'https://www.flipkart.com/kitchen-cookware-serveware/gas-stove-accessories/gas-stoves/pr?sid=upp%2Cd7m%2Cuhm&otracker=categorytree&sort=price_asc&p%5B%5D=facets.discount_range_v1%255B%255D%3D70%2525%2Bor%2Bmore&p%5B%5D=facets.number_of_burners%255B%255D%3D2&p%5B%5D=facets.number_of_burners%255B%255D%3D3&p%5B%5D=facets.number_of_burners%255B%255D%3D4&p%5B%5D=facets.number_of_burners%255B%255D%3D5&p%5B%5D=facets.number_of_burners%255B%255D%3D6&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1000'])
    arr.append(['toaster_disc500.txt', 0, False,'https://www.flipkart.com/home-kitchen/kitchen-appliances/popup-toasters/pr?sid=j9e%2Cm38%2Ctxh&otracker=categorytree&otracker=nmenu_sub_TVs+%26+Appliances_0_Pop+Up+Toasters&otracker=nmenu_sub_TVs+%26+Appliances_0_Pop+Up+Toasters&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.brand%255B%255D%3DMAHARAJA%2BWHITELINE&p%5B%5D=facets.brand%255B%255D%3DV-Guard&p%5B%5D=facets.brand%255B%255D%3DPigeon&p%5B%5D=facets.brand%255B%255D%3DPHILIPS&p%5B%5D=facets.brand%255B%255D%3DFlipkart%2BSmartBuy&p%5B%5D=facets.brand%255B%255D%3DButterfly&p%5B%5D=facets.brand%255B%255D%3DMorphy%2BRichards&p%5B%5D=facets.brand%255B%255D%3DBAJAJ&p%5B%5D=facets.brand%255B%255D%3DUSHA&p%5B%5D=facets.brand%255B%255D%3DBOROSIL&p%5B%5D=facets.brand%255B%255D%3DHAVELLS&p%5B%5D=facets.brand%255B%255D%3DWONDERCHEF&p%5B%5D=facets.brand%255B%255D%3Dcello&p%5B%5D=facets.brand%255B%255D%3DPrestige&p%5B%5D=facets.brand%255B%255D%3DBLACK%252BDECKER&p%5B%5D=facets.brand%255B%255D%3DWipro&p%5B%5D=facets.brand%255B%255D%3DPigeon%2Bby%2BStovekraft&p%5B%5D=facets.brand%255B%255D%3DKenstar&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D500'])
    arr.append(['electrickettle_disc200.txt', 0, False,'https://www.flipkart.com/electric-jugheatertravel-kettles/pr?sid=j9e%2Cm38%2Cxrv&otracker=categorytree&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D200&sort=price_asc'])
    arr.append(['grinder_500.txt', 1, False,'https://www.flipkart.com/home-kitchen/kitchen-appliances/wet-grinders/pr?sid=j9e%2Cm38%2Chtd&otracker=categorytree&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DPrestige&p%5B%5D=facets.brand%255B%255D%3DButterfly&p%5B%5D=facets.brand%255B%255D%3DPanasonic&p%5B%5D=facets.brand%255B%255D%3DPigeon&p%5B%5D=facets.brand%255B%255D%3DWONDERCHEF&p%5B%5D=facets.brand%255B%255D%3DUSHA&p%5B%5D=facets.brand%255B%255D%3DHAVELLS&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D500'])
    arr.append(['lunchbox_100.txt', 0, False,'https://www.flipkart.com/kitchen-cookware-serveware/lunch-boxes-bottles-and-flasks/pr?sid=upp%2Cf2k&otracker=categorytree&sort=price_asc&p%5B%5D=facets.discount_range_v1%255B%255D%3D70%2525%2Bor%2Bmore&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D100'])
    arr.append(['gas_2000.txt', 1, False,'https://www.flipkart.com/kitchen-cookware-serveware/gas-stove-accessories/gas-stoves/pr?sid=upp%2Cd7m%2Cuhm&marketplace=FLIPKART&otracker=product_breadCrumbs_Gas+Stoves&sort=price_asc&p%5B%5D=facets.discount_range_v1%255B%255D%3D70%2525%2Bor%2Bmore&p%5B%5D=facets.brand%255B%255D%3DPrestige&p%5B%5D=facets.brand%255B%255D%3DPigeon&p%5B%5D=facets.brand%255B%255D%3DButterfly&p%5B%5D=facets.brand%255B%255D%3DSunflame&p%5B%5D=facets.brand%255B%255D%3DLifelong&p%5B%5D=facets.brand%255B%255D%3DElica&p%5B%5D=facets.brand%255B%255D%3DBAJAJ&p%5B%5D=facets.brand%255B%255D%3DBalaji&p%5B%5D=facets.brand%255B%255D%3DBalajiflame&p%5B%5D=facets.brand%255B%255D%3DBOROSIL&p%5B%5D=facets.brand%255B%255D%3DBOSCH&p%5B%5D=facets.brand%255B%255D%3Dcello&p%5B%5D=facets.brand%255B%255D%3DCrompton&p%5B%5D=facets.brand%255B%255D%3DFaber&p%5B%5D=facets.brand%255B%255D%3DHindware&p%5B%5D=facets.brand%255B%255D%3DIFB&p%5B%5D=facets.brand%255B%255D%3DIMPEX&p%5B%5D=facets.brand%255B%255D%3DKhaitan&p%5B%5D=facets.brand%255B%255D%3DMAHARAJA%2BWHITELINE&p%5B%5D=facets.brand%255B%255D%3DMILTON&p%5B%5D=facets.brand%255B%255D%3DPIGEON%2BBY%2BSTOVE%2BKRAFT&p%5B%5D=facets.brand%255B%255D%3DPigeon%2Bby%2BStovekraft&p%5B%5D=facets.brand%255B%255D%3DSinger&p%5B%5D=facets.brand%255B%255D%3DSun%2BFlame&p%5B%5D=facets.brand%255B%255D%3DSURYA&p%5B%5D=facets.brand%255B%255D%3DUSHA&p%5B%5D=facets.brand%255B%255D%3DV-Guard&p%5B%5D=facets.brand%255B%255D%3DWhirlpool&p%5B%5D=facets.brand%255B%255D%3DWONDERCHEF&p%5B%5D=facets.brand%255B%255D%3DUrban%2BFlame&p%5B%5D=facets.brand%255B%255D%3DKaff&p%5B%5D=facets.brand%255B%255D%3DKraft%2BItaly&p%5B%5D=facets.brand%255B%255D%3DHafele&p%5B%5D=facets.brand%255B%255D%3DMeglio&p%5B%5D=facets.brand%255B%255D%3DGlen&p%5B%5D=facets.brand%255B%255D%3DALSTORM&p%5B%5D=facets.brand%255B%255D%3DSunblaze&p%5B%5D=facets.brand%255B%255D%3DBlowhot&p%5B%5D=facets.brand%255B%255D%3DVidiem&p%5B%5D=facets.brand%255B%255D%3DKutchina&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D2000'])
    arr.append(['cookware_100.txt', 0, False,'https://www.flipkart.com/kitchen-cookware-serveware/cookware/pr?sid=upp%2Ctnx&p%5B%5D=facets.discount_range_v1%255B%255D%3D70%2525%2Bor%2Bmore&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D200&otracker=categorytree&sort=price_asc'])
    arr.append(['tableware_100.txt', 0, False,'https://www.flipkart.com/kitchen-cookware-serveware/tableware-dinnerware/pr?sid=upp%2Ci7t&otracker=categorytree&sort=price_asc&p%5B%5D=facets.discount_range_v1%255B%255D%3D70%2525%2Bor%2Bmore&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D90'])

    if creation_time(foldername)<1200:
        telegram = "off"
    else:
        telegram = "on"
    threads = []

    for i in arr:
        filename = foldername + i[0]
        force = i[1]
        notassured = i[2]
        url = i[3]
        process = Thread(target=flipkart_parse, args=[filename, telegram, force, url, res_queue, notassured])
        process.setDaemon(True)
        process.start()
        threads.append(process)

    process = Thread(target=block, args=[foldername])
    process.start()
    threads.append(process)

    process = Thread(target=updatetoserver, args=[foldername])
    process.start()
    threads.append(process)

    for process in threads:
        process.join()

    print("\nTotal Active Threads : " + str(threading.active_count()))
    print("Telegram = " + telegram)
    #pcmemory()

    gotosleep=False
    with open(foldername.strip("/") + '_output.txt', 'w+') as fall:
        res_queue.put(None)
        while True:
            item = res_queue.get()
            if str(item).find("529 Error")!=-1:
                gotosleep=True
            if item is None:
                break
            fall.write(item + "\r\n")
        fall.write("Telegram = " + telegram)
    res_queue.empty()
    del res_queue
    collected = gc.collect()
    print("Garbage collector: collected", "%d objects." % collected)
    if gotosleep == True:
        print("\n529 errors found. sleep 120 seconds")
        time.sleep(120)

while True:
    try:
        clear()
        dowork()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())

    d = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    hour = d.hour
    if hour >= 3 and hour <= 7:
        sleep = random.randint(5, 10)
        print("----------------------- Sleeping for " + str(sleep) + " Seconds ------------------------")
        time.sleep(sleep)
    else:
        sleep = random.randint(2, 3)
        print("----------------------- Sleeping for " + str(sleep) + " Seconds ------------------------")
        time.sleep(sleep)
