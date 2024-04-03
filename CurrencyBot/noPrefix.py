import discord
import re



async def send_message(message: discord.Message, user_message: str) -> None:
    user_message = user_message.lower()
    if user_message == "damn":
        await message.channel.send(":skull:") 
    if "idiot" in user_message:
        await message.channel.send("https://media.discordapp.net/attachments/1191146162946834453/1220126258680041632/Drawing-52.sketchpad.png?ex=660dce20&is=65fb5920&hm=f52e3749a91630e07a751bf9c13b6176777e7bde78bd0982f5eb32084b3d0a95&=&format=webp&quality=lossless&width=755&height=670")
    if "sigma" in user_message:
        await message.channel.send(f"{message.author.mention} is the real sigma <:sigma:1212940952746856449>")
    if user_message.startswith("erm"):
        await message.channel.send("erm")
    if "sus" in user_message:
        await message.channel.send("https://media.discordapp.net/attachments/796560510057316353/1170741792895938652/IMG_6983.gif?ex=6612b742&is=66004242&hm=3900e21dd981eb5899bb339b69283e001e90243f9650b3b522f28e691937bdd0&=&width=175&height=160") 
    if "cap" in user_message:
        await message.channel.send("https://tenor.com/view/cap-you-sure-ok-okay-sure-this-bear-gif-20127342")
    if "ayo" in user_message:
        await message.channel.send("https://tenor.com/view/bert-shook-sesame-street-wtf-did-i-just-read-bert-and-ernie-gif-11751136")
    if user_message == "w":
        await message.channel.send("https://tenor.com/view/wario-w-gif-11314906105849731646")
    if " w " in user_message:
        await message.channel.send("https://tenor.com/view/wario-w-gif-11314906105849731646")
    if "mew" in user_message:
        await message.channel.send("Me rn ong:")
        await message.channel.send("https://tenor.com/view/mewing-cat-mewing-mogging-mogging-cat-looksmaxxing-gif-7825399306863391777")
    if "denis" in user_message:
        await message.channel.send("this guy?", file=discord.File("denis.jpg"))
    if "cutie patootie" in user_message:
        await message.channel.send("ong", file=discord.File("cutie.mov"))
    if "shiven" in user_message:
        await message.channel.send("this guy?", file=discord.File("shiven.jpg"))