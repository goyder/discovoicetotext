from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
import voice2text.data_structure as ds
import json
import os

def convert_voice_library_json_to_mapping(voice_library: dict) -> dict:
    voice_library_mapped = [
        convert_voice_library_mapping(item) for item in voice_library["clipInformations"]
    ]
    return voice_library_mapped


def convert_voice_library_mapping(voice_library_item: dict) -> dict:
    return {
        "asset_name": voice_library_item["AssetName"],
        "articy_id": voice_library_item["ArticyID"],
        "asset_bundle": voice_library_item["AssetBundle"],
        "path_to_clip_in_project": voice_library_item["PathToClipInProject"],
        "filename": os.path.split(voice_library_item["PathToClipInProject"])[-1]
    }


class VoiceLibrary:
    def __init__(self, engine: Engine, voice_library_filepath: str):
        self.engine = engine
        self.voice_library_filepath = voice_library_filepath

    def _read_in_voice_library(self):
        with open(self.voice_library_filepath, "r") as f:
            voice_library_json = json.load(f)
        voice_library = convert_voice_library_json_to_mapping(voice_library_json)
        session = sessionmaker(bind=self.engine)()
        session.bulk_insert_mappings(
            ds.VoiceOverEntry,
            voice_library
        )
        session.commit()


def convert_conversation_node_json_to_mapping(conversation_nodes_json: dict):
    return []


def read_in_conversation_nodes(engine: Engine, conversation_components_filepath: str):
    with open(conversation_components_filepath, "r") as f:
        conversation_nodes_json = json.load(f)
    conversation_node_mapping = convert_conversation_node_json_to_mapping(conversation_nodes_json)
    session = sessionmaker(bind=engine)()
    session.bulk_insert_mappings(
        ds.ConversationNode,
        conversation_node_mapping
    )
    session.commit()


        

        