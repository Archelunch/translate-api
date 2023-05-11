from typing import Dict, List

from db.mongo import database


async def create(word_data: Dict) -> Dict:
    words_collection = database.get_collection("words_collection")
    result = await words_collection.insert_one(word_data)
    new_word = await words_collection.find_one({"_id": result.inserted_id})
    return new_word


async def find_word(word: str, source_code: str, target_code: str) -> Dict:
    words_collection = database.get_collection("words_collection")
    result = await words_collection.find_one({"word": word, "source_code": source_code, "target_code": target_code})
    return result


async def find(
        word: str = "", skip: int = 0, limit: int = 10,
        source_code: str = "", target_code: str = "", sorting: int = 1,
        include_translations: bool = False, include_definitions: bool = False) -> List:
    projection = {"word": 1, "examples": 1, "source_code": 1, "target_code": 1}
    if include_definitions:
        projection["definitions"] = {"word_type": 1, "definition": 1, "example": 1, "synonyms": 1}
    if include_translations:
        projection["translations"] = 1

    search_params = {}
    if word != "":
        search_params["word"] = {"$regex": word, "$options": "i"}
    if source_code != "":
        search_params['source_code'] = source_code
    if target_code != "":
        search_params['target_code'] = target_code

    words_collection = database.get_collection("words_collection")
    cursor = words_collection.find(
        search_params, projection=projection,
        sort=[("word", sorting)]).skip(skip).limit(limit)
    return [document async for document in cursor]


async def delete(word: str, source_code: str, target_code: str) -> int:
    words_collection = database.get_collection("words_collection")
    result = await words_collection.delete_one({"word": word, "source_code": source_code, "target_code": target_code})
    return result.deleted_count
