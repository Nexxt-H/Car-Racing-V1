import pygame
from typing import List
from model.track import Track
from model.car import Car
from model.race import RaceState, RaceMode


class GameView:
    def __init__(self, width: int, height: int, title: str):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.font = pygame.font.SysFont("consolas", 18)
        self.bg_color = (20, 20, 20)

    def color_for(self, idx: int):
        palette = [
            (220,60,60), (60,200,80), (70,140,240), (240,200,70),
            (200,80,200), (60,220,200), (255,140,40)
        ]
        return palette[idx % len(palette)]

    def draw_track(self, track: Track):
        # Fondo
        self.screen.fill(self.bg_color)
        # Dibujar camino aproximado uniendo waypoints
        if track.waypoints:
            pygame.draw.lines(self.screen, (50,50,50), True, track.waypoints, 8)
        # Línea de salida
        pygame.draw.line(self.screen, (255,255,255), track.start_line[0], track.start_line[1], 4)

    def draw_cars(self, cars: List[Car]):
        for c in cars:
            # Placeholder: rectángulo rotado como coche
            surf = pygame.Surface((c.width, c.height), pygame.SRCALPHA)
            pygame.draw.rect(surf, c.color, (0,0,c.width,c.height), border_radius=4)
            # Flecha frente
            pygame.draw.polygon(surf, (255,255,255), [(c.width-6, c.height/2), (c.width-12, c.height/2-5), (c.width-12, c.height/2+5)])
            rot = pygame.transform.rotate(surf, -c.angle)
            rect = rot.get_rect(center=(c.x, c.y))
            self.screen.blit(rot, rect)

    def draw_hud(self, state: RaceState):
        # Mostrar posiciones y laps/time
        standings = state.standings()
        lines = [f"Mode: {state.config.mode.name}"]
        for i, p in enumerate(standings[:6]):
            status = "FIN" if p.finished else ("OUT" if p.eliminated else "RUN")
            lines.append(f"{i+1}. Car {p.car_id} | Lap {p.lap}/{state.config.total_laps} | t={p.time:5.1f} | {status}")
        if state.config.mode == RaceMode.TIME_TRIAL:
            lines.append(f"Time: {state.time:5.1f}/{state.config.time_limit:5.1f}")
        elif state.config.mode == RaceMode.ELIMINATION:
            lines.append(f"Next OUT in: {max(0.0, state.config.elimination_interval - state.elimination_timer):4.1f}s")
        y = 8
        for t in lines:
            txt = self.font.render(t, True, (255,255,255))
            self.screen.blit(txt, (8, y))
            y += 20

    def draw_scene(self, track: Track, cars: List[Car], state: RaceState):
        self.draw_track(track)
        self.draw_cars(cars)
        self.draw_hud(state)
        pygame.display.flip()
