import random
import os
import json
from typing import Tuple, List


class Filesystem:
    def is_file_valid_json(self, path: str) -> bool:
        if not os.path.isfile(path):
            return False

        try:
            f = open(path, encoding="utf8")
            dict_json = json.load(f)
            return True
        except ValueError:  # includes JSONDecodeError
            return False

    def get_dataset(self, dataset_size: int) -> Tuple[List[str], List[str]]:
        dir = "./dataset"
        train_dataset = []
        test_dataset = []

        # Clean macOS specific files
        workdir = os.listdir(dir)
        if ".DS_Store" in workdir:
            workdir.remove(".DS_Store")

        # Always randomize the dataset
        random.shuffle(workdir)
        enumeration = enumerate(workdir)

        for i, filename in enumeration:
            path = os.path.join(dir, filename)
            # checking if it is a file
            if self.is_file_valid_json(path) and i < dataset_size:
                f = open(path, encoding="utf8")
                data = json.load(f)

                entities = []

                for item in data["items"]:
                    entities.append((item["start"], item["end"], item["type"]))

                train_dataset.append([data["source"], {"entities": entities}])

            elif self.is_file_valid_json(path) and i >= dataset_size:
                f = open(path, encoding="utf8")
                data = json.load(f)

                entities = []

                for item in data["items"]:
                    entities.append(
                        (
                            item["start"],
                            item["end"],
                            item["type"],
                            item["selected-text"],
                        )
                    )

                test_dataset.append([data["source"], {"entities": entities}])

        return (train_dataset, test_dataset)

    def get_models(self):
        return [
            "./models/" + d
            for d in os.listdir("./models")
            if os.path.isdir(os.path.join("./models", d))
        ]
