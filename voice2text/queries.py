import voice2text.data_structure as ds
import voice2text.data_entry as de
import voice2text.text_analysis as ta
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from typing import Iterable
from sqlalchemy.schema import Column


class QueryEngine:

    def __init__(self, 
        voice_library_filepath: str, 
        game_data_filepath: str, 
        audio_clip_directory: str):

        self.voice_library_filepath = voice_library_filepath
        self.game_data_filepath = game_data_filepath
        self.audio_clip_directory = audio_clip_directory

        self.engine = create_engine("sqlite:///:memory:", echo=True)
        ds.Base.metadata.create_all(self.engine)

    def read_in_data(self):
        de.read_in_voice_library(self.engine, os.environ["VOICEOVER_LIBRARY_FILEPATH"])
        de.read_in_dialogue_entries(self.engine, os.environ["GAME_DATA_FILEPATH"])
        de.read_in_audio_clips(self.engine, os.environ["AUDIO_CLIP_DIRECTORY"])
        de.read_in_actors(self.engine, os.environ["GAME_DATA_FILEPATH"])

    query_clips_by_actor_default_entities = [
        ds.DialogueEntry.raw_dialogue_entry, 
        ds.AudioClip.filepath,
        ds.Actor.name,
        ds.AudioClip.filename,
        ds.DialogueEntry.actor_id, 
    ]

    def query_clips_by_actor(self, 
        actor: str, 
        entities_to_retrieve: Iterable[Column] = query_clips_by_actor_default_entities) -> Iterable[Column]:
        with sessionmaker(bind=self.engine)() as session:
            clips = (session.query(ds.DialogueEntry)
                .join(ds.VoiceOverEntry, ds.VoiceOverEntry.articy_id==ds.DialogueEntry.articy_id)
                .join(ds.AudioClip, ds.AudioClip.filename==ds.VoiceOverEntry.filename)
                .join(ds.Actor, ds.Actor.actor_id == ds.DialogueEntry.actor_id)
                .with_entities(
                    *entities_to_retrieve
                    )
                .filter(ds.Actor.name == actor)
                .all()
                )
        return clips

    @property
    def session(self):
        return sessionmaker(bind=self.engine)()

    def build_training_dataset(self, actor, format="JSON"):
        clips = self.query_clips_by_actor(
            actor=actor, 
            entities_to_retrieve=self.query_clips_by_actor_default_entities)
        
        if format == "JSON":
            output = [{
                "dialogue": ta.extract_dialogue(clip.raw_dialogue_entry),
                "filepath": clip.filepath
            } for clip in clips if ta.extract_dialogue(clip.raw_dialogue_entry) != ""]
            return output