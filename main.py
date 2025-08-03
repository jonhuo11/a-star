import pygame
import sys
import heapq
import math

from typing import List, Tuple

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 480
MAP_TILE_SIZE = 16

DIRT_COLOR = (0, 100, 45)
WALL_COLOR = (100, 0, 45)
MARK_COLOR = (20,20,20)


class Map:
    FLOOR = 0
    WALL = 1
    def __init__(self, width_tiles, height_tiles, tile_size_px):
        self.width: int = width_tiles
        self.height: int = height_tiles
        self.tile_size_px: int = tile_size_px

        self.map = [[0] * self.height for _ in range(self.width)] # x, y
        self.marks = [[0] * self.height for _ in range(self.width)]

        print(f"{self.width * self.height} ({self.height}x{self.width})")

    def in_bounds(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height
    
    def is_walkable(self, tile):
        return self.map[tile[0]][tile[1]] == Map.FLOOR


    def same_size_map(self, fill_with: any) -> List[List[int]]:
        out = [[fill_with] * self.height for _ in range(self.width)]
        return out
    
    def regen(self, wall_ratio: float) -> None:
        self.map = [[
            0
        ] * self.height for _ in range(self.width)]
        for y in range(self.height):
            for x in range(self.width):
                self.map[x][y] =  0 if random.random() > wall_ratio else 1
        self.marks = [[0] * self.height for _ in range(self.width)]
        

    def mark(self, tile) -> None:
        self.marks[tile[0]][tile[1]] = 1


    def draw(self, screen: pygame.Surface):
        for x in range(self.width):
            for y in range(self.height):
                val = self.map[x][y]
                color = DIRT_COLOR
                if val == Map.WALL:
                    color = WALL_COLOR
                
                if self.marks[x][y] != 0:
                    color = MARK_COLOR

                pygame.draw.rect(
                    screen,
                    color, 
                    (x * self.tile_size_px, y * self.tile_size_px, self.tile_size_px, self.tile_size_px)
                )
                pygame.draw.rect(
                    screen,
                    (50,50,50), 
                    (x * self.tile_size_px, y * self.tile_size_px, self.tile_size_px, self.tile_size_px),
                    1
                )

    def lookup_tile(self, x: float, y: float) -> Tuple[int, int]:
        return (
            min(max(0, x // self.tile_size_px), self.width - 1),
            min(max(0, y // self.tile_size_px), self.height - 1)
        )
    

    def manhattan(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        ax, ay = a
        bx, by = b
        return abs(ax - bx) + abs(ay - by)
    

    def neighbors(self, tile: Tuple[int,int]) -> int:
        tx, ty = tile
        nb = [
            (tx + 1, ty),
            (tx - 1, ty),
            (tx, ty + 1),
            (tx, ty - 1)
        ]
        return [
            (nx, ny)
            for nx, ny in nb
            if self.in_bounds(nx, ny) and self.is_walkable((nx, ny))
        ]



def a_star(gridmap: Map, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
    g_costs = gridmap.same_size_map(math.inf) # minimum known g_costs
    parents = gridmap.same_size_map(None)
    start_x, start_y = start
    g_costs[start_x][start_y] = 0
    
    def h(n: Tuple[int, int]) -> int:
        return gridmap.manhattan(n, end)

    q = [(
        0 + h(start),
        0,
        start
    )] # (f_cost, g_cost, (x,y))
    
    found_path = False
    while q:
        _, g_cost, xy = heapq.heappop(q)
        x, y = xy

        if g_cost > g_costs[x][y]:
            continue # this is a stale heap entry

        if (x,y) == end:
            found_path = True
            break
        
        for nbx, nby in gridmap.neighbors((x, y)):
            # f(n) = h(n) + g(n)
            g_cost_prime = g_cost + 1 # g_cost of neighbor
            if g_cost_prime < g_costs[nbx][nby]:
                g_costs[nbx][nby] = g_cost_prime
                heapq.heappush(q, (
                    g_cost_prime + h((nbx, nby)),
                    g_cost_prime,
                    (nbx, nby)
                ))
                parents[nbx][nby] = xy
            

    if found_path:
        path = [end]
        while path[-1] != start:
            cx, cy = path[-1]
            path.append(parents[cx][cy])
            if path[-1] == None:
                return [] # invalid somehow
        path.reverse()
        return path

    return []

import random

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("A Star Demo")

    map_obj = Map(SCREEN_WIDTH // MAP_TILE_SIZE, SCREEN_HEIGHT // MAP_TILE_SIZE, MAP_TILE_SIZE)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                # pick two new points
                start = (
                    random.randint(0, map_obj.width - 1),
                    random.randint(0, map_obj.height - 1)
                )
                end = (
                    random.randint(0, map_obj.width - 1),
                    random.randint(0, map_obj.height - 1)
                )
                map_obj.regen(0.1)
                path = a_star(map_obj, start, end)
                print(len(path))
                for t in path:
                    map_obj.mark(t)

        screen.fill((0, 0, 0))
        map_obj.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()