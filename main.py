#Importing libraries
import requests, discord, os, asyncio, prsaw2, shutil, datetime, random, aiohttp
from discord_interactive import Page, Help
from PIL import Image, ImageFont, ImageDraw
import imgfunctions as functions
from replit import db
from discord.ext import commands #Import stuff to make making commands easier
from discord.ext.commands import CommandNotFound, MissingPermissions
intents = discord.Intents.default()
intents.members = True #It's to know when a new member joins
bot = commands.Bot(commands.when_mentioned_or("v!","V!","vuln!","Vuln!"),intents=intents,activity=discord.Activity(type=discord.ActivityType.listening,name="v!help or mentions!"), case_insensitive=True) #Setting bot status and initialising it.
#Removing some default commands, if they exist.
bot.remove_command("help")
bot.remove_command("restart")
bot.remove_command("ping")
#Main Functions
#Hug function
huglist = ["https://media1.tenor.com/images/8af307989eb713d2f3817f0e2fd1676d/tenor.gif","https://media1.tenor.com/images/579fdfefae8935a61b6e9614b16cfb3d/tenor.gif","https://media.tenor.com/images/7fb2191b81067c1ca30364ad49f8ae32/tenor.gif","https://media.tenor.com/images/07c1ce46716afd965e274cf927c52310/tenor.gif","https://media.tenor.com/images/882621bff72f582fa9d2a07c85d28776/tenor.gif"]
def hugfunc(ctx, name):
  embedHug = discord.Embed(title=f"{ctx.author.display_name} hugged {name}!", color=0xD53EB6)
  huglink = random.choice(huglist)
  embedHug.set_image(url=huglink)
  return embedHug
#Avatar embed 
def embedAv(mem, av):
  embedAva = discord.Embed(title=f"{mem.display_name}'s Avatar, lookin good!")
  embedAva.set_image(url=av)
  return embedAva
#Factorial
def factorialcalc(n):
  if n == 0:
    return 1
  else:
    return n * factorialcalc(n - 1)
#Gets the UUID of a user through their ign
def returnName(uuid=None):
  try:
    return requests.get(f"https://api.mojang.com/user/profile/{uuid}").json()["name"]
  except:
    return "`Name not found`"
def returnUUID(ign=None):
  try:
    return requests.get(f"https://api.mojang.com/users/profiles/minecraft/{ign}").json()["id"]
  except:
    return "`UUID not found`"
def returnExistence(ign=None):
  try:
    x = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{ign}").json()["id"]
    return True
  except:
    return False
#Return staff status of a user
def stcheck(ctx):
    role = discord.utils.find(lambda r: r.name == db["staffRole"], ctx.message.guild.roles)
    roleasd = discord.utils.find(lambda r: r.name == "God Father", ctx.message.guild.roles)
    if role in ctx.author.roles or str(ctx.author.id) == str(ctx.guild.owner.id) or roleasd in ctx.author.roles or ctx.author.guild_permissions.administrator is True or str(ctx.author.id) == str(562175882412687361):
      return True
    else:
      return False
#Returns last login
def returnLast(uuid:int):
  last = requests.get(f'https://api.hypixel.net/player?key=8db38b57-10ed-4c9b-9fea-cab0857529f5&uuid={uuid}').json()["player"]["lastLogin"]
  return datetime.datetime.utcfromtimestamp(int(last)/1000).strftime('%d')
#Returns the Discord of a user
def returnDiscord(ign=None):
  try:
    uuid = returnUUID(ign)
    return str(requests.get(f'https://api.hypixel.net/player?key=8db38b57-10ed-4c9b-9fea-cab0857529f5&uuid={uuid}').json()["player"]["socialMedia"]["links"]["DISCORD"])
  except:
    return 404
#Checks if a user is in the guild
def returnMS(ign=None):
  uuid = returnUUID(ign)
  try:
    members = requests.get('https://api.hypixel.net/guild?key=8db38b57-10ed-4c9b-9fea-cab0857529f5&id=5e8c16788ea8c9ec75077ba2').json()["guild"]["members"]
    for member in members:
      if member["uuid"] == uuid:
      	 return True
      else:
        continue
  except:
    return False
