import pytest
import asyncio
import pytest_asyncio
from dice import parse_roll_input, roll_dice

# =========================================================
# Testing for parse_roll_input()
# =========================================================
@pytest.mark.asyncio
async def test_parsing_empty_roll():
    test_roll = await parse_roll_input('')
    assert test_roll == None

@pytest.mark.asyncio
async def test_parsing_simple_roll():
    test_roll = await parse_roll_input('4d6')
    assert test_roll == ['4d6']

@pytest.mark.asyncio
async def test_parsing_roll_with_plus_modifier():
    test_roll = await parse_roll_input('4d6+4')
    assert test_roll == ['+4','4d6']

@pytest.mark.asyncio
async def test_parsing_roll_with_minus_modifier():
    test_roll = await parse_roll_input('4d6-1')
    assert test_roll == ['-1','4d6']

@pytest.mark.asyncio
async def test_parsing_roll_with_two_dice_and_modifier():
    test_roll = await parse_roll_input('4d6+2d10-1')
    assert test_roll == ['-1','4d6','2d10']

@pytest.mark.asyncio
async def test_parsing_roll_value_error():
    with pytest.raises(ValueError) as excinfo:
        test_roll = await parse_roll_input('4d6*2d10-1')
        assert test_roll == ['-1','4d6','2d10']
    assert str(excinfo.value) == ('Illegal character found. '
                                  'Please enter a roll without '
                                  'using *, /, !, @, #, $, %, etc.')

# =========================================================
# Testing for roll_dice()
# =========================================================
@pytest.mark.asyncio
async def test_empty_message():
    test_outcome = await roll_dice('')
    assert test_outcome == 'Hey! You forgot your message! Try again.'

@pytest.mark.asyncio
async def test_empty_space_message():
    test_outcome = await roll_dice('     ')
    assert test_outcome == ('Sorry! There was something wrong in '
                            'your message: Illegal character found. '
                            'Please enter a roll without using '
                            '*, /, !, @, #, $, %, etc.')

@pytest.mark.asyncio
async def test_basic_roll():
    test_outcome = await roll_dice('4d6')
    assert test_outcome == '4d6'

@pytest.mark.asyncio
async def test_basic_roll_with_modifier():
    test_outcome = await roll_dice('4d6+3')
    assert test_outcome == '+3'

@pytest.mark.asyncio
async def test_basic_roll_with_two_dice():
    test_outcome = await roll_dice('4d6+2d10')
    assert test_outcome == '4d6+2d10'

@pytest.mark.asyncio
async def test_basic_roll_with_two_dice_and_modifier():
    test_outcome = await roll_dice('4d6+2d10+5')
    assert test_outcome == '+5'

@pytest.mark.asyncio
async def test_invalid_message_with_symbols():
    test_outcome = await roll_dice('#$!VNDads')
    assert test_outcome == ('Sorry! There was something wrong in '
                            'your message: Illegal character found. '
                            'Please enter a roll without using '
                            '*, /, !, @, #, $, %, etc.')
    
    