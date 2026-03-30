import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE,
    COLOR_BLACK, COLOR_WHITE, COLOR_RED, COLOR_GREEN, COLOR_BLUE
)

class SnakeUI:
    """
    負責遊戲的視覺化渲染。
    """
    def __init__(self, screen):
        self.screen = screen
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)

    def draw_score(self, score):
        """在畫面上方顯示分數。"""
        value = self.score_font.render(f"Your Score: {score}", True, COLOR_BLUE)
        self.screen.blit(value, [10, 10])

    def draw_snake(self, snake_list):
        """繪製蛇身。"""
        for x, y in snake_list:
            pygame.draw.rect(self.screen, COLOR_GREEN, [x, y, GRID_SIZE, GRID_SIZE])

    def draw_food(self, food_pos):
        """繪製食物。"""
        pygame.draw.rect(self.screen, COLOR_RED, [food_pos[0], food_pos[1], GRID_SIZE, GRID_SIZE])

    def display_message(self, msg, color):
        """在螢幕中央顯示訊息（如 Game Over）。"""
        mesg = self.font_style.render(msg, True, color)
        self.screen.blit(mesg, [WINDOW_WIDTH / 6, WINDOW_HEIGHT / 3])

    def update_display(self, game):
        """更新完整畫面內容。"""
        self.screen.fill(COLOR_BLACK)
        self.draw_food(game.food)
        self.draw_snake(game.snake)
        self.draw_score(game.score)
        pygame.display.update()