#Returns the rank of a user
def returnRank(ign=None):
  if returnMS(ign) is True:
    uuid = returnUUID(ign)
    members = requests.get('https://api.hypixel.net/guild?key=8db38b57-10ed-4c9b-9fea-cab0857529f5&id=5e8c16788ea8c9ec75077ba2').json()["guild"]["members"]
    for member in members:
      if member["uuid"] == uuid:
        return str(member["rank"])

#Embeds
helpMain = Page("**VULN**\n\nWelcome to Vuln, this is its bot. You can click on the emojis below to navigate the help page :)")
helpCommands = Page("**COMMANDS**\n\n`v!av` - Displays mentioned users avatar.\n`v!hug` - Hugs the mentioned user.\n`v!ping` - Shows the bots delay.\n`v!define <word>` - Finds the dictionary definition of a word.\n`v!ud <word` - Get the urban dictionary definition of a word.\n`v!meme` - Sends a meme.\n`v!joke` - Sends a joke (Could be nsfw).\n`v!s <sentence>` - Talk to an AI Chatbot\n`v!stop` - Close a user's chatbot session.\n`v!printnerds [level] [afk days] [gexp]` - Prints the list of people to kick, defaults to 20, 3, 21000.\n`v!pair <ign>` - Pair to this user (mc username)\n`v!forcepair <user> <ign>` - Forcepair a user to that username.\n`v!staffCheck` - Checks if you're staff.\n`v!getDiscord <mc_ign>` - Gets the user's discord if connected.\n`v!rank <ign>` - Get the user's rank in the guild\n`v!triggers <view/add/reset/remove> [<word to add/remove> <response to word>]` - Allows you to manage triggers.\n`v!blacklist <view/add/reset/delete> [<word to add/remove>]` - Adds a word to be blacklisted.\n`v!ignore <blacklist/triggers> <channel>` - Channels to ignore for triggers/blacklist.\n`v!warn <user> <reason>` - Warn a user.\n`v!resetwarns` - Clears all warns in the server.\n`v!delwarn <user> <number>` - Deletes a warn.\n`v!warns <user>` - Display all the warns of a user.")
helpInfo = Page("**INFO**\n\nCreated by 5232TheElder#1923 for Vuln.")
helpMain.link(helpCommands, description="Click me to view the list of commands!", reaction='🤖')
helpMain.link(helpInfo, description="Click me to view some bot info :)", reaction='❓')
helpMain.root_of([helpCommands,helpInfo])
helpObj = Help(bot, helpMain)
#The help embed
embedHelp = discord.Embed(title="VULN", description="A skyblock, skywars and bedwars focused guild. Level 61 with a 40% chance of dexp.", color=0x00ff00)
embedHelp.add_field(name="Commands", value=f"**Staff**\n*v!rankGive* - Update rank roles\n*v!forcePair <mention> <ign>* - Force pairs a user. Not recommended.\n*v!restart* - Restarts the bot, only The godfather, Jones can do this.\n\n**General**\n*v!ping* - Check if the bot is online\n*v!pair* - Pair your account and synchronise roles if it hasn't already.\n*v!invite* - Get an invite to this server\n*v!getDiscord* - Get the discord of someone using their MC Username.\n*v!rank <ign>* - Get a user's rank in the server", inline=False)
embedHelp.add_field(name="Staff", value=f"Jones, Lon, Harry, Nero.", inline=False)
embedHelp.add_field(name="Developed by", value=f"<@562175882412687361>", inline=False)
#Pairing embed
def pairing(ign=None, disco=None, author=None):
  global embedPairSuccess
  global embedPairFailure
  global embedPairPartial
  embedPairSuccess = discord.Embed(title="Pairing Successful! :ballot_box_with_check:", description=f"You have successfully paired to {ign} with {disco}.",color=0x96cdcd)
  embedPairFailure = discord.Embed(title="Pairing Failed! :x:", description=f"Failed to pair to {ign}. The connected account is {disco} and yours is {author}.",color=0xf08080)
  embedPairPartial = discord.Embed(title="Pairing Partially Successful! :negative_squared_cross_mark:", description=f"You have successfully paired to {ign} with {disco} but I was unable to change your nickname and/or roles, please rectify immediately.",color=0xbbd6af)
#RankGive embed
def rankGiving(author=None, Unlinked=None, Updates=None):
  global embedRankGiving
  embedRankGiving = discord.Embed(title="RankGive Successful  :ballot_box_with_check:", description=f"Run by {author}, {Unlinked} unlinked users and {Updates} updates.",color=0x96cdcd)
