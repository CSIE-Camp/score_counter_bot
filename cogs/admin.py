import discord
from discord.ext import commands

# 定義名為 Main 的 Cog
class admin_checkup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # 前綴指令
    @commands.command()
    async def Hello(self, ctx: commands.Context):
        await ctx.send(f"Hello admin{ctx.message.author}")

# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(admin_checkup(bot))