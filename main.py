import discord
import random
import asyncpraw
from PIL import Image
from io import BytesIO
from keep_alive import keep_alive
from discord.ext import commands
from prsaw import RandomStuffV2

client = commands.Bot(command_prefix='.')
client.remove_command('help')

rs = RandomStuffV2(async_mode=True)

kutipan_jokowi = open('jokoquotes.txt','r').readlines()
kutipan_merdeka = open('merdekaquotes.txt','r').readlines()

redit = asyncpraw.Reddit(client_id="QlGKgj6_Yjcvp3YJV1JQUQ",
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

@client.command()
async def okk(ctx, user: discord.Member = None):
    """Twibbon OKK"""
    if user == None:
        user = ctx.author

    print(ctx.message.attachments)

    if ctx.message.attachments != []:
        asset = ctx.message.attachments[0]
    else:
        asset = ctx.author.avatar_url_as()

    foreground = Image.open("Twibbon3.png")


    data = BytesIO(await asset.read())
    background = Image.open(data)
    background = background.resize((1080,1080))
    background.paste(foreground, (0,0), foreground.convert('RGBA'))
    background.save("profile.jpg")
    await ctx.send(file = discord.File("profile.jpg"))

@client.command(pass_context=True)
async def reddit(ctx, sub = "meme"):
    "Use .redit [sub] to specify a sub. Default is meme"
    subreddit = await redit.subreddit(sub)
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

@client.command()
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        title="List of commands",
        color=discord.Color.blue()
    )
    embed.add_field(name=".help", value="Need help?", inline=False)
    embed.add_field(name=".jokowi", value="Quotes from the man himself", inline=False)
    embed.add_field(name=".merdeka", value="Quotes from national heroes", inline=False)
    embed.add_field(name=".ping", value="Pings", inline=False)
    embed.add_field(name=".8ball", value="8Ball game", inline=False)
    embed.add_field(name=".join", value="Joins a voice channel", inline=False)
    embed.add_field(name=".stop", value="Stops and disconnects the bot from voice", inline=False)
    embed.add_field(name=".okk", value="Twibbon OKK", inline=False)
    embed.add_field(name=".reddit", value="Use .redit [sub] to specify a sub. Default is meme", inline=False)
    embed.add_field(name=".t", value="You ever feel lonely? Well, talk to an AI!", inline=False)

    await ctx.send(embed=embed)

@client.command()
async def t(ctx, *, msg):
    response = await rs.get_ai_response(msg)
    await ctx.send(response)


keep_alive()
client.run('TOKEN')



