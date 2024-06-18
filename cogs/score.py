import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import json
from typing import Optional
from adminRole import adminRoleName 
from sort import score_sort
import os
import shutil

# 身分組檢查
def roleCheck(role: str, usr: discord.Member):
    rol = usr.roles
    for i in rol:
        if i.name == role:
            return 1
    return 0

# JSON 處理
score_file = "personal_score.json"
team_score_file = "team_score.json"

def initScore():
    src = "sample.json"
    dst = "personal_score.json"
    if os.path.exists(dst):
        os.remove(dst)
    shutil.copyfile(src, dst)

async def addScore():
    if not os.path.isfile(score_file):
        await initScore()

async def allScoreRead():
    if not os.path.isfile(score_file):
        await initScore()
    with open(score_file, "r") as r:
        return json.load(r)

async def allTeamScoreRead():
    if not os.path.isfile(team_score_file):
        with open(team_score_file, "w") as w:
            json.dump({}, w)
    with open(team_score_file, "r") as r:
        return json.load(r)

async def newStudent(team, member_id):
    data = await allScoreRead()
    team_str = str(team)
    # member_id_str = str(member_id)
    
    if member_id in data[team_str]["members"]:
        return 0
    else:
        if "members" not in data[team_str]:
            data[team_str]["members"] = {}
        data[team_str]["members"][member_id] = {"score": 0, "name": f"member{member_id}"}
        with open(score_file, "w") as w:
            json.dump(data, w)
    return 1

async def newTeam(team):
    data = await allTeamScoreRead()
    team_str = str(team)
    
    if team_str in data:
        return 0
    else:
        data[team_str] = {"members": {}, "total": 0}
        with open(team_score_file, "w") as w:
            json.dump(data, w)
    return 1
    
async def sortScore():
    data = await allScoreRead()
    sorted_data = {}
    for team, details in data.items():
        members = details["members"]
        sorted_members = dict(sorted(members.items(), key=lambda x: x[1]["score"], reverse=True))
        sorted_data[team] = {"members": sorted_members, "total": details["total"]}
    with open(score_file, "w") as w:
        json.dump(sorted_data, w)
    return 0

async def personalScoreWrite(team: int, member: str, score: int):
    await addScore()
    data = await allScoreRead()
    # print(data)
    team_str = str(team)
    if await newStudent(team_str, member):
        print(member)
        data = await allScoreRead()
        data[team_str]["members"][member] = {"score": score, "name": f"member{member}"}
    else:
        data[team_str]["members"][member]["score"] += score
        # print(data[team_str]["members"][member]["score"])
    
    with open(score_file, "w") as w:
        json.dump(data, w)
    
    await sortScore()
    return 0

async def teamScoreWrite(team: int, score: int):
    data = await allScoreRead()
    team_str = str(team)
    
    if await newTeam(team_str):
        data[team_str] = {"total": score, "members": {}}
    else:
        data[team_str]["total"] += score
    
    for member_id in data[team_str]["members"]:
        data[team_str]["members"][member_id]["score"] += score
    
    with open(score_file, "w") as w:
        json.dump(data, w)
    
    await sortScore()
    return 0

class Score(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        initScore()

    @app_commands.command(name="score_add", description="變動小隊員分數")
    @app_commands.describe(team_idx="輸入數字", name="輸入名字", score="輸入分數")
    async def score_add(self, interaction: discord.Interaction, team_idx: int, name: str, score: int):
        if roleCheck(adminRoleName, interaction.user):
            await personalScoreWrite(team_idx, name, score)
            await interaction.response.send_message("done")
            

    @app_commands.command(name="team_score_add", description="變動小隊分數")
    @app_commands.describe(team_idx="輸入數字", score="輸入分數")
    async def team_score_add(self, interaction: discord.Interaction, team_idx: int, score: int):
        if roleCheck(adminRoleName, interaction.user):
            await teamScoreWrite(team_idx, score)
            await interaction.response.send_message("done")

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if "custom_id" in interaction.data:
            if interaction.data["custom_id"] == "get_score":
                score_embed = discord.Embed(title="賭場分數")
                user_name = interaction.user.nick
                if user_name is None:
                    user_name = interaction.user.global_name
                score_embed.set_author(name=user_name, icon_url=interaction.user.avatar.url, url="https://discord.com")
                point = 0
                rank = 0
                usr_check = 0
                for i in score_sort():
                    rank += 1
                    if i[1] == user_name:
                        point = i[0]
                        usr_check = 1
                        break
                    
                if usr_check == 1:
                    await interaction.response.defer()
                    score_embed.add_field(name="點數", value=point, inline=True)
                    score_embed.add_field(name="排名", value=rank, inline=True)
                    await interaction.followup.send(embed=score_embed, ephemeral=True)
                else:
                    await interaction.response.send_message("是否暱稱與姓名不同？", ephemeral=True)

    @app_commands.command(name="show_my_score", description="顯示個人排名")
    async def button_interaction_on(self, interaction: discord.Interaction):
        view = discord.ui.View()
        button = discord.ui.Button(
            label="點我查看分數",
            style=discord.ButtonStyle.blurple,
            custom_id="get_score"
        )
        view.add_item(button)
        await interaction.response.send_message(view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Score(bot))