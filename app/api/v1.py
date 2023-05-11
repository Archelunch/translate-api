from core.crud import create, delete, find, find_word
from core.schemas import Word
from external.translate import get_translation
from fastapi import APIRouter, HTTPException

v1 = APIRouter(tags=["v1"])


@v1.get('/word', status_code=201, response_model=Word)
async def get_word(q: str, source_code: str, target_code: str):
    q = q.lower()
    word = await find_word(q, source_code, target_code)
    if word is None:
        word_data = get_translation(q, source_code, target_code)
        word = await create(word_data)
    word = Word(**word)
    return word


@v1.get('/words')
async def get_words_list(word: str = "", skip: int = 0, limit: int = 10,
                         source_code: str = "", target_code: str = "", sorting: int = 1,
                         include_translations: bool = False, include_definitions: bool = False):
    if word == "" and source_code == "" and target_code == "":
        raise HTTPException(status_code=400,
                            detail="It's required to provide at least one parameter: word, source_code, target_code")

    if sorting != -1 and sorting != 1:
        raise HTTPException(status_code=400,
                            detail="Sorting can be 1 or -1")

    words = await find(word, skip, limit, source_code, target_code, sorting, include_translations, include_definitions)
    if len(words) == 0:
        raise HTTPException(status_code=404, detail="Nothing was found")

    return [Word(**document) for document in words]


@v1.delete('/word')
async def delete_word(q: str, source_code: str, target_code: str):
    q = q.lower()
    result = await delete(q, source_code, target_code)
    if result > 0:
        return {'deleted count':  result}
    else:
        raise HTTPException(status_code=404, detail="Word is not found")
