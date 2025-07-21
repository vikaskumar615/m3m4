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
from multiprocessing import Process, Queue
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
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# vikasatpnp
foldername = "mukta/"
if not os.path.exists(foldername):
    os.mkdir(foldername)


def creation_time(path_to_file):
    current = time.time()
    try:
        return current - float(os.path.getctime(path_to_file))
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

    arr.append(['kitchen_3k.txt', 0, False, 'https://www.flipkart.com/home-kitchen/kitchen-appliances/~cs-3segusukeg/pr?sid=j9e%2Cm38&fm=neo%2Fmerchandising&iid=M_3281ae8b-c579-4093-ac28-2746830b155c_4.L4EA8JME8ZRM&ppt=dynamic&ppn=dynamic&ssid=4xoly3xc7khnhreo1681451282171&otracker=hp_omu_Top%2BOffers_8_4.dealCard.OMU_L4EA8JME8ZRM_4&otracker1=hp_omu_PINNED_neo%2Fmerchandising_Top%2BOffers_NA_dealCard_cc_8_NA_view-all_4&cid=L4EA8JME8ZRM&sort=price_asc&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D3000'])
    arr.append(['kitchen_1500.txt', 0, False, 'https://www.flipkart.com/home-kitchen/home-appliances/~cs-3segusukeg/pr?sid=j9e%2Cabm&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InZhbHVlQ2FsbG91dCI6eyJtdWx0aVZhbHVlZEF0dHJpYnV0ZSI6eyJrZXkiOiJ2YWx1ZUNhbGxvdXQiLCJpbmZlcmVuY2VUeXBlIjoiVkFMVUVfQ0FMTE9VVCIsInZhbHVlcyI6WyJVcCB0byA3MCUgT2ZmIl0sInZhbHVlVHlwZSI6Ik1VTFRJX1ZBTFVFRCJ9fSwidGl0bGUiOnsibXVsdGlWYWx1ZWRBdHRyaWJ1dGUiOnsia2V5IjoidGl0bGUiLCJpbmZlcmVuY2VUeXBlIjoiVElUTEUiLCJ2YWx1ZXMiOlsiQmVzdHNlbGxpbmcgSG9tZSBBcHBsaWFuY2VzIl0sInZhbHVlVHlwZSI6Ik1VTFRJX1ZBTFVFRCJ9fX19fQ%3D%3D&fm=neo%2Fmerchandising&iid=43cee7ae-c723-4cad-a18d-f7e71348c990.3R7UTRHJWF4X&ppt=dynamic&ppn=dynamic&ssid=de27cztwn4upbbi81681452266019&otracker=dynamic_omu_Top%252BOffers_11_Up%2Bto%2B70%2525%2BOff_3R7UTRHJWF4X&cid=3R7UTRHJWF4X&sort=price_asc&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1500'])
    arr.append(['foodprocessor_500.txt', 0, False, 'https://www.flipkart.com/food-processors/pr?sid=j9e%2Cm38%2Crj3&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&otracker=categorytree&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D500'])
    arr.append(['airfryer_500.txt', 0, False, 'https://www.flipkart.com/home-kitchen/kitchen-appliances/air-fryers/pr?sid=j9e%2Cm38%2Cj1e&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&otracker=categorytree&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D500'])
    arr.append(['juicermixergrinder_500.txt', 0, False, 'https://www.flipkart.com/mixerjuicergrinders/pr?sid=j9e%2Cm38%2C7ek&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&otracker=categorytree&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.power%255B%255D%3D751%2BW%2B-%2B1000%2BW&p%5B%5D=facets.power%255B%255D%3DMore%2Bthan%2B1000%2BW&p%5B%5D=facets.power%255B%255D%3D501%2BW%2B-%2B750%2BW&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D500'])
    arr.append(['cooktop_500.txt', 0, False, 'https://www.flipkart.com/induction-cooktops/pr?sid=j9e%2Cm38%2C575&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&otracker=categorytree&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D500'])
    arr.append(['chimney_4k.txt', 0, False, 'https://www.flipkart.com/chimney/pr?sid=j9e%2Cm38%2Ctgz&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&otracker=categorytree&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D4000'])
    arr.append(['coffee_500.txt', 0, False, 'https://www.flipkart.com/coffee-makers/pr?sid=j9e%2Cm38%2Cwqo&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&otracker=categorytree&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.type%255B%255D%3DEspresso%2BMachine&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D500'])
    arr.append(['dishwasher_5k.txt', 0, False, 'https://www.flipkart.com/dish-washers/~cs-wskz10kr87/pr?sid=j9e%2Cm38%2C58n&collection-tab-name=Best-selling+Dishwashers&otracker=clp_creative_card_3_7.creativeCard.CREATIVE_CARD_tvs-and-appliances-new-clp-store_TKJGHI4WKQ00&fm=neo%2Fmerchandising&iid=M_6fe5a0e2-092b-4a1e-b9dd-c81e6e052d52_7.TKJGHI4WKQ00&ppt=None&ppn=None&ssid=el91ac53bnrwk7pc1662909878394&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D5000'])
    arr.append(['vacc_2k.txt', 0, False, 'https://www.flipkart.com/vacuum-cleaners/~cs-3segusukeg/pr?sid=j9e%2Cabm%2Cul2&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D1500&otracker=categorytree&sort=price_asc'])
    #arr.append(['mixergrinder_1k.txt', 0, False,'https://www.flipkart.com/home-kitchen/kitchen-appliances/~cs-21526mrbpm/pr?sid=j9e%2Cm38&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&otracker=clp_creative_card_3_16.creativeCard.CREATIVE_CARD_tvs-and-appliances-new-clp-store_43H9YJS7JPEV&fm=neo%2Fmerchandising&iid=M_6fe5a0e2-092b-4a1e-b9dd-c81e6e052d52_16.43H9YJS7JPEV&ppt=None&ppn=None&ssid=el91ac53bnrwk7pc1662909878394&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1000'])
    arr.append(['oven_3k.txt', 0, False, 'https://www.flipkart.com/microwave-ovens/pr?sid=j9e%2Cm38%2Co49&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InZhbHVlQ2FsbG91dCI6eyJtdWx0aVZhbHVlZEF0dHJpYnV0ZSI6eyJrZXkiOiJ2YWx1ZUNhbGxvdXQiLCJpbmZlcmVuY2VUeXBlIjoiVkFMVUVfQ0FMTE9VVCIsInZhbHVlcyI6WyJGcm9tIOKCuTQsMDk5Il0sInZhbHVlVHlwZSI6Ik1VTFRJX1ZBTFVFRCJ9fSwidGl0bGUiOnsibXVsdGlWYWx1ZWRBdHRyaWJ1dGUiOnsia2V5IjoidGl0bGUiLCJpbmZlcmVuY2VUeXBlIjoiVElUTEUiLCJ2YWx1ZXMiOlsiVG9wIE1pY3Jvd2F2ZXMiXSwidmFsdWVUeXBlIjoiTVVMVElfVkFMVUVEIn19LCJoZXJvUGlkIjp7InNpbmdsZVZhbHVlQXR0cmlidXRlIjp7ImtleSI6Imhlcm9QaWQiLCJpbmZlcmVuY2VUeXBlIjoiUElEIiwidmFsdWUiOiJNUkNEV0s4VFRIVkhXM1dZIiwidmFsdWVUeXBlIjoiU0lOR0xFX1ZBTFVFRCJ9fX19fQ%3D%3D&fm=neo%2Fmerchandising&iid=M_6fe5a0e2-092b-4a1e-b9dd-c81e6e052d52_27.X0R7ZYLUG3TL&ppt=None&ppn=None&ssid=el91ac53bnrwk7pc1662909878394&otracker=clp_omu_Up%2Bto%2B75%2525%2BOff_3_27.dealCard.OMU_tvs-and-appliances-new-clp-store_tvs-and-appliances-new-clp-store_X0R7ZYLUG3TL_16&otracker1=clp_omu_PINNED_neo%2Fmerchandising_Up%2Bto%2B75%2525%2BOff_NA_dealCard_cc_3_NA_view-all_16&cid=X0R7ZYLUG3TL&sort=price_asc&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D3000'])
    arr.append(['bldcfan_1500.txt', 0, False, 'https://www.flipkart.com/fan/pr?sid=j9e%2Cabm%2Clbz&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&otracker=categorytree&sort=price_asc&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D2000&p[]=facets.theme%255B%255D%3DBLDC%2BTechnology'])
    arr.append(['powermixergrinder_1k.txt', 0, False, 'https://www.flipkart.com/home-kitchen/~cs-o5efjasver/pr?sid=j9e&collection-tab-name=750W+Mixer+Grinders&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&otracker=clp_bannerads_7_1.bannerAdCard.BANNERADS_m_tvs-and-appliances-new-clp-store_757MZV47UQOF&sort=price_asc&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1000'])
    arr.append(['tv_6k.txt', 0, False, 'https://www.flipkart.com/televisions/pr?sid=ckf%2Cczl&otracker=clp_bannerads_1_1.bannerAdCard.BANNERADS_ss_tvs-and-appliances-new-clp-store_3K6VLLQ2FM9T&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.resolution%255B%255D%3DFull%2BHD&p[]=facets.resolution%255B%255D%3DUltra%2BHD%2B%25284K%2529&p[]=facets.resolution%255B%255D%3DUltra%2BHD%2B%25288K%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D6000'])
    arr.append(['mixedappliance_500.txt', 0, False, 'https://www.flipkart.com/home-kitchen/~appliances-for-a-healthy-living/pr?sid=j9e&otracker=nmenu_sub_TVs+%26+Appliances_0_Healthy+Living+Appliances&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D500'])
    arr.append(['mattress_2k.txt', 0, False, 'https://www.flipkart.com/furniture/mattresses/~bedroom-furniture-/pr?sid=wwe%2Crg9&otracker=categorytree&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D2000'])
    arr.append(['bed_5k.txt', 0, False, 'https://www.flipkart.com/furniture/beds-more/~bedroom-furniture-/pr?sid=wwe%2C7p7&otracker=categorytree&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D5000'])
    arr.append(['furniture_1500.txt', 0, False, 'https://www.flipkart.com/furniture/~bedroom-furniture-/pr?sid=wwe&otracker=nmenu_sub_Home+%26+Furniture_0_Bed+Room+Furniture&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D1500'])
    arr.append(['livingroomfurniture_2k.txt', 0, False, 'https://www.flipkart.com/furniture/~living-room-furniture-/pr?sid=wwe&otracker=nmenu_sub_Home+%26+Furniture_0_Living+Room+Furniture&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D2000'])
    arr.append(['sofset_5k.txt', 0, False, 'https://www.flipkart.com/furniture/sofas/sofa-sets/pr?sid=wwe%2Cc3z%2Cr0c&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&otracker=categorytree&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D5000'])
    arr.append(['sofabed_1k.txt', 0, False, 'https://www.flipkart.com/furniture/sofa-beds-more/sofa-beds/pr?sid=wwe%2Cosg%2Citp&otracker=categorytree&sort=price_asc&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D5000&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529'])
    arr.append(['exercisebikes_1500.txt', 0, False, 'https://www.flipkart.com/exercise-fitness/fitness-equipment/exercise-bikes/pr?sid=qoc%2Camf%2Ceut&otracker=categorytree&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D1500'])
    arr.append(['treadmill_3k.txt', 0, False, 'https://www.flipkart.com/exercise-fitness/fitness-equipment/treadmills/pr?sid=qoc%2Camf%2Coyq&otracker=categorytree&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D3000'])
    arr.append(['crosstrainers_2k.txt', 0, False, 'https://www.flipkart.com/exercise-fitness/fitness-equipment/cross-trainers/pr?sid=qoc%2Camf%2Cgci&otracker=categorytree&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D2000'])
    arr.append(['helmet_200.txt', 0, False, 'https://www.flipkart.com/automotive-accessories/helmets-and-riding-gear/helmet-and-accessories/biker-helmets/vega~brand/pr?marketplace=FLIPKART&p%5B%5D=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&affid=harishank6&sort=price_asc&sid=1mt%2Cztf%2Civ8%2Ctih&pageUID=1608188325694&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.availability%255B%255D%3DInclude%2BOut%2Bof%2BStock&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D200'])
    arr.append(['compbooks_50.txt', 0, False, 'https://www.flipkart.com/books/higher-education-and-professional-books/computing-and-information-technology-books/pr?sid=bks%2Cf50%2Cksz&otracker=categorytree&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D50'])
    arr.append(['skates_200.txt', 0, False, 'https://www.flipkart.com/sports/skating/skates/pr?sid=abc%2Cmgq%2Crbi&otracker=categorytree&sort=price_asc&p[]=facets.discount_range_v1%255B%255D%3D70%2525%2Bor%2Bmore&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D200'])
    arr.append(['smarthome_100.txt', 0, False, 'https://www.flipkart.com/search?sid=igc&otracker=CLP_Filters&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&sort=price_asc&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D100'])
    arr.append(['securitycameras_150.txt', 0, False, 'https://www.flipkart.com/automation-robotics/surveillance-devices/security-cameras/pr?sid=igc%2Cj69%2Cagd&marketplace=FLIPKART&otracker=product_breadCrumbs_Security+Cameras&sort=price_asc&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D150'])
    arr.append(['kitchensink_500.txt', 0, False, 'https://www.flipkart.com/building-materials-and-supplies/bathroom-and-kitchen-fittings/kitchen-sinks/pr?sid=b8s%2Cecr%2Cd2r&otracker=categorytree&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D500'])
    arr.append(['faucetmixer_100.txt', 0, False, 'https://www.flipkart.com/building-materials-and-supplies/bathroom-and-kitchen-fittings/faucets/pr?sid=b8s%2Cecr%2Cxpl&otracker=categorytree&sort=price_asc&p[]=facets.discount_range_v1%255B%255D%3D70%2525%2Bor%2Bmore&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.material%255B%255D%3DStainless%2BSteel&p[]=facets.material%255B%255D%3DNickle&p[]=facets.material%255B%255D%3DBrass&p[]=facets.material%255B%255D%3DSteel&p[]=facets.material%255B%255D%3DZinc&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D100'])
    arr.append(['assembledpc_5k.txt', 0, False, 'https://www.flipkart.com/computers/desktop-pcs/all-in-one-pcs/pr?sid=6bo%2Cnl4%2Cigk&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&otracker=categorytree&sort=price_asc&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D5000'])
    arr.append(['cpu_3k.txt', 0, False, 'https://www.flipkart.com/computers/desktop-pcs/tower-pcs/pr?sid=6bo%2Cnl4%2Cdze&otracker=categorytree&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D3000'])
    arr.append(['monitor_2k.txt', 0, False, 'https://www.flipkart.com/search?sid=6bo%2Ftia%2F9no&otracker=CLP_Filters&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&sort=price_asc&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D2000'])
    arr.append(['printers_3k.txt', 0, False, 'https://www.flipkart.com/computers/computer-peripherals/printers-inks/printers/multi-function-printers/pr?sid=6bo%2Ctia%2Cffn%2Ct64%2Cmpr&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D3000&otracker=categorytree&sort=price_asc'])
    arr.append(['keyboard_200.txt', 0, False, 'https://www.flipkart.com/laptop-accessories/keyboards/pr?sid=6bo%2Cai3%2C3oe&marketplace=FLIPKART&otracker=product_breadCrumbs_Keyboards&sort=price_asc&p%5B%5D=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D200'])
    arr.append(['mouse_80.txt', 0, False, 'https://www.flipkart.com/laptop-accessories/mouse/pr?sid=6bo%2Cai3%2C2ay&otracker=categorytree&sort=price_asc&p[]=facets.discount_range_v1%255B%255D%3D50%2525%2Bor%2Bmore&p[]=facets.fulfilled_by%255B%255D%3DPlus%2B%2528FAssured%2529&p[]=facets.price_range.from%3DMin&p[]=facets.price_range.to%3D80'])

    if creation_time(foldername) < 1200:
        telegram = "off"
    else:
        telegram = "on"
    threads = []

    for i in arr:
        filename = foldername + i[0]
        force = i[1]
        notassured = i[2]
        url = i[3]
        process = Thread(target=flipkart_parse, args=[
                         filename, telegram, force, url, res_queue, notassured])
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
    # pcmemory()

    with open(foldername.strip("/") + '_output.txt', 'w+') as fall:
        res_queue.put(None)
        while True:
            item = res_queue.get()
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
        clear()
        dowork()
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())

    d = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    hour = d.hour
    if hour >= 3 and hour <= 7:
        sleep = random.randint(5, 10)
        print("----------------------- Sleeping for " +
              str(sleep) + " Seconds ------------------------")
        time.sleep(sleep)
    else:
        sleep = random.randint(2, 3)
        print("----------------------- Sleeping for " +
              str(sleep) + " Seconds ------------------------")
        time.sleep(sleep)
