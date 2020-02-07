# -*- coding: utf-8 -*-

__author__='onefeng'

import random
from analysis import DataGet,DataAnalysis
from datasource.database import DataBase
from datasource.out import write_to_file
import time
import datetime
import configparser

cf = configparser.ConfigParser()
cf.read('_config.ini')
acount = dict((x, y) for x, y in cf.items('postgre-database'))
acount['port']=int(acount['port'])

class Master(object):

    def __init__(self):
        # 对象实例化
        self.sj = DataGet()
        self.jiexi=DataAnalysis()
        self.lj = DataBase(acount)

    # 建表
    def create_table(self, name):
        sqls='''
        create table {} (
            match_id int,
            league_id int,
            match_date varchar(50),
            starttime varchar(50),
            endtime varchar(50),
            league varchar(50),
            away varchar(50),
            home varchar(50),
            week varchar(50),
            score varchar(50),
            w_first_home_win float,
            w_first_stand_off float,
            w_first_guest_win float,
            j_first_home_win float,
            j_first_stand_off float,
            j_first_guest_win float,
            p_first_home_win float,
            p_first_stand_off float,
            p_first_guest_win float
        );
        '''.format(name)
        self.lj.nonquery(sqls)


    # 按日期获取数据
    def get_all_data(self,*dates):
        all_data={}
        for date in dates:
            # 请求每一天的数据
            source=self.sj.get_source(date,method='sport')
            try:
                datas=self.jiexi.sport_jiexi(source)
            except Exception as e:
                datas=[]
            print(date + ','+str(len(datas))+'场竞彩比赛')
            for data in datas:
                #请求竞彩的指数
                time.sleep(2*random.random())
                index_source=self.sj.get_source(data[0],method='index')

                #解析竞彩指数数据
                index_datas=self.jiexi.index_jiexi(index_source)
                # 请求赛事数据
                league_source = self.sj.get_source(data[0],method='league')
                league_data=self.jiexi.league_jiexi(league_source)
                all_data['match_id']=data[0]
                all_data['league_id']=data[1]
                all_data['match_date']=date
                all_data['starttime'] = data[3]
                all_data['endtime'] = data[4]
                all_data['league']=league_data.get('sub_league')
                all_data['away'] = data[5]
                all_data['home'] = data[6]
                all_data['week'] = data[-1]
                all_data['score'] = data[7]+'-'+data[8]
                all_data['w_first_home_win'] = index_datas.get('w_first_home_win')
                all_data['w_first_stand_off']=index_datas.get('w_first_stand_off')
                all_data['w_first_guest_win']=index_datas.get('w_first_guest_win')
                all_data['j_first_home_win']=index_datas.get('j_first_home_win')
                all_data['j_first_stand_off']=index_datas.get('j_first_stand_off')
                all_data['j_first_guest_win']=index_datas.get('j_first_guest_win')
                all_data['p_first_home_win']=index_datas.get('p_first_home_win')
                all_data['p_first_stand_off']=index_datas.get('p_first_stand_off')
                all_data['p_first_guest_win']=index_datas.get('p_first_guest_win')
                yield all_data
    # 返回时间列表
    def getdate(self, begin_date, end_date):
        date_list = []
        begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        return date_list

    def start(self):
        t1=cf.get("input", "start")
        t2=cf.get("input", "end")
        table=cf.get("input", "table_name")
        time_list=self.getdate(t1,t2)
        # 建表
        self.create_table(table)
        # 获取所有数据
        results=self.get_all_data(*time_list)
        for result in results:
            write_to_file(result)
            self.lj.insert_json(table, data=result)
import requests
class Spider(object):
    headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }

    def get_one_page(self,n,start='2014-01-01',end='2020-02-25'):
        url='http://www.lottery.gov.cn/football/result_{}.jspx?f_league_id=0&f_league_name=全部联赛&startDate={}&endDate={}'.format(n,start,end)
        response=requests.get(url,headers=self.headers)
        if response.status_code==200:
            return response.text
        return None

    def parse_one_page(self,html):
        pass
    def main(self):

        pass


if __name__ == '__main__':
    spider=Spider()
    d=spider.get_one_page(1)
    print(d)
    # master=Master()
    # master.start()



