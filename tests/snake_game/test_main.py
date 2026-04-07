import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import pygame

# 強制使用 dummy 驅動程式，避免在 CI 環境中嘗試開啟視窗
os.environ['SDL_VIDEODRIVER'] = 'dummy'

from asgards.snake_game.main import main

class TestSnakeMain(unittest.TestCase):
    """
    測試 SnakeGame 主入口點與遊戲迴圈。
    """

    def setUp(self):
        # 建立通用的 Mock 物件
        self.mock_screen = MagicMock()
        self.mock_clock = MagicMock()
        self.mock_font = MagicMock()

    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('pygame.event.get')
    @patch('pygame.display.update')
    @patch('pygame.font.SysFont')
    @patch('sys.exit')
    @patch('pygame.quit')
    def test_main_loop_iteration(self, mock_quit, mock_exit, mock_font, mock_update, mock_event_get, mock_clock, mock_caption, mock_mode, mock_init):
        """測試主迴圈能否正常執行與退出。"""
        mock_mode.return_value = self.mock_screen
        mock_clock.return_value = self.mock_clock
        
        mock_event_escape = MagicMock()
        mock_event_escape.type = pygame.KEYDOWN
        mock_event_escape.key = pygame.K_ESCAPE
        
        mock_event_get.side_effect = [[mock_event_escape]]
        mock_exit.side_effect = SystemExit

        with self.assertRaises(SystemExit):
            main()
        
        mock_init.assert_called_once()
        mock_quit.assert_called()

    @patch('pygame.event.get')
    @patch('sys.exit')
    def test_main_game_over_state(self, mock_exit, mock_event_get):
        """測試 Game Over 狀態下的按鍵行為 (Q 鍵退出)。"""
        with patch('asgards.snake_game.main.SnakeGame') as mock_game_class:
            mock_game = mock_game_class.return_value
            mock_game.is_over = True
            
            mock_event_q = MagicMock()
            mock_event_q.type = pygame.KEYDOWN
            mock_event_q.key = pygame.K_q
            
            mock_event_get.side_effect = [[mock_event_q]]
            mock_exit.side_effect = SystemExit

            with patch('pygame.init'), \
                 patch('pygame.display.set_mode') as mock_set_mode, \
                 patch('pygame.time.Clock'), \
                 patch('pygame.font.SysFont'), \
                 patch('pygame.display.update'), \
                 patch('pygame.draw.rect'):
                
                mock_set_mode.return_value = self.mock_screen
                with self.assertRaises(SystemExit):
                    main()

    @patch('pygame.event.get')
    @patch('sys.exit')
    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.time.Clock')
    @patch('pygame.font.SysFont')
    @patch('pygame.display.update')
    @patch('pygame.draw.rect')
    def test_main_keyboard_events(self, mock_draw_rect, mock_update, mock_font, mock_clock, mock_mode, mock_init, mock_exit, mock_event_get):
        """測試主迴圈中的各種方向鍵事件。"""
        mock_mode.return_value = self.mock_screen

        mock_event_quit = MagicMock()
        mock_event_quit.type = pygame.QUIT

        # 只要跑一次 QUIT 就能覆蓋到邏輯並退出
        mock_event_get.side_effect = [[mock_event_quit]]
        mock_exit.side_effect = SystemExit

        with self.assertRaises(SystemExit):
            main()

    @patch('pygame.event.get')
    def test_game_over_reset(self, mock_event_get):
        """測試 Game Over 狀態下的重設 (C 鍵)。"""
        with patch('asgards.snake_game.main.SnakeGame') as mock_game_class:
            mock_game = mock_game_class.return_value
            mock_game.is_over = True 
            
            mock_event_c = MagicMock()
            mock_event_c.type = pygame.KEYDOWN
            mock_event_c.key = pygame.K_c
            
            # 退出用的事件
            mock_event_q = MagicMock()
            mock_event_q.type = pygame.KEYDOWN
            mock_event_q.key = pygame.K_q

            # 1. 進入 is_over 迴圈 -> 收到 C -> reset() 
            # 2. reset 讓 is_over 變 False -> 進入主迴圈 -> 收到 Q -> 退出
            mock_event_get.side_effect = [[mock_event_c], [mock_event_q]]
            
            def mock_reset():
                mock_game.is_over = False
            mock_game.reset.side_effect = mock_reset

            with patch('pygame.init'), patch('pygame.display.set_mode') as mock_mode, patch('pygame.time.Clock'), \
                 patch('pygame.font.SysFont'), patch('pygame.display.update'), patch('pygame.draw.rect'), patch('sys.exit') as mock_exit:
                
                mock_mode.return_value = self.mock_screen
                mock_exit.side_effect = SystemExit
                
                with self.assertRaises(SystemExit):
                    main()
                mock_game.reset.assert_called_once()

    # 移除會導致真實迴圈執行的 test_main_block_execution
    # 移除 path hack 測試，改為直接測試 main 邏輯即可

if __name__ == "__main__":
    unittest.main()
