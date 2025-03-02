import numpy as np
from tcod.console import Console

import tile_types


class GameMap:
    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        
        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles que el jugador esta viendo
        self.explored = np.full((width, height), fill_value=False, order="F")  # Tiles que el jugador vio en el pasado
        

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
        
    
