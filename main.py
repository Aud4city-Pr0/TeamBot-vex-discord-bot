# The main file of the project
# created by: Zach

# imports, the requests part of the bot will be handled in another script
# discord api
import discord
from discord.ext import commands

# logging and enviroment variable loading
import logging
from dotenv import load_dotenv
import os

# bot modules
from modules import requestHandler
from modules import embedParser
from modules.embedParser import EmbedDialougeType

# random join messages
import random

BOT_GREETING = [
    "Hi there, welcome to the server!",
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
    print(BOT_GREETING[random.randint(0, len(BOT_GREETING))])
    current_channel = member.guild.system_channel

    # checking to see if it is real
    if current_channel is not None:
        if current_channel.permissions_for(member.guild.me).send_messages:
            # sends to channel
            await current_channel.send(BOT_GREETING[random.randint(0, len(BOT_GREETING))])
        else:
            # sends to member if channel is not real
            await member.send(BOT_GREETING[random.randint(0, len(BOT_GREETING))])

# command handeling
@bot.command()
async def info(ctx):
    # setting our embed
    embed_to_say = embedParser.create_embed_dialogue(EmbedDialougeType.INFO_DIALOUGE, "you have requested help about how to use me, here are my commands:", f"""
                   \n 1. !info - Displays commands that are used with this bot
                   \n 2. !team - Looks for VEX V5 teams based on their number and shows statistics about them (eg. 4303D)
                   \n 3. !event - Shows the current events that a team is enrolled in/has attended for the current season
                   \n 4. !version - States the current version of the bot
                   \n 5. !skills - Gets skills information about a team from a certain season
                   \n 6. !awards - Gets award information about a team from a certain season""")
    
    # checking to make sure that the embed is ready
    if embed_to_say:
        await ctx.send(embed=embed_to_say)

@bot.command()
async def version(ctx):
    #TODO: put verison info in a .json file before realsing bot
    about_embed = embedParser.create_embed_dialogue(EmbedDialougeType.ABOUT_DIALOUGE, f"About {bot.user} - A VEX Discord bot", "created by: Zach D (4303D) Timothy (4303B),  version: 0.1.0")
    await ctx.send(embed=about_embed)

@bot.command()
async def team(ctx, team_name):
    global bot_name
    bot_name = ""
    # getting data
    data, record_info = requestHandler.get_team_from_number(team_name)

    #checking to see if data is real and if it is a dictionary
    if data and type(data) is dict:
        #checking to see if bot name exsits
        if data["data"][0]['robot_name'] == "":
            bot_name = "No bot name found or provided"
        else:
            bot_name = data["data"][0]["robot_name"]

        team_data_embed = embedParser.create_embed_dialogue(EmbedDialougeType.INFO_DIALOUGE, "Team Information:", f"""
                       \n- **Team Name**: {data["data"][0]['team_name']}
                       \n- **Team Number**: {data["data"][0]['number']}
                       \n- **Robot Name**: {bot_name}
                       \n- **Organization**: {data["data"][0]['organization']}
                       """)
        await ctx.send(embed=team_data_embed)
        
        team_record_embed = embedParser.create_embed_dialogue(EmbedDialougeType.INFO_DIALOUGE, "Team Statistics:", f"""
                       \n- 🏆️ **Matches Won:** {record_info.get("wins")} 
                       \n- 😔 **Matches Lost:** {record_info.get("losses")}
                       \n- 🤝 **Matches Tied:** {record_info.get("ties")}""")
        await ctx.send(embed=team_record_embed)
    else:
        await ctx.send(embed=embedParser.create_embed_dialogue(EmbedDialougeType.ERROR_DIALOGUE, "Sorry, an error has occured D:", f"are you sure that team {team_name} exsits or is registered for this season?"))

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
        error_embed = embedParser.create_embed_dialogue(EmbedDialougeType.ERROR_DIALOGUE, "Sorry, an error has occured D:", f"No event data found for team `{team}`.")
        return await ctx.send(embed=error_embed)
    
    msg = f"Events attended by **{team}** in the season: **{season_name}**:\n"
    data_embed = embedParser.create_embed_dialogue(EmbedDialougeType.INFO_DIALOUGE, msg, "")
    for event in data:
        formated_event = f"{event['name']} ({event['start'][:10]})\n"
        data_embed.add_field(name=f"Event {data.index(event) + 1}:", value=formated_event, inline=False)
    await ctx.send(embed=data_embed)


# running the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)