import pytest
import asyncio
import pytest_asyncio
from dice import parse_roll_input, roll_dice

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
    assert test_roll == ['-1','4d6']