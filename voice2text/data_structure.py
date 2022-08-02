from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Boolean, Column, Integer, String, null
from sqlalchemy import ForeignKey

Base = declarative_base()

class AudioClip(Base):
    __tablename__ = "audio_clip"

    id = Column(Integer, primary_key=True)
    size = Column(Integer)
    filename = Column(String)
    filepath = Column(String)

    voiceover_entry = relationship("VoiceOverEntry")


class DialogueEntry(Base):
    __tablename__ = "dialogue_entry"

    id = Column(Integer, primary_key=True)
    articy_id = Column(String)
    raw_dialogue_entry = Column(String, nullable=True)
    cleaned_dialogue_entry = Column(String, nullable=True)
    narrator_override = Column(Boolean, nullable=True)
    actor_id = Column(Integer, nullable=True)
    conversant_id = Column(Integer, nullable=True)

    voiceover_entry = relationship("VoiceOverEntry", back_populates="dialogue_entry", uselist=False)


class VoiceOverEntry(Base):
    __tablename__ = "voiceover_entry"

    articy_id = Column(String, ForeignKey("dialogue_entry.articy_id"), primary_key=True)
    asset_name = Column(String)
    asset_bundle = Column(String)
    path_to_clip_in_project = Column(String)
    filename = Column(String, ForeignKey("audio_clip.filename"), nullable=True)
    dialogue_entry = relationship("DialogueEntry", back_populates="voiceover_entry", uselist=False)

    audio_clip = relationship("AudioClip", back_populates="voiceover_entry")

