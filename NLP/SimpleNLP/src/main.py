import pandas as pd
import os
from neo4japi import Neo
from simpleNLP import SimpleNLP as xxx
from processing import processing as prc

def Connect():
    connect = Neo("neo4j", "1")
    connect.CLEAR()
    #connect.CREATE("His dog eats turkey on tuesday My cat eats fish on Saturday")
    result = connect.MATCH()
    connect.UPDATE()
    connect.DELETE()

if __name__ == "__main__":
    df = prc('../data/input/mtsamples.csv')
    for index in range(0, len(df)):
        data = df["transcription"][index]
        print(type(data))
