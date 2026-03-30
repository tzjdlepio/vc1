# Data Model: Snake Game

## Entities

### Snake
- `body`: List[Tuple[int, int]] - 蛇身座標列表，index 0 為蛇頭。
- `direction`: Tuple[int, int] - 當前移動向量 (dx, dy)。
- `grow_pending`: bool - 是否在下一幀增長。

### Food
- `position`: Tuple[int, int] - 當前食物座標。

### GameState
- `score`: int - 目前分數。
- `is_over`: bool - 遊戲是否結束。
- `grid_size`: int - 網格大小（像素）。

## 狀態轉換邏輯
1. **Move**: `new_head = (head.x + dx, head.y + dy)`。
2. **Check Collision**: 
   - 若 `new_head` 於邊界外 -> `is_over = True`。
   - 若 `new_head` 於 `body` 中 -> `is_over = True`。
3. **Eat**:
   - 若 `new_head == food.position` -> `score += 1`, `grow_pending = True`。