#discordCheck embed
def discordEmbed(author=None, MC=None, discorda=None):
  global embedDiscordSuccess
  global embedDiscordFailure
  embedDiscordSuccess = discord.Embed(title=f"{MC}'s Discord is {discorda}.", description=f"Run by {author}.",color=0x96cdcd)
  embedDiscordFailure = discord.Embed(title=f"{MC}'s Discord is not linked.", description=f"Run by {author}.", color=0xf08080)
#staffCheck embed
def staff(author=None):
  global embedStaffSuccess
  global embedStaffFailure
  embedStaffSuccess = discord.Embed(title=f"You're staff!", description=f"Run by {author}.",color=0x96cdcd)
  embedStaffFailure = discord.Embed(title=f"You're not staff!", description=f"Run by {author}.", color=0xf08080)
#rank embed
def rankget(author=None, rank=None, user=None):
  global embedRank
  embedRank = discord.Embed(title=f"{user}'s rank is {rank}", description=f"Run by {author}.",color=0x96cdcd)
#Commands
#Help command
@bot.command()
async def help(ctx):
  await ctx.reply("Check DMs.", mention_author=False)
  await helpObj.display(ctx.message.author)
#Gets the rank of a user.
@bot.command()
async def rank(ctx, user=None):
  if user is None:
    await ctx.send("Correct usage - `v!rank <MC_Username>`.")
  else:
    if returnMS(user) is True and returnExistence(user) is True:
      rank = returnRank(user)
      rankget(ctx.author, rank, user)
      await ctx.send(embed=embedRank)
    elif returnMS(user) == 404:
      await ctx.send("User not in guild!")
    elif returnExistence(user) is False:
      await ctx.send("Incorrect username!")
    else:
      await ctx.send("There was an error, this was reported to the developer.")
      print(f"There was an error getting {user}'s rank.")
#Return a user's discord
@bot.command()
async def getDiscord(ctx, user=None):
  if user is None:
    await ctx.send("Correct usage - `v!discord <MC_Username>`.")
  else:
    if returnExistence(user) is True:
      try:
        disc = returnDiscord(user)
        discordEmbed(ctx.author, user, disc)
        await ctx.send(embed=embedDiscordSuccess)
      except:
        discordEmbed(ctx.author, user)
        await ctx.send(embed=embedDiscordFailure)
    else:
      await ctx.send("User does not exist!")
#restart command
@bot.command()
async def restart(ctx):
  if stcheck(ctx) is True:
    await ctx.send("Restarting")
    os.system('python3 startup.py')
    exit()
#Staff check command
@bot.command()
async def staffCheck(ctx):
  if stcheck(ctx) is True:
    staff(ctx.author)
    await ctx.send(embed=embedStaffSuccess)
  else:
    staff(ctx.author)
    await ctx.send(embed=embedStaffFailure)
#Pair command
@bot.command()
async def pair(ctx, user=None):
  if returnExistence(user) is True:
    dcRole = discord.utils.get(ctx.guild.roles, name="Discord Member")
    disc = returnDiscord(user)
    pairing(user, disc, ctx.author)
    ranks = ["Vulnerable","Active-Vuln","InVulnerable","Helpers"]
    rank = returnRank(user)
    roles=[
  discord.utils.get(ctx.guild.roles, name="Guild member"),
  discord.utils.get(ctx.guild.roles, name="Active Guild Member"),
  discord.utils.get(ctx.guild.roles, name="Special Guild Member"),
discord.utils.get(ctx.guild.roles, name="Helper")]  
    if str(disc) == str(ctx.author):
      if rank == ranks[0]:
        await ctx.author.add_roles(roles[0], reason=f"v!pair by {ctx.author}")
        await ctx.author.remove_roles(roles[1], roles[2], roles[3])
      if rank == ranks[1]:
        await ctx.author.add_roles(roles[0], roles[1], reason=f"v!pair by {ctx.author}")
        await ctx.author.remove_roles(roles[2], roles[3])
      if rank == ranks[2]:
        await ctx.author.add_roles(roles[0], roles[2], reason=f"v!pair by {ctx.author}")
        await ctx.author.remove_roles(roles[1], roles[3])
      if rank == ranks[3]:
        await ctx.author.add_roles(roles[0], roles[3], reason=f"v!pair by {ctx.author}")
        await ctx.author.remove_roles(roles[1], roles[2])
      try:
        await ctx.author.edit(nick=user)
        await ctx.send(embed=embedPairSuccess)
      except Exception as e:
        print(e)
        await ctx.send(embed=embedPairPartial)
    else:
      try:
        tutorial = await ctx.fetch_message(866971922109038603)
        await tutorial.reply(embed=embedPairFailure, mention_author=False)
      except:
        await ctx.reply(embed=embedPairFailure, mention_author=False)
  else:
    await ctx.send("That Minecraft account doesn't exist!")
