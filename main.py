# The main file of the project
# created by: Zach

# imports, the requests part of the bot will be handled in another script
# discord api
import discord
from discord.ext import commands
from datetime import datetime
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

# helper functions

def format_event_date(date_string):
    """
    Convert variants like:
      - "2024-02-12"
      - "2024-02-12T00:00:00Z"
      - "2024-02-12T00:00:00+00:00"
      - "2024-02-12 00:00:00"
    into "M/D/Y" (e.g. "2/12/2024").
    Falls back to returning the original string if parsing fails.
    """
    if not date_string:
        return "Unknown"

    s = str(date_string).strip()

    # Try ISO parsing first (handles timezone if we replace trailing Z)
    try:
        if s.endswith("Z"):
            # Python's fromisoformat doesn't accept trailing 'Z' — convert to +00:00
            s_iso = s[:-1] + "+00:00"
        else:
            s_iso = s

        # datetime.fromisoformat handles "YYYY-MM-DD" and "YYYY-MM-DDTHH:MM:SS[+HH:MM]"
        dt = datetime.fromisoformat(s_iso)
    except Exception:
        # Fallback: try parsing first 10 chars as YYYY-MM-DD
        try:
            dt = datetime.strptime(s[:10], "%Y-%m-%d")
        except Exception:
            # couldn't parse — return original so you can see what's actually coming back
            return date_string

    # Build M/D/Y using integers so it's portable across platforms
    return f"{dt.month}/{dt.day}/{dt.year}"

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
    embed_to_say = embedParser.create_embed_dialogue(EmbedDialougeType.INFO_DIALOUGE, "Bot Commands:", """
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
    if data != None and type(data) is dict:
        #checking to see if bot name exsits
        if data["data"][0]['robot_name'] == "":
            bot_name = "N/A"
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
@bot.command()
async def skills(ctx, team_name):
    data = requestHandler.get_team_skills(team_name)

    if not data:
        error_embed = embedParser.create_embed_dialogue(EmbedDialougeType.ERROR_DIALOGUE, f"Team {team_name} has no skills", "This team might not have any skills runs for this season.")
        return await ctx.send(embed=error_embed)

    # creating skills embed
    skills_embed = embedParser.create_embed_dialogue(EmbedDialougeType.INFO_DIALOUGE, f"Skills for {team_name}:", "")

    # adding fields to embed
    skills_embed.add_field(name="Driver Skills 🏎️:", value=f"**{data["driver"]}**", inline=False)
    skills_embed.add_field(name="Programming Skills 👨‍💻:", value=f"**{data["programming"]}**", inline=False)
    skills_embed.add_field(name="Total Skills 📊:", value=f"**{data["total_score"]}**", inline=False)

    #sending the embed
    await ctx.send(embed=skills_embed)   


@bot.command()
async def awards(ctx, team_name):
    awards_list = requestHandler.get_team_awards(team_name)
    # checking to see if we have info
    if awards_list != None:
        # creating the embed
        award_embed = embedParser.create_embed_dialogue(EmbedDialougeType.INFO_DIALOUGE, f"Awards won by {team_name} this season:", "")
        # loop through awards properly
        for index ,award in enumerate(awards_list, start=1):
            event_name = award.get("event", {}).get("name", "Unknown Event")
            award_title = award.get("title", "Unknown Award")

            qualifications = award.get("qualifications", [])
            # If empty list → show "N/A"
            if not qualifications:
                qualifications_text = "N/A"
            else:
                #join list into readable string
                qualifications_text = ", ".join(qualifications)

            formatted_award = (
                f"- **Event:** {event_name}\n"
                f"- **Award:** {award_title}\n"
                f"- **Qualifications:** {qualifications_text}"
            )

            award_embed.add_field(
                name=f"Award {index}.",
                value=formatted_award,
                inline=False
            )
        await ctx.send(embed=award_embed)
    else:
        error_embed = embedParser.create_embed_dialogue(EmbedDialougeType.ERROR_DIALOGUE, "No awards found 😭", f"are you sure that team {team_name} has an award?")
        await ctx.send(embed=error_embed)

@bot.command()
async def events(ctx, team):
    data = requestHandler.get_events_attended_by_team(team)
    season_name = requestHandler.get_current_season_name()

    # ai code, will rewirte message data later
    if data != None:
        msg = f"Events attended by **{team}** in the season: **{season_name}**:"
        data_embed = embedParser.create_embed_dialogue(EmbedDialougeType.INFO_DIALOUGE, msg, "")
        for event in data:
            formated_event = f"- **Date:** ({format_event_date(event.get("start", "")[:10])})\n"
            data_embed.add_field(name=f"Event {data.index(event) + 1}: {event.get("name")}", value=formated_event, inline=False)
        await ctx.send(embed=data_embed)
    else:
        error_embed = embedParser.create_embed_dialogue(EmbedDialougeType.ERROR_DIALOGUE, "Sorry, an error has occured D:", f"No event data found for team `{team}`.")
        return await ctx.send(embed=error_embed)
    


# running the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)