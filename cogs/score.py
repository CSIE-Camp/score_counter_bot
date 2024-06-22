import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from typing import Optional
from adminRole import *
from sort import score_sort
from score_file_operate import *

class Score(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if "custom_id" in interaction.data:
            if interaction.data["custom_id"] == "get_score":
                score_embed = discord.Embed(title="賭場分數")
                user_name = interaction.user.nick
                if user_name is None:
                    user_name = interaction.user.global_name
                if interaction.user.avatar is None:
                    score_embed.set_author(name=user_name)
                else:    
                    score_embed.set_author(name=user_name, icon_url=interaction.user.avatar.url)
                point = 0
                rank = 0
                team = 0
                id_num = 0
                usr_check = 0
                for i in score_sort():
                    rank += 1
                    if i[1] == user_name:
                        point = i[0]
                        team = i[2]
                        id_num = i[3]
                        usr_check = 1
                        break
                    
                if usr_check == 1:
                    await interaction.response.defer()
                    score_embed.add_field(name="小隊", value=team, inline=True)
                    score_embed.add_field(name="編號", value=id_num, inline=True)
                    score_embed.add_field(name="點數", value=point, inline=False)
                    score_embed.add_field(name="排名", value=rank, inline=False)
                    await interaction.followup.send(embed=score_embed, ephemeral=True)
                else:
                    await interaction.response.send_message("是否暱稱與姓名不同？", ephemeral=True)

    @commands.command(name="show_score")
    async def button_interaction_on(self, interaction: discord.Interaction):
        view = discord.ui.View()
        button = discord.ui.Button(
            label="點我查看點數與排名",   
            style=discord.ButtonStyle.blurple,
            custom_id="get_score"
        )
        view.add_item(button)
        await interaction.channel.send(view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Score(bot))