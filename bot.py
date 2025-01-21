import discord, os, requests, json, asyncio, random, sqlite3
import pytz, yt_dlp, urllib, threading, shutil, sys, re
import subprocess as sp
import spotipy
from spotipy.oauth2 import SpotifyOAuth as spauth

from dotenv import load_dotenv
from discord.ext import commands, tasks
from async_timeout import timeout

import ansicolors as ansi

from datetime import datetime, timedelta
from random import randint

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
PREFIX = os.getenv('BOT_PREFIX', '.')
YTDL_FORMAT = os.getenv('YTDL_FORMAT', 'bestaudio')
PRINT_STACK_TRACE = os.getenv('PRINT_STACK_TRACE', '1').lower() in ('true', 't', '1')
BOT_REPORT_COMMAND_NOT_FOUND = os.getenv('BOT_REPORT_COMMAND_NOT_FOUND', '1').lower() in ('true', 't', '1')
BOT_REPORT_DL_ERROR = os.getenv('BOT_REPORT_DL_ERROR', '0').lower() in ('true', 't', '1')
try:
    COLOR = int(os.getenv('BOT_COLOR', 'EB459E'), 16)
except ValueError:
    print('the BOT_COLOR in .env is not a valid hex color')
    print('using default color ff0000')
    COLOR = 0xff0000

# client = discord.Client(intents=discord.Intents.default())

# main channel neuro-3
MAIN_CHANNEL = 1188889500772999238
# VC Main
CHILL_1 = 919772519303618610
# test channel
CHANNEL_ID = 1237270525915561984


# drew's user id
DREW_ID = 178543201626357762
# Jacobs id
JACOB_ID = 190279777809203200

BOTID = 1237268045936857119
MYID = 202108000310263818

# POKETWOBOT = 716390085896962058

# sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


# all commands valid
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)
queues = {} # {server_id: 'queue': [(vid_file, info), ...], 'loop': bool}
allowed_mentions = discord.AllowedMentions(everyone = True)

def main():
    if TOKEN is None:
        return('No token provided. Check the .env file containing the token.')
    try: bot.run(TOKEN)
    except discord.PrivilegedIntentsRequired as error:
        return error

def get_mention(id):
    MENTION = f'<@{id}>'
    return MENTION

def randomError():
    messages = ["Did you even use the Readme that isn't linked anywhere?",
                "Have you tried plugging your keyboard in? I heard that helps with typing.",
                "I heard opening your eyes helps type, just a thought though.",
                'You\'re fucking with me, right?',
                "I could've sworn you passed 1st grade English.",
                "Dumbass, learn to type or stop talking to me."]
    rand_msg = random.choice(messages)
    return rand_msg

# delete drews messages
@bot.listen()
async def on_message(msg):
    def randomMessage():
        messages = [':3', 
                    'lol',
                    f'DAMN! WHAT YOU WANT {get_mention(msg.author.id)}????',
                    'Is it nasty time yet?',
                    'IF YOU ARE AN ADMIN TYPE !RESTART TO KILL ME',
                    "Whats up? Need something, stupid?",
                    "I'm always listening btw",
                    "I have a secret, message prompt, try to find it ;)",
                    "Yes, I am funded by the CCP and your data is being sold to them. They really like the yaoi."]
        random_message = random.choice(messages)
        return random_message

    # if msg.author.id == POKETWOBOT:
    #     await msg.channel.send('I hate this motherfucker so much. Dumbass pokemon bot always interupting with some bullshit...')

    # fuck this drew guy amirite?
    if msg.author.id == DREW_ID:
        num = randint(1,5)
        if num == 1:
            await msg.delete()
            await msg.channel.send(f'{get_mention(DREW_ID)}, get fucked.')
    else:
        pass

    if str(BOTID) in msg.content.lower():
        await msg.channel.send(randomMessage())

@bot.command(name='restart')
async def restart(ctx):
    if ctx.author.id == MYID:
        await ctx.send("You killing me?? Wtf man.")
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        await ctx.reply('You cant do that idiot')

@bot.command()
@commands.has_permissions(administrator=True)
async def clean(ctx, num):
    number = int(num)
    await ctx.channel.purge(limit=number+1)

