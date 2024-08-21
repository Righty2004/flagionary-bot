import random
import json
import discord
from flag_data import flags
from discord.ui import Button, View

def write_json(file, content):
    with open(file, 'w') as json_file:
        json.dump(content, json_file)
        return

def read_json(file):
    content = {"channels" : []}
    try:
        with open(file, 'r') as json_file:
            return json.load(json_file)
        
    except FileNotFoundError:
        write_json(file, content)
        return read_json(file)


class Channel:
    def __init__(self, name, id, ):
        self.name = name
        self.id = id
        self.going_on = False
        self.skippable = False
        self.hint_usable = True
        self.skipped = False
        self.hint = str()
        self.hints_left = 6
        self.skips_left = 3
        self.lb_list = list()
        self.lb_dict = dict()
        self.level = 1

    def reset(self):
        self.skippable = True
        self.hint_usable = True
        self.skipped = False
        self.hint = str()

    def get_hint(self):
        if not(self.going_on):
            embed = discord.Embed(title = 'No round is going on!!', description = 'type `f.start` to start a round', color = discord.Colour.red())

        elif not(self.hint_usable):
            embed = discord.Embed(title = 'Hint has already been used!!', description = 'LOl you can only know the initial using hint, nothing more', color = discord.Colour.red())
            embed.set_footer(text = 'Try using f.skip for skipping')
            
        elif self.hints_left == 0:
            embed = discord.Embed(title = 'No hints left!!', description = 'Now everything is upto you without hints LOl', color = discord.Colour.red())
            embed.set_footer(text = 'Try using f.skip for skipping')

        elif self.hint == " ":
            embed = discord.Embed(title = "Atleast wait for next level to start :joy:", color = discord.Colour.red())
            
        else:
            hint = hint_creator(self.hint)
            embed = discord.Embed(title = 'Hint has been used', description = hint, color = discord.Colour.green())
            self.hints_left -= 1
            self.hint_usable = False
            embed.set_footer(text = f"Hints left: {self.hints_left}")
        return embed

    def skip(self):
        if not(self.going_on):
            embed = discord.Embed(title = 'No round is going on!!', description = 'type `f.start` to start a round', color = discord.Colour.red())

        elif not(self.skippable):
            embed = discord.Embed(title = "Atleast wait for next level to start :joy:", color = discord.Colour.red())

        elif self.skips_left == 0:
            embed = discord.Embed(title = 'No skips left!!', description = 'Now everything is upto you without skips LOl', color = discord.Colour.red())
            
        else:
            self.skipped = True
            self.skippable = False
            self.skips_left -= 1
            embed = discord.Embed(title = "Skip has been used" ,color = discord.Colour.green())
            embed.set_footer(text = f"Skips left: {self.skips_left}")
        return embed

    def end(self):
        if not(self.going_on):
            embed = discord.Embed(title = 'No round is going on!!', description = 'type `f.start` to start a round', color = discord.Colour.red())

        else:
            self.going_on = False
            embed = discord.Embed(title="Round has been ended",description=lb_creator(self.lb_list, self.lb_dict),color=discord.Colour.brand_green())
            embed.add_field(name="Final score",value=f"{self.level-1}")
            self.reset
                
        return embed
    
def generator():
    return random.choice(flags)
    
def lb(user, lb_list, lb_dict):
    if user in lb_dict.keys():
        lb_dict[user] += 1

    else:
        lb_dict[user] = 1
        lb_list.append(user)
    for i in range(len(lb_list)-1):
        for i in range(len(lb_list)-1):
            first_channel = lb_list[i]
            second_channel = lb_list[i+1]
            first = lb_dict[lb_list[i]]
            second = lb_dict[lb_list[i+1]]

            if first < second:
                lb_list[i] = second_channel
                lb_list[i+1] = first_channel
    return lb_list, lb_dict

def lb_creator(lb_list, lb_dict):
    leaderboard = ''
    for i in range(len(lb_list)):
        name = f"<@{lb_list[i]}>"
        score = lb_dict[lb_list[i]]
        leaderboard += f"{i+1}.{name}: **{score}** points\n"
    return leaderboard
        
def hint_creator(answer):
    hint = answer[0]
    for i in range(1, len(answer)):
        if answer[i] != ' ':
            hint += ' _'

        else:
            hint += ' '
            
    return f"`{hint}`"

def help_func():
    embed = discord.Embed(title = "Flagionary", color = 0xf1c40f)
    embed.add_field(name = '`f.set`', value = "Used to add a channel, a game can only be played in added channels.", inline = False)
    embed.add_field(name = '`f.remove`', value = "Used to remove a channel.", inline = False)
    embed.add_field(name = '`f.start`', value = "Used to start a game, you get 90 seconds to guess the flag.", inline = False)
    embed.add_field(name = '`f.hint`', value = "Gives you the initial of the country, can be used only 5 times per game.", inline = False)
    embed.add_field(name = '`f.skip`', value = "Used to skip a level, can be used only 3 times per game.", inline = False)
    embed.add_field(name = '`f.end`', value = "Used to end a game.", inline = False)
    embed.add_field(name = '`f.invite`', value = "Gives you the invite link to add the bot to your server.", inline = False)
    embed.add_field(name = 'Creator and owner of the bot', value = "<@900394377623519304> / easyone_1")
    embed.set_footer(text = "Ty for using the bot, you can dm the owner about any queries and suggestion about the bot.")
    return embed

def invite_func(client_id):
    button = Button(
        label='Invite to server',
        url=
        f"https://discord.com/oauth2/authorize?client_id={client_id}&permissions=412317240384&integration_type=0&scope=bot"
    )
    view = View()
    view.add_item(button)
    embed = discord.Embed(
        title=
        "Ty for using the bot, You can invite it to your server by clicking the button below",
        color=discord.Colour.dark_blue())
    return embed, view




