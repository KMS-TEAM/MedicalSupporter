import pandas as pd
from numpy import math
from common import Transcription
from simpleNLP import SimpleNLP as nlp

def read_fake_data(url):
    df = pd.read_csv(url)
    # print(df.head(10))
    df.dropna()
    df.shape
    df.reset_index(drop=True)
    trans_data = []
    trans_id = 0
    # print(df['transcription'][12])
    #for i in range(0, len(df)):
    for i in range(0, 50):
        check = df['transcription'][i]
        index = 0
        transcription = {}
        key = []
        pre_i = []
        pre_p = []
        data = []
        if (isinstance(check, float)):
            pass
        else:
            while (index < len(check)):
                _key = ''
                if ((check[index] == ":") and check[index - 1].isupper()):
                    index_2 = index - 1
                    while ((check[index_2] != ',') and (check[index_2].isupper()) or (index_2 == 0) or (
                            (check[index_2] != ',') and (check[index_2] == ' ')) or (
                                   (check[index_2] != ',') and (check[index_2] == '-'))):
                        _key = check[index_2] + _key
                        index_2 = index_2 - 1
                    key.append(_key)
                    pre_i.append(index)
                    pre_p.append(index_2)
                index = index + 1
            for i in range(0, len(pre_i)):
                _data = ''
                if (i < len(pre_i) - 1):
                    for j in range(pre_i[i] + 2, pre_p[i + 1]):
                        _data = _data + check[j]
                else:
                    for j in range(pre_i[i] + 2, len(check)):
                        _data = _data + check[j]
                data.append(_data.strip())
            if (len(key) == 0 or len(data) == 0):
                pass
            else:
                for i in range(0, len(key)):
                    transcription[key[i]] = data[i]
            if ((len(transcription) > 0)):
                trans_data.append(Transcription(trans_id,df['description'][i], \
                                                df['medical_specialty'][i], df['sample_name'][i], \
                                                transcription, df['keywords'][i]))
                trans_id = trans_id + 1

    return trans_data
if __name__ == "__main__":
    print("Hello world")
    data = read_fake_data("../data/input/mtsamples.csv")
    for item in data:
        item = nlp.processing(item)








