import discord
import os
import json

prefix: str = "="
os.chdir('C:\\Users\\nakul\\OneDrive\\Desktop\\Code\\DiscordBots\\CurrencyBot')


commands: str = {f"{prefix}open account", f"{prefix}check balance", f"{prefix}deposit (amt)", f"{prefix}withdraw (amt)"}


async def print_commands(message: discord.Message):
    em = discord.Embed(title = "Currency Commands", description="Commands that work with the money system",
               color=discord.Color.purple())
    for command in commands:
        em.add_field(name=command, value="", inline=False)
    await message.channel.send(embed=em)




async def check_balance(message: discord.Message):
    
    a = await open_account(message, True) #just to make sure an account has been made
    if(a):
        await message.channel.send(f'<{message.author.mention}> an account has been made for you :D Looking forward to our business')
    
    users = await get_bank_data() #gets all users
    
    wallet_amt = users[str(message.author.id)]["wallet"]
    bank_amt = users[str(message.author.id)]["bank"]

    
    em = discord.Embed(title = f"{str(message.author)}'s balance", color = discord.Color.red())
    em.add_field(name = "Wallet balance", value = wallet_amt)
    em.add_field(name = "Bank balance", value = bank_amt)
    await message.channel.send(embed = em)




async def open_account(message: discord.Message, check: bool):
    author = message.author
    users = await get_bank_data()
    
    
    if str(author.id) in users:     #if there is already an account
        if check:                   #if you are just checking if an account is made
            return False
        else:
            await message.channel.send('You already have an account')
    else: #An account hasn't been made
        users[str(author.id)] = {}
        users[str(author.id)]["username"] = str(author)
        users[str(author.id)]["wallet"] = 1000
        users[str(author.id)]["bank"] = 0
        users[str(author.id)]["job"] = "none"
        users[str(author.id)]["items"] = [{"name": "pencil", "count": 1}]
        await message.channel.send('Your account has been made. It will be a pleasure doing business with you')
        
    with open("mainbank.json", "w") as f:
        json.dump(users, f, indent=2)
    return True


# spends money (makes sense)
async def spend_money(message: discord.Message, amt: int) -> bool: #returns true if the transation was completed, false if not
    users = await get_bank_data()
    author = message.author
    
    if(users[str(author.id)]["wallet"] >= amt):
        original: int = users[str(author.id)]["wallet"]
        
        await message.channel.send(f"The transaction was completed: ${original} -> ${original-amt}")
        users[str(author.id)]["wallet"] -= amt
        
        with open("mainbank.json", "w") as f:
            json.dump(users, f, indent=2)
        return True
    else:
        await message.channel.send(f"You do not have enough money in your wallet. Use {prefix}withdraw to move money from your bank if you need")
        return False
    
    
    
async def withdraw(message: discord.Message, amt: int):
    a = await open_account(message, True)
    if(a):
        await message.channel.send(f'<{message.author.mention}> an account has been made for you :D Looking forward to our business')
    users = await get_bank_data()
    author = message.author
    
    if(users[str(author.id)]["bank"] >= amt):
        original: int = users[str(author.id)]["bank"]
        original_wallet: int = users[str(author.id)]["wallet"]
        await message.channel.send(f"The transaction was completed: Bank: ${original} -> ${original-amt}")
        await message.channel.send(f"The transaction was completed: Bank: ${original_wallet} -> ${original_wallet+amt}")
        users[str(author.id)]["bank"] -= amt
        users[str(author.id)]["wallet"] += amt
        with open("mainbank.json", "w") as f:
            json.dump(users, f, indent=2)
        return
    else:
       await message.channel.send(f"You do not have enough money in your bank. *cough* *cough* *poor* *cough*") 
       
       
async def withdraw(message: discord.Message, amt: int):
    a = await open_account(message, True)
    if(a):
        await message.channel.send(f'<{message.author.mention}> an account has been made for you :D Looking forward to our business')
    users = await get_bank_data()
    author = message.author
    
    if(users[str(author.id)]["bank"] >= amt):
        original: int = users[str(author.id)]["bank"]
        original_wallet: int = users[str(author.id)]["wallet"]
        await message.channel.send(f"The transaction was completed: Bank: ${original} -> ${original-amt}")
        await message.channel.send(f"The transaction was completed: Wallet: ${original_wallet} -> ${original_wallet+amt}")
        users[str(author.id)]["bank"] -= amt
        users[str(author.id)]["wallet"] += amt
        with open("mainbank.json", "w") as f:
            json.dump(users, f, indent=2)
        return
    else:
       await message.channel.send(f"You do not have enough money in your bank. *cough* *cough* *poor* *cough*") 
       
       
       
async def deposit(message: discord.Message, amt: int):
    a = await open_account(message, True)
    if(a):
        await message.channel.send(f'<{message.author.mention}> an account has been made for you :D Looking forward to our business')
    users = await get_bank_data()
    author = message.author
    
    if(users[str(author.id)]["wallet"] >= amt):
        original: int = users[str(author.id)]["wallet"]
        original_bank: int = users[str(author.id)]["bank"]
        await message.channel.send(f"The transaction was completed: Wallet: ${original} -> ${original-amt}")
        await message.channel.send(f"The transaction was completed: Bank: ${original_bank} -> ${original_bank+amt}")
        users[str(author.id)]["wallet"] -= amt
        users[str(author.id)]["bank"] += amt
        with open("mainbank.json", "w") as f:
            json.dump(users, f, indent=2)
        return
    else:
       await message.channel.send(f"You do not have enough money in your wallet.") 

    
    

# accesses data from json file
async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f) #loads every user into an array
        return users