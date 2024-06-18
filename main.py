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
async def reload(ctx):
    try:
        if role_check("admin",ctx.message):
            for i in __cogs:
                await bot.reload_extension(f"cogs.{i}")
            await ctx.send("reload all cogs")
        else:
            print(f"{ctx.message.author} try to reload all cogs")
    except Exception as e:
        await ctx.send("reload error")
        print(f"reload error {e}")
# @bot.command()
# async def help(ctx):
#     with open("HELP.md","r") as f:
#         await ctx.send(f.read())

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
    