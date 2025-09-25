from __future__ import annotations

from typing import Optional, Any, TYPE_CHECKING

import tcod.event

from actions import Action, EscapeAction, BumpAction, WaitAction
import actions

if TYPE_CHECKING:
    from engine import Engine


MOVE_KEYS = {
    #arrow keys
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    tcod.event.KeySym.HOME: (-1, -1),
    tcod.event.KeySym.END: (-1, 1),
    tcod.event.KeySym.PAGEUP: (1, -1),
    tcod.event.KeySym.PAGEDOWN: (1, 1),
    #numpad keys
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_4: (-1, 0),
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_9: (1, -1),
    tcod.event.KeySym.KP_3: (1, 1),
    # vi keys
    tcod.event.KeySym.K: (0, -1),
    tcod.event.KeySym.J: (0, 1),
    tcod.event.KeySym.H: (-1, 0),
    tcod.event.KeySym.L: (1, 0),
    tcod.event.KeySym.Y: (-1, -1),
    tcod.event.KeySym.U: (1, -1),
    tcod.event.KeySym.B: (-1, 1),
    tcod.event.KeySym.N: (1, 1),
}

WAIT_KEYS = {
    tcod.event.KeySym.PERIOD,
    tcod.event.KeySym.KP_5,
    tcod.event.KeySym.CLEAR,
}


class EventHandler:
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        raise NotImplementedError()
    
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keyup(self, event: tcod.event.KeyUp) -> Optional[Action]:
        """No-op handler for key release events in the base EventHandler."""
        return None
    
    def dispatch(self, event: Any) -> Optional[Action]:
        """Dispatch an event to an `ev_*` method (replacement for EventDispatch).

        Keeps behavior compatible with the previous tcod.event.EventDispatch:
        - warns when `event.type` is None
        - warns when handler method is missing
        - returns the result of the `ev_*` call (or None)
        """
        import warnings

        event_type = getattr(event, "type", None)
        if event_type is None:
            warnings.warn("`event.type` attribute should not be None.", DeprecationWarning, stacklevel=2)
            return None
        # Some events may provide an empty string as the type. Treat that as
        # a harmless/ignored event instead of warning about a missing handler.
        if event_type == "":
            return None
        func_name = f"ev_{event_type.lower()}"
        func = getattr(self, func_name, None)
        if func is None:
            warnings.warn(f"{func_name} is missing from this EventHandler object.", RuntimeWarning, stacklevel=2)
            return None
        return func(event)

class MainGameEventHandler(EventHandler):
    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()


    def ev_windowclose(self, event: tcod.event.WindowEvent) -> Optional[Action]:
        """Handle window manager close request the same as quit."""
        raise SystemExit()

    # No-op handlers for common events we don't need to handle explicitly.
    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> Optional[Action]:
        return None

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[Action]:
        return None

    def ev_mousebuttonup(self, event: tcod.event.MouseButtonUp) -> Optional[Action]:
        return None

    def ev_windowshown(self, event: tcod.event.WindowEvent) -> Optional[Action]:
        return None

    def ev_windowexposed(self, event: tcod.event.WindowEvent) -> Optional[Action]:
        return None

    def ev_windowenter(self, event: tcod.event.WindowEvent) -> Optional[Action]:
        return None

    def ev_windowleave(self, event: tcod.event.WindowEvent) -> Optional[Action]:
        return None

    def ev_windowfocusgained(self, event: tcod.event.WindowEvent) -> Optional[Action]:
        return None

    def ev_windowfocuslost(self, event: tcod.event.WindowEvent) -> Optional[Action]:
        return None
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Action | None:
        action: Optional[Action] = None

        key = event.sym

        player = self.engine.player

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx=dx, dy=dy)

        elif key in WAIT_KEYS:
            action = WaitAction(player)

        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(player)

        
        return action

    def ev_keyup(self, event: tcod.event.KeyUp) -> Optional[Action]:
        """No-op handler for key release events."""
        return None
    

class GameOverEventHandler(EventHandler):
    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()


    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(self.engine.player)

        return action