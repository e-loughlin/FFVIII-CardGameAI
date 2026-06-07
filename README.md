# Final Fantasy VIII Triple Triad AI & Web UI

A visual, high-performance tool for analyzing and winning Triple Triad matches from FFVIII. This tool features a modern Web UI for easy board setup, manual move recording, and an optimized Minimax AI with Alpha-Beta pruning.

## 🚀 Quick Start (with `uv`)

The easiest way to run the application is using [uv](https://github.com/astral-sh/uv).

1. **Start the server:**
   ```bash
   uv run app.py
   ```
2. **Access the UI:**
   Open your browser and navigate to: **`http://localhost:8080`**

---

## 🎨 Web UI Features

### **1. Visual Game Setup**
*   **Card Customization:** Define all 10 cards (5 Player, 5 Opponent) with their symbols and power values.
*   **Auto-Tab Entry:** Type power values (1-9 or A) and the cursor will automatically jump to the next field for rapid setup.
*   **Diamond Pattern:** Input fields are arranged in the authentic game pattern (Top, Left, Right, Bottom).
*   **Persistence:** Use **"Export to File"** to save your deck as a JSON file and **"Import from File"** to restore it later.

### **2. Gameplay & Mirroring**
*   **Manual Control:** Click any card in any hand and click an empty board cell to record a move. Use this to mirror what happens in your actual game.
*   **Undo/Redo:** Correct mistakes or explore different branches of play with the dedicated history buttons.
*   **Visual Feedback:** Cards pulse when recommended by AI, and captured cards instantly change color.

### **3. Optimized AI Engine**
*   **Alpha-Beta Pruning:** Drastically reduces computation time, allowing for deeper searches.
*   **Configurable Depth:** Adjust the **"Search Depth"** in the UI. 
    *   *Depth 4:* Instant results.
    *   *Depth 6:* Strategic play.
    *   *Depth 8+:* Grandmaster-level analysis.
*   **Move Evaluations:** Click **"Ask AI"** to see a ranked list of every possible move and its calculated score.

---

## ⚙️ Technical Details

*   **Backend:** Flask (Python)
*   **Frontend:** Vanilla JS / CSS / HTML5
*   **Package Management:** `uv` (recommended) or `pip`
*   **AI Algorithm:** Minimax with Alpha-Beta Pruning and custom State Cloning.

---

## 🛠 Manual Installation (without `uv`)

If you prefer not to use `uv`, you can install dependencies via `pip`:

```bash
pip install -r requirements.txt
python3 app.py
```

*Note: If port 8080 is occupied, you can change it in the last line of `app.py`.*