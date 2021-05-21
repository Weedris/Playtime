from os import curdir
import discord
import json
from discord.ext import commands
from discord.utils import find


# Get configuration.json
with open("config.json", "r") as config:
    data = json.load(config)
    token = data["token"]
    prefix = data["prefix"]


client = commands.Bot(command_prefix = prefix)


@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game( name = "https://github.com/Weedris/Playtime" ) )
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('Hello ' + guild.name + ' call me by : ' + prefix)


#-----------------------------------------------------------------------------
@client.command(
    name = "hello",
    help = "Really ? You want more info ? For that ?",
    brief = "Reply 'Hello !' to the user"
)
async def hello(ctx):
    await ctx.reply("Hello !")


#-----------------------------------------------------------------------------
@client.command(
    name = "storyList",
    help = "Send the list of the stories available",
    brief = "Send the list of the stories available"
)
async def storyList(ctx):
    out = ""
    with open("stories.json", "r") as pannelson:
        data = json.load( pannelson )
        for story in data[ "stories" ]:
            out += " - " + story ["name"] + "\n"
    
    await ctx.channel.send("```" + "Voici la liste des histoires disponnible\n" + out + "```")


#-----------------------------------------------------------------------------
@client.command(
    name = "storyTime",
    help = "write !pt storyTime 'nom d'histoire', afin de commencer une histoire interactive",
    brief = "start a stories where You are the hero"
)
async def storyTime(ctx, arg):
    await ctx.channel.send("It's stories time then...\nN'oublie pas il faut juste repondre un chiffre")
    panels = []
    author = ctx.author

    class Panel:
        def __init__(self, choices, content):
            self.choices = choices
            self.content = content
            self.end = [] == self.choices
        
        def __str__(self):
            return "```" + self.content + "```"
    
    def check(m):
        return m.author == author

    with open("stories.json", "r") as pannelson:
        data = json.load( pannelson )
        for story in data[ "stories" ]:
            if story["name"] == arg:
                for panel in story["panel"]:
                    panels.append( Panel( panel["choices"], panel["content"] ) )
    
    curent = panels[0]
    
    while curent.end != True:
        await ctx.channel.send(curent.__str__())
        msg = await client.wait_for('message', check = check)
        curent = panels[ curent.choices[ int(msg.content) - 1 ] ]
    
    await ctx.channel.send(curent.__str__())
    await ctx.channel.send("Merci d'avoir joue cette histoire interactive")


client.run(token)
