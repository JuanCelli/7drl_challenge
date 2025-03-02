from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

# Nos evita el import circular
if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    def __init__(self, entity: Entity) -> None:
            super().__init__()
            self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine
    
    def perform(self) -> None:
        """Realiza esta acción con los objetos necesarios para determinar su alcance.
        `self.engine` es el ámbito en el que se realiza esta acción.
        `self.entity` Es el objeto que realiza la acción.
        Este método puede ser sobreescrito por las subclases.
        """
        raise NotImplementedError()


class ActionWithDirection(Action):
    def __init__(self, entity: Entity, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy


    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Devuelve el destiono de esta acción."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)


    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
   def perform(self) -> None:
       target = self.blocking_entity
       if not target:
           return  # No hay entidad para atacar.

       print(f"Atacaste a un {target.name}")


class EscapeAction(Action):
    def perform(self) -> None:
        raise SystemExit()


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return  # Fuera de rango
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Bloqueado por un objeto
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
           return  # Bloqueado por otra entidad.

        self.entity.move(self.dx, self.dy)

class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.blocking_entity:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
