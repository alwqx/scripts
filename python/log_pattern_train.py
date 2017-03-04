# -*- coding: utf-8 -*-
import json
import random
import os
import operator
import math

def validate_subpath(subpath):
    """Return validate subpath in path

    Args:
        subpath:A subpath splited from path. "api", "v1" or "user_project"
    
    Returns:
        True is subpath is validate otherwise False. 
        "68492458" "ff4850fe828147f8bbb9" "MzQ5Mzk2" 
        "2016-11-27" are invalidate.
    """
    if len(subpath) == 0 or subpath == ",":
        return False
    if len(subpath) >= 20 or "-" in subpath:
        return False
    if subpath == "v1" or subpath == "v2":
        return True
    if subpath.isdigit():
        return False
    return True

def group_path_by_viewname(filepath):
    """Group path by view_name
    Groupby viewname's all paths in form of list.

    Args:
        filepath: filepath of train_clean.jsonl

    Returns:
        group_paths: A dict which k is view_name and 
            value is a list with all paths
    """
    group_paths = {}
    with open(filepath, "r") as f:
        for line in f.readlines():
            pattern = json.loads(line.rstrip("\n"))
            path = pattern["path"]
            path_list = [x.strip() for x in path.split("/") 
                            if validate_subpath(x)]
            view_name = pattern["view_name"]
            if view_name in group_paths.keys():
                group_paths[view_name].append(path_list)
            else:
                group_paths[view_name] = []
                group_paths[view_name].append(path_list)
    return group_paths

def caculate_subpath_weight(path_list, ratio):
    """Caculate subpaths' weight of view_name
    Args:
        path_list: A list of view_name's all subpath.
        ratio: ratio for filtering low weight.

    Returns:
        weight_path_dict: A dict which key is subpath and 
            value is weight.
    """
    weight_path_dict = {}
    length = len(path_list)
    total_letter = sum([len(l) for l in path_list]) #total number of subpath
    avg_path_len = total_letter/float(length) #average length of each path
    letter_bags = get_letter_bags(path_list) #letter bags of all subpath
    for letter in letter_bags:
        count = 0
        for path in path_list:
            if letter in path:
                count += 1
        weight = (float(count)/float(total_letter))*avg_path_len
        if weight > ratio:
            weight_path_dict[letter] = weight
    return weight_path_dict

def get_letter_bags(path_list):
    """Return letter bags of input
    Args:
        path_list: List of subpath.

    Returns:
        letter_bags: letter bags from path_list
    """
    letter_bags = set()
    for path in path_list:
        letter_bags.update(path)
    return list(letter_bags)

def generate_key_weight_value(filepath, ratio):
    """Generate weighted path

    Args: 
        filepath: filepath of train data.
        ratio: ratio for filtering low weight.

    Returns:
        weight_path: A dict which key is view name and 
            value is weight path.
    """
    group_path = group_path_by_viewname(filepath)
    weight_path = {k:caculate_subpath_weight(v, ratio) 
        for k,v in group_path.items()}
    return weight_path

def test_generate_key_weight_value():
    filepath = "/tmp/PatternAssignment/train_clean_norepeat.jsonl"
    ret = generate_key_weight_value(filepath, 0.2)
    assert len(ret) > 1

def parse_url(url):
    """Split input path to subpath list

    Args:
        url: path url.
    
    Returns:
        subpath_list: list of subpath.
    """
    path = url.split("?")[:1]
    subpath_list = [letter for letter in path[0].split("/") if len(letter) != 0]
    return subpath_list

def test_parse_url():
    url1 = "/api/v1/palegreen/example/?ids=3865003,3865006"
    assert parse_url(url1) == ["api", "v1", "palegreen", "example"]

def similarity(weight_path, path_list):
    """Caculate similarity between two args.

    Args:
        weight_path: A dict which key is subpath and
            value is its weight.
        path_list: A list from parse_url.
        
    Returns:
        weight: Weight between two args
    """
    weight = 0.0
    subpaths = weight_path.keys()
    for subpath in path_list:
        if subpath in subpaths:
            weight += weight_path[subpath]
    return weight

