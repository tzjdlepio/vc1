import random
from asgards.snake_game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, DIR_RIGHT

class SnakeGame:
    """
    貪吃蛇遊戲引擎。
    負責遊戲邏輯（座標運算、碰撞偵測、計分），與渲染分離。
    """
    def __init__(self):
        self.grid_size = GRID_SIZE
        self.reset()

    def reset(self):
        """初始化或重置遊戲狀態。"""
        # 初始蛇身：index 0 為蛇頭
        start_x = WINDOW_WIDTH // 2
        start_y = WINDOW_HEIGHT // 2
        self.snake = [
            (start_x, start_y),
            (start_x - self.grid_size, start_y),
            (start_x - 2 * self.grid_size, start_y)
        ]
        self.direction = DIR_RIGHT
        self.score = 0
        self.is_over = False
        self.food = self._generate_food()
        self.grow_pending = False

    def _generate_food(self):
        """在隨機位置生成食物，並避開蛇身。"""
        while True:
            food_x = random.randrange(0, WINDOW_WIDTH, self.grid_size)
            food_y = random.randrange(0, WINDOW_HEIGHT, self.grid_size)
            if (food_x, food_y) not in self.snake:
                return (food_x, food_y)

    def move(self):
        """處理蛇的移動邏輯。"""
        if self.is_over:
            return

        # 計算新蛇頭位置
        curr_head = self.snake[0]
        new_head = (curr_head[0] + self.direction[0], curr_head[1] + self.direction[1])

        # 檢查邊界碰撞
        if (new_head[0] < 0 or new_head[0] >= WINDOW_WIDTH or
            new_head[1] < 0 or new_head[1] >= WINDOW_HEIGHT):
            self.is_over = True
            return

        # 檢查自身碰撞
        if new_head in self.snake:
            self.is_over = True
            return

        # 檢查是否吃到食物
        if new_head == self.food:
            self.score += 1
            self.grow_pending = True
            self.food = self._generate_food()

        # 加入新蛇頭
        self.snake.insert(0, new_head)

        # 處理增長或移動
        if self.grow_pending:
            self.grow_pending = False
        else:
            self.snake.pop()

    def change_direction(self, new_dir):
        """
        改變移動方向。
        禁止 180 度直接回頭（例如正在往左不能直接轉右）。
        """
        # 判斷是否為相反方向
        if (new_dir[0] + self.direction[0] == 0) and (new_dir[1] + self.direction[1] == 0):
            return
        self.direction = new_dir
