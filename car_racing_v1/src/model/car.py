import math
from typing import Tuple


class Car:
    def __init__(self, id_:int, x: float, y: float, angle: float, color: Tuple[int,int,int], is_player: bool=False):
        # Estado
        self.id = id_
        self.x = x
        self.y = y
        self.angle = angle  # grados
        self.v = 0.0  # velocidad
        self.color = color
        self.is_player = is_player

        # Controles (encapsulados via propiedades simples)
        self.throttle = 0.0
        self.brake = 0.0
        self.steer = 0.0

        # Parámetros de física arcade
        self.max_speed = 300.0
        self.acceleration = 600.0
        self.brake_power = 900.0
        self.friction = 300.0
        self.turn_speed = 180.0  # grados/seg con steer=1

        # Waypoint tracking
        self.waypoint_index = 0

        # Dimensiones para render placeholder
        self.width = 40
        self.height = 20

    def seek_target(self, target: Tuple[float,float]):
        # Gira hacia el objetivo con una corrección proporcional
        tx, ty = target
        dx = tx - self.x
        dy = ty - self.y
        desired_angle = math.degrees(math.atan2(dy, dx))
        # Normalizar diferencia de ángulo a [-180,180]
        diff = (desired_angle - self.angle + 540) % 360 - 180
        self.steer = max(-1.0, min(1.0, diff / 45.0))  # P sencillo

    def update(self, dt: float):
        # Actualizar velocidad
        if self.throttle > 0:
            self.v += self.acceleration * self.throttle * dt
        if self.brake > 0:
            self.v -= self.brake_power * self.brake * dt
        # Fricción simple
        if self.throttle == 0 and self.brake == 0:
            if self.v > 0:
                self.v = max(0.0, self.v - self.friction * dt)
            else:
                self.v = min(0.0, self.v + self.friction * dt)
        # Limitar velocidad
        self.v = max(-self.max_speed*0.3, min(self.max_speed, self.v))
        
        # Girar
        self.angle += self.turn_speed * self.steer * dt * (0.5 + 0.5*abs(self.v)/self.max_speed)
        self.angle %= 360

        # Mover
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.v * dt
        self.y += math.sin(rad) * self.v * dt

    def position(self) -> Tuple[float,float]:
        return (self.x, self.y)
