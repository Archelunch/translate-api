from fastapi import HTTPException

from app.external.translate import get_translation


def test_translate_succes():
    test_data = None
    try:
        test_data = get_translation("nice", "en", "de")
    except HTTPException:
        pass
    assert test_data is not None


def test_translate_failed_language():
    test_data = None
    try:
        test_data = get_translation("nice", "en", "nde")
    except HTTPException as e:
        assert e.status_code == 400
    assert test_data is None


def test_translate_failed_word():
    test_data = None
    try:
        test_data = get_translation("nceg2", "en", "de")
    except HTTPException as e:
        assert e.status_code == 404
    assert test_data is None
