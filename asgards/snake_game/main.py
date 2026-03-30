import pygame
import sys
from engine import SnakeGame
from ui import SnakeUI
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, SNAKE_SPEED,
    DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT,
    COLOR_RED
)

def main():
    """遊戲主入口點。"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('經典貪吃蛇遊戲')
    
    clock = pygame.time.Clock()
    game = SnakeGame()
    ui = SnakeUI(screen)

    while True:
        # 1. 遊戲結束畫面處理
        while game.is_over:
            screen.fill((0, 0, 0))
            ui.display_message("Game Over! Press C-Play Again or Q-Quit", COLOR_RED)
            ui.draw_score(game.score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_c:
                        game.reset()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        # 2. 事件監控（鍵盤輸入）
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.change_direction(DIR_LEFT)
                elif event.key == pygame.K_RIGHT:
                    game.change_direction(DIR_RIGHT)
                elif event.key == pygame.K_UP:
                    game.change_direction(DIR_UP)
                elif event.key == pygame.K_DOWN:
                    game.change_direction(DIR_DOWN)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # 3. 遊戲邏輯更新
        game.move()

        # 4. 畫面渲染
        ui.update_display(game)

        # 5. 控制 FPS
        clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    main()
