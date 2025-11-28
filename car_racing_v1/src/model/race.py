from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List


class RaceMode(Enum):
    LAPS = auto()
    TIME_TRIAL = auto()
    ELIMINATION = auto()


@dataclass
class RaceConfig:
    mode: RaceMode = RaceMode.LAPS
    total_laps: int = 3
    time_limit: float = 60.0
    elimination_interval: float = 15.0
    players: int = 1
    ai_count: int = 3


@dataclass
class CarProgress:
    car_id: int
    lap: int = 0
    time: float = 0.0
    finished: bool = False
    eliminated: bool = False


@dataclass
class RaceState:
    config: RaceConfig
    track: 'Track'
    time: float = 0.0
    elimination_timer: float = 0.0
    progress: List[CarProgress] = field(default_factory=list)

    def register_cars(self, cars: List['Car']):
        self.progress = [CarProgress(c.id) for c in cars]

    def update(self, dt: float):
        self.time += dt
        if self.config.mode == RaceMode.ELIMINATION:
            self.elimination_timer += dt
            if self.elimination_timer >= self.config.elimination_interval and len(self.progress) > 1:
                # Eliminar el último (mayor tiempo de vuelta + menor lap)
                self.elimination_timer = 0.0
                last = sorted(self.progress, key=lambda p: (p.lap, -p.time)) [0]
                last.eliminated = True

        # actualizar tiempos por coche
        for p in self.progress:
            if not (p.finished or p.eliminated):
                p.time += dt

    def update_progress(self, car: 'Car'):
        # Avanzar waypoint
        self.track.advance_waypoint_if_reached(car)
        # Chequear vuelta al cruzar linea de salida
        # Usamos una aproximación: si waypoint se reinicia a 0 y cruzó la línea
        # Para mejor precisión, almacenar posición previa; aquí lo haremos con un atributo temporal
        if not hasattr(car, '_prev_pos'):
            car._prev_pos = car.position()
        prev = car._prev_pos
        new = car.position()
        if self.track.crossed_start_line(prev, new):
            prog = self._prog(car.id)
            if not prog.finished and not prog.eliminated:
                prog.lap += 1
                if self.config.mode == RaceMode.LAPS and prog.lap >= self.config.total_laps:
                    prog.finished = True
        car._prev_pos = new

    def standings(self) -> List[CarProgress]:
        # Orden descendente: mayor lap y menor tiempo (tiempo es cronómetro individual)
        return sorted(self.progress, key=lambda p: (-p.lap, p.time))

    def _prog(self, car_id: int) -> CarProgress:
        for p in self.progress:
            if p.car_id == car_id:
                return p
        raise KeyError(car_id)
