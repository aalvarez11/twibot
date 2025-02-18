from random import randint
import re

async def roll_die(num_of_sides: int):
    return randint(1, num_of_sides)

async def parse_roll_input(msg: str):
    # trim excess characters
    cropped_msg = re.sub(r'[^\d+\-*\/d]', '', msg)
    # get the modifier portion of the command, if any
    roll_modifier = re.search(r'([\+|-]+\d+$)', cropped_msg).group() if re.search(r'([\+|-]+\d+$)', cropped_msg) else ''
    # make a list with sets matching xdy format where x & y are numbers
    rolls = re.split(r'(\d+d\d+)', cropped_msg)
    # remove the modifier from the list
    if roll_modifier in rolls: rolls.remove(roll_modifier)
    rolls.insert(0, roll_modifier)
    # remove empty strings from the list
    rolls[:] = [i for i in rolls if i != '']
    
    if rolls == [] :
        return None
    else:
        return rolls 
    
async def roll_dice(msg: str):
    if not msg: return 'Hey! You forgot your message! Try again.'

    parsed_roll = parse_roll_input(msg)

    dice_count = sides = roll_modifier = 0
    
    
    return msg