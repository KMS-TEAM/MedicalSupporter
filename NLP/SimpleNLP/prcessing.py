import pandas as pd


if __name__ == "__main__":
    print("Hello world")

    df = pd.read_csv("data/input/mtsamples.csv")
    #print(df.head(10))
    df.dropna(inplace=True)
    df.shape
    for i in range(0, 2):
        check = df['transcription'][i]
        index = 0
        transcription = {}
        print(len(check))
        key = []
        pre_i = []
        pre_p = []
        data = []
        while(index < len(check)):
            _key = ''
            if ((check[index] == ":") and check[index-1].isupper()):
                index_2 = index - 1
                while((check[index_2] != ',') and (check[index_2].isupper()) or (index_2 == 0) or (check[index_2] != ',') and (check[index_2] == ' ')):
                    _key = check[index_2] + _key
                    index_2 = index_2 - 1
                print(_key, " ", index_2)
                key.append(_key)
                pre_i.append(index)
                pre_p.append(index_2)
            index = index + 1
        for i in range (0, len(pre_i)):
            _data = ''
            if (i < len(pre_i) - 1):
                for j in range(pre_i[i] + 2, pre_p[i+1]):
                    _data = _data + check[j]
            else:
                for j in range(pre_i[i] + 2, len(check)):
                    _data = _data + check[j]
            data.append(_data.strip())

        for i in range(0, len(key)):
            transcription[key[i]] = data[i]
        print(transcription)




