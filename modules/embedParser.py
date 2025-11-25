# this is the embed message parser
# created by: Zach

# imports
import discord
from discord import Embed
from enum import Enum

# module variables

class EmbedDialougeType(Enum):
    ABOUT_DIALOUGE = 0
    INFO_DIALOUGE = 1
    ERROR_DIALOGUE = 2

class DialougeColors(Enum):
    ABOUT_COLOR = discord.Color.green()
    INFO_COLOR = discord.Color.blue()
    ERROR_COLOR = discord.Color.red()

def create_embed_dialogue(dialouge_type: EmbedDialougeType, dialouge_title: str, info_message) -> Embed:
    """This functions takes in a EmdebDialougeType, a title and message and returns an Embed object"""
    global color_to_use
    color_to_use = None
    print("creating embed")

    # getting the color
    match dialouge_type:
        case EmbedDialougeType.ABOUT_DIALOUGE:
            color_to_use = DialougeColors.ABOUT_COLOR.value
        case EmbedDialougeType.INFO_DIALOUGE:
            color_to_use = DialougeColors.INFO_COLOR.value
        case EmbedDialougeType.ERROR_DIALOGUE:
            color_to_use = DialougeColors.ERROR_COLOR.value
    
    # creating the embed
    if color_to_use != None:
        new_embed = Embed(
            title=dialouge_title,
            description=info_message,
            color=color_to_use)
        return new_embed


