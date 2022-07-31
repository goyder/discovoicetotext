from email.mime import audio
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.orm import sessionmaker, Session
import pytest

import voice2text.data_structure as ds


@pytest.fixture
def sql_engine() -> Engine:
    engine = create_engine("sqlite:///:memory:", echo=True)
    ds.Base.metadata.create_all(engine)
    return engine


def test_item_creation(sql_engine: Engine):
    Session = sessionmaker(bind=sql_engine)
    audioclip = ds.AudioClip(
        size=510,
        filename="here.wav",
        filepath="/home/user/here.wav"
    )
    session = Session()
    session.add(audioclip)
    session.commit()

    pulled_audioclip = session.query(ds.AudioClip).filter_by(filename="here.wav").first()

    assert pulled_audioclip.filename == audioclip.filename

    pass


def test_linked_item_creation(sql_engine: Engine):
    Session = sessionmaker(bind=sql_engine)
    audioclip = ds.AudioClip(
        size=500,
        filename="there.wav",
        filepath="home/there.wav"
    )

    conversation_node = ds.ConversationNode(
        id=100,
        node_name="node1",
        raw_conversation_text="The door is indifferent to your loneliness. The world does not care."
    )

    voice_over_entry = ds.VoiceOverEntry(
        articy_id="1a",
        asset_name="asset1",
        asset_bundle="kim",
        path_to_clip_in_project="kim/kim1.wav",
        filename=audioclip.filename,
    )

    session = Session()
    session.add(audioclip)
    session.add(conversation_node)
    session.add(voice_over_entry)
    session.commit()

    pulled_audioclip = session.query(ds.AudioClip).filter_by(filename="there.wav").first()

    pass