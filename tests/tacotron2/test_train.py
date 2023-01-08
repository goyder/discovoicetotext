import tacotron2.train as train
import argparse
import pytest
import os
from dataclasses import dataclass
from disco_ttv.settings import Settings

settings = Settings()


@dataclass
class TrainingConfig:
    dataset_name: str
    training_datasets_directory: str
    output_directory: str
    model_directory: str
    training_filename: str = "train_filelist.txt"
    validation_filename: str = "validation_filelist.txt"
    tacotron2_model_filename: str = "checkpoint_Tacotron2_test.pt"
    waveglow_model_filename: str = "checkpoint_WaveGlow_test.pt"
    test_phrases_text_filename: str = "test_phrases.txt"

    @property
    def validation_filelist_filepath(self) -> str:
        return os.path.join(self.training_datasets_directory, self.dataset_name, self.validation_filename)

    @property
    def training_filelist_filepath(self) -> str:
        return os.path.join(self.training_datasets_directory, self.dataset_name, self.training_filename)

    @property
    def dataset_path(self) -> str:
        return os.path.join(self.training_datasets_directory, self.dataset_name)

    @property
    def tacotron_model_filepath(self) -> str:
        return os.path.join(self.model_directory, self.tacotron2_model_filename)

    @property
    def waveglow_model_filepath(self) -> str:
        return os.path.join(self.model_directory, self.waveglow_model_filename)

    @property
    def test_phrases_text_filepath(self) -> str:
        return os.path.join(self.training_datasets_directory, self.test_phrases_text_filename)


@pytest.fixture
def training_config() -> TrainingConfig:

    # TODO: Clear the output directory each time

    # Define the inputs
    output_directory = os.path.join(
        settings.output_directory,
        "test_directory"
    )
    training_datasets_directory = settings.training_datasets_directory
    dataset_name = settings.test_dataset_name
    model_directory = settings.model_directory

    # Delete, and then create, our directories
    os.makedirs(
        output_directory,
        exist_ok=True
    )

    # Return the config
    training_config = TrainingConfig(
        output_directory=output_directory,
        training_datasets_directory=training_datasets_directory,
        dataset_name=dataset_name,
        model_directory=model_directory
    )

    return training_config


@pytest.fixture
def insert_tacotron2_args(training_config: TrainingConfig):

    def insert_args_dropin(parser: argparse.ArgumentParser):
        args, _ = parser.parse_known_args(
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


def test_train_tacotron2_from_scratch(mocker, insert_tacotron2_args):
    mocker.patch(
        "tacotron2.train.parse_args",
        new=insert_tacotron2_args
        )
    train.main()


@pytest.fixture
def insert_waveglow_args(training_config: TrainingConfig):

    def insert_args_dropin(parser: argparse.ArgumentParser):
        args, _ = parser.parse_known_args(
            [
                "-o", training_config.output_directory,
                "-d", training_config.dataset_path,
                "--training-files", training_config.training_filelist_filepath,
                "--validation-files", training_config.validation_filelist_filepath,
                "-m", "WaveGlow",
                "--epochs", "2",
                "-lr", "1e-4",
                "-bs", "12",
                "--cudnn-enabled"
                "--wn-channels", "256",
            ]
        )
        return args

    return insert_args_dropin


def test_train_waveglow_from_scratch(mocker, insert_waveglow_args):
    mocker.patch(
        "tacotron2.train.parse_args",
        new=insert_waveglow_args
        )
    train.main()


@pytest.fixture
def insert_tacotron2_with_inference_args(training_config: TrainingConfig):

    def insert_args_dropin(parser: argparse.ArgumentParser):
        args, _ = parser.parse_known_args(
            [
                "-o", training_config.output_directory,
                "-d", training_config.dataset_path,
                "--training-files", training_config.training_filelist_filepath,
                "--validation-files", training_config.validation_filelist_filepath,
                "-m", "Tacotron2",
                "--epochs", "2",
                "-lr", "1e-3",
                "-bs", "12",
                "--inference",
                "--wn-channels", "256",
                "--waveglow", training_config.waveglow_model_filepath,
                "--epochs-per-inference", "1",
                "-i", training_config.test_phrases_text_filepath,
                "--cpu"
            ]
        )
        return args

    return insert_args_dropin


@pytest.mark.skip("Inference doesn't work yet.")
def test_train_tacotron2_with_inference(mocker, insert_tacotron2_with_inference_args):
    mocker.patch(
        "tacotron2.train.parse_args",
        new=insert_tacotron2_with_inference_args
        )
    mocker.patch(
        "tacotron2.inference.parse_args",
        new=insert_tacotron2_with_inference_args
        )
    train.main()
