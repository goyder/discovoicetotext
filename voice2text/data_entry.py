from tkinter import dialog
from pyparsing import Set
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
import voice2text.data_structure as ds
import json
import os


"""
Voice library conversions
"""


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

def read_in_voice_library(engine: Engine, voice_library_filepath: str):
    with open(voice_library_filepath, "r") as f:
        voice_library_json = json.load(f)
    voice_library = convert_voice_library_json_to_mapping(voice_library_json)
    with sessionmaker(bind=engine)() as session:
        session.bulk_insert_mappings(
            ds.VoiceOverEntry,
            voice_library
        )
        session.commit()


"""
Conversation node conversions
"""

dialogue_entry_mapping_key = {
    "Articy Id": "articy_id",
    "Dialogue Text": "raw_dialogue_entry",
    "Actor": "actor_id",
    "Conversant": "conversant_id"
}


def extract_dialogue_entry_mappings(dialogue_entry: dict) -> dict:
    fields = {
        field["title"]: field["value"] for field in dialogue_entry["fields"]
    }
    return {
        value: fields[key] for key, value in dialogue_entry_mapping_key.items()
    }


def extract_dialogue_entries_from_conversation(conversation: dict):
    """
    Pull out dialogue entries from conversation objects.
    """
    required_field_titles = set(dialogue_entry_mapping_key.keys())
    dialogue_entries = conversation["dialogueEntries"]
    mapped_dialogue_entries = []
    for dialogue_entry in dialogue_entries:
        field_titles = [field["title"] for field in dialogue_entry["fields"] if field["title"] in required_field_titles]
        if set(field_titles) != required_field_titles:
            continue
        mapped_dialogue_entries.append(extract_dialogue_entry_mappings(dialogue_entry))
    return mapped_dialogue_entries


def convert_conversation_node_json_to_mapping(conversation_nodes_json: dict):
    dialogue_entries = []
    for conversation_node in conversation_nodes_json:
        dialogue_entries += extract_dialogue_entries_from_conversation(conversation_node)
    return dialogue_entries


def read_in_dialogue_entries(engine: Engine, game_data_filepath: str):
    with open(game_data_filepath, "r") as f:
        conversation_nodes_json = json.load(f)["conversations"]
    conversation_node_mapping = convert_conversation_node_json_to_mapping(conversation_nodes_json)
    with sessionmaker(bind=engine)() as session:
        session.bulk_insert_mappings(
            ds.DialogueEntry,
            conversation_node_mapping
        )
        session.commit()


        

        