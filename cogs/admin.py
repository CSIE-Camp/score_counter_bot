import discord
from discord.ext import commands
from adminRole import *
from discord import app_commands
from discord.app_commands import Choice
from typing import Optional
from sort import score_sort
from score_file_operate import *

class admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    # 前綴指令
    @commands.command(name="Hello")
    async def Hello(self, ctx: commands.Context):
        if roleCheck(superAdminRoleName,ctx.author):
            await ctx.send(f"Hello super admin {ctx.message.author}")
        elif roleCheck(adminRoleName,ctx.author):
            await ctx.send(f"Hello admin {ctx.message.author}")

    @app_commands.command(name="score_add", description="變動小隊員分數")
    @app_commands.describe(team_idx="輸入數字", id="輸入編號", score="輸入分數")
    @app_commands.choices(
    team_idx = [
        Choice(name = "第一小隊", value = 1),
        Choice(name = "第二小隊", value = 2),
        Choice(name = "第三小隊", value = 3),
        Choice(name = "第四小隊", value = 4),
        Choice(name = "第五小隊", value = 5),
        Choice(name = "第六小隊", value = 6),
        Choice(name = "第七小隊", value = 7),
        Choice(name = "第八小隊", value = 8),
    ],
    id = [
        Choice(name = "1 號", value = 1),
        Choice(name = "2 號", value = 2),
        Choice(name = "3 號", value = 3),
        Choice(name = "4 號", value = 4),
        Choice(name = "5 號", value = 5),
        Choice(name = "6 號", value = 6),
        Choice(name = "7 號", value = 7),
        Choice(name = "8 號", value = 8),
        Choice(name = "9 號", value = 9),
        Choice(name = "10 號", value = 10),
    ],
)
    async def score_add(self, interaction: discord.Interaction, team_idx: int, id: int, score: int):
        if roleCheck(adminRoleName, interaction.user) or roleCheck(superAdminRoleName, interaction.user):
            # await interaction.response.defer()
            print(team_idx, id, score)
            score_now = await checkScore(team_idx, id)
            score_now = int(score_now)
            if score + score_now < 0:
                await interaction.response.send_message("`分數`不可為負")
            else:
                await personalScoreWrite(team_idx, id, score)
                await interaction.response.send_message("done")
        else:
            print(f"{interaction.user} try to add score")
    @app_commands.command(name="init_score", description="初始化分數")
    @app_commands.describe(score="輸入初始化分數")
    async def init_score(self, interaction: discord.Interaction,score:int):
        if roleCheck(superAdminRoleName, interaction.user):
            await initScore(score)
            await interaction.response.send_message("done")
        else:
            print(f"{interaction.user} try to init score")

# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(admin(bot))