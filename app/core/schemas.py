from typing import Any, Dict, List, Optional

from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class WordDefinition(BaseModel):
    word_type: Optional[str]
    definition: Optional[str]
    example: Optional[str]
    synonyms: Optional[List[str]] = Field(default=None, exclude_unset=True)

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        # excluding empty fields
        _ignored = kwargs.pop('exclude_none')
        return super().dict(*args, exclude_none=True, **kwargs)


class Word(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    word: str
    source_code: str
    target_code: str
    definitions: Optional[List[WordDefinition]] = Field(default=None, exclude_unset=True)
    examples: Optional[List[str]]
    translations: Optional[Dict[str, List[str]]] = Field(default=None, exclude_unset=True)

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        # excluding empty fields
        _ignored = kwargs.pop('exclude_none')
        return super().dict(*args, exclude_none=True, **kwargs)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
