import cv2
import numpy as np
from typing import Any, Dict
from collections import deque, defaultdict


class Service:

    def __init__(self, config: Dict[str, Any]):
        self._bg_class = config.get('back_class', 0)
        self._wall_class = config.get('wall_class', 9)
        self._door_class = config.get('door_class', 10)

    def _bfs(self, mask: np.ndarray,
                   ff_mask: np.ndarray,
                   visited: np.ndarray,
                   start_x: int,
                   start_y: int) -> int:
        colors = defaultdict(lambda: 0)
        queue = deque()
        queue.append((start_x, start_y))
        visited[start_x, start_y] = True

        ddx = [0, 1,  0, -1]
        ddy = [1, 0, -1,  0]

        while len(queue) > 0:
            fx, fy = queue.pop()

            for dx, dy in zip(ddx, ddy):
                cx, cy = fx + dx, fy + dy
                if cx < 0: continue
                if cy < 0: continue
                if cx >= visited.shape[0]: continue
                if cy >= visited.shape[1]: continue

                if not visited[cx, cy]:
                    if ff_mask[cx, cy] != 0:
                        queue.appendleft((cx, cy))
                        visited[cx, cy] = True
                    else:
                        colors[mask[cx, cy]] += 1
                        visited[cx, cy] = True

        colors = [(k, v) for k, v in colors.items()]
        major_k, _ = max(colors, key=lambda x: x[1])
        return int(major_k)

    def _process(self, mask: np.ndarray) -> np.ndarray:
        height, width = mask.shape
        ff_mask = np.zeros((height + 2, width + 2), np.uint8)
        ff_mask[1:-1, 1:-1] = np.not_equal(mask, self._bg_class)
        ff_flags = 4 | (1 << 8) | cv2.FLOODFILL_MASK_ONLY
        cv2.floodFill(mask, ff_mask, (0, 0), 10, flags=ff_flags)

        ff_mask_short = np.copy(ff_mask[1:-1, 1:-1] == 0)
        ff_mask = np.copy(ff_mask != 0).astype(np.uint8)

        visited = np.zeros_like(ff_mask_short)
        for x in range(visited.shape[0]):
            for y in range(visited.shape[1]):
                if (not visited[x, y]) and (ff_mask_short[x, y] != 0):
                    major = self._bfs(mask, ff_mask_short, visited, x, y)
                    cv2.floodFill(mask, ff_mask, (y, x), major)

        return mask

    def process(self, mask: np.ndarray) -> np.ndarray:
        mask = np.copy(mask)
        mask = self._process(mask)
        return mask
