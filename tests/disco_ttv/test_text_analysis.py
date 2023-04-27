from dataclasses import dataclass
import disco_ttv.text_analysis as ta
import pytest


@dataclass
class DialogueExample:
    raw_dialogue_entry: str
    cleaned_dialogue_entry: str
    skip: bool = False


dialogue_example_cases = [
    DialogueExample(
        raw_dialogue_entry=""" He smiles ashamedly through the rebuke. He feels the sting for a moment before returning the key under the desk. "I understand. Is there anything else you want?" """,
        cleaned_dialogue_entry="I understand. Is there anything else you want?",
    ),
    DialogueExample(
        raw_dialogue_entry=""" Suddenly you tense up, blood is being pushed to your muscles. You should hound him on this, hound him *hard*, the prey drive says. """,
        cleaned_dialogue_entry="",
    ),
    DialogueExample(
        raw_dialogue_entry=""" "What are you, a chauvinist then? Hah!" """,
        cleaned_dialogue_entry="What are you, a chauvinist then? Hah!",
    ),
    DialogueExample(
        raw_dialogue_entry=""" "No way, I have duties. I'm a cop, I'm not talking to a tie. (Take the tie off.)" """,
        cleaned_dialogue_entry="No way, I have duties. I'm a cop, I'm not talking to a tie.",
        skip=True,
    ),
    DialogueExample(
        raw_dialogue_entry=""" "I\'ll see what I can do." """,
        cleaned_dialogue_entry="I'll see what I can do.",
    ),
    DialogueExample(
        raw_dialogue_entry=""" "Tsk... tsk..." she says to herself. "Took it like a common highwayman. Don\'t think this won\'t come up again during what will be an opportune moment for me, Officer Disco." She smiles.' """,
        cleaned_dialogue_entry="Tsk... tsk... Took it like a common highwayman. Don't think this won't come up again during what will be an opportune moment for me, Officer Disco.",
    ),
]


@pytest.mark.parametrize("dialogue_example", dialogue_example_cases)
def test_dialogue_case_conversion(dialogue_example: DialogueExample):
    if dialogue_example.skip:
        pytest.skip()
    cleaned_dialogue = ta.extract_dialogue(dialogue_example.raw_dialogue_entry)
    assert cleaned_dialogue == dialogue_example.cleaned_dialogue_entry
