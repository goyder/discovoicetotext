import boto3
import os
from disco_ttv.settings import Settings

settings = Settings()

s3 = boto3.resource("s3")
bucket = s3.Bucket("disco-ml-949012111517")

# Create all the required directories, as according to the settings directory.
game_data_directory = os.path.split(settings.game_data_filepath)[0]
voiceover_library_directory = os.path.split(settings.voiceover_library_filepath)[0]
audio_clip_directory = os.path.split(settings.audio_clip_directory)[0]

for directory in [
    settings.model_directory,
    settings.training_datasets_directory,
    settings.output_directory,
    game_data_directory,
    voiceover_library_directory,
    audio_clip_directory,
]:
    os.makedirs(directory, exist_ok=True)

# Pull in our Disco data
game_data_key = "gameassets/text/MonoBehaviour/Disco Elysium.json"
voiceover_library_key = "gameassets/text/MonoBehaviour/VoiceOverClipsLibrary.json"
audio_clip_root_key = "gameassets/disco/AudioClip/"

bucket.Object(game_data_key).download_file(settings.game_data_filepath)
bucket.Object(game_data_key).download_file(settings.game_data_filepath)
# Do our clunky syncing for the audioclip work
for item in bucket.objects.all():
    if item.key.startswith(audio_clip_root_key):
        key_filename = os.path.split(item.key)[-1]
        local_filepath = os.path.join(audio_clip_directory, key_filename)
        bucket.Object(item.key).download_file(local_filepath)

# Pull in our model data
tacotron2_key = "model/tacotron2_1032590_6000_amp"
waveglow_key = "model/waveglow_1076430_14000_amp"

bucket.Object(tacotron2_key).download_file(settings.root_tacotron2_model_filepath)
bucket.Object(waveglow_key).download_file(settings.root_waveglow_model_filepath)
