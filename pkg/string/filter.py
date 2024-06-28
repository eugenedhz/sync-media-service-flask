import nltk
from nltk.corpus import stopwords


nltk.download('stopwords')

stopwords_ru = set(stopwords.words('russian'))
stopwords_en = set(stopwords.words('english'))


def get_words_with_no_stopwords(string: str) -> tuple[str]:
	words = set(string.split())
	words -= stopwords_ru
	words -= stopwords_en

	return tuple(words)