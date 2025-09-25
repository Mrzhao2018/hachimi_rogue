from __future__ import annotations

from typing import TYPE_CHECKING

import entity

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    from game_map import GameMap


class BaseComponent:
    entity: Entity

    @property
    def engine(self) -> Engine:
        """Return the engine this component belongs to."""
        return self.entity.game_map.engine