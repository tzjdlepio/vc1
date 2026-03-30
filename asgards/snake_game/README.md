# 經典貪吃蛇遊戲 (Snake Game)

這是一個基於 Python `pygame` 的單機版貪吃蛇遊戲。

## 目錄結構
- `asgards/snake_game/`: 核心原始碼
- `tests/snake_game/`: 針對遊戲引擎的單元測試

## 安裝步驟
1. 確保安裝 Python 3.9+。
2. 安裝依賴：
   ```bash
   pip install -r asgards/snake_game/requirements.txt
   ```

## 執行遊戲
```bash
python asgards/snake_game/main.py
```

## 執行測試
```bash
python -m unittest discover tests/snake_game
```

## 控制說明
- **方向鍵**: 控制蛇移動。
- **ESC**: 退出遊戲。

## 憲法規範落實
- **結構化資料夾**: 原始碼與測試完全分離。
- **自動化品質**: 提供針對核心邏輯的單元測試。
