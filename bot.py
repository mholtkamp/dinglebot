# bot.py
import os
import discord
import random

from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('./bot-token.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='~')

class UserStat:
    user:discord.User = None
    banned_word_uses:int = 0

master_user_ids = [242449408715653122]
user_stats = {}

test_emotes = ['💯', '🙀', '💩', '👺']
banned_words = ['pubg', 'zeus', 'milf', 'dilf', 'gilf', 'fun', 'mr. nice guy', 'spice', 'trump', 'shunt', 'clussy', 'moist', 'gape', 'gaping', 'yolo', 'twerk', 'shit', 'bitch', 'fuck', 'titty', 'titties']
redacted_words = ['delta point']
randGen = random.Random(datetime.now())

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})')

    # Alert owners when Dinglebot comes online
    for user_id in master_user_ids:
        print(user_id)
        user = await bot.fetch_user(user_id)
        print(user)
        await user.send('Dinglebot reporting for duty!!')

@bot.event
async def on_message(message:discord.Message):
    if (message.author == bot.user):
        return

    print(f'[{message.author.name}] {message.content}')

    # Add new users to stat list
    if (message.author not in user_stats.keys()):
        user_stats[message.author] = UserStat()
        user_stats[message.author].user = message.author

    # Message Handlers
    await message_reaction(message)
    await message_banned_word(message)
    await message_custom_response(message)
    await message_redacted(message)

    await bot.process_commands(message)

async def message_reaction(message:discord.Message):
    emote_chance = randGen.randint(0,10)
    print(emote_chance)

    if (emote_chance < 2):
        emote_list = test_emotes
        emote_resp = randGen.choice(emote_list)
        print(emote_resp)
        await message.add_reaction(emote_resp)

async def message_banned_word(message:discord.Message):

    lower_case_message = message.content.lower()

    for word in banned_words:
        if word in lower_case_message:
            user_stats[message.author].banned_word_uses += 1
            num_banned_words = user_stats[message.author].banned_word_uses
            msg_content = f'{word.upper()} is a banned word.\nYou have used {num_banned_words} banned words.'
            if (num_banned_words >= 3):
                msg_content += '\nIf you keep using banned words you will be kicked from the server.'
            await message.channel.send(msg_content)
    
async def message_custom_response(message:discord.Message):

    lower_case_message = message.content.lower()
    response:str = ''

    if ('magello' in lower_case_message):
        response = 'FBI, OPEN UP!!'
    elif (('games' in lower_case_message) or ('games tonight' in lower_case_message)):
        response = 'GAMES! GAMES! LETS GOOOOOO'

    if (response != ''):
        await message.channel.send(response)

async def message_redacted(message:discord.Message):
    redacted_message:str = message.content
    lower_case_message:str = message.content.lower()
    need_to_redact = False

    for word in redacted_words:
        found_index = lower_case_message.find(word)
        if (found_index != -1):
            need_to_redact = True
            cased_redact_word = redacted_message[found_index : found_index + len(word)]
            redacted_message = redacted_message.replace(cased_redact_word, '[REDACTED]')
            lower_case_message = redacted_message.lower()

    if (need_to_redact):
        channel_to_send = message.channel
        original_author = message.author.display_name
        # Delete author's message
        await message.delete()
        # Send the redacted message on behalf of the author
        redacted_message = 'Redacted message originally sent by ' + original_author + ':\n' + redacted_message
        await channel_to_send.send(redacted_message)

@bot.command(name='meep', help='Responds with moop')
async def cmd_meep(ctx):
        await ctx.send('moop')

gameList3 = ['Apex Legends', 'The Cycle', 'Rocket League']
gameList4 = ['PUBG lol', 'Warzone', 'Phasmophobia', 'Fallguys', 'Raft']
gameList5 = ['League of Legos', 'CSGO']
gameList6 = ['Overwatch', 'Duckball', 'Jackbox']
gameList7 = ['Tabletop Simulator', 'Pummel Party']

@bot.command(name='game', help='Recommends games based on number of players')
async def cmd_games(ctx, num_players : int):
    game_name:str = 'idk??'

    if (num_players < 3):
        num_players = 3
    if (num_players > 7):
        num_players = 7

    if (num_players == 3):
        game_name = randGen.choice(gameList3)
    elif (num_players == 4):
        game_name = randGen.choice(gameList4)
    elif (num_players == 5):
        game_name = randGen.choice(gameList5)
    elif (num_players == 6):
        game_name = randGen.choice(gameList6)
    elif (num_players == 7):
        game_name = randGen.choice(gameList7)

    await ctx.send(f'Try playing... {game_name}??')

@bot.command(name='buyBoosterPack', help='Purchase a booster pack of wiggle cards using BitchPoints')
async def cmd_buy_booster_pack(ctx):
    await ctx.send('Feature not yet implemented.')

@bot.command(name='source', help='Request link to the bot source code.')
async def cmd_source(ctx):
    await ctx.send('Feature not yet implemented.')

bot.run(TOKEN)