#Invite command
@bot.command()
async def invite(ctx):
  await ctx.send("You can join the discord server here ||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ _ _ https://bit.ly/VULNDiscord")
#Website command
@bot.command()
async def website(ctx):
  await ctx.send("You can view our website at https://bit.ly/VULN. It would really mean a lot of you shared it!")
#Ping command
@bot.command()
async def ping(ctx):
    await ctx.reply(embed=discord.Embed(title="Pong!", description=f"Your ping is {round(bot.latency * 1000)}ms.", color=0x39f220))
@bot.command()
async def hug(ctx, member: discord.Member=None, nick=None):
  async with ctx.typing():
    await asyncio.sleep(1)
  if nick is None and member is None:
    await ctx.send("You need to mention a user or name!")
  elif nick is None:
    await ctx.send(embed=hugfunc(ctx, member.display_name))
#Resets or changes everyone's nickname
@bot.command()
async def nickReset(ctx, change=3, nock=None):
  print(stcheck(ctx))
  if change == 0 and stcheck(ctx) is True:
    await ctx.send("Resetting all nicknames...")
    for user in ctx.guild.members:
      try:
        await user.edit(nick=None, reason=f"nickReset {change} {nock} by {ctx.author}")
      except:
        continue
  elif change == 1 and stcheck(ctx) is True:
    await ctx.send(f"Setting all nicknames to {nock}.")
    for user in ctx.guild.members:
      try:
        await user.edit(nick=nock, reason=f"nickReset {change} {nock} by {ctx.author}")
      except:
        continue
  elif change == 2 and stcheck(ctx) is True:
    await ctx.send("Resetting unpaired user's nicknames")
    for user in ctx.guild.members:
      if returnExistence(user.display_name) is False and stcheck(ctx) is True:
        try:
          await user.edit(nick=None, reason=f"nickReset {change} {nock} by {ctx.author}")
        except:
          continue
      else:
        continue
  elif change == 3:
    await ctx.send("Incorrect usage! `v!nickReset <0/1/2/3> [new_nickname]`")
  elif stcheck(ctx) is False:
    await ctx.send("No permissions.")

@bot.command()
async def meme(ctx):
  membed = discord.Embed(title="oOo a meme!")
  async with aiohttp.ClientSession() as cs:
    async with cs.get('https://www.reddit.com/r/memes/new.json?sort=hot') as r:
      res = await r.json()
      membed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
  await ctx.send(embed=membed)
@bot.command()
async def forcepair(ctx, member: discord.Member,user=None):
  if stcheck(ctx) is True:
    disc = returnDiscord(user)
    rank = returnRank(user)
    pairing(user, disc, ctx.author)
    ranks = ["Vulnerable","Active-Vuln","InVulnerable","Helpers","UnVulnerable"]
    roles=[
  discord.utils.get(ctx.guild.roles, name="Guild member"),
  discord.utils.get(ctx.guild.roles, name="Active Guild Member"),
  discord.utils.get(ctx.guild.roles, name="Special Guild Member"),
discord.utils.get(ctx.guild.roles, name="Helper")]  
    try:
      if rank == ranks[0]:
        await member.add_roles(roles[0], reason=f"v!pair by {ctx.author}")
        await member.remove_roles(roles[1], roles[2], roles[3])
      if rank == ranks[1]:
        await member.add_roles(roles[0], roles[1], reason=f"v!pair by {ctx.author}")
        await member.remove_roles(roles[2], roles[3])
      if rank == ranks[2] or returnRank(user) == ranks[4]:
        await member.add_roles(roles[0], roles[2], reason=f"v!pair by {ctx.author}")
        await member.remove_roles(roles[1], roles[3])
      if rank == ranks[3]:
        await member.add_roles(roles[0], roles[3], reason=f"v!pair by {ctx.author}")
        await member.remove_roles(roles[1], roles[2])
      try:
        await member.edit(nick=user)
        await ctx.send(embed=embedPairSuccess)
      except Exception as e:
        print(e)
        await ctx.send(embed=embedPairPartial)
    except:
      tutorial = await ctx.fetch_message(866971922109038603)
      await tutorial.reply(embed=embedPairFailure, mention_author=False)
  else:
    await ctx.send("That Minecraft account doesn't exist!")
