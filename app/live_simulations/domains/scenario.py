import uuid
from attr import dataclass, field


@dataclass
class Entity:
  """A base class for all entities"""
  id: uuid.UUID = field(default_factory=lambda: globals()['Entity'].next_id(), kw_only=True)

  @classmethod
  def next_id(cls) -> uuid.uuid4:
    """Generates new UUID"""
    return uuid.uuid4()


@dataclass
class Map(Entity):
    name: str = field()
    file: map = field()
    description:str = field()

