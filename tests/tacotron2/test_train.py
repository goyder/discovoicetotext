import tacotron2.train as train
import argparse
import pytest
import os
from dataclasses import dataclass

@dataclass
class TrainingConfig:
    dataset_name: str
    training_datasets_directory: str
    output_directory: str
    training_filename: str = "train_filelist.txt"
    validation_filename: str = "validation_filelist.txt"

    @property
    def validation_filelist_filepath(self) -> str:
        return os.path.join(self.training_datasets_directory, self.dataset_name, self.validation_filename)

    @property
    def training_filelist_filepath(self) -> str:
        return os.path.join(self.training_datasets_directory, self.dataset_name, self.training_filename)

    @property
    def dataset_path(self) -> str:
        return os.path.join(self.training_datasets_directory, self.dataset_name)


@pytest.fixture
def training_config() -> TrainingConfig:

    # TODO: Clear the output directory each time

    # Define the inputs
    output_directory = os.path.join(
        os.environ["OUTPUT_DIRECTORY"],
        "test_directory"
    )
    training_datasets_directory = os.environ["TRAINING_DATASETS_DIRECTORY"]
    dataset_name = os.environ["TEST_DATASET_NAME"]

    # Create our directories
    os.makedirs(
        output_directory,
        exist_ok=True
    )

    # Return the config
    training_config = TrainingConfig(
        output_directory=output_directory,
        training_datasets_directory=training_datasets_directory,
        dataset_name=dataset_name
    )

    return training_config


@pytest.fixture
def insert_tacotron2_args(training_config: TrainingConfig):

    def insert_args_dropin(parser: argparse.ArgumentParser):
        args = parser.parse_args(
            [
                "-o", training_config.output_directory,
                "-d", training_config.dataset_path,
                "--training-files", training_config.training_filelist_filepath,
                "--validation-files", training_config.validation_filelist_filepath,
                "-m", "Tacotron2",
                "--epochs", "2",
                "-lr", "1e-3",
                "-bs", "12",
                "--cudnn-enabled",
            ]
        )
        return args

    return insert_args_dropin


@pytest.fixture
def insert_waveglow_args(training_config: TrainingConfig):

    def insert_args_dropin(parser: argparse.ArgumentParser):
        args = parser.parse_args(
            [
                "-o", training_config.output_directory,
                "-d", training_config.dataset_path,
                "--training-files", training_config.training_filelist_filepath,
                "--validation-files", training_config.validation_filelist_filepath,
                "-m", "WaveGlow",
                "--epochs", "2",
                "-lr", "1e-4",
                "-bs", "12",
                "--cudnn-enabled",
            ]
        )
        return args

    return insert_args_dropin


def test_train_tacotron2_from_scratch(mocker, insert_tacotron2_args):
    mocker.patch(
        "tacotron2.train.parse_args",
        new=insert_tacotron2_args
        )
    train.main()


def test_train_waveglow_from_scratch(mocker, insert_waveglow_args):
    mocker.patch(
        "tacotron2.train.parse_args",
        new=insert_waveglow_args
        )
    train.main()