def similarity_v1(weight_path, path_list):
    """Caculate similarity between two args.

    Args:
        weight_path: A dict which key is subpath and
            value is its weight.
        path_list: A list from parse_url.
        
    Returns:
        weight: Weight between two args
    """
    weight = 0.0
    subpaths = weight_path.keys()
    length_weight = abs(len(subpaths) - len(path_list))*0.1
    for subpath in path_list:
        if subpath in subpaths:
            weight += weight_path[subpath]
    return weight + length_weight

def similarity_v3(weight_path, path_list):
    weight = 0.0
    subpaths = weight_path.keys()

    length_weight = abs(len(subpaths) - len(path_list))*1

    for subpath in path_list:
        if subpath in subpaths:
            weight += pow(weight_path[subpath]*10, 2)
    return math.sqrt(weight) + length_weight

def generate_data(filepath, ratio, testSet):
    """Generate test data according to ratio

    Args:
        filepath: filepath of train data.
        ratio: ratio for split data from data.
        testSet: test data set.
    """
    with open(filepath, "r") as f:
        for line in f.readlines():
            if random.random() < ratio:
                jf = json.loads(line.rstrip("\n"))
                path = parse_url(jf["path"])
                jf["path"] = path
                testSet.append(jf)

def get_accuracy(actual, predictions):
    """Caculate accuracy of predict

    Args:
        actual: actual values.
        predictions: predict values.
    
    Returns:
        accuracy
    """
    length = len(actual)
    count = 0
    for i in range(length):
        if actual[i] == predictions[i]:
            count += 1
    accuracy = float(count)/length * 100.0
    return accuracy

def get_predict_view(view_weight_path, url):
    """Return predict view.

    Args:
        view_weight_path: A dict which key is view name and 
            value is weight path.
        url: path url.

    Returns:
        view_name: view_name predicted from key_weight_value.
    """
    subpath = parse_url(url)
    similaritis = {k:similarity_v1(v, subpath) 
            for k,v in view_weight_path.items()}
    sorted_similaritis = sorted(similaritis.items(), 
        key=operator.itemgetter(1), reverse=True)
    view_name = sorted_similaritis[0][0]
    return view_name

def test_get_predict_view():
    filepath = "/tmp/PatternAssignment/train_clean_norepeat.jsonl"
    url = "/api/v1/palegreen/note/?ids=323281,93582"

    view_weight_path = generate_key_weight_value(filepath, 0.2)
    view_name = get_predict_view(view_weight_path, url)
    print(view_name)
    assert view_name is not None

def train():
    filepath = "/tmp/PatternAssignment/train_clean_norepeat.jsonl"
    # filepath2 = "/tmp/PatternAssignment/train_clean.jsonl"
    testSet = []
    predictions = []
    actual = []

    generate_data(filepath, 0.8, testSet)
    # view_weight_path = generate_key_weight_value(filepath, 0.1)
    view_weight_path = generate_key_weight_value(filepath, 0.2)

    for ele in testSet:
        similaritis = {k:similarity_v1(v, ele["path"]) 
            for k,v in view_weight_path.items()}
        sorted_similaritis = sorted(similaritis.items(), 
            key=operator.itemgetter(1), reverse=True)
        predictions.append(sorted_similaritis[0][0])
        actual.append(ele["view_name"])
    acc = get_accuracy(actual, predictions)
    print("Accuracy: " + repr(acc) + "%")

def save_file(train_path, url_path, result_path):
    """Run model and save to result.txt.

    Args:
        train_path: filepath of train data.
        url_path: filepath of url file.
        result_path: filepath of result.txt .
    """
    template = "url: {}, view_name: {}\n"
    view_weight_path = generate_key_weight_value(train_path, 0.2)

    url_f = open(url_path)
    result_f = open(result_path, "w")

    for url in url_f.readlines():
        view_name = get_predict_view(view_weight_path, url)
        result_f.write(template.format(url.rstrip("\n"), view_name))
    url_f.close()
    result_f.close()
    print("complete!")

def main():
    train_path = "/tmp/PatternAssignment/train_clean_norepeat.jsonl"
    url_path = "/tmp/PatternAssignment/path_unique"
    result_path = os.path.join(os.getcwd(), "result.txt")
    save_file(train_path, url_path, result_path)

if __name__ == "__main__":
    # main()
    train()