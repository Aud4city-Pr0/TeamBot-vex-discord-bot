# The main file of the project

# imports, the requests part of the bot will be handled in another script
# discord api
import discord
from discord.ext import commands

# logging and enviroment variable loading
import logging
from dotenv import load_dotenv
import os

# bot modules
from scripts import requestHandler

# random join messages
import random

BOT_GREATING = [
    "Hi there, welcome to the sever!",
    "Welcome to the server :D, have fun!",
    "Hello and welcome!",
    "Hey! Glad you could join us!"
]

# loading enviorment vars
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# setting up logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# bot setup
bot = commands.Bot(command_prefix='!', intents=intents)

# the bot events
@bot.event
async def on_ready():
    print(f"Bot: {bot.user} is ready to use.")

@bot.event
async def on_member_join(member):
    # prints out greeting
    print(BOT_GREATING[random.randint(0, len(BOT_GREATING))])
    current_channel = member.guild.system_channel

    # checking to see if it is real
    if current_channel is not None:
        if current_channel.permissions_for(member.guild.me).send_messages:
            # sends to channel
            await current_channel.send(BOT_GREATING[random.randint(0, len(BOT_GREATING))])
        else:
            # sends to member if channel is not real
            await member.send(BOT_GREATING[random.randint(0, len(BOT_GREATING))])

# command handeling
@bot.command()
async def info(ctx):
    await ctx.send(f"""{ctx.author.mention}, you have requseted help about how to use me, here are my commands:
                   \n !info - displays commands that are used with this bot
                   \n !team - looks for vex teams based of their number and shows statistics about them (eg. 1234D)
                   \n !event - looks for events based of their name or events in a season if one is provided
                   \n !version - says the current version of the bot
                   \n !skills - gets skills information about a team from a certain season
                   \n !awards - gets award information about a team from a certian season""")

@bot.command()
async def version(ctx):
    #TODO: put verison info in a .json file before realsing bot
    await ctx.send("TeamBot - A VEX Discord bot, created by: Zach D, version: 0.1.0")

@bot.command()
async def team(ctx, team_name):
    data = requestHandler.get_team_from_number(team_name)
    #TODO: switch to discord's built-in markdown system (Embeds)
    #checking to see if data is a dict
    if type(data) is dict:
        await ctx.send(f"""Information for team: **{team_name}**
                       \n- **Team Name**: {data["data"][0]['team_name']}
                       \n- **Team Number**: {data["data"][0]['number']}
                       \n- **Robot Name**: {data["data"][0]['robot_name']}
                       \n- **Org**: {data["data"][0]['organization']}""")

#TODO: get page funtionality working first
#@bot.command()
#async def skills(ctx, team_name):
    #data = requestHandler.get_team_skills(team_name)

@bot.command()
async def events(ctx, team):
    data = requestHandler.get_events_attended_by_team(team)
    season_name = requestHandler.get_current_season_name()

    # ai code, will rewirte message data later
    if not data:
        return await ctx.send(f"No event data found for team `{team}`.")
    
    msg = f"Events attended by **{team}** in the season: **{season_name}**:\n"
    for event in data:
        msg += f"- {event['name']} ({event['start'][:10]})\n"

    await ctx.send(msg)


# running the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)