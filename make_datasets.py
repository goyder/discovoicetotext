import voice2text.queries as queries
import os
from dotenv import load_dotenv

load_dotenv()

actor = "Kim Kitsuragi"

query_engine = queries.QueryEngine(
    voice_library_filepath=os.environ["VOICEOVER_LIBRARY_FILEPATH"],
    game_data_filepath=os.environ["GAME_DATA_FILEPATH"],
    audio_clip_directory=os.environ["AUDIO_CLIP_DIRECTORY"]
)
query_engine.read_in_data()
query_engine.output_training_dataset(
    actor=actor,
    dataset_name="kk_training_1",
    output_folder="datasets",
)