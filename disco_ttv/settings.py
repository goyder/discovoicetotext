from pydantic import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Items associated with the dataset management
    game_data_filepath: str
    voiceover_library_filepath: str
    audio_clip_directory: str

    # Items associated with model training
    training_datasets_directory: str
    output_directory: str
    test_dataset_name: str

    class Config:
        env_prefix = "DISCO_"
        env_file = ".env"
        case_sensitive = False