import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO
import os
import random
from dotenv import load_dotenv

load_dotenv()
command_prefix = os.getenv('COMMAND_PREFIX')
bot = commands.Bot(command_prefix=command_prefix)

landingNumbers = [1,2,3,4,5,6]

# Append 2 dice images onto one blank image
def create_2_dice_image( die1: str, die2: str):
  finalImage = Image.new('RGBA', (101,50), color=(0,0,0,0))
  firstDie = Image.open(die1)
  secondDie = Image.open(die2)
  finalImage.paste(firstDie, box=(1,0), mask=0)
  finalImage.paste(secondDie, box=(52,0), mask=0)

  return finalImage

def rollDice(numOfDice, landingNumbers):
  if numOfDice == 1:
    return random.choice(landingNumbers)
  else:
    return random.choice(landingNumbers), random.choice(landingNumbers)

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user}')

@bot.command()
async def diceroll(ctx, subCommand: str=None):
  # Prints usage
  if subCommand is None:
    await ctx.send(f'```\nUsage: {command_prefix}diceroll # \n\n[#] - can be 1 or 2 dice.\n```')
    return

  # Roll 1 die
  if subCommand == '1':
    rollNumber = str(rollDice(1,landingNumbers))
    await ctx.send(file=discord.File(f'images/Die_{rollNumber}.png'))
    await ctx.send(f'>>> {ctx.author.mention} rolls a {rollNumber}!')

  # Roll 2 dice
  elif subCommand == '2':
    rollNumber1, rollNumber2 = rollDice(2, landingNumbers)
    # Place 2 die images into one canvas
    with BytesIO() as image_binary:
      create_2_dice_image(
        (f'images/Die_{str(rollNumber1)}.png'),
        (f'images/Die_{str(rollNumber2)}.png')
      ).save(image_binary, 'PNG')
      image_binary.seek(0)

      await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
      await ctx.send(f'>>> {ctx.author.mention} rolls a {rollNumber1} and {rollNumber2}!')

  # Invalid subcommand
  else:
    await ctx.send('>>> Specify `1` or `2` dice to roll.')

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send('Command not found.')

bot.run(os.getenv('TOKEN'))