from random import randint
import re

async def parse_roll_input(msg: str):
    # only simple rolls allowed
    if re.search(r'[^0-9a-zA-Z\+-]+', msg) is not None: 
        raise ValueError('Illegal character found. Please enter a roll without using *, /, !, @, #, $, %, etc.')
    # trim excess characters
    cropped_msg = re.sub(r'[^\d+\-*\/d]', '', msg)
    # get the modifier portion of the command, if any
    roll_modifier = re.search(r'([\+|-]+\d+$)', cropped_msg).group() if re.search(r'([\+|-]+\d+$)', cropped_msg) else ''
    # make a list with sets matching xdy format where x & y are numbers
    rolls = re.split(r'(\d+d\d+)[^0-9a-zA-Z]+', cropped_msg)
    # remove the modifier from the list
    if roll_modifier != '': rolls.pop()
    rolls.insert(0, roll_modifier)
    # remove empty strings from the list
    rolls[:] = [i for i in rolls if i != '']
    
    if rolls == [] :
        return None
    else:
        return rolls 
    
async def roll_die(single_roll: str):
    dice_count = sides = 0

    dice_count, sides = single_roll.split('d')

    result = randint(1, int(sides)) * int(dice_count)
    return result

async def roll_dice(msg: str):
    roll_result = roll_modifier = 0
    
    if not msg: return 'Hey! You forgot your message! Try again.'

    try:
        parsed_rolls = await parse_roll_input(msg)

        if parsed_rolls is None: raise ValueError('Your message was empty! Try again.')

        for roll in parsed_rolls:
            if roll == parsed_rolls[0] and re.search(r'^[\+|-]+\d+$', roll):
                roll_modifier = parsed_rolls[0]
                return roll_modifier

        return msg
    except ValueError as e:
        return f'Sorry! There was something wrong in your message: {e}'
     