import re


def extract_dialogue(raw_dialogue_entry: str):
    extractions = re.findall('"([^"]*)"', raw_dialogue_entry)
    extractions = " ".join(extractions)
    return extractions
