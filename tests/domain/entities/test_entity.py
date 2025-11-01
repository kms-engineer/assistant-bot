import pytest
from src.domain.entities.entity import Entity


class TestEntity:
    """Tests for the Entity class."""

    def test_entity_creation(self):
        """Test that an Entity object can be created."""
        entity = Entity()
        assert isinstance(entity, Entity)
