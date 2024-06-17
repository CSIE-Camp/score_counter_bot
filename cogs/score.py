import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import json
from typing import Optional
import json
from adminRole import adminRoleName 

#TODO : show the score

# 身分組檢查
def roleCheck(role:str,usr:discord.Member):
    rol = usr.roles
    for i in rol:
        if i.name == role:
            return 1
    return 0

# JSON 處理
score_file = "personal_score.json"
team_score_file = "team_score.json"
async def allScoreRead():
    try:
        with open(score_file, 'r') as r:
            data = json.load(r)
            print(data)
    except:
        with open(score_file, "w") as w:
            w.write("{}")
        with open(score_file, 'r') as r:
            data = json.load(r)
    return data
async def allTeamScoreRead():
    try:
        with open(team_score_file, 'r') as r:
            data = json.load(r)
            print(data)
    except:
        with open(team_score_file, "w") as w:
            w.write("{}")
        with open(team_score_file, 'r') as r:
            data = json.load(r)
    return data

async def sortScore():
    data = await allScoreRead()
    data = dict(sorted(data.items(), key=lambda x: x[1]["personal score"], reverse=True))
    with open(score_file, "w") as w:
        json.dump(data, w)
    return 0

async def newStudent(team:int,name):
    all_data = await allScoreRead()
    if name in all_data:
        return 0
    else:
        all_data[name] = {}
        all_data[name]["team"] = team
        all_data[name]["personal score"] = 0
        with open(score_file, "w") as w:
            json.dump(all_data, w)
    return 1
async def newTeam(team:int):
    all_data = await allTeamScoreRead()
    if str(team) in all_data:
        return 0
    else:
        all_data[str(team)] = {}
        all_data[str(team)]["team score"] = 0
        with open(team_score_file, "w") as w:
            json.dump(all_data, w)
    return 1

async def personalScoreWrite(team:int, name, score:int):
    data = await allScoreRead()
    if await newStudent(team, name):
        data = await allScoreRead()
        data[name]["personal score"] = score
    else:
        data[name]["personal score"] += score
    with open(score_file, "w") as w:
        json.dump(data, w)
    await sortScore()
    return 0
async def teamScoreWrite(team, score):
    data = await allTeamScoreRead()
    if await newTeam(team):
        data = await allTeamScoreRead()
        data[str(team)]["team score"] = score
    else:
        data[str(team)]["team score"] += score
    with open(team_score_file, "w") as w:
        json.dump(data, w)
    personal_data = await allScoreRead()
    for i in personal_data:
        if personal_data[i]["team"] == team:
            personal_data[i]["personal score"] += score
    with open(score_file, "w") as w:
        json.dump(personal_data, w)
    await sortScore()
    return 0

class Score(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    # 斜線命令
    @app_commands.command(name = "score_add", description = "變動小隊員分數")
    @app_commands.describe(team_idx = "輸入數字", name = "輸入名字", score = "輸入分數")
    async def score_add(self, interaction: discord.Interaction, team_idx: int, name: str, score: int):
        if roleCheck(adminRoleName,interaction.user):
            await personalScoreWrite(team_idx, name, score)
            await interaction.response.send_message("done")
    # 斜線命令
    @app_commands.command(name = "team_score_add", description = "變動小隊分數")
    @app_commands.describe(team_idx = "輸入數字", score = "輸入分數")
    async def team_score_add(self, interaction: discord.Interaction, team_idx: int, score: int):
        if roleCheck(adminRoleName,interaction.user):
            await teamScoreWrite(team_idx, score)
            await interaction.response.send_message("done")
async def setup(bot: commands.Bot):
    await bot.add_cog(Score(bot))
