from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import MainGameEventHandler
from message_log import MessageLog
from render_functions import render_bar, render_names_at_mouse_location

if TYPE_CHECKING:
    from game_map import GameMap
    from entity import Actor
    from input_handlers import EventHandler

class Engine:
    game_map: GameMap
    # Use the base EventHandler type for the attribute so different
    # handler subclasses (e.g. MainGameEventHandler, GameOverEventHandler)
    # can be assigned at runtime without causing type checker errors.
    event_handler: "EventHandler"
    mouse_location: Tuple[int, int]

    def __init__(self, player: Actor):
        self.event_handler = MainGameEventHandler(self)
        self.player = player
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)

    def handle_enemy_turns(self) -> None:
        # Iterate actors and skip the player explicitly. Using set difference
        # caused type-checkers to complain (set[Actor] - {self.player}). This
        # loop is equivalent at runtime and clearer to type checkers.
        for entity in self.game_map.actors:
            if entity is self.player:
                continue
            if entity.ai:
                entity.ai.perform()


    def update_fov(self) -> None:
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_names_at_mouse_location(console, 21, 44, self)