import requests
import pprint
from os import name
import xml.etree.ElementTree as et
import pandas as pd
import bs4
from lxml import html
from urllib.parse import urlencode, quote_plus, unquote

def dt_init(IATA) :
    # serviceKey
    encoding = 'CTJg8d36mDcNC6BODZJwwoo9LADNrQpJDyqlQr6fzaerKNWt%2FVTd8ZdEE4BqJzY5cNLgToIxqEUpbCcpKNfCqQ%3D%3D'
    decoding = 'CTJg8d36mDcNC6BODZJwwoo9LADNrQpJDyqlQr6fzaerKNWt/VTd8ZdEE4BqJzY5cNLgToIxqEUpbCcpKNfCqQ=='

    url = 'http://openapi.airport.co.kr/service/rest/AirportParking/airportparkingRT'
    params ={'serviceKey' : decoding, 'schAirportCode' : IATA }

    response = requests.get(url, params=params)
    content = response.text
    pp = pprint.PrettyPrinter(indent=4)
    xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
    rows = xml_obj.findAll('item')

    # 리스트 만들기
    row_list = []   # 행값
    name_list = []  # 열이름값
    value_list = [] # 데이터값

    # xml 데이터 수집
    for i in range(0, len(rows)):
        columns = rows[i].find_all()
        
        for j in range(0,len(columns)):
            if i ==0:
                name_list.append(columns[j].name)
            value_list.append(columns[j].text)

        row_list.append(value_list)
        value_list=[]

    air_df = pd.DataFrame(row_list, columns=name_list)

    if IATA == 'GMP' :
        return air_df.loc[1]
    else :
        return air_df.loc[0]


def airport_name(airport) :
    return airport[1]


def parking(airport) :
    return int(airport[3])-int(airport[8])


gimpo = dt_init('GMP')
gimhae = dt_init('PUS')
jeju = dt_init('CJU')
gwangju = dt_init('KWJ')

print('================================================================================')
print('          전국 공항 주차장 실시간 정보 안내 ({0} {1} 기준)'.format(gimpo[4], gimpo[5]))
print('================================================================================')

print(' 공항명 |     주차장명     | 전체 주차면 수 | 현재 주차된 차량수 | 잔여 주차면 수')
print(' %3s    %10s      %5s %15s  %14d' % (airport_name(gimpo)[0:2], gimpo[2], gimpo[3],gimpo[8], parking(gimpo)))
print(' %3s      %9s     %6s %15s   %13d' % (airport_name(gimhae)[0:2], gimhae[2], gimhae[3],gimhae[8], parking(gimhae)))
print(' %3s       %10s       %3s %15s      %10d' % (airport_name(jeju)[0:2], jeju[2], jeju[3],jeju[8], parking(jeju)))
print(' %3s     %11s     %5s %15s    %13d' % (airport_name(gwangju)[0:2], gwangju[2], gwangju[3],gwangju[8], parking(gwangju)))
