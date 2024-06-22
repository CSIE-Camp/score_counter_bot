import discord

adminRoleName = "admin"
superAdminRoleName = "superAdmin"
def roleCheck(role:str,usr:discord.Member):
    rol = usr.roles
    for i in rol:
        if i.name == role:
            return 1
    return 0