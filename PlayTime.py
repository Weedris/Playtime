from os import curdir
import discord
import json
import random
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
    await client.change_presence(activity = discord.Game( name = "Type : .pt help" ) )
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
    
    await ctx.channel.send("```" + "Voici la liste des histoires disponnible :\n" + out + "```")


#-----------------------------------------------------------------------------
@client.command(
    name = "storyTime",
    help = "write .pt storyTime 'nom d'histoire', afin de commencer une histoire interactive.",
    brief = "start a stories where You are the hero."
)
async def storyTime(ctx, arg):
    await ctx.reply("It's stories time then...\nN'oublie pas il faut juste repondre un chiffre",  mention_author = False )
    panels = []
    author = ctx.author
    players = dict()

    class Panel :
        def __init__(self, choices, content):
            self.choices = choices
            self.content = content
            self.end = [] == self.choices
        
        def __str__(self):
            return "```" + self.content + "```"
    
    def check(m):
        return m.author == author

    with open( "Stories.json", "r" ) as pannelson :
        data = json.load( pannelson )
        for story in data[ "stories" ] :
            if story[ "name" ] == arg :
                for panel in story[ "panel" ] :
                    panels.append( Panel( panel[ "choices" ], panel[ "content" ] ) )
    
    with open( "Players.json", "r" ) as playerSon :
        players = json.load( playerSon )
    
    foundIt = False

    for player in players :
        if player == author.name :
            for game in players[player] :
                if game[ 0 ] == arg :

                    foundIt = True

                    await ctx.reply( "Would you like to resume your stories ? : y / n" )

                    msg = await client.wait_for( 'message', check = check )

                    if msg.content.lower() == "n" :
                        current = panels[ 0 ]
                        lastChoice = 0
                        players[ author.name ].remove( [ arg, game[ 1 ] ] )
                    
                    elif msg.content.lower() == "y" :
                        current = panels[ game[ 1 ] ]
                        lastChoice = game[ 1 ]
    
                else :
                    current = panels[ 0 ]
                    lastChoice = 0

    if not foundIt :
        current = panels[ 0 ]
        lastChoice = 0

    stop = False
    
    await ctx.reply( current.__str__() )
    while not current.end and not stop :
        msg = await client.wait_for( 'message', check = check )

        if msg.content == "stop" :
            await ctx.reply( "Sauvegarde de votre progression..." )

            if author.name in players :
                players[ author.name ].append( ( arg, lastChoice ) )

            else :
                players[ author.name ] = [ ( arg, lastChoice ) ]

            with open( "Players.json", "w" ) as data :
                json.dump( players, data, indent = 4 )
            
            await ctx.reply( "Sauvegarde affectué à bientôt !" )

            stop = True
        
        elif msg.content.isdigit() :
            lastChoice = current.choices[ int(msg.content) - 1 ]
            current = panels[ current.choices[ int(msg.content) - 1 ] ]
            await ctx.reply( current.__str__() )
        
        elif msg.content == "help" :
            await ctx.reply( "```Write :\n   - help : receive this messages\n    - stop : Sauvegarde de votre progression et mise en pause de votre partie\n - je sait pas quoi encore```" )

        else :
            await ctx.reply( "I don't understand what you're saying, you have to answer by a `number`, `help`" )

    if current.end:
        with open( "Players.json", "r+" ) as data :
            d = json.load( data )
            for a in d:
                if a == author.name:
                    for c in d[a]:
                        if c[0] == arg:
                            print("c'est la")

    await ctx.reply( "Merci d'avoir joué cette histoire interactive" )
        

