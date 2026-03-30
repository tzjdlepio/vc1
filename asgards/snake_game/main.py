import os
import sys

# --- 路徑自動校正 (Path Hack) ---
# 取得目前檔案 (main.py) 的絕對路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
# 取得專案根目錄 (即包含 asgards 資料夾的那一層)
project_root = os.path.abspath(os.path.join(current_dir, "../../"))

# 將專案根目錄加入 Python 的搜尋路徑中
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# ------------------------------

import pygame
from asgards.snake_game.engine import SnakeGame
from asgards.snake_game.ui import SnakeUI
from asgards.snake_game.constants import (
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
