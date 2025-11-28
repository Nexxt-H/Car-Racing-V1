from controller.game_controller import GameController

def main():
    game = GameController(width=1280, height=720, title="Car Racing V1")
    game.run()

if __name__ == "__main__":
    main()
