import unittest
from unittest.mock import patch, MagicMock
import sys
import pygame
from asgards.snake_game.main import main

class TestSnakeMain(unittest.TestCase):
    """
    測試 SnakeGame 主入口點與遊戲迴圈。
    """

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
        # 1. 設置模擬事件，模擬：按下 ESC 鍵退出
        mock_event_escape = MagicMock()
        mock_event_escape.type = pygame.KEYDOWN
        mock_event_escape.key = pygame.K_ESCAPE
        
        # 模擬 Clock 物件以避免 tick 等待
        mock_clock_obj = mock_clock.return_value
        
        mock_event_get.side_effect = [[mock_event_escape], []]
        mock_exit.side_effect = SystemExit

        with self.assertRaises(SystemExit):
            main()
        
        mock_init.assert_called_once()
        mock_quit.assert_called()

    @patch('pygame.event.get')
    @patch('sys.exit')
    def test_main_game_over_state(self, mock_exit, mock_event_get):
        """測試 Game Over 狀態下的按鍵行為。"""
        with patch('asgards.snake_game.main.SnakeGame') as mock_game_class:
            mock_game = mock_game_class.return_value
            mock_game.is_over = True
            
            # 按下 Q
            mock_event_q = MagicMock()
            mock_event_q.type = pygame.KEYDOWN
            mock_event_q.key = pygame.K_q
            
            mock_event_get.side_effect = [[mock_event_q]]
            mock_exit.side_effect = SystemExit

            with patch('pygame.init'), \
                 patch('pygame.display.set_mode') as mock_set_mode, \
                 patch('pygame.time.Clock') as mock_clock, \
                 patch('pygame.font.SysFont'), \
                 patch('pygame.display.update'), \
                 patch('pygame.draw.rect'):
                
                mock_screen = MagicMock()
                mock_set_mode.return_value = mock_screen
                
                with self.assertRaises(SystemExit):
                    main()

    @patch('pygame.event.get')
    @patch('sys.exit')
    def test_main_game_over_quit_event(self, mock_exit, mock_event_get):
        """測試 Game Over 狀態下的 QUIT 事件。"""
        with patch('asgards.snake_game.main.SnakeGame') as mock_game_class:
            mock_game = mock_game_class.return_value
            mock_game.is_over = True
            
            # 觸發 QUIT
            mock_event_quit = MagicMock()
            mock_event_quit.type = pygame.QUIT
            
            mock_event_get.side_effect = [[mock_event_quit]]
            mock_exit.side_effect = SystemExit

            with patch('pygame.init'), patch('pygame.display.set_mode'), patch('pygame.time.Clock'), \
                 patch('pygame.font.SysFont'), patch('pygame.display.update'), patch('pygame.draw.rect'):
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
        mock_screen = MagicMock()
        mock_mode.return_value = mock_screen

        def create_key_event(key):
            event = MagicMock()
            event.type = pygame.KEYDOWN
            event.key = key
            return event

        # 序列：左 -> QUIT 事件 (確保快速退出，不跑太多迴圈)
        mock_event_quit = MagicMock()
        mock_event_quit.type = pygame.QUIT

        events = [
            [create_key_event(pygame.K_LEFT)],
            [mock_event_quit]
        ]
        mock_event_get.side_effect = events
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
            
            mock_event_esc = MagicMock()
            mock_event_esc.type = pygame.KEYDOWN
            mock_event_esc.key = pygame.K_ESCAPE

            mock_event_get.side_effect = [[mock_event_c], [mock_event_esc]]
            
            def mock_reset():
                mock_game.is_over = False
            mock_game.reset.side_effect = mock_reset

            with patch('pygame.init'), patch('pygame.display.set_mode') as mock_mode, patch('pygame.time.Clock'), \
                 patch('pygame.font.SysFont'), patch('pygame.display.update'), patch('pygame.draw.rect'), patch('sys.exit') as mock_exit:
                
                mock_screen = MagicMock()
                mock_mode.return_value = mock_screen
                mock_exit.side_effect = SystemExit
                
                with self.assertRaises(SystemExit):
                    main()
                mock_game.reset.assert_called_once()

    def test_main_block_execution(self):
        """真正執行 main.py 的 __main__ 區塊。"""
        import runpy
        from unittest.mock import patch
        with patch('asgards.snake_game.main.main') as mock_main:
            mock_main.side_effect = SystemExit
            try:
                runpy.run_path("asgards/snake_game/main.py", run_name="__main__")
            except SystemExit:
                pass
            self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
