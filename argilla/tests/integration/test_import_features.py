# Copyright 2024-present, Argilla, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import random
import uuid
from string import ascii_lowercase
from tempfile import TemporaryDirectory
from typing import Any, List

import argilla as rg
import pytest
from argilla._exceptions import ConflictError, SettingsError
from datasets import Dataset as HFDataset, Value, Features, ClassLabel
from huggingface_hub.utils._errors import BadRequestError, FileMetadataError, HfHubHTTPError

_RETRIES = 5


@pytest.fixture
def dataset(client) -> rg.Dataset:
    mock_dataset_name = "".join(random.choices(ascii_lowercase, k=16))
    settings = rg.Settings(
        fields=[
            rg.TextField(name="text"),
            rg.ImageField(name="image"),
        ],
        questions=[
            rg.LabelQuestion(name="label", labels=["positive", "negative"]),
        ],
    )
    dataset = rg.Dataset(
        name=mock_dataset_name,
        settings=settings,
        client=client,
    )
    dataset.create()
    yield dataset
    dataset.delete()


@pytest.fixture
def mock_data() -> List[dict[str, Any]]:
    return [
        {
            "text": "Hello World, how are you?",
            "image": "http://mock.url/image",
            "label": "positive",
            "id": uuid.uuid4(),
        },
        {
            "text": "Hello World, how are you?",
            "image": "http://mock.url/image",
            "label": "negative",
            "id": uuid.uuid4(),
        },
        {
            "text": "Hello World, how are you?",
            "image": "http://mock.url/image",
            "label": "positive",
            "id": uuid.uuid4(),
        },
    ]


@pytest.fixture
def token():
    return os.getenv("HF_TOKEN_ARGILLA_INTERNAL_TESTING")


class TestImportFeaturesFromHub:
    def test_import_records_from_datasets_with_classlabel(
        self, token: str, dataset: rg.Dataset, client, mock_data: List[dict[str, Any]]
    ):
        repo_id = f"argilla-internal-testing/test_import_dataset_from_hub_with_classlabel_{uuid.uuid4()}"

        hf_dataset = HFDataset.from_dict(
            {
                "text": [record["text"] for record in mock_data],
                "label": [record["label"] for record in mock_data],
            },
            features=Features(
                {
                    "text": Value("string"),
                    "label": ClassLabel(names=["positive", "negative"]),
                }
            ),
        )

        hf_dataset.push_to_hub(repo_id=repo_id, token=token)

        dataset.records.log(mock_data)

        for i, record in enumerate(dataset.records(with_suggestions=True)):
            assert record.fields["text"] == mock_data[i]["text"]
            assert record.suggestions["label"].value == mock_data[i]["label"]

        exported_dataset = dataset.records.to_datasets()

        assert exported_dataset.features["label.suggestion"].names == ["positive", "negative"]
        assert exported_dataset["label.suggestion"] == [0, 1, 0]