#Prints logged in into console, on ready
@bot.event
async def on_ready():
  print("Logged in!")

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, CommandNotFound):
      await ctx.message.add_reaction('⁉️')
  if isinstance(error, MissingPermissions):
      await ctx.message.add_reaction('❌')
  else:
    print(error)

@bot.command(aliases=["gtop","best"])
async def top(ctx):
  data = requests.get(
  url = "https://api.hypixel.net/guild",
  params = {
        "key": "8db38b57-10ed-4c9b-9fea-cab0857529f5",
        "name": "Vuln" 
    }
).json()
  embedStats = discord.Embed(title="Today's GTop", description="Today's top earning players.",color=0x6C9FCB)
  playerDict = {}
  guild_stats = data['guild']['members']
  for item in guild_stats:
    total = sum(item['expHistory'].values())
    playerDict[item['uuid']] = total
  playerDict = sorted(playerDict.items(), key=lambda x: -x[1])[:10]
  for x in range(10):
    embedStats.add_field(name=returnName(playerDict[x][0]),value=f"{playerDict[x][1]} GExp", inline=False)
  await ctx.send(embed=embedStats)
#prsaw
pTalk = prsaw2.Client(key='Yfbjgiz58BIR')

@bot.command(aliases=["say","ai","talk"])
async def s(ctx, *, msg):
  global inSesh
  try:
    await ctx.send(pTalk.get_ai_response(msg))
    inSesh=ctx.author.display_name
  except Exception as e:
    inSesh=None
    print(f"{ctx.author} tried '{msg}' but got {e}.")
    await ctx.send("There was an error, this has been reported to the dev.")
@bot.command(aliases=["stop","terminate"])
async def close(ctx):
  global inSesh
  if inSesh != None:
    pTalk.close()
    await ctx.send(f"Closed {inSesh}'s session, requested by {ctx.author}.")
    inSesh = None
  else:
    await ctx.send("No sessions active.")
@bot.command(aliases=["j","laugh"])
async def joke(ctx):
  pJoke = prsaw2.Client(key='Yfbjgiz58BIR')
  await ctx.send(f'||{pJoke.get_joke(type="any").joke}||')
  pJoke.close()
@bot.command(aliases=["dict","urban"])
async def ud(ctx, *, word):
  url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
  querystring = {"term":word}
  headers = {
    'x-rapidapi-key': "284d301836msh3bcccd73d2de2a4p106e55jsnb38c121f66a0",
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
    }
  response = requests.request("GET", url, headers=headers, params=querystring)

  await ctx.send(f'Definition -\n{response.json()["list"][0]["definition"]}\n\nExamples -\n{response.json()["list"][0]["example"]}')
@bot.command()
async def purge(ctx, amount=30):
  if stcheck(ctx) is True:
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=amount + 1):
      messages.append(message)
    await channel.delete_messages(messages)
    await ctx.send(f'{amount} messages have been purged by {ctx.message.author.mention}')
  else:
    await ctx.reply("Not staff.")
@bot.command(aliases=['av'])
async def avatar(ctx, avamember : discord.Member=None):
    async with ctx.typing():
      await asyncio.sleep(1)
    av = avamember.avatar_url
    await ctx.reply(embed=embedAv(avamember, av))
@bot.command()
async def memall(ctx,boo=0):
  if boo == 0:
    await ctx.send("You did not confirm, cancelling")
  elif boo == 1 and stcheck(ctx) is True:
    member = discord.utils.get(ctx.guild.roles, name="Discord Member")
    await ctx.send("In Progress...")
    for user in ctx.guild.members:
      await user.add_roles(member,reason=f"Gave role Discord member, run by {ctx.author}")
    await ctx.send("Completed!")
  elif boo != 0 and boo != 1:
    await ctx.send("Please provide a valid output `v!memall <0/1>`")
  elif stcheck(ctx) is False:
    await ctx.send("This command can only be run by staff!")
