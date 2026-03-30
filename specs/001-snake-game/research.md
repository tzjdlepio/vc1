# Research: 貪吃蛇遊戲實作與 CI 整合

## 決策 1: 遊戲庫選型 (pygame)
- **決定**: 使用 `pygame`。
- **理由**: 社群支援強大、API 簡單直觀，適合初學者且符合「簡單維護」原則。
- **備選**: `tkinter`（太過陽春）、`arcade`（依賴較新，穩定性稍遜）。

## 決策 2: CI 環境中的 GUI 測試
- **決定**: 將 `SnakeEngine` 與 `SnakeUI` 完全解耦。
- **理由**: Azure DevOps 的 Ubuntu Agent 預設無 X11 Server（無螢幕）。透過解耦，CI 僅需執行 `test_engine.py` 驗證座標運算，不需啟動 `pygame` 視窗即可完成 90% 的邏輯驗證。
- **實作方式**: `SnakeEngine` 維護一個二維陣列或座標列表，`SnakeUI` 僅負責讀取這些座標並繪圖。

## 決策 3: 隨機食物生成演算法
- **決定**: 使用 `random.randrange` 配合「排除蛇身座標」的檢查。
- **理由**: 簡單有效。若蛇身佔滿大部分空間，則使用可用空間列表隨機選取。
