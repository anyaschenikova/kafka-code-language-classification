import os
import fire

from datasets import load_dataset
from pathlib import Path


def download_data_to_local(
        data_path="data",
        dataset_name="code_search_net"):

    save_path = Path(data_path) / dataset_name

    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    if not os.path.isfile(save_path / "train.json"):

        dataset = load_dataset(
            dataset_name, "all")

        for split in dataset.keys():
            print(split)
            dataset[split].to_json(save_path / f"{split}.json")


if __name__ == '__main__':
    fire.Fire()
