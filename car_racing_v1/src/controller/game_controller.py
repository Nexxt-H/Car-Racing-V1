import pygame
from model.race import RaceConfig, RaceMode, RaceState
from model.track import Track
from model.car import Car
from view.game_view import GameView


class GameController:
    def __init__(self, width: int, height: int, title: str = "Car Racing V1"):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.view = GameView(width, height, title)

        # Config inicial: modo por vueltas (3)
        self.config = RaceConfig(
            mode=RaceMode.LAPS,
            total_laps=3,
            players=1,
            ai_count=3,
        )
        
        # Modelo pista + autos
        self.track = Track.default_track(width, height)
        self.state = RaceState(self.config, self.track)

        # Crear autos (jugadores + IA) en la línea de salida
        start_positions = self.track.get_start_positions(self.config.players + self.config.ai_count)
        self.cars: list[Car] = []
        for idx, pos in enumerate(start_positions):
            is_player = idx < self.config.players
            car = Car(id_=idx, x=pos[0], y=pos[1], angle=pos[2], color=self.view.color_for(idx), is_player=is_player)
            self.cars.append(car)
        self.state.register_cars(self.cars)

        # Controles de jugadores
        self.player_bindings = [
            {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT},
            {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d},
        ]

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
        keys = pygame.key.get_pressed()
        # Aplicar controles a jugadores
        for i, car in enumerate(self.cars):
            if not car.is_player:
                continue
            binds = self.player_bindings[min(i, len(self.player_bindings)-1)]
            car.throttle = 1.0 if keys[binds["up"]] else 0.0
            car.brake = 1.0 if keys[binds["down"]] else 0.0
            steer = 0.0
            if keys[binds["left"]]:
                steer -= 1.0
            if keys[binds["right"]]:
                steer += 1.0
            car.steer = steer
        return True

    def update(self, dt: float):
        # Actualizar autos (IA simple placeholder: acelerar y corrección al waypoint actual)
        for car in self.cars:
            if not car.is_player:
                # AI simple: acelera y vira hacia el siguiente waypoint
                target = self.track.current_waypoint_for(car)
                car.seek_target(target)
                car.throttle = 0.9
                car.brake = 0.0
            car.update(dt)
            # Validar paso por meta/waypoint
            self.state.update_progress(car)
        # Actualizar estado general (tiempos, posiciones)
        self.state.update(dt)

    def render(self):
        self.view.draw_scene(self.track, self.cars, self.state)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            running = self.handle_input()
            self.update(dt)
            self.render()
        pygame.quit()
