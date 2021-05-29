from spacy.lang.en import English
import spacy
import en_core_web_sm
from example import example

def spacy_tokenizing(nlp, text):
    my_doc = nlp(text)
    token_list = []
    for token in my_doc:
        token_list.append(token.text)
    print(token_list)

def spacy_sentencizer(nlp, text):
    nlp.add_pipe('sentencizer')
    doc = nlp(text)
    sents_list = []
    for sent in doc.sents:
        sents_list.append(sent.text)
    print(sents_list)

def eng_stop_words(num):
    spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
    print('Number of stop words: %d' % len(spacy_stopwords))
    print('Some stop words example: %s' % list(spacy_stopwords)[:num])

def remove_stopwords(nlp, text):
    filtered_sent = []
    doc = nlp(text)

    for word in doc:
        if word.is_stop == False:
            filtered_sent.append(word)
    return filtered_sent

# Something woring here ....
def stremming(nlp, text):
    word_stremed = []
    lem = nlp(text)
    for word in lem:
        word_stremed.append(word.lemma_)
        print(word.text, word.lemma_)
    return word_stremed

def spacy_tagging(text):
    nlp = en_core_web_sm.load()
    docs = nlp(text)
    for word in docs:
        print(word.text, word.pos_)

if __name__ == "__main__":

    example.printSomething(example, "Hello !!!")

    f = open("text.txt", "r")
    text = f.read()

    nlp = English()

    spacy_tokenizing(nlp, text)
    spacy_sentencizer(nlp, text)

    eng_stop_words(20)

    print(remove_stopwords(nlp, text))
    # print(stremming(nlp, text))
    spacy_tagging(text)

