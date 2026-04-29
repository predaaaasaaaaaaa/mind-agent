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

## Hardware Requirements

Since this runs advanced AI models locally, you need the following hardware:
- **RAM:** 8GB+ minimum memory
- **Swap Space:** 15GB+ swap memory to prevent crashes
- **Compute Time:** Because it runs on a CPU, a single 15-20 second video will take approximately **1 to 3 hours** to fully analyze.

## Detailed Setup Instructions (For Beginners!)

Don't worry if you aren't a programmer! Just follow these steps from A to Z to set up the core AI model and get your Telegram bot running.

### Step 1: Setting up the Meta TRIBE v2 Model & Environment
Because this bot runs heavy local AI models (instead of sending data to the cloud), you need to set up the engine first.

1. **Create a Virtual Environment:** 
   You need an isolated Python environment for all the heavy dependencies. Open your terminal in your home folder and run:
   ```bash
   python3 -m venv ~/tribe-env
   source ~/tribe-env/bin/activate
   ```
2. **Download the Model Cache:**
   You must acquire the Meta TRIBE v2 model cache and place it in your home directory at `~/tribev2-cache/`. This folder contains the pre-trained weights for:
   - **Whisper (small)** for audio transcription
   - **LLaMA 3.2-3B** for text generation and reasoning
   - **V-JEPA2** for visual feature extraction
   - **Wav2Vec-BERT** for audio features
3. **Configure the Model for CPU:**
   Inside `~/tribev2-cache/`, there is a `config.yaml` file. Because you are running this without a massive GPU, ensure the following settings are present in that file:
   - `device: cpu`
   - `llm_model: LLaMA 3.2-3B`
   *(Note: Do not modify these settings once they are working!)*

### Step 2: Install Project Requirements
Now that the environment is set up, make sure it is activated, navigate to your `mind-agent` project folder, and install the required tools:
```bash
source ~/tribe-env/bin/activate
pip install -r requirements.txt
```
*(You will need to run the `source` command every time you open a new terminal to work on this project!)*

### Step 3: Get Your Telegram Bot Token
To connect the code to Telegram, you need to create a bot on Telegram and get a secret "Token".
1. Open the Telegram app on your phone or computer.
2. Search for **@BotFather** (make sure it has a blue verified checkmark).
3. Send the message `/newbot` to BotFather.
4. It will ask for a name (e.g., "My Mind Agent") and a username that ends in "bot" (e.g., "mind_agent_test_bot").
5. BotFather will give you a message with your **Token** (it looks like a long string of random letters and numbers). Copy this entire token!

### Step 4: Connect the Token to the Code
We need to put that token into a hidden configuration file.
1. In your terminal, inside the `mind-agent` folder, make a copy of the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Open the newly created `.env` file using a text editor (like `nano` or your VS Code editor):
   ```bash
   nano .env
   ```
3. You will see a line that says `TELEGRAM_BOT_TOKEN=your_bot_token_here`. Replace `your_bot_token_here` with the token you copied from BotFather. It should look like this:
   `TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ`
4. Save the file and close it (in `nano`, press `Ctrl+O`, hit `Enter`, then press `Ctrl+X`).

---

## Usage

Now that you're set up, you can run the bot or test the system!

### 1. Run the Telegram Bot (The Main Feature!)
To start the bot, run this command in your terminal:
```bash
python src/telegram_bot.py
```
You should see a message saying `🤖 Mind Agent bot is running...`.
Now, go to your Telegram app, search for the bot you created, and press **Start**. 
- Send it a video (max 20 seconds) with no caption for a standard analysis.
- Send it a video **WITH** a caption (like "I want them to feel excitement") to get editing tips and a target goal breakdown!

### 2. Run a Fast Simulation (For Testing)
If you want to check if everything works without waiting 3 hours for the AI model to think, you can run a 5-second simulation using fake data:
```bash
python scripts/simulate_pipeline.py
```

### 3. Run Real Inference from the Command Line
If you want to run the real AI on a video without using Telegram, use this command:
```bash
python scripts/run_real_inference.py --video /path/to/your/video.mp4 --goal excitement
```

## Credits

Powered by Meta TRIBE v2.
