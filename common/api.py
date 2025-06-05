import pandas as pd
import numpy as np
import requests
import time
import datetime
import json


def re_getaccesstoken():

    url = 'https://www.yunzhijia.com/gateway/oauth2/token/getAccessToken'


    headers = {
        "Content-Type": "application/json"
    }
    unix = int(time.time() * 1000)
    resGroupSecret_data =  {
                        "eid": "13410137",
                        "secret": "IPGx7HUPuFbQk1gEGeapszRqz7Dbgx1z",
                        "timestamp": unix,
                        "scope": "resGroupSecret"
                    }
    resGroupSecret_response = requests.post(url, data=json.dumps(resGroupSecret_data), headers=headers)
    return resGroupSecret_response


def getall_data(access_token):
    access_token = access_token.json()['data']['accessToken']
    url = f"https://www.yunzhijia.com/gateway/openimport/open/person/getall?accessToken={access_token}"
    
    data_param = json.dumps({"eid": "13410137","begin": 0,"count": 1000})

    post_data = {
        "eid": "13410137",
        "nonce":"11",
        "data": data_param
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=post_data, headers=headers)

    birthday = response.json()

    current_month = datetime.datetime.now().month
    # current_month = 10
    birthday_data = pd.DataFrame(birthday['data'])[["birthday","name"]]
    birthday_data['birthday'] = pd.to_datetime(birthday_data['birthday'])
    birthday_data = birthday_data.query("birthday.dt.month==@current_month")

    result = birthday_data['name'].apply(lambda x: {"name": x}).tolist()
    return result


def get_current_quarter_timestamps():
    now = datetime.datetime.now()
    year = now.year
    month = now.month

    # 确定当前季度的开始月份
    if month in (1, 2, 3):
        start_month = 1
    elif month in (4, 5, 6):
        start_month = 4
    elif month in (7, 8, 9):
        start_month = 7
    else:
        start_month = 10

    # 计算季度的开始时间
    quarter_start = datetime.datetime(year, start_month, 1, 0, 0, 0)

    # 计算季度的结束时间
    if start_month == 10:
        quarter_end = datetime.datetime(year + 1, 1, 1, 0, 0, 0) - datetime.timedelta(milliseconds=1)
    else:
        quarter_end = datetime.datetime(year, start_month + 3, 1, 0, 0, 0) - datetime.timedelta(milliseconds=1)

    # 转换为毫秒时间戳
    start_timestamp = int(quarter_start.timestamp() * 1000)
    end_timestamp = int(quarter_end.timestamp() * 1000)

    return start_timestamp, end_timestamp




# 获取team级别token
def team_getaccesstoken():
    headers = {
    "Content-Type": "application/json"
    }
    url = 'https://www.yunzhijia.com/gateway/oauth2/token/getAccessToken'
    
    unix = int(time.time() * 1000)

    team_data = {'appId': 'SP13410137',
             'eid': '13410137',
             'secret': 'T2iFaqJkwdafR4ri3257x2WJ7VRBgU',
             'timestamp': unix,
             'scope': 'team'
            }
    team_response = requests.post(url, data=json.dumps(team_data), headers=headers)
    return team_response


# 获取审批流程列表
def process_lis_performance(start_ts,end_ts,team_response):
    headers = {
    "Content-Type": "application/json"
    }
    url = 'https://www.yunzhijia.com/gateway/workflow/form/thirdpart/findFlows?accessToken={}' # 流程列表list
    list_data = {
                        "pageSize": 500,
                        "title": "绩效考核通知单",
                        "formCodeIds": ['5cc8a7b5390e4660aed95dd9684e0497'],
                        "createTime": [start_ts,end_ts]
                        }
    
    process_lis_response = requests.post(url.format(team_response.json()['data']['accessToken']), data=json.dumps(list_data), headers=headers)
    return process_lis_response

# 获取单据实例信息中部门副总人以及分管副总
def examples_performance(formInstId,team_response):
    headers = {
    "Content-Type": "application/json"
    }
    url = 'https://www.yunzhijia.com/gateway/workflow/form/thirdpart/viewFormInst?accessToken={}' # 表单实例
    Examples_data = {
                        "formInstId":formInstId,
                        "formCodeId":"5cc8a7b5390e4660aed95dd9684e0497"
                        }
    Examples_response = requests.post(url.format(team_response.json()['data']['accessToken']), data=json.dumps(Examples_data), headers=headers)
    try:
        vice_manager_name = Examples_response.json()['data']['formInfo']['widgetMap']['Ps_2']['personInfo'][0]['name']
        manager_name = Examples_response.json()['data']['formInfo']['widgetMap']['Ps_1']['personInfo'][0]['name']
    except:
        vice_manager_name = ""
        manager_name = ""
    return manager_name, vice_manager_name


# 获取审批流程列表
def process_lis_award(start_ts,end_ts,team_response):
    headers = {
    "Content-Type": "application/json"
    }
    url = 'https://www.yunzhijia.com/gateway/workflow/form/thirdpart/findFlows?accessToken={}' # 流程列表list
    list_data = {
                        "pageSize": 500,
                        "title": "奖励申请",
                        "formCodeIds": ['2fe4736c4f4042569da1f415a1c537d9'],
                        "createTime": [start_ts,end_ts]
                        }
    
    process_lis_response = requests.post(url.format(team_response.json()['data']['accessToken']), data=json.dumps(list_data), headers=headers)
    return process_lis_response

# 获取表彰奖励实例单据的人员信息
def examples_award(formInstId,team_response):
    headers = {
    "Content-Type": "application/json"
    }
    url = 'https://www.yunzhijia.com/gateway/workflow/form/thirdpart/viewFormInst?accessToken={}' # 表单实例
    Examples_data = {
                        "formInstId":formInstId,
                        "formCodeId":"5cc8a7b5390e4660aed95dd9684e0497"
                        }
    data = requests.post(url.format(team_response.json()['data']['accessToken']), data=json.dumps(Examples_data), headers=headers).json()
    
    try:
        person_info = data["data"]["formInfo"]["widgetMap"]["Ps_0"].get("personInfo", [])
        if person_info:
            name = person_info[0]["name"]
        else:
            dept_info = data["data"]["formInfo"]["widgetMap"]["Ds_0"].get("deptInfo", [])
            name = dept_info[0]["name"] if dept_info else ""
        
        # 申请奖励项目
        ra1_value = data["data"]["formInfo"]["widgetMap"]["Ra_1"].get("value", "")
        options = data["data"]["formInfo"]["widgetMap"]["Ra_1"].get("options", [])
        project = ""
        for option in options:
            if option.get("key") == ra1_value:
                project = option.get("value", "")
                break
        
        # 奖励金额（为空返回0）
        reward = data["data"]["formInfo"]["widgetMap"]["Nu_0"].get("value", "")
        reward = reward if reward else "0"

    except:
        name = ""
        project = ""
        reward = ""
        
    return name,project,reward
    