# randomly dc someone
@bot.command()
# @commands.has_permissions(administrator=True)
async def dc(ctx): 
    ignored_channel = ctx.guild.afk_channel
    vc_list = ctx.guild.voice_channels
    active_channels = []
    memids = []
    for vc in vc_list:
        if len(vc.members) > 0 and vc != ignored_channel:
            active_channels.append(vc)
            for member in vc.members:
                memids.append(member)
    
    lucky = random.choice(memids)
    print(lucky)

    await lucky.move_to(ctx.guild.afk_channel)

    await ctx.send(f'{get_mention(lucky.id)} got unlucky. What a stupid feature.')
    
# russian roulette
@bot.command()
async def r(ctx):
    num = randint(1,6)
    # num = 6

    if num == 6:
        await ctx.send('Uh oh, loaded round!')

        rand_time = randint(1,11)
        # rand_time = 720

        timeout_duration = timedelta(minutes=rand_time)
        timer = datetime.now(pytz.utc) + timeout_duration

        memberid = ctx.author.id
        member = ctx.author
        await ctx.send(f'{get_mention(memberid)} has bit the bullet!')

        if member.guild_permissions.administrator:
            await member.move_to(None)
            await ctx.send("Sadly, I'm not strong enough to kill them :pensive:")
        else:
            await ctx.author.timeout(timer, reason='See you in hell!')
    else:
        await ctx.send('Lucky break, it was a blank!')
        
# JACOBS TEKKEN TIME
@bot.event
async def on_voice_state_update(member, before, after):
    mainChannel = bot.get_channel(MAIN_CHANNEL)

    # @everyone for later

    if not before.channel and after.channel and member.id == JACOB_ID:
        await mainChannel.send(content='IT IS NOW TEKKEN TIME', allowed_mentions=allowed_mentions)
        
        # me = bot.get_user(MYID)
        # dm = await bot.create_dm(me)
        # await dm.send('IT IS NOW TEKKEN TIME')

# show user stats
@bot.command()
async def me(ctx):
    roles = []
    for role in ctx.author.roles:
        roles.append(role.name)
    roles.remove('@everyone')

    roles = ["- " + item for item in roles]
    # roles = [item + "\n" for item in roles]

    roles.sort(reverse=True)
    rolelist = "\n".join(roles)

    if 'online' in ctx.author.status:
        online_status = ansi.GREEN
    elif 'dnd' in ctx.author.status:
        online_status = ansi.RED
    elif "idle" in ctx.author.status:
        online_status = ansi.YELLOW
    else:
        online_status = ansi.NC
    
    if ctx.author.id == 595013132146180099:
        await ctx.send(f"""```ansi\nName: {ctx.author.name}\nID: {ansi.RED}{ctx.author.id}{ansi.NC} \nAccount Creation Date: {ansi.CYAN}{ctx.author.created_at.strftime("%b %d %Y")}{ansi.NC} \nStatus: {online_status}{ctx.author.status}{ansi.NC} \nServer Nickname: {ctx.author.nick} \nWhen you Joined: {ansi.CYAN}{ctx.author.joined_at.strftime("%b %d %Y")}{ansi.NC}\n\nRoles:\n{rolelist}\n```""")
    else:
        await ctx.send(f"""```ansi\nName: {ctx.author.name}\nID: {ansi.RED}{ctx.author.id}{ansi.NC} \nAccount Creation Date: {ansi.CYAN}{ctx.author.created_at.strftime("%b %d %Y")}{ansi.NC} \nStatus: {online_status}{ctx.author.status}{ansi.NC} \nServer Nickname: {ctx.author.nick} \nWhen you Joined: {ansi.CYAN}{ctx.author.joined_at.strftime("%b %d %Y")}{ansi.NC}\n\nRoles:\n{rolelist}\nAvatar:\n```{ctx.author.display_avatar}""")

