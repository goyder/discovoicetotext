from tkinter import dialog
from pyparsing import Set
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
import disco_ttv.data_structure as ds
import json
import os
import os.path


"""Voice library conversions"""


def convert_voice_library_json_to_mapping(voice_library: dict) -> dict:
    voice_library_mapped = [
        convert_voice_library_mapping(item)
        for item in voice_library["clipInformations"]
    ]
    return voice_library_mapped


def convert_voice_library_mapping(voice_library_item: dict) -> dict:
    return {
        "asset_name": voice_library_item["AssetName"],
        "articy_id": voice_library_item["ArticyID"],
        "asset_bundle": voice_library_item["AssetBundle"],
        "path_to_clip_in_project": voice_library_item["PathToClipInProject"],
        "filename": voice_library_item["PathToClipInProject"].split("\\")[-1],
    }


def read_in_voice_library(engine: Engine, voice_library_filepath: str):
    with open(voice_library_filepath, "r") as f:
        voice_library_json = json.load(f)
    voice_library = convert_voice_library_json_to_mapping(voice_library_json)
    with sessionmaker(bind=engine)() as session:
        session.bulk_insert_mappings(ds.VoiceOverEntry, voice_library)
        session.commit()


"""Dialogue entry conversions"""


dialogue_entry_mapping_key = {
    "Articy Id": "articy_id",
    "Dialogue Text": "raw_dialogue_entry",
    "Actor": "actor_id",
    "Conversant": "conversant_id",
}


def extract_dialogue_entry_mappings(dialogue_entry: dict) -> dict:
    fields = {field["title"]: field["value"] for field in dialogue_entry["fields"]}
    return {value: fields[key] for key, value in dialogue_entry_mapping_key.items()}


def extract_dialogue_entries_from_conversation(conversation: dict):
    """
    Pull out dialogue entries from conversation objects.
    """
    required_field_titles = set(dialogue_entry_mapping_key.keys())
    dialogue_entries = conversation["dialogueEntries"]
    mapped_dialogue_entries = []
    for dialogue_entry in dialogue_entries:
        field_titles = [
            field["title"]
            for field in dialogue_entry["fields"]
            if field["title"] in required_field_titles
        ]
        if set(field_titles) != required_field_titles:
            continue
        mapped_dialogue_entries.append(extract_dialogue_entry_mappings(dialogue_entry))
    return mapped_dialogue_entries


def convert_conversation_node_json_to_mapping(conversation_nodes_json: dict):
    dialogue_entries = []
    for conversation_node in conversation_nodes_json:
        dialogue_entries += extract_dialogue_entries_from_conversation(
            conversation_node
        )
    return dialogue_entries


def read_in_dialogue_entries(engine: Engine, game_data_filepath: str):
    with open(game_data_filepath, "r") as f:
        conversation_nodes_json = json.load(f)["conversations"]
    conversation_node_mapping = convert_conversation_node_json_to_mapping(
        conversation_nodes_json
    )
    with sessionmaker(bind=engine)() as session:
        session.bulk_insert_mappings(ds.DialogueEntry, conversation_node_mapping)
        session.commit()


"""Audio Clip extractions"""


def extract_audio_clip_mappings(directory: str) -> dict:
    file_list = os.listdir(directory)
    file_list = [
        file for file in file_list if os.path.splitext(file)[-1].lower() == ".wav"
    ]
    audio_clip_mapping = [
        {
            "filename": filename,
            "filepath": os.path.join(directory, filename),
            "size": os.path.getsize(os.path.join(directory, filename)),
        }
        for filename in file_list
    ]
    return audio_clip_mapping


def read_in_audio_clips(engine: Engine, directory: str):
    audio_clip_mapping = extract_audio_clip_mappings(directory)
    with sessionmaker(bind=engine)() as session:
        session.bulk_insert_mappings(ds.AudioClip, audio_clip_mapping)
        session.commit()


"""Actor ID extraction"""


actor_mapping_key = {"Name": "name", "character_short_name": "character_short_name"}


def extract_actor_field_mappings(actor_object: dict) -> dict:
    fields = {field["title"]: field["value"] for field in actor_object["fields"]}
    return {value: fields[key] for key, value in actor_mapping_key.items()}


def extract_actor_mappings(actor_objects: list):
    required_field_titles = set(actor_mapping_key.keys())
    mapped_actors = []
    for actor_object in actor_objects:
        field_titles = [
            field["title"]
            for field in actor_object["fields"]
            if field["title"] in required_field_titles
        ]
        if set(field_titles) != required_field_titles:
            continue
        actor_mapping = extract_actor_field_mappings(actor_object)
        actor_mapping["actor_id"] = actor_object["id"]
        mapped_actors.append(actor_mapping)
    return mapped_actors


def read_in_actors(engine: Engine, game_data_filepath: str):
    with open(game_data_filepath, "r") as f:
        actor_json = json.load(f)["actors"]
    actor_mappings = extract_actor_mappings(actor_json)
    with sessionmaker(bind=engine)() as session:
        session.bulk_insert_mappings(ds.Actor, actor_mappings)
        session.commit()
