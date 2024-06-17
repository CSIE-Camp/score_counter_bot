import discord
from discord.ext import commands
from adminRole import adminRoleName

def roleCheck(role:str,usr:discord.Member):
    rol = usr.roles
    for i in rol:
        if i.name == role:
            return 1
    return 0
class admin_checkup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    # 前綴指令
    @commands.command()
    async def Hello(self, ctx: commands.Context):
        if roleCheck(adminRoleName,ctx.author):
            await ctx.send(f"Hello admin {ctx.message.author}")

# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(admin_checkup(bot))