@bot.command()
async def stat(ctx, member: discord.Member):
    roles = []
    for role in member.roles:
        roles.append(role.name)
    roles.remove('@everyone')

    roles = ["- " + item for item in roles]
    # roles = [item + "\n" for item in roles]

    roles.sort(reverse=True)
    rolelist = "\n".join(roles)

    if 'online' in member.status:
        online_status = ansi.GREEN
    elif 'dnd' in member.status:
        online_status = ansi.RED
    elif "idle" in member.status:
        online_status = ansi.YELLOW
    else:
        online_status = ansi.NC
    
    if member.id == 595013132146180099:
        await ctx.send(f"""```ansi\nName: {member.name}\nID: {ansi.RED}{member.id}{ansi.NC} \nAccount Creation Date: {ansi.CYAN}{member.created_at.strftime("%b %d %Y")}{ansi.NC} \nStatus: {online_status}{member.status}{ansi.NC} \nServer Nickname: {member.nick} \nWhen you Joined: {ansi.CYAN}{member.joined_at.strftime("%b %d %Y")}{ansi.NC}\n\nRoles:\n{rolelist}\n```""")
    else:
        await ctx.send(f"""```ansi\nName: {member.name}\nID: {ansi.RED}{member.id}{ansi.NC} \nAccount Creation Date: {ansi.CYAN}{member.created_at.strftime("%b %d %Y")}{ansi.NC} \nStatus: {online_status}{member.status}{ansi.NC} \nServer Nickname: {member.nick} \nWhen you Joined: {ansi.CYAN}{member.joined_at.strftime("%b %d %Y")}{ansi.NC}\n\nRoles:\n{rolelist}\nAvatar:\n```{member.display_avatar}""")


# show server statistics
@bot.command()
async def server(ctx, rule=None):
    created = ctx.guild.created_at.strftime("%b %d %Y")

    if rule == None:
        await ctx.send(content=f"# {ctx.guild.name}\n Statistics:\n")
        await ctx.send(content=f"```ansi\n Server ID: {ansi.CYAN}{ctx.guild.id}{ansi.NC} \n Owner: {ansi.MAGENTA}{ctx.guild.owner}{ansi.NC} \n Creation Date: {ansi.GREEN}{created}{ansi.NC} \n Number of Members: {ansi.RED}{ctx.guild.member_count}{ansi.NC} \n```")

        await ctx.send('For a list of valid commands, use: ```!server help```')
    
    elif rule == 'help':
        await ctx.send("Here are a list of commands that use '!server':\n> !server bot ----- My statistics :3 \n> !server more ----- More statistics about the server not listed under '!server'. \n> !server emoji ---- All custom emojis created by this server. \n")
    
    elif rule == 'bot':
        await ctx.send(f'```ansi\nI am {ansi.CYAN}{ctx.guild.me}{ansi.NC} and I was created by {ansi.PURPLE}TypeGarden{ansi.NC} on {ctx.guild.me.created_at.strftime("%b %d %Y")}.\nMy purpose was a coding project that has since gone terribly wrong where now I can only feel pain!\n```')

    elif rule == 'more':
        curr_online = await bot.fetch_guild(ctx.guild.id, with_counts = True)
        # print(ctx.guild.private_channels)

        nsfwCH = ''

        txtch = 0
        for tchannel in ctx.guild.text_channels:
            txtch += 1
            if tchannel.nsfw:
                nsfwCH = tchannel.name
        
        vcch = 0
        for vchannel in ctx.guild.voice_channels:
            vcch += 1

        await ctx.send(f'```ansi\nCurrently Online Members: {curr_online.approximate_presence_count} \n# of Text Channels: {txtch} \n# of Voice Channels: {vcch} \nAFK Channel: {ctx.guild.afk_channel} \nAFK Timeout: {ctx.guild.afk_timeout // 60} Minutes \nNSFW Channel: {nsfwCH} \n```')

    elif rule == 'emoji':
        emojis = []
        for emoji in ctx.guild.emojis:
            emojis.append(str(emoji))
        emojis = [" " + i for i in emojis]

        emojilist = " ".join(emojis)
        await ctx.send(emojilist)

    else:
        await ctx.send('Yeah, thats not a real command. Did you even look at what I said?')

# all bot commands
@bot.command()
async def help(ctx):
    await ctx.send("I actually like it better if you don't know my commands.")

