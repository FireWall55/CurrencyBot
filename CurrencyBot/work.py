import json
import discord
import economy
import random
import items


async def work(message: discord.Message, job: str):
    if job == "none":
        await none(message=message)
        return
    if job == "supplier":
        await supplier(message=message)

async def none(message: discord.Message):
    users = await economy.get_bank_data()
    amt: int = random.randint(100,300)
    response: str = random.choice([f"You complete a construction job for fun and gain ${amt}",
                                  f"You did a 1 day job at Google! As a janitor :) You gained ${amt}",
                                  f"W bro hit the griddy at a football game and gained ${amt}"])
    await message.channel.send(response)
    users[str(message.author.id)]["wallet"] += amt
    with open("mainbank.json", "w") as f:
        json.dump(users, f, indent=2)
    return

async def supplier(message: discord.Message):
    await items.add_items_bank(message=message, item="pistol", count=1, print=False)
    response: str = random.choice([f"You worked with the mafia and were paid with a great quality pistol",
                                  f"You were given a pistol as a gift from an interesting guy in the alley"])
    await message.channel.send(response)
    return
