import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk import word_tokenize
from nltk import WordNetLemmatizer
import string

path = '/Users/alinajam/Desktop/smsspamcollection/SMSSpamCollection.csv'
data = pd.read_csv(path)

def clean_text(unprocessed_string):
    stop_words = stopwords.words()
    cleaned_text = ""
    unprocessed_string = np.str.lower(unprocessed_string)
    unprocessed_string = np.str.replace(unprocessed_string, "'", "")

    text_tokens = word_tokenize(unprocessed_string)
    for word in text_tokens:
        if word not in string.punctuation:
            if word not in stop_words:
                if len(word) > 1:
                    cleaned_text = cleaned_text + " " + word
    cleaned_text = ("").join(cleaned_text)
    return cleaned_text


def stematize_sentence(sentence):
    sb_stemmer = SnowballStemmer('english')
    wordnet_lemmatizer = WordNetLemmatizer()

    token_words = word_tokenize(sentence)
    stem_sentence = []
    for word in token_words:
        lem_word = wordnet_lemmatizer.lemmatize(word)
        stem_sentence.append(sb_stemmer.stem(lem_word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)


def term_count(sentence):
    document_frequency = {}
    tokens = word_tokenize(sentence)
    for i in range(len(tokens)):
        token = tokens[i]
        try:
            document_frequency[token].add(i)
        except:
            document_frequency[token] = {i}
    for i in document_frequency:
        document_frequency[i] = len(document_frequency[i])
    return document_frequency


def term_frequency(word_count, sentence):
    term_freq = {}
    for term in word_count:
        tf = word_count.get(term) / len(word_tokenize(sentence))
        term_freq[term] = tf
    return term_freq


def inverse_document_frequency(corpus, term_frequencies):
    idfs = []
    for term_freq in term_frequencies:
        inv_doc_freq = {}
        for document in corpus:
            for term in term_freq:
                if term in word_tokenize(document):
                    try:
                        inv_doc_freq[term] += 1
                    except:
                        inv_doc_freq[term] = 1
        idfs.append(inv_doc_freq)

    for i in range(len(idfs)):
        idf = idfs[i]
        for term in idf:
            idf[term] = np.log(len(corpus) / idf.get(term))
    return idfs


def tf_idf(corpus):
    document_frequencies = []
    for document in corpus:
        document_frequencies.append(term_frequency(term_count(document), document))
    inverse_document_frequencies = inverse_document_frequency(corpus, document_frequencies)

    output_extracted_features = []
    for document_id in range(len(document_frequencies)):
        document = document_frequencies[document_id]
        inv_document_data = inverse_document_frequencies[document_id]
        tfidf_features = {}
        for term in document:
            tfidf_features[term] = document.get(term) * inv_document_data.get(term)
        output_extracted_features.append(tfidf_features)
    return output_extracted_features


# rowIndex = 0
# docFrequences = []
# for article in data.iloc[:, 9]:
#     processedArticle = clean_text(article)
#     processedArticle = stematize_sentence(processedArticle)
#     processedArticle = clean_text(processedArticle)
#     processedArticle = stematize_sentence(processedArticle)
#     data.iloc[rowIndex, 9] = processedArticle
#     rowIndex += 1
#
# TF_IDF_Features = tf_idf(data.iloc[:, 9])
# data['TF-IDF features'] = TF_IDF_Features
# print(data)