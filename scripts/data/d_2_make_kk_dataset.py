import disco_ttv.queries as queries
from disco_ttv.settings import Settings

settings = Settings()

actor = "Kim Kitsuragi"
dataset_name = "kk_training_dataset_1"
output_folder = settings.training_datasets_directory

query_engine = queries.QueryEngine(
    settings=settings
)
query_engine.read_in_data()
query_engine.output_training_dataset(
    actor=actor,
    dataset_name=dataset_name,
    output_folder=output_folder,
)