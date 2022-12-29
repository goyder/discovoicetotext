import tacotron2.train as train
import Tacotron2.tacotron2.train as train
import argparse


def insert_args(parser: argparse.ArgumentParser):

    return parser.parse_args(
        [
            "-o", "/dev/null/",
            "-d", "dataset/path",
            "--training-files", "'training_filelist.txt'",
            "--validation-files", "'validation_filelist.txt'"
            "-m", "Tacotron2",
            "--epochs", "2",
            "-lr", "1e-3",
            "-bs", "12",
            "--cudnn-enabled",
        ]
    )


def test_train_from_scratch(mocker):
    mocker.patch(
        "tacotron2.train.parse_args",
        new=insert_args)
    train.main()