# -*- coding: UTF-8 -*-
import requests
import re
from selenium import webdriver
import os
import time


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print(r.status_code)
        # //print(r.text)
        return r.text
    except:
        return "fail to get html"


def getCarId(ist, html):
    # print(1)
    f = open('f:\\67.txt', 'w', encoding='utf-8')
    f.write(html)
    f.close()
    tlt = re.findall(r'\"/buy/detail/.*?\"', html)
    print(len(tlt))
    for i in range(len(tlt)):
        ist.append(tlt[i].strip('"'))
    # print(ist)


# 所有车辆的图片均以车辆id+图片名的形式存放在carImage文件夹中，车型亮点的图片均以车辆id+图片名的形式存放在carLiangDian文件夹中，这个函数
# 中我们只拿到图片的链接，保存使用另一个函数


def save_car_image(path, ist, carId):
    try:
        for i in range(len(ist)):
            real_path = path + str(carId) + ist[i].split('/')[-1]
            if not os.path.exists(real_path):
                r = requests.get(ist[i])
                with open(real_path, 'wb') as f:
                    f.write(r.content)
                    f.close()
            else:
                print("file alread exist")
    except:
        print("save_car_image")


def getCarInfo( html, car_id):
    car_name2 = ''
    car_price = ''
    car_structure = ''
    car_changkuangao = ''
    car_engineer = ''
    car_biansuxiang = ''
    car_qudongfangshi = ''
    car_ranyouxingshi = ''
    car_zhongheyouhao = ''
    car_cheliangcolor = ''
    # try:
    f = open('f:\\car\\y.txt', 'a', encoding='utf-8')
    tlt1 = re.findall(r'<div class="title fs20">.*?<', html)
    car_name = tlt1[0].split('<')
    car_name1 = car_name[1].split('>')
    car_name2 = car_name1[1].strip()
    tlt2 = re.findall(r' 厂商指导价：.*?万', html)
    car_price = tlt2[0].split('：')[1].strip('万')
    tlt3 = re.findall(r'车身结构</div> <div.*?<', html)
    car_structure = tlt3[0].split('<')[2].split('>')[1]
    tlt4 = re.findall(r'高.*?mm<', html)
    car_changkuangao = tlt4[0].split('<')[2].split('>')[1]
    tlt5 = re.findall(r'发动机.*?变速箱', html)
    car_engineer = tlt5[0].split('<')[2].split('>')[1]
    tlt6 = re.findall(r'变速箱.*?驱动方式', html)
    car_biansuxiang = tlt6[0].split('<')[2].split('>')[1]
    # print(tlt)
    tlt7 = re.findall(r'驱动方式.*?燃料形式', html)
    car_qudongfangshi = tlt7[0].split('<')[2].split('>')[1]
    tlt8 = re.findall(r'燃料形式.*?综合油耗', html)
    car_ranyouxingshi = tlt8[0].split('<')[2].split('>')[1]
    tlt9 = re.findall(r'综合油耗.*?车辆配色', html)
    car_zhongheyouhao = tlt9[0].split('<')[2].split('>')[1]
    tlt10 = re.findall(r'车辆配色.*?<img', html)
    car_cheliangcolor = tlt10[0].split('<')[2].split('>')[1]
    car_all_image = re.findall(r'<img data-src="https://img.souche.com/model-material.*?\.jpg', html)
    car_liangdian_picture_origin = re.findall(r'<img src="//img.souche.com/.*?.jpg" width="100%', html)
    car_liangdian_info = re.findall('<div class="info-text fs16">.*?<', html, re.S)
    tlt13 = re.findall('https://img.souche.com/.*?/jpg/.*?.jpg', html)
    car_liangdian_picture = []
    car_liangdian_text = []
    # 车型亮点图片链接获取
    for i in car_liangdian_picture_origin:
        tempStr = 'http:' + i.split('"')[1]
        car_liangdian_picture.append(tempStr)
    # 车型两点对应文字获取
    for i in car_liangdian_info:
        tempStr = i.split('<')[1].split('>')[1].strip("'")
        car_liangdian_text.append(tempStr)
    car_text = '&'.join(car_liangdian_text)
    car_clear_image = []
    # 车辆图片对应连接获取
    for i in car_all_image:
        tempStr = i.split('"')[1]
        car_clear_image.append(tempStr)
    if len(tlt13)==1:
        car_biaoti_picture = [tlt13[0]]
    else:
        car_biaoti_picture = [tlt13[2]]
    car_picture_path = "f://car//car_image//"
    car_biaoti_path = "f://car//car_biaoti//"
    car_liangdian_path = "f://car//car_liangdian//"
    array = [
        car_id,
        car_name2, car_price, car_structure, car_changkuangao,
        car_engineer, car_biansuxiang, car_qudongfangshi,
        car_ranyouxingshi, car_zhongheyouhao, car_cheliangcolor,
        car_liangdian_path, car_picture_path, car_biaoti_path
    ]
    carInfo = ','.join(array)
    save_car_image(car_picture_path, car_clear_image, car_id)
    save_car_image(car_biaoti_path, car_biaoti_picture, car_id)
    save_car_image(car_liangdian_path, car_liangdian_picture, car_id)
    f.write(car_text)
    f.close()
    return carInfo

    # except:
    #     print("youcuowu")
    # car_all_image.pop(0)
    # car_all_image.pop(1)
    # car_liangdian_picture = re.findall('', html)


