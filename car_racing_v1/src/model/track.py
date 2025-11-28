from __future__ import annotations
from typing import List, Tuple
import math


class Track:
    def __init__(self, waypoints: List[Tuple[float,float]], start_line: Tuple[Tuple[float,float], Tuple[float,float]], width: int, height: int):
        self.waypoints = waypoints
        self.start_line = start_line  # (p1, p2)
        self.width = width
        self.height = height

    @staticmethod
    def default_track(w: int, h: int) -> 'Track':
        # Ovalado simple basado en el tamaño de pantalla
        cx, cy = w/2, h/2
        rx, ry = w*0.35, h*0.35
        pts = []
        for i in range(16):
            t = i/16 * 2*math.pi
            pts.append((cx + math.cos(t)*rx, cy + math.sin(t)*ry))
        # Línea de salida: vertical a la izquierda del centro
        start = (cx - rx, cy - 40)
        end = (cx - rx, cy + 40)
        return Track(pts, (start, end), w, h)

    def get_start_positions(self, count: int) -> List[Tuple[float,float,float]]:
        # Devuelve posiciones espaciadas cerca de la línea de salida, con ángulo hacia el primer waypoint
        p1, p2 = self.start_line
        sx, sy = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
        first_wp = self.waypoints[0]
        ang = math.degrees(math.atan2(first_wp[1]-sy, first_wp[0]-sx))
        positions = []
        offset = 30
        cols = 2
        for i in range(count):
            row = i // cols
            col = i % cols
            positions.append((sx - row*offset, sy + (col-0.5)*offset, ang))
        return positions

    def current_waypoint_for(self, car) -> Tuple[float,float]:
        idx = getattr(car, 'waypoint_index', 0)
        return self.waypoints[idx % len(self.waypoints)]

    def advance_waypoint_if_reached(self, car, threshold: float=40.0):
        tx, ty = self.current_waypoint_for(car)
        dx = tx - car.x
        dy = ty - car.y
        if dx*dx + dy*dy < threshold*threshold:
            car.waypoint_index = (car.waypoint_index + 1) % len(self.waypoints)

    def crossed_start_line(self, prev_pos: Tuple[float,float], new_pos: Tuple[float,float]) -> bool:
        # Chequeo simple de intersección de segmentos
        (x1,y1), (x2,y2) = self.start_line
        x3,y3 = prev_pos
        x4,y4 = new_pos

        def ccw(ax, ay, bx, by, cx, cy):
            return (cy-ay)*(bx-ax) > (by-ay)*(cx-ax)
        return (ccw(x1,y1,x3,y3,x4,y4) != ccw(x2,y2,x3,y3,x4,y4)) and (ccw(x1,y1,x2,y2,x3,y3) != ccw(x1,y1,x2,y2,x4,y4))
