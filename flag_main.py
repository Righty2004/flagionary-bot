import discord
from discord.ext import commands
from flag_func import *
import asyncio
from flag_data import *
import json

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = 'f.', intents = intents, help_command=None)
set_channels = read_json("set_channels.json")
channels = dict()
going_on = list()

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

@bot.command()
async def set(ctx):
    if ctx.channel.id in set_channels["channels"]:
        embed = discord.Embed(title='Channel already added',description="Try a channel that's not already added",color=discord.Colour.dark_blue())

    else:
        set_channels["channels"].append(ctx.channel.id)
        write_json("set_channels.json", set_channels)
        embed = discord.Embed(title='Channel added',description="Type `f.start` to start a new round",color=discord.Colour.brand_green())

    await ctx.channel.send(embed = embed)

@bot.command()
async def remove(ctx):
    if ctx.channel.id in set_channels["channels"]:
        set_channels["channels"].remove(ctx.channel.id)
        write_json("set_channels.json", set_channels)
        embed = discord.Embed(title='Channel Removed Successfully', description = "Type `f.set` to add the channel back", color = discord.Colour.brand_green())

    else:
        embed = discord.Embed(title='Channel not in list', description="Type `f.set` to add the channel back", color = discord.Colour.brand_green())

    await ctx.channel.send(embed = embed)
        
        