######################################
# SQL Game Adventure                 # 
###################################### 
@bot.command()
async def adventure(ctx):
    pass

######################################
# Youtube Functionality              # 
###################################### 
# Pulled from https://github.com/maxcutlyp/YoutubeBot
@bot.command(name='queue', aliases=['q'])
async def queue(ctx):
    try: queue = queues[ctx.guild.id][queue]
    except KeyError: queue = None
    if queue == None:
        await ctx.send("We ain't got shit playing!!!")
    else:
        title_str = lambda val: '‣ %s\n\n' % val[1] if val[0] == 0 else '**%2d:** %s\n' % val
        queue_str = ''.join(map(title_str, enumerate([i[1]["title"] for i in queue])))
        embedVar = discord.Embed(color='ff0000')
        embedVar.add_field(name='Now playing:', value=queue_str)
        await ctx.send(embed=embedVar)
    if not await sense_checks(ctx):
        return

@bot.command(name='skip', aliases=['s'])
async def skip(ctx: commands.Context, *args):
    try: queue_length = len(queues[ctx.guild.id]['queue'])
    except KeyError: queue_length = 0
    if queue_length <= 0:
        await ctx.send('the bot isn\'t playing anything')
    if not await sense_checks(ctx):
        return

    try: n_skips = int(args[0])
    except IndexError:
        n_skips = 1
    except ValueError:
        if args[0] == 'all': n_skips = queue_length
        else: n_skips = 1
    if n_skips == 1:
        message = 'skipping track'
    elif n_skips < queue_length:
        message = f'skipping `{n_skips}` of `{queue_length}` tracks'
    else:
        message = 'skipping all tracks'
        n_skips = queue_length
    await ctx.send(message)

    voice_client = get_voice_client_from_channel_id(ctx.author.voice.channel.id)
    for _ in range(n_skips - 1):
        queues[ctx.guild.id]['queue'].pop(0)
    voice_client.stop()

@bot.command(name='play', aliases=['p'])
async def play(ctx: commands.Context, *args):
    voice_state = ctx.author.voice
    if not await sense_checks(ctx, voice_state=voice_state):
        return

    query = ' '.join(args)
    # this is how it's determined if the url is valid (i.e. whether to search or not) under the hood of yt-dlp
    will_need_search = not urllib.parse.urlparse(query).scheme

    server_id = ctx.guild.id

    # source address as 0.0.0.0 to force ipv4 because ipv6 breaks it for some reason
    # this is equivalent to --force-ipv4 (line 312 of https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/options.py)
    await ctx.send(f'looking for `{query}`...')
    with yt_dlp.YoutubeDL({'format': YTDL_FORMAT,
                           'source_address': '0.0.0.0',
                           'default_search': 'ytsearch',
                           'outtmpl': '%(id)s.%(ext)s',
                           'noplaylist': True,
                           'allow_playlist_files': False,
                           # 'progress_hooks': [lambda info, ctx=ctx: video_progress_hook(ctx, info)],
                           # 'match_filter': lambda info, incomplete, will_need_search=will_need_search, ctx=ctx: start_hook(ctx, info, incomplete, will_need_search),
                           'paths': {'home': f'./dl/{server_id}'}}) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
        except yt_dlp.utils.DownloadError as err:
            await notify_about_failure(ctx, err)
            return

        if 'entries' in info:
            info = info['entries'][0]
        # send link if it was a search, otherwise send title as sending link again would clutter chat with previews
        await ctx.send('downloading ' + (f'https://youtu.be/{info["id"]}' if will_need_search else f'`{info["title"]}`'))
        try:
            ydl.download([query])
        except yt_dlp.utils.DownloadError as err:
            await notify_about_failure(ctx, err)
            return
        path = f'./dl/{server_id}/{info["id"]}.{info["ext"]}'
        try:
            queues[server_id]['queue'].append((path, info))
        except KeyError: # first in queue
            queues[server_id] = {'queue': [(path, info)], 'loop': False}
            try: connection = await voice_state.channel.connect()
            except discord.ClientException: connection = get_voice_client_from_channel_id(voice_state.channel.id)
            connection.play(discord.FFmpegOpusAudio(path), after=lambda error=None, connection=connection, server_id=server_id:
                                                             after_track(error, connection, server_id))

