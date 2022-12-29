import tacotron2.train as train
import argparse


def insert_args(parser: argparse.ArgumentParser):

    return parser.parse_args(
        [
            "-o", "/dev/null/",
            "-m", "Tacotron2",
            "--epochs", "1",
            "-lr", "0.01",
            "-bs", "12"
        ]
    )


def test_train_from_scratch(mocker):
    mocker.patch(
        "tacotron2.train.parse_args",
        new=insert_args)
    train.main()