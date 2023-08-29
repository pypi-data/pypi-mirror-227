rules_data = {
    "detect_duplicates": [
        {
            "params": {
                "preprocess_args": {
                    "ignore_case": False,
                    "remove_punctuation": True,
                    "normalize_unicode": True,
                    "remove_stopwords": True,
                },
                "threshold": {"lte": 20},
            }
        }
    ],
    "detect_unknown_tokens": [
        {
            "params": {
                "preprocess_args": {
                    "remove_punctuation": True,
                    "remove_stopwords": True,
                    "do_lemmatization": False,
                },
                "threshold": {"lte": 20},
            }
        }
    ],
    "text_complexity_distribution": [
        {
            "params": {
                "preprocess_args": {
                    "remove_punctuation": True,
                    "remove_stopwords": True,
                },
                "threshold": {"lte": 10},
            }
        }
    ],
}