@bot.command()
async def start(ctx):
    channel_id = ctx.channel.id
    if channel_id not in set_channels["channels"]:
        embed = discord.Embed(title='Channel not added',description='Type `f.set` to add the channel',color=discord.Colour.dark_blue())
        await ctx.channel.send(embed = embed)
        
    elif channel_id in going_on:
        embed = discord.Embed(title = "A round is already goin on you cannot start a new one :pensive:", color = discord.Colour.red())
        embed.set_footer(text = "Try f.end to end the round")
        await ctx.channel.send(embed = embed)

    else:
        channel = Channel(ctx.channel.name, ctx.channel.id)
        channel_id = ctx.channel.id
        going_on.append(channel_id)
        channels[channel_id] = channel
        channel.going_on = True
        channels[channel_id].going_on = True
        embed = discord.Embed(title = 'Starting Round', color = discord.Colour.dark_blue())
        embed.set_image(url = "https://media.discordapp.net/attachments/1265372975771680829/1267953312045600888/images.png?ex=66aaa90b&is=66a9578b&hm=59dc114e1173c386da772ae817bd47ce4cbb0deb23d427ef7eed5bac337396c3&=&format=webp&quality=lossless")
        await ctx.channel.send(embed = embed)
        while channel.going_on:
            channel.going_on = True
            channels[channel_id].going_on = True
            answer, question = generator()
            channel.skippable = True
            channel.hint = answer
            embed = discord.Embed(title = f"Level {channel.level}", color = 0xf1c40f)
            embed.set_image(url = f"https://flagcdn.com/w320/{question.lower()}.png")
            embed.set_footer(text = "⏳Try guessing in 90 secs....")
            await ctx.channel.send(embed = embed)
            def check(m):
                a = (m.channel == ctx.channel and m.content.lower() == answer.lower() and m.author.name != bot.user.name) or channel.skipped == True or m.content == "f.end"
                return a
            try:
                guess = await bot.wait_for('message', check = check, timeout = 60)

            except asyncio.TimeoutError:
                embed = discord.Embed(title = f"{int(30)} seconds left to answer", colour = discord.Colour.orange())
                embed.set_image(url = f"https://flagcdn.com/w320/{question.lower()}.png")
                hint_skip = ["You can skip level using f.skip", "You can get a hint using f.hint"]
                footer_message = random.choice(hint_skip)
                embed.set_footer(text = footer_message)
                await ctx.channel.send(embed = embed)

                def check_2(m_2):
                    a_2 = (m_2.channel == ctx.channel and m_2.content.lower() == answer.lower() and m_2.author.name != bot.user.name) or channel.skipped == True or m_2.content == "f.end"
                    return a_2

                try:
                    guess_2 = await bot.wait_for('message', check = check_2, timeout = 30)

                except asyncio.TimeoutError:
                    embed = discord.Embed(title = "Answer couldn't be found!!!", description = f"Correct answer was {answer}", color = discord.Colour.red())
                    embed.add_field(name = "Round record: ", value = f"**{channel.level -1}** points")
                    await ctx.channel.send(embed = embed)
                    channels[channel_id].reset()
                    going_on.remove(channel_id)
                    if channel.level != 1:
                        lb_embed = discord.Embed(title = "Round Leaderboard!!!", description = lb_creator(channel.lb_list, channel.lb_dict), color = discord.Colour.magenta())
                        a = [True, False]
                        if random.choice(a):
                            lb_embed.set_footer(text = "You can support the bot by inviting it to your server and voting for it")
                        await ctx.channel.send(embed = lb_embed)
                    break

                else:
                    if channel.skipped:
                        embed = discord.Embed(titel = "Skipping the round", description = "Moving onto the next round", colour = discord.Colour.green())
                        channel.skipped = False

                    elif guess_2.content.lower() == answer.lower():
                        embed = discord.Embed(title = "WOOHOO!!", description = f"Answer has been found by {guess_2.author.mention}", colour = discord.Colour.green())
                        embed.set_footer(text = "⏳Starting round in 10 seconds...")
                        await guess_2.add_reaction("⭐")
                        channels[channel_id].reset()
                        channel.skippable = False
                        channel.lb_list, channel.lb_dict = lb(guess_2.author.id, channel.lb_list, channel.lb_dict)
                        lb_embed = discord.Embed(title = "Current Leaderboard!!!", description = lb_creator(channel.lb_list, channel.lb_dict), color = discord.Colour.magenta())
                        lb_embed.add_field(name = "Next Level:", value = channel.level+1)
                        await ctx.channel.send(embed = lb_embed)
                        

                    elif str(guess_2.content) == "f.end":
                        channel.going_on = False
                        going_on.remove(channel_id)
                        break
                        
                    
                    channel.level += 1
                    
                    channel.hint = " "
                    channel.hint_usable = True
                    await ctx.channel.send(embed = embed)
                    
                    await asyncio.sleep(10)
                         
            else:
                if channel.skipped:
                    embed = discord.Embed(title = "Skipping the round", description = "Moving onto the next round", colour = discord.Colour.green())
                    channel.skipped = False
                elif guess.content.lower() == answer.lower():
                    embed = discord.Embed(title = "WOOHOO!!", description = f"Answer has been found by {guess.author.mention}", colour = discord.Colour.green())
                    embed.set_footer(text = "⏳Starting round in 10 seconds...")
                    await guess.add_reaction("⭐")
                    channels[channel_id].reset()
                    channel.skippable = False
                    channel.lb_list, channel.lb_dict = lb(guess.author.id, channel.lb_list, channel.lb_dict)
                    lb_embed = discord.Embed(title = "Current Leaderboard!!!", description = lb_creator(channel.lb_list, channel.lb_dict), color = discord.Colour.magenta())
                    lb_embed.add_field(name = "Next Level:", value = channel.level+1)
                    await ctx.channel.send(embed = lb_embed)

                elif str(guess.content) == "f.end":
                    channel.going_on = False
                    going_on.remove(channel_id)
                    break
                    
                channel.level += 1
                channel.hint = " "
                channel.hint_usable = True
                await ctx.channel.send(embed = embed)
                await asyncio.sleep(10)

@bot.command()
async def hint(ctx):
    try:
        embed = channels[ctx.channel.id].get_hint()
    except KeyError or IndexError:
        embed = discord.Embed(title = 'No round is going on!!', description = 'type `f.start` to start a round', color = discord.Colour.red())
    await ctx.channel.send(embed = embed)

@bot.command()
async def skip(ctx):
    try:
        embed = channels[ctx.channel.id].skip()
    except KeyError:
        embed = discord.Embed(title = 'No round is going on!!', description = 'type `f.start` to start a round', color = discord.Colour.red())
    await ctx.channel.send(embed = embed)
    
@bot.command()
async def end(ctx):
    try:
        embed = channels[ctx.channel.id].end()
    except KeyError:
        embed = discord.Embed(title = 'No round is going on!!', description = 'type `f.start` to start a round', color = discord.Colour.red())
    await ctx.channel.send(embed = embed)

@bot.command()
async def help(ctx):
    await ctx.channel.send(embed = help_func())

@bot.command()
async def invite(ctx):
    embed, view = invite_func(bot.user.id)
    await ctx.channel.send(embed = embed, view = view)
                         
bot.run(bot_token)
