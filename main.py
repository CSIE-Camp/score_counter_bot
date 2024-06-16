import json
import os
import discord
from discord.ext import commands
import asyncio

def role_check(role:str,mes):
    rol = mes.author.roles
    for i in rol:
        if i.name == role:
            return 1
    return 0

__cogs=["admin","score"]

intents = discord.Intents.default()
intents.message_content = True
# client = discord.Client(intents=intents)
token = os.getenv("DC_BOT_TOKEN")


bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def reloadAll(ctx):
    try:
        if role_check("admin",ctx.message):
            for i in __cogs:
                await bot.reload_extension(f"cogs.{i}")
            await ctx.send("reload all cogs")
        else:
            print(f"{ctx.message.author} try to reload all cogs")
    except:
        await ctx.send("reload error")


# async def all_score_read():
#     if("personal_score.json" not in os.listdir()):
#         with open("personal_score.json", "w") as w:
#             w.write("{}")
#     with open("personal_score.json", 'r') as r:
#         data = json.load(r)
#     return data

# async def sort_score():
#     data = await all_score_read()
#     data = dict(sorted(data.items(), key=lambda x: x[1]["personal score"], reverse=True))
#     with open("personal_score.json", "w") as w:
#         json.dump(data, w)
#     return 0

# async def new_student(team:int,name):
#     all_data = await all_score_read()
#     if name in all_data:
#         return 0
#     else:
#         all_data[name] = {}
#         all_data[name]["team"] = team
#         all_data[name]["personal score"] = 0
#         with open("personal_score.json", "w") as w:
#             json.dump(all_data, w)
#     return 1

# async def personal_score_write(team:int, name, score:int):
#     data = await all_score_read()
#     if await new_student(team, name):
#         data = await all_score_read()
#         data[name]["personal score"] = score
#     else:
#         data[name]["personal score"] += score
#     with open("personal_score.json", "w") as w:
#         json.dump(data, w)
#     await sort_score()
#     return 0
# async def team_score_write(team, score):
#     data = await all_score_read()
#     data[team]["team score"] += score
#     with open("team_score.json", "w") as w:
#         json.dump(data, w)
#     return 0

# @client.event
# async def on_ready():
#     print('login: ', client.user)
#     game = discord.Game("use \"help\" command to get help")
#     # discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
#     await client.change_presence(status=discord.Status.online, activity=game)

# async def ind_err(mes):
#     await mes.channel.send("?")
#     errhelp = discord.Embed(
#         title=f"Hi,{mes.author.name}", color=discord.Color.dark_purple())
#     errhelp.set_author(name=mes.author, icon_url=mes.author.avatar_url)
#     errhelp.add_field(name="help", value="help!")
#     await mes.channel.send(embed=errhelp)

# def is_me(m):
#     return m.author == client.user

# def content_help(cth):
#     return cth.content.startswith("help")  # search meeages which content help

# #main code
# @client.event
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
# client.run(token)   #run

@bot.event
async def on_ready():
    print('login: ', bot.user)
    game = discord.Game("use \"help\" command to get help")
    # discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await bot.change_presence(status=discord.Status.online, activity=game)
    
    try:
        # for filename in os.listdir("./cogs"):
        #     if filename.endswith(".py"):
        #         await bot.load_extension(f"cogs.{filename[:-3]}")
        for i in __cogs:
            await bot.load_extension(f"cogs.{i}")
            print(f"load {i}")
    except Exception as e:
        print(f"load error {e}")
    else:
        print("load all cogs")
    slash = await bot.tree.sync()
    print(f"load {len(slash)} slash commands")

if __name__ == "__main__":
    bot.run(token)
    