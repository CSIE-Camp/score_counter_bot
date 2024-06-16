import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import json
from typing import Optional
import json
import os

#TODO : start the score system

score_file = "../personal_score.json"
async def all_score_read():
        if(score_file not in os.listdir()):
            with open(score_file, "w") as w:
                w.write("{}")
        with open(score_file, 'r') as r:
            data = json.load(r)
        return data
async def sort_score():
    data = await all_score_read()
    data = dict(sorted(data.items(), key=lambda x: x[1]["personal score"], reverse=True))
    with open(score_file, "w") as w:
        json.dump(data, w)
    return 0

async def new_student(team:int,name):
    all_data = await all_score_read()
    if name in all_data:
        return 0
    else:
        all_data[name] = {}
        all_data[name]["team"] = team
        all_data[name]["personal score"] = 0
        with open(score_file, "w") as w:
            json.dump(all_data, w)
    return 1

async def personal_score_write(team:int, name, score:int):
    data = await all_score_read()
    if await new_student(team, name):
        data = await all_score_read()
        data[name]["personal score"] = score
    else:
        data[name]["personal score"] += score
    with open(score_file, "w") as w:
        json.dump(data, w)
    await sort_score()
    return 0
async def team_score_write(team, score):
    data = await all_score_read()
    data[team]["team score"] += score
    with open("../team_score.json", "w") as w:
        json.dump(data, w)
    return 0

class Score(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(name = "score_add", description = "變動小隊員分數")
    @app_commands.describe(team_idx = "輸入數字", name = "輸入名字", score = "輸入分數")
    async def add(self, interaction: discord.Interaction, team_idx: int, name: str, score: int):
        await personal_score_write(team_idx, name, score)
        await interaction.response.send_message("done")
async def setup(bot: commands.Bot):
    await bot.add_cog(Score(bot))
#    

    # async def on_message(message):
    #     if message.author == client.user:
    #         return 0
    #     t = message.content.split("!", 1)
    #     if message.content.startswith("help"):
    #         texts = open("help.md", "rb")
    #         say = texts.read().decode("utf-8")
    #         texts.close()
    #         await message.channel.send(say)
    #         # delete help message and ask help message in 5s
    #         await asyncio.sleep(5)  # sec
    #         await message.channel.purge(limit=2, check=content_help)
    #     if message.content.startswith("score"):
    #         try:
    #             data = await all_score_read()
    #             if message.content == "score!":
    #                 for i in data:
    #                     await message.channel.send(f"{i} : {data[i]}")
    #             else:
    #                 await ind_err(message)
    #         except:
    #             await ind_err(message)
    #     if message.content.startswith("add"):
    #         try:
    #             data = await all_score_read()
    #             if message.content == "add":
    #                 await message.channel.send("error")
    #             else:
    #                 t = message.content.split(" ", 3)
    #                 await personal_score_write(int(t[1]), t[2], int(t[3]))
    #                 await message.channel.send("done")
    #         except:
    #             await ind_err(message)
    #     if message.content.startswith("team_add"):
    #         try:
    #             data = await all_score_read()
    #             if message.content == "team_add":
    #                 await ind_err(message)
    #             else:
    #                 t = message.content.split(" ", 2)
    #                 await team_score_write(int(t[1]),int(t[2]))
    #                 await message.channel.send("done")
    #         except:
    #             await ind_err(message)
    #     if message.content.startswith("role"):
    #         rol =  message.author.roles
    #         for i in rol:
    #             if i.name == "admin":
    #                 await message.channel.send("admin")
    #                 break