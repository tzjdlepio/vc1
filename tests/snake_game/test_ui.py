import unittest
from unittest.mock import MagicMock, patch
import pygame
from asgards.snake_game.ui import SnakeUI
from asgards.snake_game.constants import COLOR_BLACK, COLOR_WHITE, COLOR_RED, COLOR_GREEN, COLOR_BLUE

class TestSnakeUI(unittest.TestCase):
    """
    測試 SnakeUI 視覺化渲染。
    """
    def setUp(self):
        # 模擬 pygame.Surface 作為螢幕
        self.mock_screen = MagicMock(spec=pygame.Surface)
        
        # 模擬 pygame.font 相關功能，避免在 CI 環境中因為沒有字型而失敗
        with patch('pygame.font.SysFont') as mock_sysfont:
            self.mock_font = MagicMock()
            mock_sysfont.return_value = self.mock_font
            self.ui = SnakeUI(self.mock_screen)

    def test_draw_score(self):
        """測試分數繪製。"""
        self.ui.draw_score(10)
        # 檢查是否呼叫了 render 和 blit
        self.mock_font.render.assert_called()
        self.mock_screen.blit.assert_called()

    def test_draw_snake(self):
        """測試蛇身繪製。"""
        snake_list = [(20, 20), (40, 20), (60, 20)]
        with patch('pygame.draw.rect') as mock_rect:
            self.ui.draw_snake(snake_list)
            # 應呼叫 3 次繪製矩形
            self.assertEqual(mock_rect.call_count, 3)

    def test_draw_food(self):
        """測試食物繪製。"""
        food_pos = (100, 100)
        with patch('pygame.draw.rect') as mock_rect:
            self.ui.draw_food(food_pos)
            mock_rect.assert_called_once()

    def test_display_message(self):
        """測試訊息顯示。"""
        self.ui.display_message("Test Message", COLOR_RED)
        self.mock_font.render.assert_called_with("Test Message", True, COLOR_RED)
        self.mock_screen.blit.assert_called()

    @patch('pygame.display.update')
    def test_update_display(self, mock_update):
        """測試完整畫面更新。"""
        # 模擬 game 物件
        mock_game = MagicMock()
        mock_game.food = (100, 100)
        mock_game.snake = [(20, 20)]
        mock_game.score = 5

        with patch('pygame.draw.rect') as mock_rect:
            self.ui.update_display(mock_game)
            
            # 應呼叫 fill 清除畫面
            self.mock_screen.fill.assert_called_with(COLOR_BLACK)
            # 應繪製食物與蛇
            self.assertGreaterEqual(mock_rect.call_count, 2)
            # 應更新顯示
            mock_update.assert_called_once()

if __name__ == "__main__":
    unittest.main()