#-----------------------------------------------------------------------------
@client.command(
    name = "tikTakToe",
    help = "The bot play a game of TikTakToe against you, to play just enter the coordinate of your move.",
    brief = "The bot play a game of TikTakToe against you."
)
async def tikTakToe(ctx):
    await ctx.channel.send( "Let's play a little game together" )
    author = ctx.author

    gameBoard = [
        [ 0, 0, 0],
        [ 0, 0, 0],
        [ 0, 0, 0]
    ]

    starter = random.randint( 1, 2 )
    player = starter

    # check if the player is the same as the original author
    def check(m):
        return m.author == author

    # send the board into the channel where the game is held
    def sendBoard():
        out = ""
        for line in gameBoard:
            for element in line:
                out += " | "
                if element == 0:
                    out += " # "
                elif element == 1:
                    out += " X "
                elif element == 2:
                    out += " O "
                
            out += "\n"
        return out
    
    # play the play from the player return true -> it went fine
    def play(player, x, y):
        if gameBoard[ x - 1][ y - 1 ] == 0:
            gameBoard[ x - 1][ y - 1 ] = player
            return True
        else:
            return False
    
    # verify if someone win the game or if the game is a draw
    # return 1 if player 1 won
    # return 2 if player 2 won
    # return 3 if it's a draw
    # return 0 if the game is still running
    def verify():
        
        # check lines
        for line in gameBoard:
            if line == [ 1, 1, 1]:
                return 1
            elif line == [ 2, 2, 2]:
                return 2
        
        # check columns
        columns = [ [], [], [] ]
        for line in range( len(gameBoard) ):
            for column in range( len( gameBoard[0] ) ):
                columns[ column ].append( gameBoard[ line ][ column ] )
        
        for column in columns:
            if column == [ 1, 1, 1]:
                return 1
            elif column == [ 2, 2, 2]:
                return 2
        
        # check diags
        diags = [ [], [] ]
        for line in range( len(gameBoard) ):
            for column in range( len( gameBoard[0] ) ):
                if line == column:
                    diags[ 0 ].append( gameBoard[ line ][ column ] )
                if line + column == 2:
                    diags[ 1 ].append( gameBoard[ line ][ column ] )
        
        for diag in diags:
            if diag == [ 1, 1, 1]:
                return 1
            elif diag == [ 2, 2, 2]:
                return 2
        
        # check if draw
        draw = True
        for line in range( len( gameBoard) ):
            for column in range( len( gameBoard[0] ) ):
                if gameBoard[ line ][ column ] == 0:
                    draw = False
                    break
        
        if draw:
            return 3
        else:
            return 0
    
    # random play from the bot
    def playFromBot():
        x = random.randint( 1, 3 )
        y = random.randint( 1, 3 )
        while not play( 1, x, y ):
            x = random.randint( 1, 3 )
            y = random.randint( 1, 3 )

        return 0
    
    # main game loop
    while verify() == 0:

        if player == 1:
            good = False 
            while not good:
                if playFromBot() == 0:
                    good = True

            await ctx.channel.send( sendBoard() )
            
            player = 2
        
        else :

            await ctx.channel.send( "Merci d'envoyé les coordonées de votre emplacement de jeu séparer ^par une virgule (genre : '2,3'), vous êtes : O." )
            msg = await client.wait_for('message', check = check)

            while not play(2, int( msg.content[0] ), int( msg.content[2] ) ):
                await ctx.channel.send( "Coordonées invalide" )
                msg = await client.wait_for('message', check = check)

            await ctx.channel.send( sendBoard() )     
            
            player = 1
    
    if verify() == 1:
        await ctx.channel.send( "Bravo vous avez perdu !" )
    elif verify() == 2:
        await ctx.channel.send( "Bravo vous avez Gagnez !" )
    elif verify() == 3:
        await ctx.channel.send( "Bravo vous avez fait une égalité !" )

#-----------------------------------------------------------------------------
@client.command(
    name = "suggestGame",
    help = "The bot suggest you a game to play with our friends (doesn't provide the friends).",
    brief = "The bot suggest you a game to play with our friends (doesn't provide the friends)."
)
async def suggestGame(ctx):
    gameList = [
        "le Ptit Bac",
        "Among us",
        "Agar.io",
        "Biscotte",
        "skribbl.io",
        "Gartic Phone",
        "Chepa demerdez vous"
    ]

    catchPhrases = [
        "Un petit : ",
        "Pourquoi pas : ",
        "Test ça : "
    ]
    
    await ctx.channel.send( random.choice(catchPhrases) + random.choice(gameList) )

client.run(token)