#! -*- coding:utf-8 -*-
import json


def PreProcessData(path):
    sentences = []
    tags = []
    with open(path, encoding="utf-8") as data_file:
        for sentence in data_file.read().strip().split('\n\n'):
            _sentence = ""
            tag = []
            for word in sentence.strip().split('\n'):
                content = word.strip().split()
                _sentence += content[0]
                tag.append(content[1])
            sentences.append(_sentence)
            tags.append(tag)
    data = (sentences, tags)
    return data


def GenerateData(json_path, train_path, validate_path):
    datas = ["", ""]  # first for training data, second for validate data
    tag_map = {'疾病和诊断': 1, '影像检查': 2, '实验室检验': 3, '药物': 4, '手术': 5, '解剖部位': 6}
    count = 0
    with open(json_path, encoding='utf-8') as f:
        for line in f:  # every line is a json object
            ini_pos = 0
            count += 1
            element = json.loads(line, encoding='utf-8')
            entities = element['entities']  # entity array
            original_text = element['originalText']
            if count <= 300:
                choose_index = 0
            else:
                choose_index = 1
            for entity in entities:
                start_pos = entity['start_pos']
                end_pos = entity['end_pos']
                tag = tag_map[entity['label_type']]
                for i in range(ini_pos, start_pos):
                    datas[choose_index] += original_text[i]
                    datas[choose_index] += ' 0\n'
                    if original_text[i] == '。':
                        datas[choose_index] += '\n'
                datas[choose_index] += original_text[start_pos]
                datas[choose_index] += ' '
                datas[choose_index] += str(2*tag-1)
                datas[choose_index] += '\n'
                tmpstr = ' ' + str(2*tag) + '\n'
                for i in range(start_pos+1, end_pos):
                    datas[choose_index] += original_text[i]
                    datas[choose_index] += tmpstr
                ini_pos = end_pos
            for i in range(end_pos, len(original_text)):
                datas[choose_index] += original_text[i]
                datas[choose_index] += ' 0\n'
                if original_text[i] == '。':
                    datas[choose_index] += '\n'
    with open(train_path, encoding='utf-8', mode='w') as f:
        f.write(datas[0])
    with open(validate_path, encoding='utf-8', mode='w') as f:
        f.write(datas[1])

# test GenerateData

if __name__ == '__main__':
    GenerateData('../Data/train.json', '../Data/train.txt', '../Data/validate.txt')



