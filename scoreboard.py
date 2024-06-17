import requests
import time
import json

url = input()
while 1:

    s = []
    with open("data.json", newline="") as jsonfile:
        data = json.load(jsonfile)

        for i in data:
            for j in data[i]["members"]:
                s.append([data[i]["members"][j]["score"], data[i]["members"][j]["name"], i])
        s.sort(key=lambda x: x[0], reverse=True)

    display_ = []

    for i in range(min(10, len(s))):
        cn_number = "一二三四五六七八九十"
        display_.append({"name" :"第{}名".format(cn_number[i]) , "value" : "第{}組  {}\n 籌碼數量 : {}".format(cn_number[int(s[i][2]) - 1], s[i][1], s[i][0])})


    data["embeds"] = [
        {
            "description": "每30秒更新",
            "title": "賭場即時排名",
            "color":0xfe7e06,
            "fields":display_
        }
    ]

    result = requests.post(url, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

    time.sleep(30)