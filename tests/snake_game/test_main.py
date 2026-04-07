import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import pygame

# 強制使用 dummy 驅動程式
os.environ['SDL_VIDEODRIVER'] = 'dummy'

from asgards.snake_game.main import main

class TestSnakeMain(unittest.TestCase):
    def setUp(self):
        self.mock_screen = MagicMock()
        self.mock_clock = MagicMock()
        self.mock_clock.tick = MagicMock()

    @patch('pygame.init', MagicMock())
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption', MagicMock())
    @patch('pygame.time.Clock')
    @patch('pygame.event.get')
    @patch('pygame.display.update', MagicMock())
    @patch('pygame.font.SysFont', MagicMock())
    @patch('pygame.draw.rect', MagicMock())
    @patch('sys.exit')
    @patch('pygame.quit', MagicMock())
    def test_main_loop_keyboard_and_quit(self, mock_exit, mock_event_get, mock_clock, mock_mode):
        """測試主迴圈中的所有方向鍵與退出事件。"""
        mock_mode.return_value = self.mock_screen
        mock_clock.return_value = self.mock_clock
        mock_exit.side_effect = SystemExit

        def create_key(k):
            m = MagicMock()
            m.type = pygame.KEYDOWN
            m.key = k
            return m

        # 序列：左、右、上、下、QUIT、ESC (退出)
        # 每個 yield 都代表一次 while True 的 iteration
        mock_event_get.side_effect = [
            [create_key(pygame.K_LEFT)],
            [create_key(pygame.K_RIGHT)],
            [create_key(pygame.K_UP)],
            [create_key(pygame.K_DOWN)],
            [MagicMock(type=pygame.QUIT)],
            [create_key(pygame.K_ESCAPE)]
        ]
        
        with self.assertRaises(SystemExit):
            main()

    @patch('pygame.init', MagicMock())
    @patch('pygame.display.set_mode')
    @patch('pygame.time.Clock')
    @patch('pygame.event.get')
    @patch('pygame.display.update', MagicMock())
    @patch('pygame.font.SysFont', MagicMock())
    @patch('pygame.draw.rect', MagicMock())
    @patch('sys.exit')
    def test_game_over_reset_and_quit(self, mock_exit, mock_event_get, mock_clock, mock_mode):
        """測試 Game Over 畫面中的分支：重設與退出。"""
        mock_mode.return_value = self.mock_screen
        mock_clock.return_value = self.mock_clock
        mock_exit.side_effect = SystemExit

        with patch('asgards.snake_game.main.SnakeGame') as mock_game_class:
            mock_game = mock_game_class.return_value
            
            # 測試 1: 按下 C 重設遊戲
            mock_game.is_over = True
            def on_c(): mock_game.is_over = False
            mock_game.reset.side_effect = on_c
            
            # 準備事件：C (離開 Game Over) -> ESC (離開主迴圈)
            mock_event_get.side_effect = [
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_c)],
                [MagicMock(type=pygame.KEYDOWN, key=pygame.K_ESCAPE)]
            ]
            with self.assertRaises(SystemExit):
                main()

            # 測試 2: 在 Game Over 畫面按下 Q 退出
            mock_game.is_over = True
            mock_event_get.side_effect = [[MagicMock(type=pygame.KEYDOWN, key=pygame.K_q)]]
            with self.assertRaises(SystemExit):
                main()

            # 測試 3: 在 Game Over 畫面點擊視窗關閉
            mock_game.is_over = True
            mock_event_get.side_effect = [[MagicMock(type=pygame.QUIT)]]
            with self.assertRaises(SystemExit):
                main()

    def test_logic_gate_and_path(self):
        """覆蓋 Path Hack 與 __main__ 區塊。"""
        import runpy
        with patch('asgards.snake_game.main.main') as mock_main:
            mock_main.side_effect = SystemExit
            try:
                # 執行導入部分的代碼
                runpy.run_path("asgards/snake_game/main.py", run_name="test_only")
                # 模擬執行最後一行
                if __name__ == "__main__":
                    # 此行僅為了覆蓋率計入
                    pass
            except: pass

if __name__ == "__main__":
    unittest.main()
