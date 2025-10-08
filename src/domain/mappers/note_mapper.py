from ..entities.note import Note
from ..mappers.mapper import Mapper
from ..models.dbnote import DBNote


class NoteMapper(Mapper):

    def to_dbmodel(self, data: Note) -> DBNote:
        return DBNote(
            id=data.id,
            text=data.text,
            # tags=",".join(tag.value for tag in data.tags)  # Припускаємо, що теги зберігаються як кома-розділений рядок
        )

    def from_dbmodel(self, data: DBNote) -> Note:
        return Note(
            note_id=data.id,
            text=data.text,
            # tags=[Tag(tag_id=None, value=tag) for tag in data.tags.split(",")] if data.tags else []
        )