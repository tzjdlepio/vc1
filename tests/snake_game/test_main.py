import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import pygame
import runpy

# 強制進入 dummy 模式，這是 CI 運作的關鍵
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
            def on_reset(): mock_game.is_over = False
            mock_game.reset.side_effect = on_reset
            
            # 準備事件：C -> ESC
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

    def test_ultimate_100_coverage(self):
        """
        擊中最後的第 12 行與第 81 行，且保證不卡住。
        """
        # 1. 準備：計算 project_root 並暫時從 sys.path 移除它
        current_dir = os.path.dirname(os.path.abspath("asgards/snake_game/main.py"))
        project_root = os.path.abspath(os.path.join(current_dir, "../../"))
        
        original_path = sys.path.copy()
        if project_root in sys.path:
            # 移除所有符合的路徑
            sys.path = [p for p in sys.path if os.path.abspath(p) != project_root]

        try:
            # 2. 透過 Patch pygame.init 讓 main() 一進去就 SystemExit 退出
            with patch('pygame.init', side_effect=SystemExit), \
                 patch('pygame.display.set_mode'), \
                 patch('pygame.display.set_caption'), \
                 patch('pygame.time.Clock'), \
                 patch('pygame.font.SysFont'), \
                 patch('pygame.quit'):
                
                # 3. 執行 runpy，這會執行整個 main.py
                # 因為 project_root 不在 sys.path，會執行第 12 行
                # 因為 run_name 是 __main__，會執行第 81 行
                # 因為 pygame.init 會 SystemExit，所以不會卡在迴圈
                runpy.run_path("asgards/snake_game/main.py", run_name="__main__")
        except SystemExit:
            pass
        finally:
            # 還原路徑
            sys.path = original_path

if __name__ == "__main__":
    unittest.main()
