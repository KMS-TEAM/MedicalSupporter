import pandas as pd
import os
from neo4japi import Neo
from simpleNLP import SimpleNLP
from processing import processing as prc
from common import input

def most_frequent(List):
    return max(set(List), key = List.count)

def check_key(key):
    neo = Neo("neo4j", "1")
    test= neo.match_check(key)
    #print(test)
    if (test == False):
        return []
    else:
        return test

if __name__ == "__main__":
    df = prc('../data/input/mtsamples.csv').data
    nlp = SimpleNLP()
    trans = []
    input_test = []
    neo = Neo("neo4j", "1")
    for index in range(0, 1000):
        #print(type(df[index].transcription))
        trans.append(df[index].transcription)
        key = list(trans[index].keys())
        value = list(trans[index].values())
        list_entitis = []
        for i in range(0, len(key)):
            temp = str(value[i]).split('.')
            #print(key[i])
            #print(temp)
            entity_pair = nlp.get_entitiy_pairs(temp)
            #print(entity_pair)
            entity = []
            for check in range(0, len(entity_pair)):
                if (len(entity_pair[check][0]) > 2):
                    entity.append(entity_pair[check][0])
                if (len(entity_pair[check][1]) > 2):
                    entity.append(entity_pair[check][1])
            list_entitis.append(entity)
        input_test.append(input(key, list_entitis))

    print(input_test[0].describe['SUBJECTIVE'])
    final_check = 0
    final_count = 0
    print(len(input_test))

    for input in input_test:
        key = list(input.describe.keys())
        value = list(input.describe.values())
        count = 0
        print(value)
        for i in range(0, len(value)):
            for j in range(0, len(value[i])):
                medical_specality = ''
                print(value[i][j])
                _key = value[i][j]
                _check = check_key(str(_key))
                if (_check == []):
                    pass
                else:
                    for something in range(0, len(_check)):
                        input.medical_specality.append(_check[something])
                        count = count + 1
        # print(input.medical_specality)
        try:
            print(most_frequent(input.medical_specality))
            if (most_frequent(input.medical_specality) == df[final_count].medicalspecialty):
                final_check = final_check + 1
        except:
            print("medical empty")
        print(final_count)
        final_count = final_count + 1

    print((final_check / 1000) * 100)


