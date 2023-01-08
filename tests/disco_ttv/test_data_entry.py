import disco_ttv.data_entry as de
import disco_ttv.data_structure as ds
from disco_ttv.settings import Settings

import os
import pytest
from pytest_mock import mocker
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import sessionmaker
import json

settings = Settings()

"""Fixtures"""


@pytest.fixture
def sql_engine() -> Engine:
    engine = create_engine("sqlite:///:memory:", echo=True)
    ds.Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="session")
def game_data_json() -> dict:
    with open(settings.game_data_filepath, "r") as f:
        game_data_json = json.load(f)
    return game_data_json


@pytest.fixture
def single_conversation(game_data_json: dict, conversation_id=18) -> dict:
    """
    Extracts a single conversion from the game data.
    """
    return game_data_json["conversations"][conversation_id]


@pytest.fixture
def actor_object(game_data_json: dict) -> list:
    """
    Extract the actor objects from the game data.
    """
    return game_data_json["actors"]


@pytest.fixture(scope="module")
def loaded_engine() -> Engine:
    
    engine = create_engine("sqlite:///:memory:", echo=True)
    ds.Base.metadata.create_all(engine)
    
    de.read_in_voice_library(engine, settings.voiceover_library_filepath)
    de.read_in_dialogue_entries(engine, settings.game_data_filepath)
    de.read_in_audio_clips(engine, settings.audio_clip_directory)
    de.read_in_actors(engine, settings.game_data_filepath)
    return engine


"""High level tests"""


def test_read_in_voice_library(sql_engine):
    de.read_in_voice_library(sql_engine, settings.voiceover_library_filepath)
    
    with sessionmaker(bind=sql_engine)() as session:
        assert session.query(ds.VoiceOverEntry).count() > 0
    pass


def test_read_in_dialogue_entries(sql_engine):
    de.read_in_dialogue_entries(sql_engine, settings.game_data_filepath)
    
    with sessionmaker(bind=sql_engine)() as session:
        assert session.query(ds.DialogueEntry).count() > 0
    pass


def test_read_in_audio_clips(sql_engine):
    de.read_in_audio_clips(sql_engine, settings.audio_clip_directory)

    with sessionmaker(bind=sql_engine)() as session:
        assert session.query(ds.AudioClip).count() > 0
    pass
        

"""Voice library conversion"""


def test_convert_voice_library():
    with open(settings.voiceover_library_filepath, "r") as f:
        voice_library_json = json.load(f)
    
    voice_library_mapped = de.convert_voice_library_json_to_mapping(voice_library_json)
    for item in voice_library_mapped:
        for header in ["articy_id", "asset_name", "asset_bundle", "path_to_clip_in_project", "filename"]:
            assert header in item.keys()

    
"""Game data"""


def test_extract_all_dialogue_from_conversation(single_conversation: dict):
    dialogue_entries = de.extract_dialogue_entries_from_conversation(single_conversation)
    assert len(dialogue_entries) > 100
    for dialogue_entry in dialogue_entries:
        for column_name in de.dialogue_entry_mapping_key.values():
            assert column_name in dialogue_entry


"""Audio clips"""


def test_generate_audio_clip_mapping(mocker):

    mock_directory = "/home/mock_directory"
    mock_filesize = 1024
    
    mocker.patch(
        "disco_ttv.data_entry.os.listdir",
        return_value=["this.wav", "that.wav", "junk.mp4"]
    )
    mocker.patch(
        "disco_ttv.data_entry.os.path.getsize",
        return_value=mock_filesize
    )
    audio_clip_mappings = de.extract_audio_clip_mappings(mock_directory)

    assert audio_clip_mappings == [
        {
            "filename": "this.wav",
            "size": mock_filesize,
            "filepath": "{}/this.wav".format(mock_directory)
        },
        {
            "filename": "that.wav",
            "size": mock_filesize,
            "filepath": "{}/that.wav".format(mock_directory)
        }
    ]


"""Actor ID extraction"""


def test_extract_all_actors_from_structure(actor_object: list):
    actor_mappings = de.extract_actor_mappings(actor_object)
    assert len(actor_mappings) > 100
    for actor_mapping in actor_mappings:
        keys = actor_mapping.keys()
        for column_name in ["actor_id", "name", "character_short_name"]:
            assert column_name in keys