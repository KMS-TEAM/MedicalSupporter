import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.matcher import Matcher
from common import Words, Chunk, Transcription
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from spacy.tokens import Span
import csv

class SimpleNLP():

    # Init Simple NLP Object
    def __init__(self):
        self.file_url = ''
        self.data = ''
        self.graph = []
        self.nlp = spacy.load("en_core_web_sm")

    def read_csv(self, url):
        self.sents = []
        with open(self.file_url,'rt') as f:
            data = csv.reader(f)
            for line in data:
                self.sents.append(line)
        return self.sents


    def read_txt(self, url):
        fd =  open(self.file_url,mode ='r', encoding='utf-8')
        self.data = fd.read().strip()
        self.doc = self.nlp(self.data)
        self.sents = []
        for sent in self.doc.sents:
            self.sents.append(sent)
        #    print(sent)
        return self.sents

    #def import_data(self, data):

    #def processing(self, data):
    #    self.import_data(data)

    def word(self, stop_word = False):
        self.words = []
        if (stop_word == False):
            for word in self.doc:
                temp = Words()
                temp.text = word.text
                temp.tagging = word.pos_
                self.words.append(temp)
            return self.words
        else:
            for word in self.doc:
                if word.is_stop == False:
                    temp = Words()
                    temp.text = word.text
                    temp.tagging = word.pos_
                    self.words.append(temp)
            return self.words

    def noun_chunk(self):
        self.noun_chunk = []
        for chunk in self.doc.noun_chunks:
            temp = Chunk()
            temp.text=chunk.text
            temp.root_text=chunk.root.text
            temp.root_dep=chunk.root.dep_
            temp.root_head_text=chunk.root.head.text
            self.noun_chunk.append(temp)
        return self.noun_chunk

    def get_entities(self, sent):
        ## chunk 1
        ent1 = ""
        ent2 = ""
        prv_tok_dep = ""  # dependency tag of previous token in the sentence
        prv_tok_text = ""  # previous token in the sentence
        prefix = ""
        modifier = ""

        for tok in self.nlp(str(sent)):
            ## chunk 2
            # if token is a punctuation mark then move on to the next token
            if tok.dep_ != "punct":
                # check: token is a compound word or not
                if tok.dep_ == "compound":
                    prefix = tok.text
                    # if the previous word was also a 'compound' then add the current word to it
                    if prv_tok_dep == "compound":
                        prefix = prv_tok_text + " " + tok.text

                # check: token is a modifier or not
                if tok.dep_.endswith("mod") == True:
                    modifier = tok.text
                    # if the previous word was also a 'compound' then add the current word to it
                    if prv_tok_dep == "compound":
                        modifier = prv_tok_text + " " + tok.text

                ## chunk 3
                if tok.dep_.find("subj") == True:
                    ent1 = modifier + " " + prefix + " " + tok.text
                    prefix = ""
                    modifier = ""
                    prv_tok_dep = ""
                    prv_tok_text = ""

                    ## chunk 4
                if tok.dep_.find("obj") == True:
                    ent2 = modifier + " " + prefix + " " + tok.text

                ## chunk 5
                # update variables
                prv_tok_dep = tok.dep_
                prv_tok_text = tok.text

        return [ent1.strip(), ent2.strip()]

    def get_entitiy_pairs(self, sents):
        self.entity_pairs = []
        for sent in sents:
            self.entity_pairs.append(self.get_entities((sent)))
        return self.entity_pairs

    def get_relation(self):
        self.relations = []
        for sent in self.sents:
            doc = self.nlp(str(sent))
            # Matcher class object
            matcher = Matcher(self.nlp.vocab)
            # define the pattern
            pattern = [{'DEP': 'ROOT'},
                       {'DEP': 'prep', 'OP': "?"},
                       {'DEP': 'agent', 'OP': "?"},
                       {'POS': 'ADJ', 'OP': "?"}]
            matcher.add("matching_1", [pattern])
            matches = matcher(doc)
            k = len(matches) - 1
            span = doc[matches[k][1]:matches[k][2]]
            self.relations.append(span.text)
        return self.relations

    def get_KG(self):
        entity_pairs = self.get_entitiy_pairs()
        relations = self.get_relation()
        # extract subjec
        source = [i[0] for i in entity_pairs]
        # extract object
        target = [i[1] for i in entity_pairs]
        kg_df = pd.DataFrame({'source': source, 'target': target, 'edge': relations})
        # create a directed-graph from a dataframe
        G = nx.from_pandas_edgelist(kg_df, "source", "target",
                                    edge_attr=True, create_using=nx.MultiDiGraph())
        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(G)
        nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos=pos)
        plt.show()
        kg_df.to_csv(path_or_buf = r"data/output/kg.csv")
        
    def source(self):
        entity_pairs = self.get_entitiy_pairs()
        self.source = [i[0] for i in entity_pairs]
        # extract object
        return self.source
      
    def target(self):
        entity_pairs = self.get_entitiy_pairs()
        self.target = [i[1] for i in entity_pairs]
        return self.target

