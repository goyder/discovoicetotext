from tkinter import dialog
import voice2text.data_entry as de
import voice2text.data_structure as ds
import os
import pytest
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import sessionmaker
import json


"""Fixtures"""


@pytest.fixture
def sql_engine() -> Engine:
    engine = create_engine("sqlite:///:memory:", echo=True)
    ds.Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="session")
def game_data_json() -> dict:
    with open(os.environ["GAME_DATA_FILEPATH"], "r") as f:
        game_data_json = json.load(f)
    return game_data_json


@pytest.fixture
def single_conversation(game_data_json: dict, conversation_id=18) -> dict:
    """
    Extracts a single conversion from the game data.
    """
    return game_data_json["conversations"][conversation_id]


"""High level tests"""


def test_read_in_voice_library(sql_engine):
    de.read_in_voice_library(sql_engine, os.environ["VOICEOVER_LIBRARY_FILEPATH"])
    
    with sessionmaker(bind=sql_engine)() as session:
        assert session.query(ds.VoiceOverEntry).count() > 0
    pass


def test_read_in_dialogue_entries(sql_engine):
    de.read_in_dialogue_entries(sql_engine, os.environ["GAME_DATA_FILEPATH"])
    
    with sessionmaker(bind=sql_engine)() as session:
        assert session.query(ds.DialogueEntry).count() > 0
    pass


"""Voice library conversion"""


def test_convert_voice_library():
    with open(os.environ["VOICEOVER_LIBRARY_FILEPATH"], "r") as f:
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