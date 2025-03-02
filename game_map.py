from __future__ import annotations
from typing import Iterable, Optional, TYPE_CHECKING
import numpy as np
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
   from entity import Entity

class GameMap:
    def __init__(self, width: int, height: int,entities: Iterable[Entity] = ()) -> None:
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        
        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles que el jugador esta viendo
        self.explored = np.full((width, height), fill_value=False, order="F")  # Tiles que el jugador vio en el pasado
        

    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[Entity]:
       for entity in self.entities:
           if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
               return entity

       return None

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Dibuja el mapa.
        
        Si el Tile esta en la matriz "Visible", entonces lo dibuja con los colores de "light".
        Si no está en "Visible", pero SI esta en "Explored", entonces lo dibuja con los colores de "Dark".
        Si no esta en ningun lado, el predeterminado es "SHROUD""
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
           condlist=[self.visible, self.explored],
           choicelist=[self.tiles["light"], self.tiles["dark"]],
           default=tile_types.SHROUD
           )
        for entity in self.entities:
           # Imprime solo las entidades dentro del FOV
            if self.visible[entity.x, entity.y]:
               console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
        
    
