import discord
import random
from keep_alive import keep_alive

client = discord.Client()

kutipan_jokowi = open('jokoquotes.txt','r').readlines()
kutipan_merdeka = open('merdekaquotes.txt','r').readlines()


@client.event
async def on_ready():
    print('we have logged in')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.jokowi'):
        await message.channel.send(random.choice(kutipan_jokowi))
    if message.content.startswith('.merdeka'):
      await message.channel.send(random.choice(kutipan_merdeka))
    if message.content.startswith('.help'):
        await message.channel.send('.jokowi atau .merdeka')
    if '854587510527885312' in message.content:
        await message.author.send('siapa suruh kamu tag saya?')
    if message.content.startswith('.chilal'):
      await message.channel.send('https://cdn.discordapp.com/attachments/542720978774392851/855505724778872902/1624038762080.jpg')


keep_alive()
client.run('ODU0NTg3NTEwNTI3ODg1MzEy.YMmGow.KbBwID57Mhd2TSDKwIAPjkS8uGw')



