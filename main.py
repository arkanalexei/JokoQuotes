import discord
import random
import asyncpraw
from PIL import Image
from io import BytesIO
from keep_alive import keep_alive
from discord.ext import commands

client = commands.Bot(command_prefix='.')

kutipan_jokowi = open('jokoquotes.txt','r').readlines()
kutipan_merdeka = open('merdekaquotes.txt','r').readlines()

reddit = asyncpraw.Reddit(client_id="QlGKgj6_Yjcvp3YJV1JQUQ",
                     client_secret="Xw88BD_g0tdpkr1HDpbrWSpL23D7QA",
                     username="KopiABC",
                     password="ayolahkamu19",
                     user_agent="KopiABC")


@client.event
async def on_ready():
    print('we have logged in')
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(name=f"{len(client.guilds)} Provinces", type=discord.ActivityType.watching))
    #await client.change_presence(status=discord.Status.online, activity=discord.Activity(name='Republik Indonesia', type=discord.ActivityType.watching))


@client.command()
async def server(ctx):
    """Server stats"""
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)
    roles = str(ctx.guild.roles)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Server Information",
        description=description,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)

@client.command()
async def jokowi(ctx):
    """Quotes from the man himself"""
    await ctx.channel.send(random.choice(kutipan_jokowi))

@client.command()
async def merdeka(ctx):
    """Quotes from national heroes"""
    await ctx.channel.send(random.choice(kutipan_merdeka))

@client.command()
async def ping(ctx):
    """Pings"""
    await ctx.channel.send(f'{round(client.latency * 1000)}ms')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    """8Ball game"""
    eightball_response = ["It is certain.",
                         "It is decidedly so.",
                         "Without a doubt.",
                         "Yes - definitely.",
                         "You may rely on it.",
                         "As I see it, yes.",
                         "Most likely.",
                         "Outlook good.",
                         "Yes.",
                         "Signs point to yes.",
                         "Reply hazy, try again.",
                         "Ask again later.",
                         "Better not tell you now.",
                         "Cannot predict now.",
                         "Concentrate and ask again.",
                         "Don't count on it.",
                         "My reply is no.",
                         "My sources say no.",
                         "Outlook not so good.",
                         "Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(eightball_response)}')

@client.command(pass_context=True)
async def join(ctx):
    """Joins a voice channel"""
    channel = ctx.message.author.voice.channel
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)

    await channel.connect()

@client.command(pass_context=True)
async def stop(ctx):
    """Stops and disconnects the bot from voice"""

    await ctx.voice_client.disconnect()

@client.command(pass_context=True)
async def wanted(ctx, user: discord.Member = None):
    """You will become wanted"""
    if user == None:
        user = ctx.author
    wanted = Image.open("wanted.jpg")

    asset = ctx.author.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((306,304))
    wanted.paste(pfp, (70,140))
    wanted.save("profile.jpg")

    await ctx.send(file = discord.File("profile.jpg"))

@client.command(pass_context=True)
async def redit(ctx, sub = "meme"):
    "Use .redit [sub] to specify a sub. Default is meme"
    subreddit = await reddit.subreddit(sub)
    all_subs = []

    post = subreddit.top("month", limit=50)

    async for subs in post:
        all_subs.append(subs)

    random_post = random.choice(all_subs)

    name = random_post.title
    url = random_post.url

    em = discord.Embed(title = name)
    em.set_image(url = url)

    await ctx.send(embed = em)

keep_alive()
client.run('TOKEN')
