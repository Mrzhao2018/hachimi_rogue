from typing import Optional, Any

import tcod.event

from actions import Action, EscapeAction, MovementAction


class EventHandler:
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

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

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

        if key == tcod.event.K_UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        
        return action