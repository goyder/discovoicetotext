from multiprocessing.sharedctypes import Value
import voice2text.data_structure as ds
import voice2text.data_entry as de
import voice2text.text_analysis as ta
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from typing import Iterable, Optional
from sqlalchemy.schema import Column
import random
import shutil
from sox import file_info


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
        entities_to_retrieve: Iterable[Column] = query_clips_by_actor_default_entities,
        item_limit: Optional[int] = None) -> Iterable[Column]:
            
        with sessionmaker(bind=self.engine)() as session:
            clips = (session.query(ds.DialogueEntry)
                .join(ds.VoiceOverEntry, ds.VoiceOverEntry.articy_id==ds.DialogueEntry.articy_id)
                .join(ds.AudioClip, ds.AudioClip.filename==ds.VoiceOverEntry.filename)
                .join(ds.Actor, ds.Actor.actor_id == ds.DialogueEntry.actor_id)
                .with_entities(
                    *entities_to_retrieve
                    )
                .filter(ds.Actor.name == actor)
            )
            if item_limit:
                clips = clips.limit(item_limit).all()
            else:
                clips = clips.all()
        return clips

    @property
    def session(self):
        return sessionmaker(bind=self.engine)()

    def build_training_dataset(self, actor, format="JSON", item_limit=None):
        clips = self.query_clips_by_actor(
            actor=actor, 
            entities_to_retrieve=self.query_clips_by_actor_default_entities,
            item_limit=item_limit
            )
        
        if format == "JSON":
            output = [{
                "dialogue": ta.extract_dialogue(clip.raw_dialogue_entry),
                "filepath": clip.filepath,
                "filename": clip.filename
            } for clip in clips if ta.extract_dialogue(clip.raw_dialogue_entry) != ""]
            return output
        else:
            raise ValueError("Unsupported format. Must be one of: JSON")

    def output_training_dataset(self, actor, dataset_name: str, output_folder: str, item_limit=None, training_ratio: float=0.8, seed: int=1):
        """
        We push our training dataset to file.
        We distinguish between the "abs" filepaths and directories, containing real filepaths to where the files get dumped, 
        and the "relative" filepaths and directories, which are created relative the dataset directory. 
        """
        output_file_directory = os.path.join(output_folder, dataset_name)
        wav_output_file_abs_directory = os.path.join(output_file_directory, "wav")
        os.makedirs(wav_output_file_abs_directory, exist_ok=True)

        training_set = []
        validation_set = []
        outputs = self.build_training_dataset(actor=actor, item_limit=item_limit)
        for output in outputs:
            ch = file_info.channels(output["filepath"])
            if ch != 1: 
                print("Encountered multi-channel audio, skipping: ")
                print(output["filepath"])
                continue

            dataset_output_abs_filepath = os.path.join(wav_output_file_abs_directory, output["filename"])
            dataset_output_relative_filepath = os.path.join("wav", output["filename"])
            shutil.copy(
                output["filepath"],
                dataset_output_abs_filepath
            )
            if random.random() < training_ratio:
                training_set.append(
                    dataset_output_relative_filepath + "|" + output["dialogue"]
                )
            else:
                validation_set.append(
                    dataset_output_relative_filepath + "|" + output["dialogue"]
                )
        
        with open(os.path.join(output_file_directory, "train_filelist.txt"), "w") as f:
            f.write("\n".join(training_set))
        with open(os.path.join(output_file_directory, "validation_filelist.txt"), "w") as f:
            f.write("\n".join(validation_set))