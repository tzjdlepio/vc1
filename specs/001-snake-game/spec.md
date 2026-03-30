# Feature Specification: 經典貪吃蛇遊戲 (Classic Snake Game)

**Feature Branch**: `001-snake-game`
**Created**: 2026-03-30
**Status**: Draft
**Input**: User description: "使用 Python 撰寫單機視窗版貪吃蛇，支援鍵盤控制，具備分數顯示與碰撞判定，程式存於 asgards/snake_game/"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 遊戲基礎控制 (Priority: P1)

使用者啟動遊戲後，可以透過鍵盤的「上、下、左、右」鍵來控制蛇的移動方向。蛇應朝指定方向持續移動，直到使用者按下另一個方向鍵。

**Why this priority**: 這是遊戲的核心互動機制，若無法控制方向，遊戲將無法進行。

**Independent Test**: 啟動遊戲後，按下「下」鍵，驗證蛇是否開始向下移動；接著按下「右」鍵，驗證蛇是否轉向右側。

**Acceptance Scenarios**:

1. **Given** 遊戲已啟動且蛇正在移動，**When** 使用者按下方向鍵，**Then** 蛇應立即改變移動方向。
2. **Given** 蛇正在向左移動，**When** 使用者按下「右」鍵（反方向），**Then** 蛇應維持向左移動（防止蛇直接 180 度回頭撞到自己）。

---

### User Story 2 - 吃食物與成長計分 (Priority: P1)

當蛇頭的座標與畫面上的食物座標重疊時，蛇身應增長一節，且畫面上顯示的分數應增加。食物隨後應在畫面上的隨機空位重新生成。

**Why this priority**: 這是遊戲的主要回饋與進度機制。

**Independent Test**: 模擬蛇頭移動到食物所在位置，驗證分數是否增加，且蛇身長度是否增加。

**Acceptance Scenarios**:

1. **Given** 蛇頭即將觸碰食物，**When** 蛇頭與食物座標重疊，**Then** 分數加一且蛇身長度增加一節。
2. **Given** 食物被吃掉，**When** 系統生成新食物，**Then** 新食物的座標不應與蛇身座標重疊。

---

### User Story 3 - 遊戲結束判定 (Priority: P1)

當蛇頭撞到視窗邊界或撞到蛇身自己的任何一部分時，遊戲應立即結束，並在畫面上顯示 "Game Over" 字樣。

**Why this priority**: 定義遊戲的失敗條件與循環結束。

**Independent Test**: 讓蛇頭移動超出視窗範圍，驗證遊戲是否停止並顯示結束訊息。

**Acceptance Scenarios**:

1. **Given** 蛇接近視窗邊緣，**When** 蛇頭座標超出邊界，**Then** 遊戲狀態轉為 GameOver。
2. **Given** 蛇身長度大於 4，**When** 蛇頭座標與蛇身座標重疊，**Then** 遊戲狀態轉為 GameOver。

---

### Edge Cases

- **視窗縮放**: 如果使用者縮放視窗，遊戲應維持原始比例或禁止縮放（建議禁止縮放以維持簡單性）。
- **極高分處理**: 當蛇身佔滿整個螢幕時，應判定為勝利或處理剩餘空間。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 系統必須使用 Python 撰寫，並採用 `pygame` 庫建立視窗介面。
- **FR-002**: 系統必須支援鍵盤方向鍵（上、下、左、右）即時控制。
- **FR-003**: 系統必須在畫面上隨機位置生成食物。
- **FR-004**: 系統必須在視窗角落即時顯示目前的得分。
- **FR-005**: 系統必須準確判定蛇頭與邊界、蛇頭與蛇身的碰撞。
- **FR-006**: 系統必須在遊戲結束時提供重新開始或退出的選項。

### Key Entities

- **Snake (蛇)**: 由一系列座標組成的列表，包含長度、移動方向與速度。
- **Food (食物)**: 畫面上的單一座標點，被吃掉後會改變位置。
- **GameBoard (遊戲棋盤)**: 定義遊戲空間的範圍與網格大小。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 使用者能以 100% 的成功率透過方向鍵改變蛇的方向。
- **SC-002**: 系統偵測到蛇頭觸碰食物後的響應時間應低於 16ms (確保流暢度)。
- **SC-003**: 當遊戲結束時，視窗必須在 0.5 秒內顯示 "Game Over"。
- **SC-004**: 系統在執行 1 小時後不應出現顯著的記憶體洩漏或效能下降。

## Assumptions

- 假設目標使用者的電腦已安裝 Python 3.x 環境。
- 假設遊戲視窗固定為 600x400 或類似的大小，不支援動態調整大小。
- 假設專案主要用於展示與基礎開發練習，不追求極致的畫面特效。
