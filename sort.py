import json

def score_sort():
    s = []
    with open("data.json", newline="") as jsonfile:
        data = json.load(jsonfile)

        for i in data:
            for j in data[i]["members"]:
                s.append([data[i]["members"][j]["score"], data[i]["members"][j]["name"], i])
        s.sort(key=lambda x: x[0], reverse=True)
    return s