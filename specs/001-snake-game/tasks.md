# Tasks: 經典貪吃蛇遊戲 (Classic Snake Game)

**Input**: Design documents from `specs/001-snake-game/`
**Prerequisites**: plan.md, spec.md, data-model.md

**Tests**: 包含針對 `engine.py` 的單元測試（遵從憲法自動化品質原則）。

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 專案初始化與基礎常數設定

- [x] T001 建立 `asgards/snake_game/` 與 `tests/snake_game/` 目錄結構
- [x] T002 建立 `asgards/snake_game/requirements.txt` 並加入 `pygame`
- [x] T003 [P] 建立 `asgards/snake_game/constants.py` 定義顏色、網格大小 (20px) 與速度
- [x] T004 建立 `asgards/snake_game/README.md` (從 quickstart.md 內容遷移)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 核心遊戲引擎基礎（不依賴 GUI）

- [x] T005 [P] 在 `asgards/snake_game/engine.py` 中建立 `SnakeGame` 類別基礎結構
- [x] T006 實作蛇的初始位置與方向邏輯於 `engine.py`
- [x] T007 建立 `tests/snake_game/test_engine.py` 並實作基礎初始化測試

---

## Phase 3: User Story 1 - 遊戲基礎控制 (Priority: P1)

**Goal**: 透過鍵盤控制蛇的移動方向

### Tests for User Story 1
- [x] T008 [P] [US1] 在 `test_engine.py` 中新增測試：驗證改變方向後蛇頭座標的正確性
- [x] T009 [P] [US1] 在 `test_engine.py` 中新增測試：驗證禁止 180 度直接回頭的邏輯

### Implementation for User Story 1
- [x] T010 [US1] 在 `engine.py` 中實作 `move()` 方法處理座標更新
- [x] T011 [US1] 在 `engine.py` 中實作 `change_direction(new_dir)` 並加入防回頭限制

---

## Phase 4: User Story 2 - 吃食物與成長計分 (Priority: P1)

**Goal**: 食物生成、碰撞偵測與長度/分數增加

### Tests for User Story 2
- [x] T012 [P] [US2] 在 `test_engine.py` 中新增測試：驗證蛇頭觸碰食物後 `score` 是否 +1
- [x] T013 [P] [US2] 在 `test_engine.py` 中新增測試：驗證食物生成座標是否避開蛇身

### Implementation for User Story 2
- [x] T014 [US2] 在 `engine.py` 中實作隨機食物生成邏輯
- [x] T015 [US2] 實作吃食物後的增長邏輯（不移除尾部座標）
- [x] T016 [US2] 更新 `score` 計分邏輯

---

## Phase 5: User Story 3 - 遊戲結束判定 (Priority: P1)

**Goal**: 偵測邊界碰撞與自身碰撞

### Tests for User Story 3
- [ ] T017 [P] [US3] 在 `test_engine.py` 中新增測試：驗證蛇頭超出邊界時 `is_over` 狀態
- [ ] T018 [P] [US3] 在 `test_engine.py` 中新增測試：驗證蛇頭撞到自己時 `is_over` 狀態

### Implementation for User Story 3
- [ ] T019 [US3] 在 `engine.py` 中實作邊界碰撞檢查邏輯
- [ ] T020 [US3] 在 `engine.py` 中實作自身碰撞檢查邏輯

---

## Phase 6: UI 渲染與整合 (Final Implementation)

**Purpose**: 使用 Pygame 實現視覺化並連結引擎

- [ ] T021 在 `asgards/snake_game/ui.py` 中實作 `SnakeUI` 類別，封裝 Pygame 繪圖方法
- [ ] T022 [US1, US2, US3] 在 `ui.py` 中實作繪製蛇、食物與分數的方法
- [ ] T023 在 `asgards/snake_game/main.py` 中整合 `SnakeGame` (Engine) 與 `SnakeUI`
- [ ] T024 實作 `main.py` 中的遊戲主循環 (FPS 控制、事件監控)

---

## Phase 7: Polish & Pipeline Validation

**Purpose**: 最終修飾與 CI 驗證

- [ ] T025 [P] 執行 `python -m unittest discover tests/snake_game` 確保全數通過
- [ ] T026 更新 `azure-pipelines.yml` 或確認 SonarQube 可掃描新目錄
- [ ] T027 移除代碼中任何剩餘的硬編碼常數，統一移至 `constants.py`

---

## Dependencies & Execution Order

1. **Setup (Phase 1)** 必須優先完成。
2. **Foundational (Phase 2)** 建立 `SnakeGame` 骨架後，Phase 3, 4, 5 的邏輯實作可以並行（若有足夠開發力），但建議依序實作：控制 -> 食物 -> 碰撞。
3. **UI (Phase 6)** 依賴於 Engine 邏輯的完整性。
4. **Validation (Phase 7)** 最後執行。

---

## Implementation Strategy

### MVP First (User Story 1 & 2)
1. 完成基礎移動與食物計分。
2. 即使沒有 GUI，透過單元測試確保邏輯正確。

### Incremental Delivery
1. 第一步：可以動的蛇 (US1)。
2. 第二步：可以變長的蛇 (US2)。
3. 第三步：會死掉的蛇 (US3)。
4. 第四步：漂亮的視覺介面 (Phase 6)。
