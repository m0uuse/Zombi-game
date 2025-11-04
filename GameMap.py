# game_map.py
import pygame
import random

# Colors
WALL_COLOR = (100, 100, 100)
DOOR_COLOR = (150, 100, 50)

class GameMap:
    """
    Grid is cols x rows of tiles.
    Walls/doors are stored on edges:
      - horizontal walls: shape (rows+1, cols)  (lines between rows, including top and bottom borders)
      - vertical   walls: shape (rows, cols+1)  (lines between cols, including left and right borders)

    Each edge value is one of:
      None -> no wall
      "wall" -> solid wall (blocks)
      {"door": hp} -> door with hp (passable but breakable when attacked)
    """
    def __init__(self, grid_size, grid_width, grid_height):
        self.grid_size = grid_size
        self.cols = grid_width // grid_size
        self.rows = grid_height // grid_size

        # Create empty edge arrays
        self.h_walls = [[None for _ in range(self.cols)] for _ in range(self.rows + 1)]
        self.v_walls = [[None for _ in range(self.cols + 1)] for _ in range(self.rows)]

        # Optionally create random walls/doors for testing
        self.generate_random_edges()

    def generate_random_edges(self, wall_count=30, door_count=8):
        # Place random walls (on edges)
        for _ in range(wall_count):
            if random.choice([True, False]):
                # horizontal edge
                r = random.randint(0, self.rows)
                c = random.randint(0, self.cols - 1)
                self.h_walls[r][c] = "wall"
            else:
                # vertical edge
                r = random.randint(0, self.rows - 1)
                c = random.randint(0, self.cols)
                self.v_walls[r][c] = "wall"

        # Place some doors (replace some walls or set as door)
        for _ in range(door_count):
            if random.choice([True, False]):
                r = random.randint(0, self.rows)
                c = random.randint(0, self.cols - 1)
                self.h_walls[r][c] = {"door": 1}
            else:
                r = random.randint(0, self.rows - 1)
                c = random.randint(0, self.cols)
                self.v_walls[r][c] = {"door": 1}

    def _normalize_cells(self, gx, gy, tx, ty):
        """Return (from_cell, to_cell) normalized and check adjacency. Raise if not adjacent."""
        # from: (gx,gy) -> to: (tx,ty)
        if abs(gx - tx) + abs(gy - ty) != 1:
            raise ValueError("Cells are not adjacent")

        return (gx, gy), (tx, ty)

    def is_blocked(self, gx, gy, tx, ty):
        """
        Return True if a wall (non-door) blocks movement from (gx,gy) to (tx,ty).
        Doors do NOT block (they can be passed); use is_door_between to detect a door.
        """
        (gx, gy), (tx, ty) = self._normalize_cells(gx, gy, tx, ty)

        # moving up (ty = gy-1) => check horizontal line at row gy (because h_walls indexed 0..rows)
        if tx == gx and ty == gy - 1:
            edge = self.h_walls[gy][gx]
            return edge == "wall"
        # moving down (ty = gy+1) => check horizontal at row gy+1
        if tx == gx and ty == gy + 1:
            edge = self.h_walls[gy + 1][gx]
            return edge == "wall"
        # moving left (tx = gx-1) => check vertical at col gx
        if tx == gx - 1 and ty == gy:
            edge = self.v_walls[gy][gx]
            return edge == "wall"
        # moving right (tx = gx+1) => check vertical at col gx+1
        if tx == gx + 1 and ty == gy:
            edge = self.v_walls[gy][gx + 1]
            return edge == "wall"

        return False

    def is_wall_between(self, gx, gy, tx, ty):
        """Return True if a wall exists between (gx, gy) and (tx, ty)."""
        dx, dy = tx - gx, ty - gy
        if dx == 1:  # moving right
            return self.v_walls[gy][gx + 1]
        elif dx == -1:  # moving left
            return self.v_walls[gy][gx]
        elif dy == 1:  # moving down
            return self.h_walls[gy + 1][gx]
        elif dy == -1:  # moving up
            return self.h_walls[gy][gx]
        return False
    
    def is_door_between(self, gx, gy, tx, ty):
        (gx, gy), (tx, ty) = self._normalize_cells(gx, gy, tx, ty)

        if tx == gx and ty == gy - 1:
            edge = self.h_walls[gy][gx]
            return isinstance(edge, dict) and "door" in edge
        if tx == gx and ty == gy + 1:
            edge = self.h_walls[gy + 1][gx]
            return isinstance(edge, dict) and "door" in edge
        if tx == gx - 1 and ty == gy:
            edge = self.v_walls[gy][gx]
            return isinstance(edge, dict) and "door" in edge
        if tx == gx + 1 and ty == gy:
            edge = self.v_walls[gy][gx + 1]
            return isinstance(edge, dict) and "door" in edge
        return False

    def break_door_between(self, gx, gy, tx, ty):
        """Hit the door (reduce hp); if hp <= 0, remove edge (becomes None)."""
        (gx, gy), (tx, ty) = self._normalize_cells(gx, gy, tx, ty)

        def _hit(edge_container, r, c):
            edge = edge_container[r][c]
            if isinstance(edge, dict) and "door" in edge:
                edge["door"] -= 1
                if edge["door"] <= 0:
                    edge_container[r][c] = None
                    return True  # broken
                return False  # still door
            return False  # nothing to hit

        if tx == gx and ty == gy - 1:
            return _hit(self.h_walls, gy, gx)
        if tx == gx and ty == gy + 1:
            return _hit(self.h_walls, gy + 1, gx)
        if tx == gx - 1 and ty == gy:
            return _hit(self.v_walls, gy, gx)
        if tx == gx + 1 and ty == gy:
            return _hit(self.v_walls, gy, gx + 1)

        return False

    def draw(self, surface):
        """Draw walls and doors as lines on the grid lines."""
        gs = self.grid_size
        # Horizontal wall lines
        for r in range(self.rows + 1):
            for c in range(self.cols):
                edge = self.h_walls[r][c]
                if edge is None:
                    continue
                x1 = c * gs
                x2 = (c + 1) * gs
                y = r * gs  # line y
                if edge == "wall":
                    pygame.draw.line(surface, WALL_COLOR, (x1, y), (x2, y), 6)
                else:  # door dict
                    # draw thinner line in door color (or a gap with door marker)
                    pygame.draw.line(surface, DOOR_COLOR, (x1, y), (x2, y), 6)

        # Vertical wall lines
        for r in range(self.rows):
            for c in range(self.cols + 1):
                edge = self.v_walls[r][c]
                if edge is None:
                    continue
                y1 = r * gs
                y2 = (r + 1) * gs
                x = c * gs  # line x
                if edge == "wall":
                    pygame.draw.line(surface, WALL_COLOR, (x, y1), (x, y2), 6)
                else:
                    pygame.draw.line(surface, DOOR_COLOR, (x, y1), (x, y2), 6)

    # Utility to set an edge explicitly
    def set_wall(self, orientation, row, col, kind="wall"):
        """
        orientation: 'h' or 'v'
        For 'h', row in 0..rows, col in 0..cols-1
        For 'v', row in 0..rows-1, col in 0..cols
        kind: "wall" or {"door": hp}
        """
        if orientation == "h":
            self.h_walls[row][col] = kind
        else:
            self.v_walls[row][col] = kind
