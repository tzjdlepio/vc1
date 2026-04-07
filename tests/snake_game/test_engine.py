import unittest
from asgards.snake_game.engine import SnakeGame
from asgards.snake_game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, DIR_RIGHT

class TestSnakeGame(unittest.TestCase):
    """
    測試 SnakeGame 引擎。
    """
    def setUp(self):
        self.game = SnakeGame()

    def test_initialization(self):
        """測試遊戲初始狀態。"""
        self.assertEqual(len(self.game.snake), 3)  # 初始長度應為 3
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.is_over)
        self.assertEqual(self.game.direction, DIR_RIGHT)

    def test_reset(self):
        """測試重置功能。"""
        self.game.score = 10
        self.game.is_over = True
        self.game.reset()
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.is_over)

    def test_move(self):
        """測試蛇的移動。"""
        initial_head = self.game.snake[0]
        self.game.move()
        new_head = self.game.snake[0]
        # 預設向右移動，x 應增加 GRID_SIZE
        self.assertEqual(new_head, (initial_head[0] + self.game.grid_size, initial_head[1]))
        # 身體長度應保持不變
        self.assertEqual(len(self.game.snake), 3)

    def test_change_direction(self):
        """測試改變方向。"""
        from asgards.snake_game.constants import DIR_UP, DIR_DOWN, DIR_LEFT
        # 測試有效轉向 (右 -> 上)
        self.game.change_direction(DIR_UP)
        self.assertEqual(self.game.direction, DIR_UP)
        
        # 測試禁止 180 度轉向 (上 -> 下)
        self.game.change_direction(DIR_DOWN)
        self.assertEqual(self.game.direction, DIR_UP)

    def test_eat_food(self):
        """測試蛇吃到食物。"""
        # 手動設置食物位置到蛇頭正前方
        head_x, head_y = self.game.snake[0]
        self.game.food = (head_x + self.game.grid_size, head_y)
        
        initial_length = len(self.game.snake)
        self.game.move()
        
        # 分數應增加
        self.assertEqual(self.game.score, 1)
        # 身體長度應增加
        self.assertEqual(len(self.game.snake), initial_length + 1)
        # 應生成新食物
        self.assertNotEqual(self.game.food, (head_x + self.game.grid_size, head_y))

    def test_food_generation(self):
        """測試食物生成。"""
        for _ in range(100):
            food = self.game._generate_food()
            # 食物不應在蛇身上
            self.assertNotIn(food, self.game.snake)

    def test_boundary_collision(self):
        """測試蛇撞到邊界。"""
        # 移動蛇直到超出右側邊界
        while not self.game.is_over:
            self.game.move()
        self.assertTrue(self.game.is_over)

    def test_self_collision(self):
        """測試蛇撞到自己。"""
        # 設定一個 U 型的蛇，讓蛇頭 (100, 100) 往右移動一格就會撞到身體 (120, 100)
        # 蛇身座標：[頭(100,100), (100,120), (120,120), (120,100), (100,100)...]
        self.game.snake = [
            (100, 100), 
            (100, 120), 
            (120, 120), 
            (120, 100), 
            (100, 100)
        ]
        from asgards.snake_game.constants import DIR_RIGHT
        self.game.direction = DIR_RIGHT
        self.game.move()
        self.assertTrue(self.game.is_over)

    def test_move_when_game_over(self):
        """測試遊戲結束時呼叫 move 應直接返回。"""
        self.game.is_over = True
        initial_snake = self.game.snake.copy()
        self.game.move()
        self.assertEqual(self.game.snake, initial_snake)

if __name__ == "__main__":
    unittest.main()
