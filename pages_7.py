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


foldername = "m7_hkpri3/"
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

    arr.append(['laptop_i3U10k.txt', 0,False,'https://www.flipkart.com/laptops/pr?sid=6bo%2Cb5g&otracker=categorytree&sort=price_asc&p%5B%5D=facets.processor%255B%255D%3DCore%2Bi3&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B3%2BDual%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B3%2BHexa%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B3%2BQuad%2BCore&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D10000'])
    arr.append(['laptop_i5U15k.txt', 0,False,'https://www.flipkart.com/laptops/pr?sid=6bo%2Cb5g&otracker=categorytree&p%5B%5D=facets.processor%255B%255D%3DCore%2Bi5&sort=price_asc&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B5%2BQuad%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B5%2BHexa%2BCore&p%5B%5D=facets.processor%255B%255D%3DM1&p%5B%5D=facets.processor%255B%255D%3DHexa%2BCore%2Bi5&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B5&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B5%2BDual%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B5%2BOcta%2BCore&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D20000'])
    arr.append(['laptop_i7u20k.txt', 0,False,'https://www.flipkart.com/laptops/pr?sid=6bo%2Cb5g&otracker=categorytree&sort=price_asc&p%5B%5D=facets.processor%255B%255D%3DCore%2Bi7&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B7%2BQuad%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B7%2BOcta%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B7%2BDual%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B7%2BHexa%2BCore&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D20000'])
    arr.append(['laptop_i9u50k.txt', 0,False,'https://www.flipkart.com/laptops/pr?sid=6bo%2Cb5g&otracker=categorytree&sort=price_asc&p%5B%5D=facets.processor%255B%255D%3DCore%2Bi9&p%5B%5D=facets.processor%255B%255D%3DM1&p%5B%5D=facets.processor%255B%255D%3DM1%2BMax&p%5B%5D=facets.processor%255B%255D%3DM1%2BPro&p%5B%5D=facets.processor%255B%255D%3DM2&p%5B%5D=facets.processor%255B%255D%3DM2%2BMax&p%5B%5D=facets.processor%255B%255D%3DM2%2BPro&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B9%2B12%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B9%2B16%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B9%2BOcta%2BCore&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D50000'])
    arr.append(['laptop_processoru18k.txt', 0,False,'https://www.flipkart.com/laptops/pr?sid=6bo%2Cb5g&otracker=categorytree&sort=price_asc&p%5B%5D=facets.processor%255B%255D%3DCore%2Bi5&p%5B%5D=facets.processor%255B%255D%3DCore%2Bi3&p%5B%5D=facets.processor%255B%255D%3DCore%2Bi7&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B7%2BQuad%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B5%2BQuad%2BCore&p%5B%5D=facets.processor%255B%255D%3DCore%2Bi9&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B5%2BHexa%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B7%2BOcta%2BCore&p%5B%5D=facets.processor%255B%255D%3DM1&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B3%2BDual%2BCore&p%5B%5D=facets.processor%255B%255D%3DHexa%2BCore%2Bi5&p%5B%5D=facets.processor%255B%255D%3DM1%2BMax&p%5B%5D=facets.processor%255B%255D%3DM1%2BPro&p%5B%5D=facets.processor%255B%255D%3DM2&p%5B%5D=facets.processor%255B%255D%3DM2%2BMax&p%5B%5D=facets.processor%255B%255D%3DM2%2BPro&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B3%2BHexa%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B3%2BQuad%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B5&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B5%2BDual%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B5%2BOcta%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B7%2BDual%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B7%2BHexa%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B9%2B12%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B9%2B16%2BCore&p%5B%5D=facets.processor%255B%255D%3DRyzen%2B9%2BOcta%2BCore&p%5B%5D=facets.processor%255B%255D%3DZen%2B2&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D18000'])
    arr.append(['frige_freezeru5k.txt', 0,False,'https://www.flipkart.com/home-kitchen/home-appliances/freezer-chests/pr?sid=j9e%2Cabm%2Cix6&otracker=categorytree&p%5B%5D=facets.brand%255B%255D%3DHaier&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DGodrej&p%5B%5D=facets.brand%255B%255D%3DBlue%2BStar&p%5B%5D=facets.brand%255B%255D%3DVoltas&p%5B%5D=facets.brand%255B%255D%3Dtrufrost&p%5B%5D=facets.brand%255B%255D%3DFRIGOGLASS&p%5B%5D=facets.brand%255B%255D%3DCelfrost&p%5B%5D=facets.brand%255B%255D%3Dcvc&p%5B%5D=facets.brand%255B%255D%3DElanpro&p%5B%5D=facets.brand%255B%255D%3DEURONOVA&p%5B%5D=facets.brand%255B%255D%3DPanasonic&p%5B%5D=facets.brand%255B%255D%3DRockwell&p%5B%5D=facets.brand%255B%255D%3DWESTERN&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D5000'])
    arr.append(['sofa_reclinceru3k.txt', 0,False,'https://www.flipkart.com/furniture/sofas/recliners/pr?sid=wwe%2Cc3z%2Cgxy&otracker=categorytree&sort=price_asc&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D3000'])
    arr.append(['frige_u7k.txt', 0,False,'https://www.flipkart.com/home-kitchen/home-appliances/refrigerators/pr?sid=j9e%2Cabm%2Chzg&otracker=categorytree&sort=price_asc&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D7000'])
    arr.append(['mob_5gU10k.txt', 0,False,'https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&p%5B%5D=facets.network_type%255B%255D%3D5G&sort=price_asc&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D10000'])
    arr.append(['mob_appleU20k.txt', 1,False,'https://www.flipkart.com/search?sid=tyy%2C4io&otracker=CLP_Filters&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DAPPLE&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D20000'])
    arr.append(['mob_oplus11k.txt', 1,False,'https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&p%5B%5D=facets.network_type%255B%255D%3D5G&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DOnePlus&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D11000'])
    arr.append(['mob_samsung5gU12k.txt', 1,False,'https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&sort=price_asc&p%5B%5D=facets.network_type%255B%255D%3D5G&p%5B%5D=facets.brand%255B%255D%3DSAMSUNG&p%5B%5D=facets.brand%255B%255D%3DAPPLE&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D12000'])
    arr.append(['mob_asusGoogle5gU15k.txt', 1,False,'https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&p%5B%5D=facets.network_type%255B%255D%3D5G&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DASUS&p%5B%5D=facets.brand%255B%255D%3DGoogle&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D15000'])
    arr.append(['mob_brandU7k.txt', 1,False,'https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&p%5B%5D=facets.operating_system%255B%255D%3DAndroid&sort=price_asc&p%5B%5D=facets.operating_system%255B%255D%3DiOS&p%5B%5D=facets.brand%255B%255D%3DSAMSUNG&p%5B%5D=facets.brand%255B%255D%3DAPPLE&p%5B%5D=facets.brand%255B%255D%3Drealme&p%5B%5D=facets.brand%255B%255D%3DPOCO&p%5B%5D=facets.brand%255B%255D%3DInfinix&p%5B%5D=facets.brand%255B%255D%3DOPPO&p%5B%5D=facets.brand%255B%255D%3Dvivo&p%5B%5D=facets.brand%255B%255D%3DREDMI&p%5B%5D=facets.brand%255B%255D%3DNothing&p%5B%5D=facets.brand%255B%255D%3DMOTOROLA&p%5B%5D=facets.brand%255B%255D%3DMi&p%5B%5D=facets.brand%255B%255D%3DLAVA&p%5B%5D=facets.brand%255B%255D%3DNokia&p%5B%5D=facets.brand%255B%255D%3DOnePlus&p%5B%5D=facets.brand%255B%255D%3DTecno&p%5B%5D=facets.brand%255B%255D%3DASUS&p%5B%5D=facets.brand%255B%255D%3DIQOO&p%5B%5D=facets.brand%255B%255D%3DHonor&p%5B%5D=facets.brand%255B%255D%3DLenovo&p%5B%5D=facets.brand%255B%255D%3DPanasonic&p%5B%5D=facets.brand%255B%255D%3DLG&p%5B%5D=facets.brand%255B%255D%3DSONY&p%5B%5D=facets.brand%255B%255D%3DHTC&p%5B%5D=facets.brand%255B%255D%3DSony%2BEricsson&p%5B%5D=facets.brand%255B%255D%3DHuawei&p%5B%5D=facets.brand%255B%255D%3DGoogle&p%5B%5D=facets.ram%255B%255D%3D6%2BGB&p%5B%5D=facets.ram%255B%255D%3D8%2BGB%2Band%2BAbove&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D7000'])
    arr.append(['monitorU2k.txt', 1,False,'https://www.flipkart.com/computers/monitors/pr?sid=6bo%2C9no&otracker=categorytree&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DDELL&p%5B%5D=facets.brand%255B%255D%3DLG&p%5B%5D=facets.brand%255B%255D%3DHP&p%5B%5D=facets.brand%255B%255D%3DSAMSUNG&p%5B%5D=facets.brand%255B%255D%3DBenQ&p%5B%5D=facets.brand%255B%255D%3DLenovo&p%5B%5D=facets.brand%255B%255D%3DMSI&p%5B%5D=facets.brand%255B%255D%3DViewSonic&p%5B%5D=facets.brand%255B%255D%3DAcer&p%5B%5D=facets.brand%255B%255D%3DASUS&p%5B%5D=facets.brand%255B%255D%3DZEBRONICS&p%5B%5D=facets.brand%255B%255D%3DAOC&p%5B%5D=facets.brand%255B%255D%3DPHILIPS&p%5B%5D=facets.brand%255B%255D%3DMarQ%2Bby%2BFlipkart&p%5B%5D=facets.brand%255B%255D%3DGIGABYTE&p%5B%5D=facets.brand%255B%255D%3DSECUREYE&p%5B%5D=facets.brand%255B%255D%3DCORNEA&p%5B%5D=facets.brand%255B%255D%3DIntex&p%5B%5D=facets.brand%255B%255D%3DPunta&p%5B%5D=facets.brand%255B%255D%3Dzebion&p%5B%5D=facets.brand%255B%255D%3DHyperX&p%5B%5D=facets.brand%255B%255D%3DHASONS&p%5B%5D=facets.brand%255B%255D%3DFINGERS&p%5B%5D=facets.brand%255B%255D%3DA1Gizmo&p%5B%5D=facets.brand%255B%255D%3Drealme&p%5B%5D=facets.brand%255B%255D%3Dantique%2Bit%2Bsolution&p%5B%5D=facets.brand%255B%255D%3DXElectron&p%5B%5D=facets.brand%255B%255D%3DPalas&p%5B%5D=facets.brand%255B%255D%3DOnePlus&p%5B%5D=facets.brand%255B%255D%3DElo&p%5B%5D=facets.brand%255B%255D%3DArzopa&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D2000'])
    arr.append(['curvemonitor5k.txt', 1,False,'https://www.flipkart.com/computers/monitors/pr?sid=6bo%2C9no&otracker=categorytree&sort=price_asc&p%5B%5D=facets.screen_form_factor%255B%255D%3DCurved&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D5000'])
    arr.append(['monitorresolu7k.txt', 1,False,'https://www.flipkart.com/computers/computer-components/monitors/pr?sid=6bo%2Cg0i%2C9no&otracker=categorytree&p%5B%5D=facets.screen_resolution%255B%255D%3D4K%2BUltra%2BHD&sort=price_asc&p%5B%5D=facets.screen_resolution%255B%255D%3DQuad%2BHD&p%5B%5D=facets.screen_resolution%255B%255D%3DUHD&p%5B%5D=facets.screen_resolution%255B%255D%3DUWQHD&p%5B%5D=facets.screen_resolution%255B%255D%3DWFHD&p%5B%5D=facets.screen_resolution%255B%255D%3DWQHD&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D7000'])
    arr.append(['printersU2k.txt', 1,False,'https://www.flipkart.com/computers/computer-peripherals/printers-inks/printers/pr?sid=6bo%2Ctia%2Cffn%2Ct64&otracker=categorytree&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DHP&p%5B%5D=facets.brand%255B%255D%3DEpson&p%5B%5D=facets.brand%255B%255D%3DCanon&p%5B%5D=facets.brand%255B%255D%3Dbrother&p%5B%5D=facets.brand%255B%255D%3DPanasonic&p%5B%5D=facets.brand%255B%255D%3DPANTUM&p%5B%5D=facets.brand%255B%255D%3DXerox&p%5B%5D=facets.brand%255B%255D%3DSAMSUNG&p%5B%5D=facets.brand%255B%255D%3DSTIER&p%5B%5D=facets.brand%255B%255D%3DRicoh&p%5B%5D=facets.brand%255B%255D%3DPrimacy&p%5B%5D=facets.brand%255B%255D%3DMY%2BPRINT&p%5B%5D=facets.brand%255B%255D%3DMAGICARD&p%5B%5D=facets.brand%255B%255D%3D3IdeaTechnology&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D2000'])
    arr.append(['laserprinterU4k.txt', 1,False,'https://www.flipkart.com/computers/computer-peripherals/printers-inks/printers/pr?sid=6bo%2Ctia%2Cffn%2Ct64&otracker=categorytree&p%5B%5D=facets.printer_type%255B%255D%3DLaser&sort=price_asc&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D4000'])
    arr.append(['multifunctionprinterU3k.txt', 1,False,'https://www.flipkart.com/computers/computer-peripherals/printers-inks/printers/multi-function-printers/pr?sid=6bo%2Ctia%2Cffn%2Ct64%2Cmpr&otracker=categorytree&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D3000'])
    arr.append(['camera_dslrU15k.txt', 1,False,'https://www.flipkart.com/cameras/dslr-mirrorless/pr?sid=jek%2Cp31%2Ctrv&otracker=categorytree&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DCanon&p%5B%5D=facets.brand%255B%255D%3DNIKON&p%5B%5D=facets.brand%255B%255D%3DSONY&p%5B%5D=facets.brand%255B%255D%3DPanasonic&p%5B%5D=facets.brand%255B%255D%3DFUJIFILM&p%5B%5D=facets.brand%255B%255D%3DPentax&p%5B%5D=facets.brand%255B%255D%3DOLYMPUS&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D15000'])
    arr.append(['camera_gopro10k.txt', 1,False,'https://www.flipkart.com/cameras/sports-action/pr?sid=jek%2Cp31%2Cs3q&otracker=categorytree&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DGoPro&p%5B%5D=facets.brand%255B%255D%3DRicoh&p%5B%5D=facets.brand%255B%255D%3DInsta360&p%5B%5D=facets.brand%255B%255D%3DMIDLAND&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D10000'])
    arr.append(['camera_shootcameraU20k.txt', 1,False,'https://www.flipkart.com/cameras/point-and-shoot/pr?sid=jek%2Cp31%2Cnxa&otracker=categorytree&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DCanon&p%5B%5D=facets.brand%255B%255D%3DSONY&p%5B%5D=facets.brand%255B%255D%3DPanasonic&p%5B%5D=facets.brand%255B%255D%3DRicoh&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D20000'])
    arr.append(['gamingconsoleU20k.txt', 0,False,'https://www.flipkart.com/gaming/gaming-consoles/pr?sid=4rr%2Cx1m&otracker=categorytree&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DMICROSOFT&p%5B%5D=facets.brand%255B%255D%3DSONY&p%5B%5D=facets.brand%255B%255D%3DAMKETTE&p%5B%5D=facets.brand%255B%255D%3DMITASHI&p%5B%5D=facets.brand%255B%255D%3DXbox&p%5B%5D=facets.brand%255B%255D%3DNintendo%2BSwitch&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore'])
    arr.append(['tv_4k8kU21k.txt', 1,False,'https://www.flipkart.com/televisions/pr?sid=ckf%2Cczl&otracker=categorytree&p%5B%5D=facets.brand%255B%255D%3Drealme&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DOnePlus&p%5B%5D=facets.brand%255B%255D%3DSAMSUNG&p%5B%5D=facets.brand%255B%255D%3DThomson&p%5B%5D=facets.brand%255B%255D%3DLG&p%5B%5D=facets.brand%255B%255D%3DSONY&p%5B%5D=facets.brand%255B%255D%3DVu&p%5B%5D=facets.brand%255B%255D%3DMi&p%5B%5D=facets.brand%255B%255D%3DMOTOROLA&p%5B%5D=facets.brand%255B%255D%3DInfinix&p%5B%5D=facets.brand%255B%255D%3DTCL&p%5B%5D=facets.brand%255B%255D%3DHisense&p%5B%5D=facets.brand%255B%255D%3DPanasonic&p%5B%5D=facets.brand%255B%255D%3DHaier&p%5B%5D=facets.brand%255B%255D%3DAcer&p%5B%5D=facets.brand%255B%255D%3DKODAK&p%5B%5D=facets.brand%255B%255D%3DiFFALCON&p%5B%5D=facets.brand%255B%255D%3DSansui&p%5B%5D=facets.brand%255B%255D%3DNokia&p%5B%5D=facets.brand%255B%255D%3DTOSHIBA&p%5B%5D=facets.brand%255B%255D%3DCompaq&p%5B%5D=facets.brand%255B%255D%3DBlaupunkt&p%5B%5D=facets.brand%255B%255D%3DLloyd&p%5B%5D=facets.brand%255B%255D%3DLIMEBERRY&p%5B%5D=facets.brand%255B%255D%3DAiwa&p%5B%5D=facets.brand%255B%255D%3DPHILIPS&p%5B%5D=facets.brand%255B%255D%3DDyanora&p%5B%5D=facets.brand%255B%255D%3DCoocaa&p%5B%5D=facets.brand%255B%255D%3DSENS&p%5B%5D=facets.brand%255B%255D%3DONIDA&p%5B%5D=facets.brand%255B%255D%3DJVC&p%5B%5D=facets.brand%255B%255D%3DPower%2BGuard&p%5B%5D=facets.brand%255B%255D%3DCORNEA&p%5B%5D=facets.brand%255B%255D%3DAISEN&p%5B%5D=facets.brand%255B%255D%3DTRUSENSE&p%5B%5D=facets.brand%255B%255D%3DHyundai&p%5B%5D=facets.brand%255B%255D%3DBITPRO&p%5B%5D=facets.brand%255B%255D%3DiMEE&p%5B%5D=facets.brand%255B%255D%3DSkywall&p%5B%5D=facets.brand%255B%255D%3DSTARSHINE&p%5B%5D=facets.brand%255B%255D%3DSKYTRON&p%5B%5D=facets.brand%255B%255D%3DReintech&p%5B%5D=facets.brand%255B%255D%3DNU&p%5B%5D=facets.brand%255B%255D%3DINVANTER&p%5B%5D=facets.brand%255B%255D%3DIMPEX&p%5B%5D=facets.brand%255B%255D%3DHUIDI&p%5B%5D=facets.brand%255B%255D%3DFoxsky&p%5B%5D=facets.brand%255B%255D%3DBPL&p%5B%5D=facets.brand%255B%255D%3DAGE&p%5B%5D=facets.brand%255B%255D%3DWeston&p%5B%5D=facets.brand%255B%255D%3DPanwood&p%5B%5D=facets.brand%255B%255D%3DLEEMA&p%5B%5D=facets.brand%255B%255D%3Dndgo&p%5B%5D=facets.brand%255B%255D%3DZEBRONICS&p%5B%5D=facets.brand%255B%255D%3DSanyo&p%5B%5D=facets.brand%255B%255D%3DSalora&p%5B%5D=facets.brand%255B%255D%3DQVA&p%5B%5D=facets.brand%255B%255D%3DNoble%2BSkiodo&p%5B%5D=facets.brand%255B%255D%3DMicromax&p%5B%5D=facets.brand%255B%255D%3DMarQ%2Bby%2BFlipkart&p%5B%5D=facets.brand%255B%255D%3DDETEL&p%5B%5D=facets.brand%255B%255D%3DCroma&p%5B%5D=facets.brand%255B%255D%3DCandes&p%5B%5D=facets.resolution%255B%255D%3DUltra%2BHD%2B%25288K%2529&p%5B%5D=facets.resolution%255B%255D%3DUltra%2BHD%2B%25284K%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D17000'])
    arr.append(['smartwatchpremiumU2k.txt', 1,False,'https://www.flipkart.com/wearable-smart-devices/smart-watches/pr?sid=ajy%2Cbuh&otracker=categorytree&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DFITBIT&p%5B%5D=facets.brand%255B%255D%3DSAMSUNG&p%5B%5D=facets.brand%255B%255D%3DFOSSIL&p%5B%5D=facets.brand%255B%255D%3DTitan&p%5B%5D=facets.brand%255B%255D%3DAMAZFIT&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D2000'])
    arr.append(['speakerBabove60wU1500.txt', 1,False,'https://www.flipkart.com/audio-video/speakers/pr?sid=0pm%2C0o7&otracker=categorytree&sort=price_asc&p%5B%5D=facets.wattage%255B%255D%3D161%2B-%2B200%2BW&p%5B%5D=facets.wattage%255B%255D%3D61-100%2BW&p%5B%5D=facets.wattage%255B%255D%3DAbove%2B200%2BW&p%5B%5D=facets.wattage%255B%255D%3D101-160%2BW&p%5B%5D=facets.brand%255B%255D%3DF%2526D&p%5B%5D=facets.brand%255B%255D%3DIntex&p%5B%5D=facets.brand%255B%255D%3DboAt&p%5B%5D=facets.brand%255B%255D%3DPanasonic&p%5B%5D=facets.brand%255B%255D%3DJBL&p%5B%5D=facets.brand%255B%255D%3DSonos&p%5B%5D=facets.brand%255B%255D%3DBose&p%5B%5D=facets.brand%255B%255D%3DAPPLE&p%5B%5D=facets.brand%255B%255D%3DSAMSUNG&p%5B%5D=facets.brand%255B%255D%3DGoogle&p%5B%5D=facets.brand%255B%255D%3DLG&p%5B%5D=facets.brand%255B%255D%3DMarshall&p%5B%5D=facets.brand%255B%255D%3DPolk%2BAudio&p%5B%5D=facets.brand%255B%255D%3DYAMAHA&p%5B%5D=facets.brand%255B%255D%3DHarman%2BKardon&p%5B%5D=facets.brand%255B%255D%3DEdifier&p%5B%5D=facets.brand%255B%255D%3DJack%2BMartin&p%5B%5D=facets.brand%255B%255D%3Dultiads&p%5B%5D=facets.brand%255B%255D%3DAnker&p%5B%5D=facets.brand%255B%255D%3DRZG&p%5B%5D=facets.brand%255B%255D%3DAhuja&p%5B%5D=facets.brand%255B%255D%3DQuaranel&p%5B%5D=facets.brand%255B%255D%3Dliluns&p%5B%5D=facets.brand%255B%255D%3DDH%2BDiscovery&p%5B%5D=facets.brand%255B%255D%3DMivi&p%5B%5D=facets.brand%255B%255D%3DBlaupunkt&p%5B%5D=facets.brand%255B%255D%3DSAREGAMA&p%5B%5D=facets.brand%255B%255D%3DIMPEX&p%5B%5D=facets.brand%255B%255D%3DLogitech&p%5B%5D=facets.brand%255B%255D%3DTOSHIBA&p%5B%5D=facets.brand%255B%255D%3DTRONICA&p%5B%5D=facets.brand%255B%255D%3DPortronics&p%5B%5D=facets.brand%255B%255D%3DPTron&p%5B%5D=facets.brand%255B%255D%3DAkai&p%5B%5D=facets.brand%255B%255D%3DZebronics&p%5B%5D=facets.brand%255B%255D%3DSony&p%5B%5D=facets.brand%255B%255D%3DPhilips&p%5B%5D=facets.brand%255B%255D%3DMotorola&p%5B%5D=facets.brand%255B%255D%3DiBall&p%5B%5D=facets.brand%255B%255D%3DInfinity&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1500'])
    arr.append(['earphoneU500.txt', 1,False,'https://www.flipkart.com/audio-video/headset/earphones/wireless-earphones/pr?sid=0pm%2Cfcn%2C821%2Ca7x&otracker=categorytree&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DboAt&p%5B%5D=facets.brand%255B%255D%3DOnePlus&p%5B%5D=facets.brand%255B%255D%3Drealme&p%5B%5D=facets.brand%255B%255D%3DSONY&p%5B%5D=facets.brand%255B%255D%3DJBL&p%5B%5D=facets.brand%255B%255D%3DNoise&p%5B%5D=facets.brand%255B%255D%3DFire-Boltt&p%5B%5D=facets.brand%255B%255D%3DOPPO&p%5B%5D=facets.brand%255B%255D%3DLenovo&p%5B%5D=facets.brand%255B%255D%3DCrossBeats&p%5B%5D=facets.brand%255B%255D%3DQuaranel&p%5B%5D=facets.brand%255B%255D%3DBlaupunkt&p%5B%5D=facets.brand%255B%255D%3DSkullcandy&p%5B%5D=facets.brand%255B%255D%3DAPPLE&p%5B%5D=facets.brand%255B%255D%3DSAMSUNG&p%5B%5D=facets.brand%255B%255D%3DNothing&p%5B%5D=facets.brand%255B%255D%3DTCL&p%5B%5D=facets.brand%255B%255D%3DREDMI&p%5B%5D=facets.brand%255B%255D%3DSoundLOGIC&p%5B%5D=facets.brand%255B%255D%3DPortnix&p%5B%5D=facets.brand%255B%255D%3DPioneer&p%5B%5D=facets.brand%255B%255D%3DPanasonic&p%5B%5D=facets.brand%255B%255D%3DPOCO&p%5B%5D=facets.brand%255B%255D%3DIntex&p%5B%5D=facets.brand%255B%255D%3DGoogle&p%5B%5D=facets.brand%255B%255D%3DGOVO&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D500'])
    arr.append(['earphoneU200k.txt', 1,False,'https://www.flipkart.com/audio-video/headset/earphones/wireless-earphones/pr?sid=0pm%2Cfcn%2C821%2Ca7x&otracker=categorytree&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DboAt&p%5B%5D=facets.brand%255B%255D%3DOnePlus&p%5B%5D=facets.brand%255B%255D%3Drealme&p%5B%5D=facets.brand%255B%255D%3DBoult%2BAudio&p%5B%5D=facets.brand%255B%255D%3DMivi&p%5B%5D=facets.brand%255B%255D%3DSONY&p%5B%5D=facets.brand%255B%255D%3DJBL&p%5B%5D=facets.brand%255B%255D%3DWings&p%5B%5D=facets.brand%255B%255D%3DNoise&p%5B%5D=facets.brand%255B%255D%3DPTron&p%5B%5D=facets.brand%255B%255D%3DFire-Boltt&p%5B%5D=facets.brand%255B%255D%3DPortronics&p%5B%5D=facets.brand%255B%255D%3DOPPO&p%5B%5D=facets.brand%255B%255D%3DLenovo&p%5B%5D=facets.brand%255B%255D%3DSyska&p%5B%5D=facets.brand%255B%255D%3DCrossBeats&p%5B%5D=facets.brand%255B%255D%3DQuaranel&p%5B%5D=facets.brand%255B%255D%3DGizmore&p%5B%5D=facets.brand%255B%255D%3DBlaupunkt&p%5B%5D=facets.brand%255B%255D%3DSkullcandy&p%5B%5D=facets.brand%255B%255D%3DLAVA&p%5B%5D=facets.brand%255B%255D%3DAPPLE&p%5B%5D=facets.brand%255B%255D%3DZiox&p%5B%5D=facets.brand%255B%255D%3DSAMSUNG&p%5B%5D=facets.brand%255B%255D%3DNothing&p%5B%5D=facets.brand%255B%255D%3DTCL&p%5B%5D=facets.brand%255B%255D%3DREDMI&p%5B%5D=facets.brand%255B%255D%3DHRX&p%5B%5D=facets.brand%255B%255D%3Diball&p%5B%5D=facets.brand%255B%255D%3DSoundLOGIC&p%5B%5D=facets.brand%255B%255D%3DPortnix&p%5B%5D=facets.brand%255B%255D%3DPioneer&p%5B%5D=facets.brand%255B%255D%3DPanasonic&p%5B%5D=facets.brand%255B%255D%3DPOCO&p%5B%5D=facets.brand%255B%255D%3DIntex&p%5B%5D=facets.brand%255B%255D%3DGoogle&p%5B%5D=facets.brand%255B%255D%3DGOVO&p%5B%5D=facets.brand%255B%255D%3DZEBRONICS&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D200'])
    arr.append(['fan_bldc_U1500k.txt', 1,False,'https://www.flipkart.com/home-kitchen/home-appliances/fans/pr?sid=j9e%2Cabm%2Clbz&otracker=categorytree&sort=price_asc&p%5B%5D=facets.theme%255B%255D%3DBLDC%2BTechnology&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1500'])
    arr.append(['fan_designer_U1500k.txt', 1,False,'https://www.flipkart.com/fan/pr?sid=j9e%2Cabm%2Clbz&otracker=categorytree&sort=price_asc&p%5B%5D=facets.theme%255B%255D%3DDesigner%2BFan&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1500'])
    arr.append(['fan_premium_U1500k.txt', 1,False,'https://www.flipkart.com/fan/pr?sid=j9e%2Cabm%2Clbz&otracker=categorytree&sort=price_asc&p%5B%5D=facets.theme%255B%255D%3DNew%2BPremium%2BRange&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1500'])
    arr.append(['fan_newlaunchesU1000k.txt', 1,False,'https://www.flipkart.com/fan/pr?sid=j9e%2Cabm%2Clbz&otracker=categorytree&sort=price_asc&p%5B%5D=facets.theme%255B%255D%3DNew%2BPremium%2BRange&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1500'])
    arr.append(['tablet_U3000k.txt', 1,False,'https://www.flipkart.com/tablets/pr?sid=tyy%2Chry&otracker=categorytree&sort=price_asc&p%5B%5D=facets.connectivity%255B%255D%3D4G&p%5B%5D=facets.connectivity%255B%255D%3DWi-Fi%2BOnly&p%5B%5D=facets.connectivity%255B%255D%3DWi-Fi%252B4G&p%5B%5D=facets.connectivity%255B%255D%3DWi-Fi%252B5G&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D3000'])
    arr.append(['tablet_topBU10k.txt', 1,False,'https://www.flipkart.com/tablets/pr?sid=tyy%2Chry&otracker=categorytree&sort=price_asc&p%5B%5D=facets.connectivity%255B%255D%3D4G&p%5B%5D=facets.connectivity%255B%255D%3DWi-Fi%2BOnly&p%5B%5D=facets.connectivity%255B%255D%3DWi-Fi%252B4G&p%5B%5D=facets.connectivity%255B%255D%3DWi-Fi%252B5G&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D3000'])
    arr.append(['tablet_U5k.txt', 1,False,'https://www.flipkart.com/tablets/pr?sid=tyy%2Chry&otracker=categorytree&p%5B%5D=facets.brand%255B%255D%3DAPPLE&sort=price_asc&p%5B%5D=facets.brand%255B%255D%3DLenovo&p%5B%5D=facets.brand%255B%255D%3DSAMSUNG&p%5B%5D=facets.brand%255B%255D%3DTCL&p%5B%5D=facets.brand%255B%255D%3DMICROSOFT&p%5B%5D=facets.brand%255B%255D%3DHuawei&p%5B%5D=facets.brand%255B%255D%3DHP&p%5B%5D=facets.brand%255B%255D%3DASUS&p%5B%5D=facets.brand%255B%255D%3DDELL&p%5B%5D=facets.brand%255B%255D%3Drealme&p%5B%5D=facets.brand%255B%255D%3DREDMI&p%5B%5D=facets.brand%255B%255D%3DMaplin&p%5B%5D=facets.brand%255B%255D%3DNokia&p%5B%5D=facets.brand%255B%255D%3DHonor&p%5B%5D=facets.brand%255B%255D%3DTecno&p%5B%5D=facets.brand%255B%255D%3DIQOO&p%5B%5D=facets.brand%255B%255D%3DOnePlus&p%5B%5D=facets.brand%255B%255D%3DAcer&p%5B%5D=facets.brand%255B%255D%3DMOTOROLA&p%5B%5D=facets.brand%255B%255D%3DWishtel&p%5B%5D=facets.brand%255B%255D%3DMi&p%5B%5D=facets.brand%255B%255D%3DElevn&p%5B%5D=facets.brand%255B%255D%3Dvivo&p%5B%5D=facets.brand%255B%255D%3DOppo&p%5B%5D=facets.brand%255B%255D%3DLifeDigital&p%5B%5D=facets.brand%255B%255D%3DCornea&p%5B%5D=facets.brand%255B%255D%3DWings&p%5B%5D=facets.brand%255B%255D%3DValve&p%5B%5D=facets.brand%255B%255D%3DFUSION5&p%5B%5D=facets.brand%255B%255D%3Ditel&p%5B%5D=facets.brand%255B%255D%3DPanasonic&p%5B%5D=facets.brand%255B%255D%3DBaatu&p%5B%5D=facets.brand%255B%255D%3DAvita&p%5B%5D=facets.brand%255B%255D%3DCoolpad&p%5B%5D=facets.brand%255B%255D%3DE%2526L&p%5B%5D=facets.brand%255B%255D%3DGIONEE&p%5B%5D=facets.brand%255B%255D%3DGoogle&p%5B%5D=facets.brand%255B%255D%3DHTC&p%5B%5D=facets.brand%255B%255D%3DElephone&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D5000'])
    arr.append(['lap_hpU16k.txt', 1,False,'https://www.flipkart.com/laptops/hp~brand/pr?sid=6bo%2Cb5g&otracker=categorytree&sort=price_asc&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D16000'])
    arr.append(['lap_dellU20k.txt', 1,False,'https://www.flipkart.com/laptops/dell~brand/pr?sid=6bo%2Cb5g&otracker=categorytree&sort=price_asc&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D20000'])
    arr.append(['lap_appleU50k.txt', 1,False,'https://www.flipkart.com/laptops/apple~brand/pr?sid=6bo%2Cb5g&otracker=categorytree&sort=price_asc&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D50000'])
    arr.append(['lap_msiU25k.txt', 1,False,'https://www.flipkart.com/laptops/msi~brand/pr?sid=6bo%2Cb5g&otracker=categorytree&sort=price_asc&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D25000'])
    arr.append(['lap_acerU15k.txt', 1,False,'https://www.flipkart.com/laptops/acer~brand/pr?sid=6bo%2Cb5g&otracker=categorytree&sort=price_asc&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D15000'])
    arr.append(['lap_asusU12k.txt', 1,False,'https://www.flipkart.com/laptops/asus~brand/pr?sid=6bo%2Cb5g&otracker=categorytree&sort=price_asc&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D12000'])
    arr.append(['tv_sonyU21k.txt', 1,False,'https://www.flipkart.com/televisions/sony~brand/pr?sid=ckf%2Cczl&otracker=categorytree&sort=price_asc&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D21000'])
    arr.append(['fan_atomberU1800.txt', 1,False,'https://www.flipkart.com/fan/atomberg~brand/pr?sid=j9e%2Cabm%2Clbz&otracker=categorytree&sort=price_asc&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1800'])
    arr.append(['fan_havellsU1500.txt', 1,False,'https://www.flipkart.com/fan/havells~brand/pr?sid=j9e%2Cabm%2Clbz&otracker=categorytree&sort=price_asc&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1500'])
    arr.append(['fan_cromptonU1k.txt', 1,False,'https://www.flipkart.com/fan/crompton~brand/pr?sid=j9e%2Cabm%2Clbz&otracker=categorytree&sort=price_asc&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1000'])
    arr.append(['fan_bajajU1k.txt', 1,False,'https://www.flipkart.com/fan/bajaj~brand/pr?sid=j9e%2Cabm%2Clbz&otracker=categorytree&sort=price_asc&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1000'])
    arr.append(['fan_polycabU1000.txt', 1,False,'https://www.flipkart.com/fan/polycab~brand/pr?sid=j9e%2Cabm%2Clbz&otracker=categorytree&sort=price_asc&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1000'])
    arr.append(['fan_kuhlU2k.txt', 1,False,'https://www.flipkart.com/fan/kuhl~brand/pr?sid=j9e%2Cabm%2Clbz&otracker=categorytree&sort=price_asc&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D2000'])
    arr.append(['tv_50inchplus21k.txt', 1,False,'https://www.flipkart.com/televisions/pr?sid=ckf%2Cczl&otracker=categorytree&p%5B%5D=facets.screen_size%255B%255D%3D48%2B-%2B55%2Binch&sort=price_asc&p%5B%5D=facets.screen_size%255B%255D%3D60%2Binch%2B%2BAbove&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D21000'])
    arr.append(['food_coffee_100.txt', 0, False, 'https://www.flipkart.com/food-products/coffee-powder/~gourmet-foods-/pr?sid=eat%2Cdui&otracker=categorytree&sort=price_asc&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D100'])
    arr.append(['food_rice_100.txt', 0, False, 'https://www.flipkart.com/food-products/rice/pr?sid=eat%2Cyul&otracker=categorytree&sort=price_asc&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D200'])
    arr.append(['food_tea_100.txt', 0, False, 'https://www.flipkart.com/food-products/tea-powder/pr?sid=eat%2Cfpm&otracker=categorytree&sort=price_asc&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D120'])
    arr.append(['food_oil_100.txt', 0, False, 'https://www.flipkart.com/food-products/edible-oil/pr?sid=eat%2C18p&otracker=categorytree&sort=price_asc&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D200&p%5B%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock'])
    arr.append(['food_combo_100.txt', 0, False, 'https://www.flipkart.com/food-products/food-combo/pr?sid=eat%2Cymr&otracker=categorytree&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D100'])
    arr.append(['food_pulses_100.txt', 0, False, 'https://www.flipkart.com/food-products/pulses/pr?sid=eat%2Canl&otracker=categorytree&sort=price_asc&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D120'])
    arr.append(['food_biscuit_100.txt', 0, False, 'https://www.flipkart.com/food-products/biscuit-cookie-and-rusk/pr?sid=eat%2C5am&otracker=categorytree&sort=price_asc&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D120&p%5B%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock'])

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

    with open(foldername.strip("/") + '_output.txt', 'w+') as fall:
        res_queue.put(None)
        while True:
            item=res_queue.get()
            if item is None:
                break
            fall.write(item + "\r\n")
        fall.write("Telegram = " + telegram)
    res_queue.empty()
    del res_queue
    collected = gc.collect()
    print("Garbage collector: collected", "%d objects." % collected)

while True:
    try:
        #clear()
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
