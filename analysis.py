# -*- coding: utf-8 -*-
__author__ = 'onefeng'
import re
import requests
import time
import hashlib
import json
'''构建请求类'''

class DataGet(object):

    def __init__(self):
        # 比赛url
        self.sport_url='https://dc.jihai8.com/match/result'
        # 指数url
        self.index_url='https://dc.jihai8.com/odds/getInfo'
        # 联赛url
        self.league_url='https://dc.jihai8.com/match/header'
        # 请求头
        self.headers={
            'User-Agent': 'okhttp/3.12.2'
        }
        self.PROXY_POOL_URL='http://106.13.201.232:5555/random'

    # 获取加密参数
    def cracked(self):
        # 创建MD5对象
        hl = hashlib.md5()
        # 盐值
        salt = '&key=f31s5884553FSBN%@&DFQ255a12'
        mytime = round(time.time() * 1000)
        src = 'client_time=' + str(mytime) + salt
        hl.update(src.encode("utf-8"))
        md5 = hl.hexdigest()[0:10]
        return mytime, md5

    # 获取代理
    def __get_proxy(self):
        try:
            response = requests.get(self.PROXY_POOL_URL)
            if response.status_code == 200:
                proxies = {
                    'http':'http://'+response.text,
                    'https':'https://'+response.text
                }
                return proxies
        except ConnectionError:
            return None

    def get_source(self, factor,method=None):
        #proxy=self.__get_proxy()
        # proxy = {
        #     'http': 'http://1.196.177.129:9999',
        #     'https': 'https://1.196.177.129:9999'
        # }
        mytime, md5 = self.cracked()
        sport_data = {
            'version': '294',
            'v': '294',
            'time_zone': 'GMT+08:00',
            'src': 'android_JH_001',
            'device': 'android',
            'date': factor,
            'company_id': '3',
            'client_time': mytime,
            'client_sign': md5,
            'channel': 'android_JH_001'
        }
        index_data = {
            'version': '294',
            'v': '294',
            'time_zone': 'GMT+08:00',
            'src': 'android_JH_001',
            'device': 'android',
            'id': factor,
            'client_time': mytime,
            'client_sign': md5,
            'channel': 'android_JH_001'
        }
        league_data = {
            'version': '294',
            'v': '294',
            'time_zone': 'GMT+08:00',
            'src': 'android_JH_001',
            'match_id': factor,
            'client_time': mytime,
            'client_sign': md5,
            'channel': 'android_JH_001'
        }
        #proxies=proxy
        try:
            if method=='sport':
                data = requests.post(url=self.sport_url,data=sport_data, headers=self.headers).text
            elif method=='index':
                data = requests.post(url=self.index_url, data=index_data, headers=self.headers).text
                data = json.loads(data)
            elif method=='league':
                data = requests.post(url=self.league_url,data=league_data, headers=self.headers).text
                data = json.loads(data)
            else:
                data=[]
        except Exception as e:
            data={}
        return data




'''构建解析类'''

class DataAnalysis(object):

    def __init__(self):
        self.w=re.compile(r'.*?周.\d{3}.*?', re.S)
    # 解析比赛数据
    def sport_jiexi(self, datas):

        # $$分隔
        x1 = datas.split('$$')
        # 获取比赛数据
        x2 = x1[1]
        ## ！分隔
        x3 = x2.split('!')
        ## 筛选星期(竞猜的数据)
        list1 = []
        for temp in x3:
            f = re.findall(self.w, temp)
            f1 = ''.join(f)
            if f1 != '':
                f2 = f1.split('^')
                list1.append(f2)

        return list1

    # 解析指数数据
    def index_jiexi(self, datas):
        index_data = {
            'w_first_home_win':None,
            'w_first_stand_off':None,
            'w_first_guest_win': None,
            'j_first_home_win': None,
            'j_first_stand_off': None,
            'j_first_guest_win': None,
            'p_first_home_win': None,
            'p_first_stand_off': None,
            'p_first_guest_win': None
        }
        # 获取欧赔数据
        try:
            standard = datas.get('data').get('standard')
            length = len(standard)
            p_first_home_win = 0
            p_first_stand_off = 0
            p_first_guest_win = 0
            for temp in standard:
                if temp.get('name_cn') == '威廉希尔':
                    index_data['w_first_home_win']=float(temp.get('first_home_win'))
                    index_data['w_first_stand_off']=float(temp.get('first_stand_off'))
                    index_data['w_first_guest_win']=float(temp.get('first_guest_win'))
                elif temp.get('name_cn') == '竞彩官方':
                    index_data['j_first_home_win'] = float(temp.get('first_home_win'))
                    index_data['j_first_stand_off'] = float(temp.get('first_stand_off'))
                    index_data['j_first_guest_win'] = float(temp.get('first_guest_win'))
                p_first_home_win = p_first_home_win + float(temp.get('first_home_win'))
                p_first_stand_off = p_first_stand_off + float(temp.get('first_stand_off'))
                p_first_guest_win = p_first_guest_win + float(temp.get('first_guest_win'))

            index_data['p_first_home_win']=p_first_home_win / length
            index_data['p_first_stand_off'] = p_first_stand_off / length
            index_data['p_first_guest_win'] = p_first_guest_win/ length
        except Exception as e:
            print('指数缺失')

        return index_data
    # 赛事数据解析

    def league_jiexi(self,datas):
        league_data = {
            'sub_league':None
        }
        league_data['sub_league'] = datas.get('data').get('sub_league')

        return league_data
if __name__ == '__main__':

    da = ['1725483', '1725484', '-1', '20200121030000', '20200121040400', '阿贾克斯青年队', '多德勒支', '2', '0', '0', '0', '0', '0',
          '0', '2', '4', '0', '4.5', '2.5', '0', '1', '2', '20', '', '0', '1', '周一001']
    sj=DataGet()
    da1=sj.get_index(da[0])
    #time.sleep(2*t)
    da2=sj.get_index(da[1])
    print(da1)
    print(da2)