def main():
    # start_url = 'https://www.tangeche.com/buy?orderBy=&prepaidAmount=&prepaidAmountName=&newPrice=&newPriceName=&brandCode=&brandCodeName=&carShapeCode=&carShapeCodeName=&installment=&installmentName=&page=1&pageSize=215&keyWord=&cityCode=&cityName=&provinceCode=&provinceName='
    # path = 'f:\\car\\cheliangxinxi.txt'
    f = open('f:\\car\\cheliangxinxi.txt', 'w', encoding='utf-8')
    # p = open('f:\\1.txt', 'r', encoding='utf-8')
    carId = []
    # getCarId(carId, str1)
    # browser = webdriver.PhantomJS()  # 使用phantomjs浏览器
    browser = webdriver.Chrome()  # 使用phantomjs浏览器
    car_detail_url = 'https://www.tangeche.com'
    # browser.get(start_url)
    # html = browser.find_element_by_xpath().get_attribute('outerHTML')
    # p.write(html)
    # print(html[100:500])
    # getCarId(carId, html)
    # time.sleep(10)
    # print(carId)
    f.write('fuck')
    carId = [
        "/buy/detail/226759", "/buy/detail/15106-n", "/buy/detail/209614", "/buy/detail/5783-n", "/buy/detail/211059", "/buy/detail/202133", "/buy/detail/11233-n", "/buy/detail/14341-n", "/buy/detail/203067", "/buy/detail/202281", "/buy/detail/10781-n", "/buy/detail/14704-n", "/buy/detail/200707", "/buy/detail/1547451", "/buy/detail/6712-n", "/buy/detail/202352", "/buy/detail/202213", "/buy/detail/200664", "/buy/detail/14317-n", "/buy/detail/14475-n", "/buy/detail/203986", "/buy/detail/14477-n", "/buy/detail/12788-n", "/buy/detail/211570", "/buy/detail/203274", "/buy/detail/203063", "/buy/detail/204752", "/buy/detail/226800", "/buy/detail/203991", "/buy/detail/202969", "/buy/detail/202975", "/buy/detail/227052", "/buy/detail/204837", "/buy/detail/14394-n", "/buy/detail/202383", "/buy/detail/227250", "/buy/detail/227249", "/buy/detail/226934", "/buy/detail/211122", "/buy/detail/211435", "/buy/detail/211438", "/buy/detail/209677", "/buy/detail/13932-n", "/buy/detail/203439", "/buy/detail/210083", "/buy/detail/210866", "/buy/detail/201339", "/buy/detail/201336", "/buy/detail/201341", "/buy/detail/203877", "/buy/detail/203879", "/buy/detail/14880-n", "/buy/detail/210572", "/buy/detail/14601-n", "/buy/detail/210978", "/buy/detail/210979", "/buy/detail/204106", "/buy/detail/201542", "/buy/detail/210430", "/buy/detail/210431", "/buy/detail/226807", "/buy/detail/226806", "/buy/detail/226749", "/buy/detail/13821-n", "/buy/detail/209849", "/buy/detail/201789", "/buy/detail/15117-n", "/buy/detail/203076", "/buy/detail/203070", "/buy/detail/203078", "/buy/detail/203875", "/buy/detail/203876", "/buy/detail/12610-n", "/buy/detail/14238-n", "/buy/detail/204491", "/buy/detail/211341", "/buy/detail/202009", "/buy/detail/13852-n", "/buy/detail/202437", "/buy/detail/204361", "/buy/detail/11087-n", "/buy/detail/202783", "/buy/detail/203210", "/buy/detail/204785", "/buy/detail/203237", "/buy/detail/202014", "/buy/detail/203448", "/buy/detail/203446", "/buy/detail/209779", "/buy/detail/209895", "/buy/detail/209894", "/buy/detail/211033", "/buy/detail/210950", "/buy/detail/204404", "/buy/detail/200919", "/buy/detail/201371", "/buy/detail/14849-n", "/buy/detail/12208-n", "/buy/detail/201100", "/buy/detail/211442", "/buy/detail/211294", "/buy/detail/210260", "/buy/detail/202394", "/buy/detail/202391", "/buy/detail/14117-n", "/buy/detail/211303", "/buy/detail/203057", "/buy/detail/203059", "/buy/detail/202915", "/buy/detail/14511-n", "/buy/detail/202826", "/buy/detail/202951", "/buy/detail/211064", "/buy/detail/12328-n", "/buy/detail/203564", "/buy/detail/210487", "/buy/detail/14659-n", "/buy/detail/202379", "/buy/detail/202280", "/buy/detail/202935", "/buy/detail/211003", "/buy/detail/203818", "/buy/detail/211000", "/buy/detail/203511", "/buy/detail/203680", "/buy/detail/203303", "/buy/detail/209486", "/buy/detail/202271", "/buy/detail/209622", "/buy/detail/209606", "/buy/detail/203452", "/buy/detail/14620-n", "/buy/detail/201878", "/buy/detail/210319", "/buy/detail/10973-n", "/buy/detail/203362", "/buy/detail/209650", "/buy/detail/14979-n", "/buy/detail/202370", "/buy/detail/204346", "/buy/detail/13740-n", "/buy/detail/204477", "/buy/detail/14327-n", "/buy/detail/13661-n", "/buy/detail/14388-n", "/buy/detail/15165-n", "/buy/detail/209611", "/buy/detail/204771", "/buy/detail/202053", "/buy/detail/14941-n", "/buy/detail/12660-n", "/buy/detail/14595-n", "/buy/detail/203352", "/buy/detail/203409", "/buy/detail/203837", "/buy/detail/204028", "/buy/detail/204029", "/buy/detail/14914-n", "/buy/detail/203558", "/buy/detail/203203", "/buy/detail/200873", "/buy/detail/14754-n", "/buy/detail/12654-n", "/buy/detail/14963-n", "/buy/detail/203142", "/buy/detail/203141", "/buy/detail/200795", "/buy/detail/14377-n", "/buy/detail/12262-n", "/buy/detail/204019", "/buy/detail/11389-n", "/buy/detail/203816", "/buy/detail/201476", "/buy/detail/202092", "/buy/detail/202059", "/buy/detail/203143", "/buy/detail/203103", "/buy/detail/14192-n", "/buy/detail/11882-n", "/buy/detail/200634", "/buy/detail/10948-n", "/buy/detail/11006-n", "/buy/detail/12391-n", "/buy/detail/201292", "/buy/detail/203122", "/buy/detail/203121", "/buy/detail/12783-n", "/buy/detail/202909", "/buy/detail/202884", "/buy/detail/202865", "/buy/detail/202697", "/buy/detail/200961", "/buy/detail/202320", "/buy/detail/11615-n", "/buy/detail/11086-n", "/buy/detail/12213-n", "/buy/detail/15077-n", "/buy/detail/9026-n", "/buy/detail/11953-n", "/buy/detail/210282", "/buy/detail/200893", "/buy/detail/9514-n", "/buy/detail/211663", "/buy/detail/210890", "/buy/detail/12619-n", "/buy/detail/204105", "/buy/detail/12094-n", "/buy/detail/211115", "/buy/detail/202698", "/buy/detail/208506", "/buy/detail/11841-n", "/buy/detail/203866", "/buy/detail/14746-n", "/buy/detail/201379", "/buy/detail/10212-n"
    ]
    print(len(carId))
    car_info = ''
    for i in range(len(carId)):
        car_True_detail = car_detail_url + carId[i]
        browser.get(car_True_detail)
        car_html = browser.page_source
        car_info = getCarInfo(car_html, carId[i].split('/')[-1])
        # print()
        print(car_info)
        f.write(car_info + '\n')
        print('woqunidayede' + car_info)
    f.close()


main()
