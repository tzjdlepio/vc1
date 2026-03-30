# Implementation Plan - 經典貪吃蛇遊戲 (Snake Game)

**Branch**: `001-snake-game` | **Date**: 2026-03-30 | **Spec**: [specs/001-snake-game/spec.md]

## Summary
實作一個基於 Python `pygame` 的單機版貪吃蛇遊戲。採用邏輯與顯示分離的架構，確保核心遊戲引擎（Engine）可在無圖形介面的 CI 環境中進行單元測試。

## Technical Context
**Language/Version**: Python 3.9+
**Primary Dependencies**: `pygame`
**Storage**: N/A (本地變數儲存分數)
**Testing**: `unittest` (針對 engine.py)
**Target Platform**: Windows/Linux/macOS (Desktop)
**Project Type**: GUI Application
**Constraints**: 必須能在 Azure DevOps Pipeline 執行基礎驗證。

## Constitution Check
- **I. 結構化目錄**: ✅ 將存於 `asgards/snake_game/`，測試存於 `tests/snake_game/`。
- **II. SDD**: ✅ 已完成 Spec，現在進行 Plan。
- **III. 自動化品質**: ✅ Pipeline 已配置 SonarQube 與單元測試。
- **IV. 安全機密**: ✅ 本專案不涉及 API Keys。
- **V. 易維護性**: ✅ 程式碼與 YAML 均附帶繁體中文註釋。

## Project Structure
```text
asgards/snake_game/
├── __init__.py
├── constants.py      # 顏色、速度、尺寸定義
├── engine.py         # 核心邏輯：蛇的移動、碰撞、食物生成
├── ui.py             # 繪圖邏輯：Pygame 渲染
├── main.py           # 遊戲進入點與循環
├── requirements.txt
└── README.md

tests/snake_game/
├── __init__.py
└── test_engine.py    # 針對 SnakeEngine 的單元測試
```

## Complexity Tracking
*無違反憲法之處。*
