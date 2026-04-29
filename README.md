# Mind Agent

Mind Agent is a Telegram bot that analyzes how human brains react to your videos using Meta's TRIBE v2 AI model. It maps user goals to target brain regions and provides gap analysis and actionable video-editing suggestions based on predicted fMRI activation.

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

(assumes user already has the venv + tribev2-cache)

1. Activate your virtual environment:
   ```bash
   source ~/tribe-env/bin/activate
   ```
2. Copy the environment template and configure your token:
   ```bash
   cp .env.example .env
   ```

## Hardware Requirements

- 8GB+ RAM
- 15GB+ swap
- ~3 hours per video on CPU

## Usage

**How to run simulation:**
```bash
python scripts/simulate_pipeline.py
```

**How to run real inference:**
```bash
python scripts/run_real_inference.py --video X.mp4 --goal Y
```

**How to run the Telegram bot:**
```bash
python src/telegram_bot.py
```

## Credits

Powered by Meta TRIBE v2.
