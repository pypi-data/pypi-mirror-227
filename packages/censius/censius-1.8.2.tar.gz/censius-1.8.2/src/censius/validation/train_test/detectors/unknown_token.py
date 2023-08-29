import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import words
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from multiprocessing import Pool, cpu_count
import string

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("words")


class UnknownTokenDetector:
    def __init__(self, training_sentences, **preprocess_args):
        train_vocab = set(words.words())  # Vocabulary from NLTK corpus
        self.stop_words = set(stopwords.words("english"))
        for sent in training_sentences:
            sent = sent.translate(str.maketrans("", "", string.punctuation))
            words_in_sent = word_tokenize(sent.lower())
            for word in words_in_sent:
                if word not in self.stop_words:
                    train_vocab.add(word)

        self.train_vocab = train_vocab
        self.preprocess_args = preprocess_args or {}
        self.lemmatizer = WordNetLemmatizer()

    def calculate_unknown_token_percentage(self, test_sentences):
        with Pool(cpu_count()) as pool:
            results = pool.map(self.process_sentence, test_sentences)

        total_unknown_tokens = sum(len(result[0]) for result in results)
        total_tokens = sum(len(result[1]) for result in results)

        total_unknown_percentage = (
            (total_unknown_tokens / total_tokens) * 100 if total_tokens else 0
        )
        return total_unknown_percentage

    def process_sentence(self, sentence):
        if self.preprocess_args.get("remove_punctuation", True):
            sentence = sentence.translate(str.maketrans("", "", string.punctuation))

        tokens = word_tokenize(sentence)

        filtered_tokens = [
            self.lemmatizer.lemmatize(token)
            if self.preprocess_args.get("do_lemmatization", False)
            else token
            for token in tokens
            if self.preprocess_args.get("remove_stopwords", True)
            and token.lower() not in self.stop_words
        ]

        unknown_tokens = [
            token for token in filtered_tokens if token not in self.train_vocab
        ]
        return unknown_tokens, filtered_tokens