@bot.command(aliases=["meaning","what", "def"])
async def define(ctx, *, arg):
  try:
    word = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{arg}").json()[0]
    await ctx.send(f'Word - {word["word"]}\nDefinition - {word["meanings"][0]["definitions"][0]["definition"]}\nExamples - {word["meanings"][0]["definitions"][0]["example"]}')
  except:
    await ctx.send("There was an error finding this word.")

#stats command
@bot.command()
async def stats(ctx, ign=None):
  if ign is not None:
    level = await functions.returnLevel(ign)
    uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{ign}").json()["id"]
    url = f'https://crafatar.com/renders/body/{uuid}'
    response = requests.get(url, stream=True)
    with open('playerhead.png', 'wb') as out_file:
      shutil.copyfileobj(response.raw, out_file)
    del response
    background = Image.open('sigma.jpg')
    head = Image.open('playerhead.png')
    I1 = ImageDraw.Draw(background)
    myFont = ImageFont.truetype('FreeMono.ttf', 65)
    myFontSize = ImageFont.truetype('FreeMono.ttf', 55)
    I1.text((66, 79), f"{ign}'s Stats", font=myFont, fill =(0,255,42))
    I1.text((70, 193), f"Level - {level}", font=myFontSize, fill =(255,213,0))
    I1.text((70, 259), f"Discord - {await functions.returnDiscord(ign)}", font=myFontSize, fill =(255,213,0))
    I1.text((70, 318), f"Guild - {await functions.returnGuild(ign)}", font=myFontSize, fill =(255,213,0))
    background.paste(head, (1148, 123), mask = head)
    background.save("userstats.png")
    with open("userstats.png", "rb") as fh:
      f = discord.File(fh, filename="userstats.png")
    await ctx.send(file=f)
  else:
    await ctx.send("Correct usage - `v!stats <ign>`")
#Prints all the idiots that didn't login in the past 3 days

@bot.command()
async def printnerds(ctx, level:int=20, afk:int=2, xp:int=21000):
  if stcheck(ctx) is True:
    await ctx.reply("Processing...")
    current_time = datetime.datetime.now() 
    members = requests.get('https://api.hypixel.net/guild?key=8db38b57-10ed-4c9b-9fea-cab0857529f5&id=5e8c16788ea8c9ec75077ba2').json()["guild"]["members"]
    nerdl = commands.Paginator()
    for member in members:
      trash = False
      try:
        if int(returnLast(member["uuid"])) - current_time.day >= afk:
          trash = True
      except Exception as e:
        #print(f"{e} at {returnName(member['uuid'])}, uuid = {member['uuid']}")
        pass
      try:
        if int(await functions.returnLevel(returnName(member['uuid']))) < level:
          trash = True
      except Exception as e:
        #print(f"{e} at {returnName(member['uuid'])}, uuid = {member['uuid']}")
        pass
      try:
        xpHistory = []
        for key, value in member["expHistory"].items():
          xpHistory.append(value)
        if sum(xpHistory[-7:]) < xp:
          trash = True
      except Exception as e:
        print(f"{e} at {returnName(member['uuid'])}, uuid = {member['uuid']}")
      if trash is True:
        nerdl.add_line(returnName(member["uuid"]))
      else:
        continue
    for page in nerdl.pages:
      await ctx.send(page)
    await ctx.send("Completed!")
  else:
    await ctx.reply("You're not staff!")
@bot.listen('on_message')
async def on_message(message):
  if int(message.author.id) != 866728186628407306:
    for word in db["blacklist"]:
      if word.lower() in message.content.lower():
        #warnuser(ctx)
        await message.delete()
        break
    for word in db["triggers"]:
      if word.lower() in message.content.lower():
        if True:
          await message.reply(db["triggers"].get(word), mention_author=False)
        break
#Warn commands
@bot.command(aliases=["w"])
async def warn(ctx, user: discord.Member, *reason):
  if reason is None:
    await ctx.reply("Provide a reason \*\*\*\*\*\*\*.")
  elif stcheck(ctx) is True:
    read_reason = ""
    for word in reason:
      read_reason = read_reason+" "+word
    db[f"{user.id}warns"].append({read_reason:ctx.author.name})
    await ctx.reply(f"Warned {user.name} for {read_reason}, run by {ctx.author.name}.")
  else:
    await ctx.reply("Get good, get staff.")
