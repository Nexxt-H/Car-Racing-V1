# Car Racing V1

## 1. Descripción general

Juego de carreras en 2D con pygame. Incluye modos: vueltas con posiciones, contrarreloj y eliminación. Soporta 1 jugador contra IA y 2 jugadores local. Vista superior y pista/auto con sprites 2D (con placeholders hasta reemplazar por PNGs reales).

- ¿Qué problema resuelve?
  - Permite practicar POO + MVC y mecánicas básicas de carreras: aceleración, giro, IA por waypoints, conteo de vueltas y cronómetro.
- ¿Quiénes serían los usuarios típicos?
  - Estudiantes y jugadores casuales que quieran una carrera arcade simple.

## 2. Objetivos del proyecto

### Objetivo general

Construir un juego de carreras arcade en pygame aplicando POO + MVC y múltiples modos de juego.

### Objetivos específicos
- Implementar pistas con puntos de control (waypoints) para IA y validación de vueltas.
- Añadir IA simple que sigue waypoints.
- Soportar 1P vs IA y 2P local.
- Modos: vueltas, contrarreloj, eliminación.
- Arquitectura MVC clara y separación de responsabilidades.

## 3. Funcionalidades principales

- [x] Selección de modo: Vueltas / Contrarreloj / Eliminación.
- [x] Soporte de 1P vs IA.
- [x] Soporte de 2P local.
- [x] Pista con waypoints (procedural) y validador de vueltas.
- [x] Física arcade (aceleración sencilla, giro inmediato).
- [x] HUD: vuelta actual, tiempo y posiciones.
- [ ] Cargar sprites PNG reales (autos y pista) desde `src/view/assets/`.
- [ ] Sonidos básicos.

## 4. Arquitectura del software (MVC + POO)

### 4.1 Diseño MVC

**Modelo (Model)**
- Clases principales: `Car`, `AIController`, `Track`, `RaceConfig`, `RaceState`.
- Responsabilidades:
  - Lógica de movimiento, velocidad, ángulo y estado (Car).
  - Seguimiento de waypoints y objetivo de conducción (AIController).
  - Datos de la pista: waypoints, línea de meta y validación de vueltas (Track).
  - Configuración de carrera (vueltas, jugadores, modo) y estado de carrera (tiempos, posiciones).

**Vista (View)**
- `GameView` (pygame): dibuja pista, autos, HUD, menús. No contiene lógica de negocio.

**Controlador (Controller)**
- `GameController`: orquesta el ciclo del juego, procesa input del usuario, actualiza el modelo y pide a la vista dibujar. Conecta modelo y vista.

Diagrama (simplificado):

Usuario -> GameController -> (Model: Car/Track/RaceState) -> GameView
                   ^                                     |
                   |_____________________________________|

### 4.2 Aplicación de los pilares de POO

**Encapsulamiento**
- Atributos internos de `Car` (velocidad, ángulo, aceleración) protegidos mediante métodos.
- `RaceState` expone métodos para actualizar tiempos/vueltas sin exponer estructuras internas.

**Abstracción**
- `AIController` abstrae la lógica de seguimiento de waypoints.
- `Track` abstrae detección de paso por meta/waypoint.

**Herencia**
- Se puede extender `BaseController` (opcional). Para el MVP se usa composición (IA separada) y clases claras por responsabilidad.

**Polimorfismo**
- Entrada del jugador vs. controlador IA: ambos exponen una interfaz de "comandos de control" que el controlador traduce a acciones del `Car`.

## 5. Librerías de Python utilizadas

- pygame (render, input, reloj, superficies)

## 6. Instalación y ejecución

```bash
# Clonar el repo (ejemplo)
# git clone https://github.com/usuario/car_racing_v1.git
# cd car_racing_v1

# Crear entorno (opcional) e instalar dependencias
pip install -r requirements.txt

# Ejecutar el juego
python -m src.main
```

Resolución predeterminada: 1280x720.

Controles:
- Jugador 1: Flechas (↑ acelerar, ↓ frenar, ←/→ girar).
- Jugador 2: WASD (W acelerar, S frenar, A/D girar).
- Pausa: Esc.

## 7. Limitaciones y trabajo futuro

- Sprites reales pendientes (PNG). De momento se usan placeholders generados por código si no hay assets.
- Colisiones con bordes simplificadas (ancho de pista). Se puede mejorar con máscaras.
- IA simple (waypoints). Se puede mejorar con sobrepasos y agresividad.

## Checklist de POO y MVC

### POO
- [x] Al menos 3 clases con responsabilidades claras (`Car`, `Track`, `RaceState`).
- [x] Explicación de encapsulamiento.
- [x] Explicación de abstracción.
- [x] Explicación de herencia/polimorfismo (enfoque composicional + interfaces de control).

### MVC
- [x] Módulo `model` con clases de lógica de negocio.
- [x] Módulo `view` solo dibuja/intefaz.
- [x] Módulo `controller` conecta modelo y vista.
- [x] La vista no accede a datos directamente, todo pasa por el controlador.
- [x] Uso de al menos una librería externa (pygame).
