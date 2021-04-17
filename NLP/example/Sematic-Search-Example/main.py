import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import spacy
import string
from gensim import corpora
import  gensim
import operator
import re
from spacy.lang.en.stop_words import STOP_WORDS
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from gensim.similarities import MatrixSimilarity
from operator import itemgetter


spacy_nlp = spacy.load('en_core_web_sm')

#create list of punctuations and stopwords
punctuations = string.punctuation
stop_words = spacy.lang.en.stop_words.STOP_WORDS

# function for data cleaning and processing
# This can be further enhanced by adding / removing reg-exps as desired.

def spacy_tokenizer(sentence):
    # remove distracting single quotes
    sentence = re.sub('\'', '', sentence)

    # remove digits adnd words containing digits
    sentence = re.sub('\w*\d\w*', '', sentence)

    # replace extra spaces with single space
    sentence = re.sub(' +', ' ', sentence)

    # remove unwanted lines starting from special charcters
    sentence = re.sub(r'\n: \'\'.*', '', sentence)
    sentence = re.sub(r'\n!.*', '', sentence)
    sentence = re.sub(r'^:\'\'.*', '', sentence)

    # remove non-breaking new line characters
    sentence = re.sub(r'\n', ' ', sentence)

    # remove punctunations
    sentence = re.sub(r'[^\w\s]', ' ', sentence)
    # creating token object
    tokens = spacy_nlp(sentence)

    # lower, strip and lemmatize
    tokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in tokens]

    # remove stopwords, and exclude words less than 2 characters
    tokens = [word for word in tokens if word not in stop_words and word not in punctuations and len(word) > 2]

    # return tokens
    return tokens

def search_similar_movies(search_term):

    query_bow = dictionary.doc2bow(spacy_tokenizer(search_term))
    query_tfidf = movie_tfidf_model[query_bow]
    query_lsi = movie_lsi_model[query_tfidf]

    movie_index.num_best = 5

    movies_list = movie_index[query_lsi]

    movies_list.sort(key=itemgetter(1), reverse=True)
    movie_names = []

    for j, movie in enumerate(movies_list):

        movie_names.append (
            {
                'Relevance': round((movie[1] * 100),2),
                'Movie Title': df_movies['title'][movie[0]],
                'Movie Plot': df_movies['wiki_plot'][movie[0]]
            }

        )
        if j == (movie_index.num_best-1):
            break

    return pd.DataFrame(movie_names, columns=['Relevance','Movie Title','Movie Plot'])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df_movies = pd.read_csv("movies.csv")
#    print(df_movies.head())
#    print(df_movies['wiki_plot'])

    print('Cleaning and Tokenizing...')

    df_movies['wiki_plot_tokenized'] = df_movies['wiki_plot'].map(lambda x: spacy_tokenizer(x))

    movie_plot = df_movies['wiki_plot_tokenized']

    series = pd.Series(np.concatenate(movie_plot)).value_counts()[:100]
    wordcloud = WordCloud(background_color='white').generate_from_frequencies(series)

    plt.figure(figsize=(15, 15), facecolor=None)
    #plt.imshow(wordcloud, interpolation='bilinear')
    #plt.axis('off')
    #plt.show()

    dictionary = corpora.Dictionary(movie_plot)

    # list of few which which can be further removed
    stoplist = set('hello and if this can would should could tell ask stop come go')
    stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
    dictionary.filter_tokens(stop_ids)

    # print top 50 items from the dictionary with their unique token-id
    #dict_tokens = [
    #    [[dictionary[key], dictionary.token2id[dictionary[key]]] for key, value in dictionary.items() if key <= 50]]
    #print(dict_tokens)

    corpus = [dictionary.doc2bow(desc) for desc in movie_plot]

    word_frequencies = [[(dictionary[id], frequency) for id, frequency in line] for line in corpus[0:3]]

    #print(word_frequencies)

    movie_tfidf_model = gensim.models.TfidfModel(corpus, id2word=dictionary)
    movie_lsi_model = gensim.models.LsiModel(movie_tfidf_model[corpus], id2word=dictionary, num_topics=300)

    gensim.corpora.MmCorpus.serialize('movie_tfidf_model_mm', movie_tfidf_model[corpus])
    gensim.corpora.MmCorpus.serialize('movie_lsi_model_mm', movie_lsi_model[movie_tfidf_model[corpus]])

    # Load the indexed corpus
    movie_tfidf_corpus = gensim.corpora.MmCorpus('movie_tfidf_model_mm')
    movie_lsi_corpus = gensim.corpora.MmCorpus('movie_lsi_model_mm')

    #print(movie_tfidf_corpus)
    #print(movie_lsi_corpus)

    movie_index = MatrixSimilarity(movie_lsi_corpus, num_features=movie_lsi_corpus.num_terms)

    # search for movie tiles that are related to below search parameters
    test = search_similar_movies('crime and drugs ')

    print(test)