@bot.command()
async def delwarn(ctx, user: discord.Member, warn:int=None):
  if warn is None:
    await ctx.reply("You need to send a warn number.")
  elif stcheck(ctx) is True:
    try:
      db[f"{user.id}warns"].pop(warn)
      await ctx.reply(f"Remved warn {warn} from {user.name}.")
    except:
      await ctx.reply("Warn not found.")
@bot.command()
async def warns(ctx, user:discord.Member):
  if stcheck(ctx) is True:
    embedWarns = discord.Embed(title=f"{user.name}'s Warns")
    for warn in db[f"{user.id}warns"]:
      embedWarns.add_field(name=f"#{db[f'{user.id}warns'].index(warn)} - {list(warn.keys())[0]}", value=list(warn.values())[0])
    await ctx.reply(embed=embedWarns)
  else:
    await ctx.reply("Get good, again, get staff.")
@bot.command()
async def resetwarn(ctx):
  if stcheck(ctx) is True:
    for user in ctx.guild.members:
      db[f"{user.id}warns"] = []
    await ctx.reply("Done.")
  else:
    await ctx.reply("You aren't staff.")
@bot.command()
async def staffRole(ctx, arg, rolement: discord.Role=712458500940496936):
  if arg == "set" and ctx.author.id == 562175882412687361 or ctx.author.id == ctx.guild.owner.id or ctx.author.guild_permissions.administrator is True:
    db["staffRole"] = rolement.name
    await ctx.send(f"I have set the staff role to {rolement}")
  elif arg=="view":
    await ctx.reply(f"The staff role is {db['staffRole']}")
  elif arg == "reset" and ctx.author.id == 562175882412687361 or ctx.author.id == ctx.guild.owner.id or ctx.author.guild_permissions.administrator is True:
    db["staffRole"] = ""
    await ctx.reply("Reset the staff role.")
@bot.command()
async def blacklist(ctx, *opt):
  if opt[0] == "view":
    await ctx.reply(embed=discord.Embed(title="Blacklisted Words", description=db["blacklist"]))
  elif opt[0] == "add" and stcheck(ctx) is True:
    db["blacklist"].append(opt[1].lower())
    await ctx.reply(f"Added {opt[1]} to the swear list!", delete_after=5)
  elif opt[0] == "reset" and stcheck(ctx) is True:
    db["blacklist"] = []
    await ctx.reply("Created/Reset the swear list!", delete_after=5)
  elif opt[0] == "delete" and stcheck(ctx) is True:
    try:
      db["blacklist"].remove(opt[1].lower())
      await ctx.reply(f"Removed {opt[1]} from the swear list!", delete_after=5)
    except:
      await ctx.reply("tf? that doesn't even exist.", delete_after=5)
  elif opt[0] != "list" and stcheck(ctx) is False:
    await ctx.reply("This is a staff-only command.")
  await asyncio.sleep(5)
  await ctx.message.delete()
@bot.command(aliases=["trigger"])
async def triggers(ctx, *opt):
  if opt[0] == "view":
    trem = discord.Embed(title="Triggers", description="The triggers list")
    for word in db["triggers"]:
      trem.add_field(name=word, value=db["triggers"].get(word))
    await ctx.reply(embed=trem, delete_after=5)
  elif opt[0] == "add" and stcheck(ctx) is True:
    db["triggers"].update({opt[1]:opt[2]})
    await ctx.reply(f"Added {opt[1]} to the triggers list!", delete_after=5)
  elif opt[0] == "reset" and stcheck(ctx) is True:
    db["triggers"] = {}
    await ctx.reply("Created/Reset the triggers list!", delete_after=5)
  elif opt[0] == "delete" and stcheck(ctx) is True:
    try:
      del db["triggers"][opt[1]]
      await ctx.reply(f"Removed {opt[1]} from the triggers list!", delete_after=5)
    except:
      await ctx.reply("tf? that doesn't even exist.", delete_after=5)
  elif opt[0] != "view" and stcheck(ctx) is False:
    await ctx.reply("This is a staff-only command.")
  await asyncio.sleep(5)
  await ctx.message.delete()
@bot.command()
async def factorial(ctx,n:int):
  await ctx.reply(factorialcalc(n))
@bot.command()
async def roleinfo(ctx, role:discord.Role):
  await ctx.reply(role)
bot.run("ODY2NzI4MTg2NjI4NDA3MzA2.YPWxhg.incVHAgz0HsZ8OqZKRsghHk6fdo")