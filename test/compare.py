import json

def load_json_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def compare_text(text1, text2):
    return text1.strip() == text2.strip()

def find_matching_item(item, json2_items):
    for json2_item in json2_items:
        if item["selected-text"] == json2_item["selected-text"]:
            return json2_item
    return None

def find_not_matching_items(json1, json2, json3):
    missing_items = []

    for json2_item in json2:
        found = False
        for json1_item in json1:
            if json1_item["selected-text"] == json2_item["selected-text"]:
                found = True
                break
        if found == False:
            missing_items.append(json2_item)

    count_found_in_json3 = 0
    for missing_item in missing_items:
        for json3_item in json3:
            if missing_item["selected-text"] == json3_item["selected-text"]:
                count_found_in_json3 += 1
                break

    return count_found_in_json3


def calculate_accuracy(json1_path, json2_path, json3_path):
    json1 = load_json_from_file(json1_path)
    json2 = load_json_from_file(json2_path)
    json3 = load_json_from_file(json3_path)

    expected_total_items = len(json1["items"])

    output_total_items = len(json2["items"])

    incorrect_matches = 0

    correct_matches = 0
    
    items_found = 0

    for item1 in json1["items"]:
        matching_item = find_matching_item(item1, json2["items"])
        if matching_item and item1["selected-text"] == matching_item["selected-text"]:
            correct_matches += 1
            items_found +=1
        if matching_item and item1["type"] == matching_item["type"]:
            correct_matches += 1
        # if matching_item and item1["start"] == matching_item["start"]:
        #     correct_matches += 1
        # if matching_item and item1["end"] == matching_item["end"]:
        #     correct_matches += 1
        if matching_item and item1["selected-text"] != matching_item["selected-text"]:
            incorrect_matches += 1          
        if matching_item and item1["type"] != matching_item["type"]:
            incorrect_matches += 1
        # if matching_item and item1["end"] != matching_item["end"]:
        #     incorrect_matches += 1
        # if matching_item and item1["start"] != matching_item["start"]:
        #     incorrect_matches += 1

    true_negatives = find_not_matching_items(json1["items"], json3["items"], json2["items"]) * 2

    true_positives = correct_matches

    false_positives = ((output_total_items - items_found) * 2) + incorrect_matches
    
    false_negatives = ((expected_total_items - items_found) * 2)

    accuracy = (true_positives + true_negatives) / (true_positives + false_positives + true_negatives + false_negatives)

    print(accuracy)

    return accuracy

def calculate_recall(json1_path, json2_path):
    json1 = load_json_from_file(json1_path)
    json2 = load_json_from_file(json2_path)

    total_items = len(json1["items"]) * 2
    correct_matches = 0

    for item1 in json1["items"]:
        matching_item = find_matching_item(item1, json2["items"])
        if matching_item and item1["selected-text"] == matching_item["selected-text"]:
            correct_matches += 1
        if matching_item and item1["type"] == matching_item["type"]:
            correct_matches += 1
        # if matching_item and item1["start"] == matching_item["start"]:
        #     correct_matches += 1
        # if matching_item and item1["end"] == matching_item["end"]:
        #     correct_matches += 1

    recall = correct_matches / total_items
    return recall

def calculate_precision(json1_path, json2_path):
    json1 = load_json_from_file(json1_path)
    json2 = load_json_from_file(json2_path)

    total_items = len(json2["items"]) * 2
    correct_matches = 0

    for item1 in json1["items"]:
        matching_item = find_matching_item(item1, json2["items"])
        if matching_item and item1["selected-text"] == matching_item["selected-text"]:
            correct_matches += 1
        if matching_item and item1["type"] == matching_item["type"]:
            correct_matches += 1
        # if matching_item and item1["start"] == matching_item["start"]:
        #     correct_matches += 1
        # if matching_item and item1["end"] == matching_item["end"]:
        #     correct_matches += 1

    precision = correct_matches / total_items
    return precision

json1_path = r"./expected.json"
json2_path = r"./output.json"
json3_path = r"./fullementa.json"

accuracy = calculate_accuracy(json1_path, json2_path, json3_path)
precision = calculate_recall(json1_path, json2_path)
recall = calculate_precision(json1_path, json2_path)
try:
    f1score = (2 * precision * recall) / (precision + recall)
except ZeroDivisionError:
    f1score = 0
print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1score: {f1score}")

