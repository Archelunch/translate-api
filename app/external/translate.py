from fastapi import HTTPException
from googletrans import LANGUAGES, Translator


def get_translation(word: str, source_code: str, target_code: str) -> dict:
    word = word.lower()
    if source_code in LANGUAGES and target_code in LANGUAGES:
        translator = Translator()
        translation = None
        for _ in range(15):  # to deal with googletrans errors
            try:
                translation = translator.translate(word, src=source_code, dest=target_code)
                break
            except TypeError:
                continue
        if translation is None:
            raise HTTPException(status_code=503, detail="Google Translate isn't available at this moment")

        word_origin = translation.extra_data['parsed'][0][0]
        if word_origin is None:
            raise HTTPException(status_code=404, detail="Word was not found in Google Translate")

        try:
            definitions = translation.extra_data['parsed'][3][1][0]
        except Exception:
            definitions = []
        def_list = []
        for defin in definitions:
            word_type = defin[0]
            ds = defin[1]
            for d in ds:
                word_dict = {"word_type": word_type}
                word_dict['definition'] = d[0]
                if len(d) > 1:
                    word_dict['example'] = d[1]

                try:
                    word_dict['synonyms'] = [syn[0] for syn in d[5][0][0]]
                except Exception:
                    word_dict['synonyms'] = []
                def_list.append(word_dict)
        if len(def_list) == 0:
            def_list = None

        try:
            examples = translation.extra_data['parsed'][3][2][0]
            parsed_examples = [e[1].replace("<b>", "").replace("</b>", "") for e in examples]
        except Exception:
            parsed_examples = None

        translations_list = translation.extra_data['parsed'][3][5][0]
        trans_dict = {}
        for tr in translations_list:
            trans_dict[tr[0]] = [k[0] for k in tr[1]]

        response = {
                    'word': word, 'definitions': def_list,
                    'examples': parsed_examples, 'translations': trans_dict,
                    'source_code': source_code, 'target_code': target_code
                    }
        return response
    else:
        raise HTTPException(status_code=400, detail="Language is not found")
