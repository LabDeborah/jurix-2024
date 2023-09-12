from typing import List
import spacy
import json


class Metrics:
    def find_matching_item(self, givenItem, givenJson):
        # alias
        selected_text = 3

        for jsonItem in givenJson["entities"]:
            if givenItem[selected_text] == jsonItem[selected_text]:
                return jsonItem
        return None

    def find_not_matching_items(
        self, expectedItems, fullItems, outputItems
    ):  # expected fullJson output
        # Aliases
        selected_text = 3

        missing_items = []

        for fullItem in fullItems["entities"]:
            found = False
            for expectedItem in expectedItems["entities"]:
                if (
                    expectedItem[selected_text] == fullItem[0]
                ):  # fullItem selected_text is misaligned
                    found = True
                    break
            if not found:
                missing_items.append(fullItem)

        count_not_found_in_output = 0
        for missingItem in missing_items:
            for outputItem in outputItems["entities"]:
                if missingItem[selected_text] != outputItem[selected_text]:
                    count_not_found_in_output += 1
                    break

        return count_not_found_in_output

    def create_json_all_items(self, expectedJson):
        # aliases
        source = 0
        items = 1

        all_items = []

        all_itemsJson = [expectedJson[source]]

        for item in expectedJson[items]["entities"]:
            current_items = (
                item[3],  # Text
                item[0],  # Start
                item[1],  # End
                item[2],  # Tag / Type
            )
            all_items.append(current_items)

        current_start = 0
        for item in expectedJson[items]["entities"]:
            current_end = item[0]  # Start
            # if current_end == 0: continue

            text_not_used_item = expectedJson[source][current_start:current_end].strip()

            if text_not_used_item and text_not_used_item.strip() != ".":
                not_used_item = (
                    text_not_used_item,
                    current_start,
                    current_end,
                    "NOT_USED",
                )
                all_items.append(not_used_item)

            current_start = item[1]  # End

        if current_start < len(expectedJson[source]):
            final_text = expectedJson[source][current_start:].strip()

            if final_text and final_text.strip() != ".":
                not_used_item = (
                    final_text,
                    current_start,
                    len(expectedJson[source]),  # End
                    "NOT_USED",
                )
                all_items.append(not_used_item)

        all_itemsJson.append({"entities": all_items})

        return all_itemsJson

    def calculate_accuracy(self, expectedJson, outputJson):
        # aliases
        items = 1
        selected_text = 3
        type = 2

        fullJson = self.create_json_all_items(outputJson)

        expectedTotalItems = len(expectedJson[items]["entities"])
        outputTotalItems = len(outputJson[items]["entities"])

        incorrectMatches = 0
        correctMatches = 0
        itemsFound = 0

        for item in expectedJson[items]["entities"]:
            matchingItem = self.find_matching_item(item, outputJson[items])
            if matchingItem and item[selected_text] == matchingItem[selected_text]:
                correctMatches += 1
                itemsFound += 1
            if matchingItem and item[type] == matchingItem[type]:
                correctMatches += 1
            if matchingItem and item[type] != matchingItem[type]:
                incorrectMatches += 1

        trueNegatives = (
            self.find_not_matching_items(
                expectedJson[items], fullJson[items], outputJson[items]
            )
            * 2
        )
        truePositives = correctMatches
        falsePositives = ((outputTotalItems - itemsFound) * 2) + incorrectMatches
        falseNegatives = (expectedTotalItems - itemsFound) * 2

        accuracy = (truePositives + trueNegatives) / (
            truePositives + falsePositives + trueNegatives + falseNegatives
        )
        precision = truePositives / (truePositives + falsePositives)
        recall = truePositives / (truePositives + falseNegatives)
        try:
            f1score = 2 * (precision * recall) / (precision + recall)
        except ZeroDivisionError:
            f1score = 0

        # return accuracy, precision, recall, f1score
        return accuracy, precision, recall, f1score

    def run(self, model, test_data):
        nlp = spacy.load(model)

        expected_list = test_data

        inferred_list = [nlp(item[0]) for item in test_data]
        given_list = []

        for item in inferred_list:
            given_list.append(
                [
                    item.text,
                    {
                        "entities": [
                            (ent.start_char, ent.end_char, ent.label_, ent.text)
                            for ent in item.ents
                        ]
                    },
                ]
            )

        print(f'model: {nlp.meta["name"]}\n')
        for i in range(len(expected_list)):
            accuracy, precision, recall, f1score = self.calculate_accuracy(
                expected_list[i], given_list[i]
            )
            print(
                f"acc: {accuracy:.3f} - prec: {precision:.3f} - rec: {recall:.3f} - f1: {f1score:.3f}"
            )

        # print(f'Model: {nlp.meta["name"]}')
