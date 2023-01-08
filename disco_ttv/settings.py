from pydantic import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Items associated with the dataset management
    game_data_filepath: str
    voiceover_library_filepath: str
    audio_clip_directory: str

    # Items associated with model training
    model_directory: str
    training_datasets_directory: str
    output_directory: str
    test_dataset_name: str
    root_tacotron2_model_name: Optional(str)
    root_waveglow_model_name: Optional(str)

    @property
    def root_tacotron2_model_filepath(self):
        return os.path.join(self.model_directory, self.root_tacotron2_model_name)

    @property
    def root_waveglow_model_filepath(self):
        return os.path.join(self.model_directory, self.root_tacotron2_model_name)

    class Config:
        env_prefix = "DISCO_"
        env_file = ".env"
        case_sensitive = False