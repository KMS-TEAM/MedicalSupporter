import pandas as pd
from numpy import math
from common import Transcription
from simpleNLP import SimpleNLP as nlp
from src import neo4japi as xxx

class processing:
    def __init__(self, url):
        self.data, self.data_len = self.read_fake_data(url)
        #self.import_to_neo4j()
        #return self.data

    def read_fake_data(self, url):
        df = pd.read_csv(url)
        df.dropna()
        df.shape
        df.reset_index(drop=True)
        trans_data = []
        trans_id = 0
        limit = len(df)

        for _index in range(0, len(df)):
        #for i in range(0, 20):
            check = df['transcription'][_index]
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
                for j in range(0, len(pre_i)):
                    _data = ''
                    if (j < len(pre_i) - 1):
                        for k in range(pre_i[j] + 2, pre_p[j + 1]):
                            _data = _data + check[k]
                    else:
                        for l in range(pre_i[j] + 2, len(check)):
                            _data = _data + check[l]
                    data.append(_data.strip())
                if (len(key) == 0 or len(data) == 0):
                    pass
                else:
                    for i_key in range(0, len(key)):
                        transcription[key[i_key]] = data[i_key]

                if ((len(transcription) > 0)):
                    trans_data.append(Transcription(trans_id,df['description'][_index], \
                                                    df['medical_specialty'][_index], df['sample_name'][_index], \
                                                    transcription, df['keywords'][_index]))
                    trans_id = trans_id + 1

        return trans_data, len(trans_data)

    def import_to_neo4j(self):
        neo = xxx.Neo("neo4j", "1")
        medical = []
        # f.write("Now the file has more content!")
        for i in range(0, self.data_len):
            medical.append(self.data[i].medicalspecialty)
        _list_medical = set(medical)
        # print(len(_list_medical))
        node_medicalspecialty = {}
        for item in _list_medical:
            _key_list = []
            for i in range(0, len(self.data)):
                if (item == self.data[i].medicalspecialty):
                    fake_key = str(self.data[i].keywords).split(', ')
                    for j in range(0, len(fake_key)):
                        if ((len(fake_key[j]) < 30) or (len(fake_key[j]) < 2)):
                            _key_list.append(fake_key[j])

            real_key = set(_key_list)
            node_medicalspecialty[item] = list(real_key)

        key_list = list(node_medicalspecialty.keys())
        val_list = list(node_medicalspecialty.values())
        # print(len(val_list))
        _count = 0
        for index in range(0, len(node_medicalspecialty)):
            name = key_list[index]
            neo.create_single_node(name, "medical_specality")
            # print(len(val_list[index]))
            for key in range(0, len(val_list[index])):
                symptom_name = val_list[index][key]
                _count = _count + 1
                # print(len(symptom_name))
                neo.create_single_node(symptom_name, "symptom")
                neo.create_relation(name, symptom_name)






