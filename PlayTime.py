from os import curdir
import discord
import json
from discord.ext import commands
from discord.utils import find


# Get configuration.json
with open("configuration.json", "r") as config:
    data = json.load(config)
    token = data["token"]
    prefix = data["prefix"]


client = commands.Bot(command_prefix = prefix)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hello ' + guild.name + ' call me by : ' + prefix)

@client.command(
    name = "hello",
    help = "Really ? You want more info ? For that ?",
    brief = "Reply 'Hello !' to the user"
)
async def hello(ctx):
    await ctx.reply("Hello !")


@client.command(
    name = "storyTime",
    help = "nothing to see here",
    brief = "start a story of 3 steps"
)
async def storyTime(ctx):
    await ctx.channel.send("It's story time then...\nN'oublie pas il faut juste repondre un chiffre")
    pannels = []
    author = ctx.author

    class Pannel:
        def __init__(self, choices, content):
            self.choices = choices
            self.content = content
            self.end = [] == self.choices
        
        def __str__(self):
            return "```" + self.content + "```"
    
    def check(m):
        return m.author == author

    with open("pannels.json", "r") as pannelson:
        data = json.load(pannelson)
        for pannel in data["pannel"]:
            pannels.append(Pannel(pannel["choices"], pannel["content"]))
    

    curent = pannels[0]
    
    while curent.end != True:
        await ctx.channel.send(curent.__str__())
        msg = await client.wait_for('message', check = check)
        curent = pannels[ curent.choices[ int(msg.content) - 1 ] ]
    
    await ctx.channel.send(curent.__str__())
    await ctx.channel.send("merci d'avoir joué cette histoire interactive")


client.run(token)
