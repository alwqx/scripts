# -*- coding: utf-8 -*-
# -*- coding:utf-8 -*-

import json
import random
import os
import operator
import math

#数据过滤出现问题，
"""
过滤：
68492458
37140619
47304187
54115
4953751
ff4850fe828147f8bbb9
MzQ5Mzk2
bcqaju
2016-11-27
保留：
v1
v2
user_project
"""
def validate_subpath(x):
    #filter "" , ff4850fe828147f8bbb9
    if len(x) == 0 or x == "," or len(x) >= 20:
        return False
    if x == "v1" or x == "v2":
        return True
    #filter 2016-11-27
    if "-" in x:
        return False
    #filter 348914534
    if x.isdigit():
        return False
    return True

"""
对key进行分组
{k:[],k:[],...,k:[]}
"""
def generate_key_group_value(filepath):
    ret = {}
    tmp = []
    f = open(filepath, "r")
    for line in f.readlines():
        pattern = json.loads(line.rstrip("\n"))
        path = pattern["path"]
        path_list = [x.strip() for x in path.split("/") if validate_subpath(x)]
        k = str(pattern["view_name"])
        if k in ret.keys():
            ret[k].append(path_list)
        else:
            ret[k] = []
            ret[k].append(path_list)
    f.close()
    return ret

#filter param in path
#选择词频率大于ratio的词
#每个sublist中的词不重复
#计算路径中每个单词的权重，过滤权重低的单词
def generate_key_validate_value(data, ratio):
    ret = {}
    b = set()
    length = len(data)
    total_letter = sum([len(l) for l in data])#总单词个数
    avg_path_len = total_letter/float(length)#平均路径长度
    bag_letter = get_bag_leter(data)#得到去重单词
    for letter in bag_letter:
        count = 0
        for l in data:
            if letter in l:
                count += 1
        pl = (float(count)/float(total_letter))*avg_path_len
        if pl > ratio:
            ret[letter] = pl
    return ret


def get_bag_leter(data):
    ret = set()
    for lists in data:
        ret.update(lists)
    return list(ret)

def generate_key_weight_value(filepath, ratio):
    kv = generate_key_group_value(filepath)
    new_kv = {k:generate_key_validate_value(v, ratio) for k,v in kv.items()}
    return new_kv

def test_generate_key_weight_value():
    filepath = "/home/geek/workspace/newjobwp/shanbay/PatternAssignment/train_clean_norepeat.jsonl"
    ret = generate_key_weight_value(filepath, 0.2)
    assert len(ret) > 1

### input logic

"""
path: /api/v1/palegreen/example/?q1=&q2=...&qn=
"""
def parse_url(url):
    path = url.split("?")[:1]
    # exception
    path_split = [letter for letter in path[0].split("/") if len(letter) != 0]
    return path_split

def test_parse_url():
    url1 = "/api/v1/palegreen/example/?ids=3865003,3865006"
    assert parse_url(url1) == ["api", "v1", "palegreen", "example"]

"""
weight_path: {"api":0.5, "v1":0.2,...,"user":0.7}
path_list: ["api", "v2", "user", "list"]
"""
def similarity(weight_path, path_list):
    weight = 0.0
    keys = weight_path.keys()
    for p in path_list:
        if p in keys:
            weight += weight_path[p]
    return weight

def similarity_v1(weight_path, path_list):
    weight = 0.0
    keys = weight_path.keys()
    diff = abs(len(keys) - len(path_list))*0.1
    for p in path_list:
        if p in keys:
            weight += weight_path[p]
    return weight+diff

def similarity_v2(weight_path, path_list):
    weight = 0.0
    keys = weight_path.keys()
    #从长度考虑差异性
    diff = abs(len(keys) - len(path_list))*0.1

    for p in path_list:
        if p in keys:
            weight += pow(weight_path[p], 2)
    return math.sqrt(weight)+diff

def similarity_v3(weight_path, path_list):
    weight = 0.0
    keys = weight_path.keys()
    #从长度考虑差异性
    diff = abs(len(keys) - len(path_list))*1

    for p in path_list:
        if p in keys:
            weight += pow(weight_path[p]*10, 2)
    return math.sqrt(weight)+diff

def get_data(filepath, ratio, testSet=[]):
    with open(filepath, "r") as f:
        for line in f.readlines():
            if random.random() < ratio:
                jf = json.loads(line)
                path = parse_url(jf["path"])
                jf["path"] = path
                testSet.append(jf)

def get_accuracy(actual, predictions):
    length = len(actual)
    count = 0
    for i in range(length):
        if actual[i] == predictions[i]:
            count += 1
    acc = float(count)/length * 100.0
    print("accuracy:" + repr(acc) + "%")

def train():
    filepath = "/tmp/PatternAssignment/train_clean_norepeat.jsonl"
    filepath2 = "/tmp/PatternAssignment/train_clean.jsonl"    
    testSet = []
    predictions = []
    actual = []

    get_data(filepath, 0.8, testSet)
    # view_weight_path = generate_key_weight_value(filepath, 0.1)
    view_weight_path = generate_key_weight_value(filepath, 0.1)    

    for ele in testSet:
        #{view_name, path}
        similaritis = {k:similarity_v1(v, ele["path"]) for k,v in view_weight_path.items()}
        sortedVotes = sorted(similaritis.items(), key=operator.itemgetter(1), reverse=True)
        predictions.append(sortedVotes[0][0])
        actual.append(ele["view_name"])
    get_accuracy(actual, predictions)

if __name__ == "__main__":
    # main()
    train()

