import json
import sys

sys.path.append("./app")
from core.crud import create, delete, find, find_word


async def test_create():
    with open("./tests/test_data.json") as f:
        test_data = json.load(f)
    resp = await create(test_data)
    assert resp is not None
    await delete(test_data['word'], test_data['source_code'], test_data['target_code'])


async def test_delete_existed_word():
    with open("./tests/test_data.json") as f:
        test_data = json.load(f)
    resp = await create(test_data)
    count = await delete(test_data['word'], test_data['source_code'], test_data['target_code'])
    assert count == 1


async def test_delete_not_existed_word():
    with open("./tests/test_data.json") as f:
        test_data = json.load(f)
    count = await delete(test_data['word'], test_data['source_code'], test_data['target_code'])
    assert count == 0


async def test_find_existed_word():
    with open("./tests/test_data.json") as f:
        test_data = json.load(f)
    await create(test_data)
    resp = await find_word(test_data['word'], test_data['source_code'], test_data['target_code'])
    assert resp['word'] == test_data['word']
    await delete(test_data['word'], test_data['source_code'], test_data['target_code'])


async def test_find_not_existed_word():
    with open("./tests/test_data.json") as f:
        test_data = json.load(f)
    resp = await find_word(test_data['word'], test_data['source_code'], test_data['target_code'])
    assert resp is None


async def test_find_list_partial():
    with open("./tests/test_data_list.json") as f:
        test_data = json.load(f)
    for t in test_data:
        await create(t)
    resps = await find("ni")
    assert len(resps) == len(test_data)
    for t in test_data:
        await delete(t['word'], t['source_code'], t['target_code'])


async def test_find_list_partial_not_existed():
    with open("./tests/test_data_list.json") as f:
        test_data = json.load(f)
    for t in test_data:
        await create(t)
    resps = await find("in")
    assert len(resps) == 0
    for t in test_data:
        await delete(t['word'], t['source_code'], t['target_code'])
