from ..models.dbtag import DBTag
from ..value_objects.tag import Tag


class TagMapper:

    @staticmethod
    def to_dbmodel(data: Tag) -> DBTag:
        return DBTag(
            id=data.id,
            value=data.value
        )

    @staticmethod
    def from_dbmodel(data: DBTag) -> Tag:
        return Tag(
            value=data.value
        )
