import voice2text.data_entry as de
import voice2text.data_structure as ds
import os
import pytest
from sqlalchemy.engine import Engine, create_engine
import json


@pytest.fixture
def sql_engine() -> Engine:
    engine = create_engine("sqlite:///:memory:", echo=True)
    ds.Base.metadata.create_all(engine)
    return engine


def test_read_in_voice_library(sql_engine):
    voice_library = de.VoiceLibrary(
        engine=sql_engine,
        voice_library_filepath=os.environ["VOICEOVER_LIBRARY_FILEPATH"]
    )

    voice_library._read_in_voice_library()
    pass


def test_read_in_conversation_nodes(sql_engine):
    de.read_in_conversation_nodes(sql_engine, os.environ["GAME_DATA_FILEPATH"])
    pass


def test_convert_voice_library():
    with open(os.environ["VOICEOVER_LIBRARY_FILEPATH"], "r") as f:
        voice_library_json = json.load(f)
    
    voice_library_mapped = de.convert_voice_library_json_to_mapping(voice_library_json)
    for item in voice_library_mapped:
        for header in ["articy_id", "asset_name", "asset_bundle", "path_to_clip_in_project", "filename"]:
            assert header in item.keys()

    
