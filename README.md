# 即嗨app比赛数据抓取

## 数据储存格式

| 字段名称         | 中文名称  | 类型      | 备注 |
|--------------|-------|---------|----|
| match\_id    | 比赛编号  | int     | 主键 |
| league\_id | 赛事编号  | int     |
| match_date         | 日期    | varchar |
| starttime        | 开始时间  | varchar |
| endtime          | 结束时间  | varchar |
| league         | 赛事  | varchar |
| away         | 主队    | varchar |
| home         | 客队    | varchar |
| week         | 星期序号   | varchar |
| score        | 比分    | varchar |
| w_first_home_win   | 胜\-威廉 | float   |
| w_first_stand_off      | 平\-威廉 | float   |
| w_first_guest_win    | 负\-威廉 | float   |
| j_first_home_win   | 胜\-官  | float   |
| j_first_stand_off    | 平\-官  | float   |
| j_first_guest_win    | 负\-官  | float   |
| j_first_home_win  | 胜\-均  | float   |
| j_first_stand_off     | 平\-均  | float   |
| j_first_guest_win    | 负\-均  | float   |


## 开发环境及工具

- linux+python+postgresql
- 抓包分析工具:fildder
- Android逆向开发工具，用于获取加密方式
- ip池的搭建

## 抓取流程

1. 抓包分析

参数有加密方式为MD5

2. 数据解析

正则，json

3. 数据储存

用关系型数据库postgresql

## 程序结构
