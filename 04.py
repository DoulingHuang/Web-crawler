import requests
import json
import re
from bs4 import BeautifulSoup
import sys
from datetime import datetime
import pandas as pd

keyword = '資料分析'
page = '1'
url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={}'.format(keyword)
data = {'page': str(page)}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}
res = requests.get(url, headers=headers, params=data)
bs = BeautifulSoup(res.text, 'html.parser')
test = [a['href'] for a in bs.findAll('a', {'class': 'js-job-link'})]
json_url = []
url_para = []
for t in test:
    pattern = re.compile('[0-9].*\?')
    para_find = pattern.findall(t)
    json_url.append('https://www.104.com.tw/job/ajax/content/' + para_find[0].split('/')[2].split('?')[0])
    url_para.append(para_find[0].split('/')[2].split('?')[0])
a = 0
COMPANY = [];
JOB = [];
JOB_CONTENT = [];
JOB_REQUIRE = [];
JOB_WELFARE = [];
JOB_CONTACT = [];
JOB_URL = []
data = []
for j, p in zip(json_url, url_para):
    referer = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Referer": "https://www.104.com.tw/job/" + p
    }
    enter_content = requests.get(j, headers=referer)
    json_data = json.loads(enter_content.text)
    # print(json_data)
    a += 1
    print(a)
    # 工作內容
    job_desciption = '工作內容:' + '\n' + json_data['data']['jobDetail']['jobDescription']
    # 職務類別
    job_category_str = '職務類別:'
    job_category = json_data['data']['jobDetail']['jobCategory']
    for j in job_category:
        job_category_str += j['description'] + '\t'
    # 工作待遇
    job_salary = '工作待遇: ' + json_data['data']['jobDetail']['salary']
    # 工作性質
    job_attr = json_data['data']['jobDetail']['jobType']
    if job_attr == 1:
        job_attr = '工作性質: 全職'
    elif job_attr == 2:
        job_attr = '工作性質: 兼職'
    # 上班地點
    job_loc = '上班地點: ' + json_data['data']['jobDetail']['addressRegion'] + json_data['data']['jobDetail'][
        'addressDetail']
    # 管理責任
    job_resp = '管理責任: ' + json_data['data']['jobDetail']['manageResp']
    # 出差外派
    job_btrip = '出差外派: ' + json_data['data']['jobDetail']['businessTrip']
    # 上班時段
    job_peri = '上班時段: ' + json_data['data']['jobDetail']['workPeriod']
    # 休假制度
    job_vac = '休假制度: ' + json_data['data']['jobDetail']['vacationPolicy']
    # 可上班日
    job_star = '可上班日: ' + json_data['data']['jobDetail']['startWorkingDay']
    # 需求人數
    job_need = '需求人數: ' + json_data['data']['jobDetail']['needEmp']
    # 完整工作內容
    full_content = job_desciption + \
                   '\n' + job_category_str + '\n' + job_salary + '\n' + job_attr + '\n' + job_loc + '\n' + \
                   job_resp + '\n' + job_btrip + '\n' + job_peri + '\n' + job_vac + '\n' + job_star + '\n' + job_need
    # print(full_content)
    # 接受身分
    require_role = '接受身分: ' + json_data['data']['condition']['acceptRole']['role'][0]['description']
    # 工作經歷
    require_workExp = '工作經歷: ' + json_data['data']['condition']['workExp']
    # 學歷要求
    require_edu = '學歷要求: ' + json_data['data']['condition']['edu']
    # 科系要求
    require_maj = '科系要求: ' + '、'.join(json_data['data']['condition']['major'])
    # 語文條件
    try:
        require_lan = '語文條件: ' + json_data['data']['condition']['language'][0]['language'] + \
                      json_data['data']['condition']['language'][0]['ability']
    except IndexError:
        require_lan = '語文條件: 不拘'
    # 擅長工具
    try:
        require_specialty = '擅長工具: ' + str(json_data['data']['condition']['specialty'][0]['description'])
    except IndexError:
        require_specialty = '擅長工具: 不拘'
    # 工作技能
    try:
        require_skill = '工作技能: ' + str(json_data['data']['condition']['skill'][0]['description'])
    except IndexError:
        require_skill = '工作技能: 不拘'
    # 其他條件
    require_other = '其他條件: ' + json_data['data']['condition']['other']
    # 福利制度
    welfare = '福利制度: ' + json_data['data']['welfare']['welfare']
    # 聯絡方式
    contact = '聯絡方式: ' + json_data['data']['contact']['hrName'] + '\n' + json_data['data']['contact'][
        'email'] + '\n' + json_data['data']['contact']['phone']
    full_require = require_role + '\n' + require_workExp + '\n' + require_edu + '\n' + require_maj + '\n' + require_lan + '\n' + \
                   require_specialty + '\n' + require_skill + '\n' + require_other
    # print(full_require)

    data_row1 = full_content
    data_row2 = full_require
    data_row = data_row1 + data_row2

    print(data_row)
    data.append(data_row)
    print(data)
    print('=============================')
