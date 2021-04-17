import pandas as pd
from testgraph import neo4jGraph
import simpleNLP as x
def Connect():
    connect = neo4jGraph("neo4j", "1")
    connect.CLEAR()
    connect.CREATE("His dog eats turkey on tuesday My cat eats fish on Saturday")
    result = connect.MATCH()
    connect.UPDATE()
    connect.DELETE()

if __name__ == "__main__":
    #with open('mtsamples.csv', 'r') as f:
    #    col_list = ["sample_name", "transcription"]
    #    my_file=pd.read_csv(f, usecols=col_list)
    #    test = x.SimpleNLP.word(my_file["transcription"][1])
    text = x.SimpleNLP.read_csv('self','/home/nguyen/Github/MedicalSupporter/NLP/SimpleNLP/mtsamples.csv')
