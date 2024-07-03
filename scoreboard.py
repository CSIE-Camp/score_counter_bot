import requests
import time
import json
import os

url = os.getenv("WEBHOOK_URL")
while 1:
    try:
        # s = []
        # with open("data.json", newline="") as jsonfile:
        #     data = json.load(jsonfile)

        #     for i in data:
        #         for j in data[i]["members"]:
        #             s.append([data[i]["members"][j]["score"], data[i]["members"][j]["name"], i])
        #     s.sort(key=lambda x: x[0], reverse=True)

        # display_ = []

        # for i in range(min(10, len(s))):
        #     cn_number = "一二三四五六七八九十"
        #     display_.append({"name" :"第{}名".format(cn_number[i]) , "value" : "第{}組  {}\n 籌碼數量 : {}".format(cn_number[int(s[i][2]) - 1], s[i][1], s[i][0]),
        #                     "inline":True})


        # data["embeds"] = [
        #     {
        #         "description": "個人排名",
        #         "title": "個人排名",
        #         "color":0xfe7e06,
        #         "fields":display_
        #     }
        # ]

        # result = requests.post(url, json=data)

        # try:
        #     result.raise_for_status()
        # except requests.exceptions.HTTPError as err:
        #     print(err)
        # else:
        #     print("Payload delivered successfully, code {}.".format(result.status_code))

        s = []
        with open("data.json", newline="") as jsonfile:
            data = json.load(jsonfile)

            for i in data:
                s.append([data[i]["total"], i])
            s.sort(key=lambda x: x[0], reverse=True)

        display_ = []

        for i in range(min(10, len(s))):
            cn_number = "一二三四五六七八九十"
            display_.append({"name": "第{}名".format(cn_number[i]),
                            "value": "第{}組 \n 籌碼數量 : {}".format(cn_number[int(s[i][1]) - 1], s[i][0]),
                            "inline":True})

        data["embeds"] = [
            {
                "description": "小隊排名",
                "title": "小隊排名",
                "color": 0x0000CCFF,
                "fields": display_
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
    except Exception as e:
        print(e)
        time.sleep(30)