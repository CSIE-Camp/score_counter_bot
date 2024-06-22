import json
import shutil


# JSON 處理
score_file = "data.json"

async def initScore():
    src = "sample.json"
    dst = score_file
    try:
        with open(dst, "r") as r:
            pass
    except FileNotFoundError:
        shutil.copyfile(src, dst)

async def allScoreRead():
    try:
        with open(score_file, "r") as r:
            return json.load(r)
    except FileNotFoundError:
        initScore()
        with open(score_file, "r") as r:
            return json.load(r)
        

async def newStudent(team, member_id):
    data = await allScoreRead()
    team_str = str(team)
    member_id_str = str(member_id)
    
    if member_id_str in data[team_str]["members"]:
        return False
    else:
        if "members" not in data[team_str]:
            data[team_str]["members"] = {}
        data[team_str]["members"][member_id_str] = {"score": 0, "name": f"member{member_id_str}"}
        with open(score_file, "w") as w:
            json.dump(data, w)
    return True


async def personalScoreWrite(team: int, member: int, score: int):
    # print(data)
    team_str = str(team)
    member_str = str(member)
    if await newStudent(team_str, member_str):
        print(member_str)
        data = await allScoreRead()
        data[team_str]["members"][member_str]["score"] += score
        data[team_str]["total"] += score
    else:
        data = await allScoreRead()
        data[team_str]["members"][member_str]["score"] += score
        data[team_str]["total"] += score
        # print(data[team_str]["members"][member]["score"])
    with open(score_file, "w") as w:
        json.dump(data, w)
    return 0

async def checkScore(team: int, member: int):
    data = await allScoreRead()
    team_str = str(team)
    member_str = str(member)
    print(data[team_str]["members"][member_str]["score"])
    return data[team_str]["members"][member_str]["score"]

async def initScore(value:int = 20):
    data = await allScoreRead()
    for i in data:
        data[i]["total"] = 0
        for j in data[i]["members"]:
            data[i]["members"][j]["score"] = value
            data[i]["total"] += value
    with open(score_file, "w") as w:
        json.dump(data, w)
    return 0