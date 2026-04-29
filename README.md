# Mind Agent

Mind Agent is a Telegram bot and CLI tool that analyzes how human brains react to your videos using Meta's TRIBE v2 AI model. It maps video content to predicted brain activations, generates heatmaps, and provides actionable editing suggestions to hit specific emotional or cognitive goals (like "excitement" or "memory").

## Architecture

```text
+-------------------+      +-------------------+
|   Telegram Bot    | ---> |     Video (mp4)   |
+-------------------+      +-------------------+
          |                          |
          v                          v
+-------------------+      +-------------------+
| Goal Mapping      |      | BrainPredictor    |
| (user text -> ROI)|      | (Meta TRIBE v2)   |
+-------------------+      +-------------------+
          |                          |
          |                          v
          |                +-------------------+
          |                | Voxel Predictions |
          |                | (shape: T, 20484) |
          |                +-------------------+
          |                          |
          |            +-------------+-------------+
          |            |                           |
          v            v                           v
+-------------------+  +-------------------+  +-------------------+
|  Goal Targeting   |  |   Brain Viz       |  |  Report Builder   |
|  (Gap Analysis)   |  | (Heatmap renders) |  | (Interpretation)  |
+-------------------+  +-------------------+  +-------------------+
          |                    |                     |
          +--------------------+---------------------+
                               |
                               v
                     +-------------------+
                     | Final Output (Bot)|
                     +-------------------+
```

## Setup Instructions

Assuming you already have the working `tribe-env` virtual environment and the `tribev2-cache` downloaded:

1. **Activate the environment**:
   ```bash
   source ~/tribe-env/bin/activate
   ```
2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment variables**:
   Copy `.env.example` to `.env` and insert your Telegram Bot Token.
   ```bash
   cp .env.example .env
   # Edit .env with your token
   ```

## Hardware Requirements

- **RAM**: 8GB+ minimum
- **Swap**: 15GB+ minimum
- **Compute**: CPU execution takes ~1-3 hours per 20-second video.

## Usage

### 1. Run Simulation (Fast, Fake Data)
Verify the pipeline works end-to-end in seconds without heavy model loading:
```bash
python scripts/simulate_pipeline.py
```

### 2. Run Real Inference (CLI)
Run the heavy inference pipeline locally from your terminal:
```bash
python scripts/run_real_inference.py --video /path/to/video.mp4 --goal excitement
```

### 3. Run the Telegram Bot
Start the bot to handle incoming requests (runs in the background):
```bash
python src/telegram_bot.py
```

## Credits

Powered by **Meta TRIBE v2**. The core model inference uses their implementation for predicting fMRI activations from video/audio features.
