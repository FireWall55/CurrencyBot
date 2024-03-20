from random import choice, randint
from discord import Message, Embed
import discord
prefix: str = "="

commands: str = {f"{prefix}hello", f"{prefix}how are you", f"{prefix}bye", f"{prefix}roll dice",
                 f"{prefix}who are you", f"{prefix}ping"}


async def print_commands(message: Message):
    em = Embed(title = "Text Commands", description="Commands that get a text response back",
               color=discord.Color.purple())
    for command in commands:
        em.add_field(name=command, value="", inline=False)
    await message.channel.send(embed=em)


def get_response(message: Message, user_input: str) -> str:
    lowered: str = user_input.lower()
    
    if lowered == "":
        return 'Well, you\'re awfully silent....'
    elif 'hello' in lowered:
        return str(f'Hi {message.author.mention}')
    elif 'how are you' in lowered:
        return 'Good, thanks!'
    elif 'bye' in lowered:
        return 'See you!'
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1,6)}'
    elif 'who are you' in lowered:
        return "I AM THE HONORED ONE"
    else:
        return choice(["I'm sorry I don't think I understood that",
                       "Ummmmm please repeat that for me?",
                       "Sorry I didn't get that",
                       "My CoMpUtInG sYsTeM cAnNoT uNdErStAnD tHaT",
                       "tf are u on ni-"])
        