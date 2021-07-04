import discord
from discord.ext import commands
from mcstatus import MinecraftServer 
import time
import datetime

token = "YOUR-TOKEN-HERE"

client = commands.Bot(command_prefix=",")
client.remove_command('help')


@client.event
async def on_ready():
	print("--------------------")
	print(client.user)
	print(client.user.id)
	print("--------------------")

@client.command()
async def help(ctx, cmd=None):
	if cmd == None:
		emb = discord.Embed(description=f" **Info**\n`help`, `status`", color = discord.Colour.blue())
		emb.set_author(name=f"Help is here!", icon_url = ctx.author.avatar_url)
		emb.set_thumbnail(url= client.user.avatar_url)
		await ctx.send(embed=emb)
	elif cmd.lower() == "help".lower():
		emb = discord.Embed(description=f"**Command**\n`help`\n\n**Aliases**\n`None`\n\n**Usage**\n`help <command>`\n\n**Description**\n`Get help about commands.`", color = discord.Colour.gold())
		emb.set_author(name=f"Help is here!", icon_url = ctx.author.avatar_url)
		await ctx.send(embed=emb)
	elif cmd.lower() == "status".lower():
		emb = discord.Embed(description=f"**Command**\n`status`\n\n**Aliases**\n`None`\n\n**Usage**\n`status <Minecraft ServerServer IP>`\n\n**Description**\n`Display the status of a Minecraft server such as server MOTS, server version...`", color = discord.Colour.gold())
		emb.set_author(name=f"Help is here!", icon_url = ctx.author.avatar_url)
		await ctx.send(embed=emb)
	else:
		emb = discord.Embed(description=f"This command doesn't exist!", color = discord.Colour.red())
		emb.set_author(name=f"Something went wrong :(", icon_url = ctx.author.avatar_url)
		await ctx.send(embed=emb)


@client.command()
async def status(ctx, ip):
	try:
		server = MinecraftServer.lookup(ip)
		status = server.status()
		version = status.raw["version"]["name"]
		protocol = status.raw["version"]["protocol"]
		max_players_count = status.raw["players"]["max"]
		online_players_count = status.raw["players"]["online"]
		if isinstance(status.raw["description"], dict):
			num = len(status.raw["description"]["extra"])
			x = 0
			y = 0
			all = []
			while True:
				if x != num:
					motd_text = "motd"
					motd_num = motd_text + str(y)
					motd_final = status.raw["description"]["extra"][x]
					all.append(motd_final["text"])
					x += 1
					y += 1
				else:
					motd = "".join(all)
					break
		else:
			motd = status.raw["description"]
		emb = discord.Embed(title=f"{ip}'s Status", description=f"\n**MOTD** • ```\n{motd}\n```\n**Server Version** • `{version}`\n\n**Protocol** • `{protocol}`\n\n**Players count** • `{online_players_count}/{max_players_count}`", color = discord.Colour.green(), timestamp = datetime.datetime.utcnow())
		emb.set_thumbnail(url=ctx.guild.icon_url)
		await ctx.send(embed=emb)
	except IOError:
		emb = discord.Embed(title="Something went wrong :(", description=f"The server `{ip}` didn't respond with any informations. This error could be for many reasons.\n- Make sure the server is online.\n- Try use **ip:port** | `Example: myserver.com:1234`", color = discord.Colour.red(), timestamp = datetime.datetime.utcnow())
		await ctx.send(embed=emb)
		raise error
	except:
		await ctx.send("Something went wrong :(")
		raise error
	

client.run(token)