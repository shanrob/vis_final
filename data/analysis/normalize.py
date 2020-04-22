import spacy
import unicodedata

nlp = spacy.load('en', parse=False, tag=False, entity=True)

import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

import string

import pkg_resources
from symspellpy import SymSpell, Verbosity

import contractions_map
import re

sym_spell = SymSpell()
dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt")
sym_spell.load_dictionary(dictionary_path, 0, 1)


def remove_prop_nouns(text):
    processed_text = text

    sentence = nlp(text)
    words_to_remove = []

    for e in sentence.ents:
        if e.label_ in ("MONEY", "PERSON"):
            words_to_remove.append(e.text.split())
            processed_text = ' '.join([j for j in text.split() if j not in words_to_remove[0]])

    return processed_text


def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text


def expand_contractions(text, contraction_mapping=contractions_map.CONTRACTION_MAP):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
            if contraction_mapping.get(match) \
            else contraction_mapping.get(match.lower())
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


def remove_stopwords(text, is_lower_case=False):
    stopword_list = nltk.corpus.stopwords.words('english')
    stopword_list.remove('no')
    stopword_list.remove('not')
    stopword_list.remove('under')

    tokens = word_tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))


def words_to_lower(text):
    tokens = word_tokenize(text)
    lowercased_tokens = [token.lower() for token in tokens]
    return ' '.join(lowercased_tokens)


def correct_spelling(sentence):
    new_sentence = []
    words_corrected = []

    tokens = word_tokenize(sentence)

    for word in tokens:
        if word != "knope":
            word = word.lower()
            suggestions = sym_spell.lookup(word, Verbosity.CLOSEST,
                                           max_edit_distance=1, include_unknown=True)
            if str(suggestions[0]._term) != word:
                word = suggestions[0]._term

                words_corrected.append(word)

        new_sentence.append(word)

    return ' '.join(new_sentence)


def lemmatize_text(text):
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text


def preprocess_text(text_list, lemmatize=True, remove_stop=True):
    processed_text = []

    for text in text_list:
        processed = remove_prop_nouns(text)
        processed = remove_accented_chars(processed)
        processed = expand_contractions(processed)
        processed = remove_punctuation(processed)
        processed = words_to_lower(processed)
        processed = correct_spelling(processed)

        if remove_stop == True:
            processed = remove_stopwords(processed)

        if lemmatize == True:
            processed = lemmatize_text(processed)

        processed_text.append(processed)

    return processed_text


def word_distribution(text):
    all_words = []
    for t in text:
        all_words += word_tokenize(t)

    fdist = FreqDist(all_words)
    return fdist.most_common(50)