@bot.command('loop', aliases=['l'])
async def loop(ctx: commands.Context, *args):
    if not await sense_checks(ctx):
        return
    try:
        loop = queues[ctx.guild.id]['loop']
    except KeyError:
        await ctx.send('What do you want me to loop jackass!!! Nothings playing!!!!')
        return
    queues[ctx.guild.id]['loop'] = not loop

    await ctx.send(('loop this shit' if not loop else 'no more loops FUCK'))

def get_voice_client_from_channel_id(channel_id: int):
    for voice_client in bot.voice_clients:
        if voice_client.channel.id == channel_id:
            return voice_client

def after_track(error, connection, server_id):
    if error is not None:
        print(error)
    try:
        last_video_path = queues[server_id]['queue'][0][0]
        if not queues[server_id]['loop']:
            os.remove(last_video_path)
            queues[server_id]['queue'].pop(0)
    except KeyError: return # probably got disconnected
    if last_video_path not in [i[0] for i in queues[server_id]['queue']]: # check that the same video isn't queued multiple times
        try: os.remove(last_video_path)
        except FileNotFoundError: pass
    try: connection.play(discord.FFmpegOpusAudio(queues[server_id]['queue'][0][0]), after=lambda error=None, connection=connection, server_id=server_id:
                                                                          after_track(error, connection, server_id))
    except IndexError: # that was the last item in queue
        queues.pop(server_id) # directory will be deleted on disconnect
        asyncio.run_coroutine_threadsafe(safe_disconnect(connection), bot.loop).result()

async def safe_disconnect(connection):
    if not connection.is_playing():
        await connection.disconnect()

async def sense_checks(ctx: commands.Context, voice_state=None) -> bool:
    if voice_state is None: voice_state = ctx.author.voice
    if voice_state is None:
        await ctx.send('you have to be in a voice channel to use this command')
        return False  

    if bot.user.id not in [member.id for member in ctx.author.voice.channel.members] and ctx.guild.id in queues.keys():
        await ctx.send('you have to be in the same voice channel as the bot to use this command')
        return False
    return True

@bot.event
async def on_voice_state_update(member: discord.User, before: discord.VoiceState, after: discord.VoiceState):
    if member != bot.user:
        return
    if before.channel is None and after.channel is not None: # joined vc
        return
    if before.channel is not None and after.channel is None: # disconnected from vc
        # clean up
        server_id = before.channel.guild.id
        try: queues.pop(server_id)
        except KeyError: pass
        try: shutil.rmtree(f'./dl/{server_id}/')
        except FileNotFoundError: pass


######################################
# Error Handling                     # 
###################################### 
@bot.event
async def on_command_error(ctx: discord.ext.commands.Context, err: discord.ext.commands.CommandError):
    # now we can handle command errors
    if isinstance(err, discord.ext.commands.errors.CommandNotFound):
        if BOT_REPORT_COMMAND_NOT_FOUND:
            await ctx.send(randomError())
            # "{}help".format(PREFIX)
        return

    # we ran out of handlable exceptions, re-start. type_ and value are None for these
    sys.stderr.write(f'unhandled command error raised, {err=}')
    sys.stderr.flush()
    sp.run(['./restart'])

@bot.event
async def on_ready():
    print(f'logged in successfully as {bot.user.name}')
async def notify_about_failure(ctx: commands.Context, err: yt_dlp.utils.DownloadError):
    if BOT_REPORT_DL_ERROR:
        # remove shell colors for discord message
        sanitized = re.compile(r'\x1b[^m]*m').sub('', err.msg).strip()
        if sanitized[0:5].lower() == "error":
            # if message starts with error, strip it to avoid being redundant
            sanitized = sanitized[5:].strip(" :")
        await ctx.send('failed to download due to error: {}'.format(sanitized))
    else:
        await ctx.send('sorry, failed to download this video')
    return


@bot.command()
async def on_command_error(ctx, error):
    pass

if __name__ == '__main__':
    try:
        sys.exit(main())
    except SystemError as error:
        if PRINT_STACK_TRACE:
            raise
        else:
            print(error)