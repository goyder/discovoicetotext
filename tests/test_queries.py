import test_data_entry as tde
import voice2text.queries as queries
import voice2text.data_structure as ds
import pytest
import os
from sqlalchemy.orm import Query


@pytest.fixture
def query_engine():
    query_engine = queries.QueryEngine(
        voice_library_filepath=os.environ["VOICEOVER_LIBRARY_FILEPATH"],
        game_data_filepath=os.environ["GAME_DATA_FILEPATH"],
        audio_clip_directory=os.environ["AUDIO_CLIP_DIRECTORY"]
    )
    query_engine.read_in_data()
    return query_engine


def test_retrieve_character_audio_clips(query_engine):
    actor = "Kim Kitsuragi"
    clips = query_engine.query_clips_by_actor(actor=actor)

    assert len(clips) > 3000


def test_complete_actor_queries(query_engine):
    outputs = Query(ds.Actor, session=query_engine.session).all()
    
    actor_id_mappings = {
        2: "Intellect",
        31: "Self-Educated Humanitarian",
        201: "Firefighter's Axe"
    }

    for output in outputs:
        if output.actor_id in actor_id_mappings.keys():
            assert output.name == actor_id_mappings[output.actor_id]


def test_complete_dialogue_entry_queries(query_engine):
    outputs = Query(ds.DialogueEntry, session=query_engine.session).all()

    pass


def test_generate_dataset(query_engine):
    output = query_engine.build_training_dataset("Kim Kitsuragi")
    pass


def test_generate_dataset_with_dataset_limit(query_engine: queries.QueryEngine):
    output = query_engine.build_training_dataset(
        "Kim Kitsuragi",
        item_count=100
        )
    assert len(output) == 100