from .mapper import Mapper
from ..entities.note import Note
from ..models.dbnote import DBNote
from ..value_objects.tag import Tag


class NoteMapper(Mapper):

    @staticmethod
    def to_dbmodel(data: Note) -> DBNote:
        return DBNote(
            id=data.id,
            text=data.text,
            tags=",".join(str(tag) for tag in data.tags) if data.tags else None
        )

    @staticmethod
    def from_dbmodel(data: DBNote) -> Note:
        note = Note(
            text=data.text,
            note_id=data.id
        )

        if data.tags:
            for tag_str in data.tags.split(","):
                tag_vo = Tag(tag_str.strip())
                note.add_tag(tag_vo)

        return note
