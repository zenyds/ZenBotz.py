import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands import has_permissions
import random
from random import randint
import asyncio
import re
from aiohttp import request
from prsaw import RandomStuff

intents = discord.Intents(messages=True, guilds=True)
client = commands.Bot(command_prefix="?")
rs = RandomStuff(async_mode = True)

@client.event
async def on_ready():
    activity = discord.Game(name="?commands for help", type=3)        #status
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is ready!")




@client.command(aliases=['user','info'])               #user stats
async def stats(ctx, member : discord.Member):
	embed = discord.Embed(title = member.name , description = member.mention , color = discord.Colour.red()) 
	embed.add_field(name = "ID", value = member.id , inline = False)
	embed.add_field(name='Account Created', value=member.created_at.__format__('%A, %d. %B %Y  %H:%M:%S'))
	embed.add_field(name='Join Date', value=member.joined_at.__format__('%A, %d. %B %Y  %H:%M:%S'))
	embed.set_thumbnail(url = member.avatar_url)
	embed.set_footer(icon_url = ctx.author.avatar_url, text = "Requested by "+ctx.author.name)
	await ctx.send(embed=embed)


@client.command()     #server stats
async def server(ctx):
  name = str(ctx.guild.name)

  id = str(ctx.guild.id)
  memberCount = str(ctx.guild.member_count)

  icon = str(ctx.guild.icon_url)
   
  embed = discord.Embed(
      title=name + " Server Info",
      color=discord.Color.red()
    )
  embed.set_thumbnail(url=icon)
  embed.add_field(name="Server ID", value=id, inline=True)
  embed.add_field(name="Member Count", value=memberCount, inline=True)
  await ctx.send(embed=embed)


@client.command()       #commands
async def commands(ctx):
	embed=discord.Embed(title="Prefix = ?", color=0xff0000)
	embed.set_author(name="Commands For ZenBotz", url="https://discord.gg/5qtnR9bckN")
	embed.add_field(name="User ", value="stats, info, user", inline=True)
	embed.add_field(name="Server", value="server", inline=True)
	embed.add_field(name="Kick/Ban", value="ban, kick", inline=True)
	embed.add_field(name="Clear", value="clear", inline=True)
	embed.add_field(name="8Ball", value="8ball", inline=True)
	embed.add_field(name="TicTacToe", value="tictactoe @you @someone", inline=True)
	await ctx.send(embed=embed)




@client.command()       #clear
@has_permissions(manage_messages = True)
async def clear (ctx,amount=1):
	await ctx.channel.purge(limit = amount)
 
@client.command(aliases=['k'])   #kick
@has_permissions(kick_members = True) 
async def kick(ctx,member : discord.Member,*,reason= "Reason not provided"): 
	await member.kick(reason=reason) 
	await ctx.send(f'User {member} has been kick because: '+reason)

@client.command(aliases=['b'])   #ban
@has_permissions(ban_members = True) 
async def ban(ctx,member : discord.Member,*,reason= "Reason not provided"): 
	await member.ban(reason=reason) 
	await ctx.send(f'User {member} has been banned because: '+reason)


@client.command(name='8ball',            #8ball
            description="Answers a yes/no question.",
            brief="Answers from the beyond.",
            aliases=['eight_ball', 'eightball', '8-ball'],
            pass_context=True)

async def eight_ball(context):            #8ball
    possible_responses = [

        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
        'Maybe so.'

    ]
    await context.channel.send(random.choice(possible_responses) + ", " + context.message.author.mention)


#tic tac toe start
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn. Use ?place (1-9)")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn. Use ?place (1-9)")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the ?tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")
#tic tac toe end


@client.event
async def on_message(message):
    if client.user == message.author:
        return

    if message.channel.id == 824698931086229515:
        response = await rs.get_ai_response(message.content)
        await message.reply(response)

    await client.process_commands(message)


































client.run("token here")