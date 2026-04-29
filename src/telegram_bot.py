import os
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from src.inference import BrainPredictor
from src.goal_mapping import available_goals, map_goal_to_regions
from src.report_builder import build_analysis_report
from src.goal_targeting import compute_gap, build_targeting_report
from src.brain_viz import render_brain_heatmap
from src.config import OUTPUTS_DIR

# Setup logging to file
logging.basicConfig(
    filename=OUTPUTS_DIR / "errors.log",
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def run_pipeline(video_path: Path, goal: str = None) -> tuple[Path, str]:
    """
    Run the heavy inference pipeline synchronously.
    Returns a tuple of (image_path, report_text).
    """
    predictor = BrainPredictor()
    preds = predictor.predict(video_path)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = OUTPUTS_DIR / f"brain_{timestamp}.png"
    
    render_brain_heatmap(preds, image_path, title="Brain Activation Heatmap")
    
    if goal:
        target_regions = map_goal_to_regions(goal)
        if target_regions:
            gap = compute_gap(preds, target_regions)
            report = build_targeting_report(gap, goal)
        else:
            report = build_analysis_report(preds)
            report = f"⚠️ Goal '{goal}' not recognized or mapped. Defaulting to general analysis.\n\n" + report
    else:
        report = build_analysis_report(preds)
        
    return image_path, report

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🧠 Welcome to Mind Agent!\n\n"
        "I can analyze how human brains react to your videos using Meta's TRIBE v2 AI.\n\n"
        "**Mode A — Analyze:**\n"
        "Send me a video (up to 20s) without a caption. I'll reply with a brain activation heatmap and a breakdown of the most stimulated regions.\n\n"
        "**Mode B — Goal Targeting:**\n"
        "Send me a video WITH a caption stating your goal (e.g., 'excitement', 'memory'). I'll map the goal to target brain regions, compare actual activation, and give you editing suggestions!"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    goals = ", ".join(available_goals())
    help_text = (
        f"Available goals for Goal Targeting Mode:\n{goals}\n\n"
        "To use: send a video and add one of these goals as the caption."
    )
    await update.message.reply_text(help_text)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video
    if not video:
        return
        
    if video.duration > 20:
        await update.message.reply_text("❌ Maximum video length is 20 seconds. Please send a shorter video.")
        return
        
    goal = update.message.caption
    
    await update.message.reply_text("⏳ Analyzing — this takes 1-3 hours, I'll DM you when done.")
    
    user_id = update.message.from_user.id
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_path = OUTPUTS_DIR / f"incoming_{user_id}_{timestamp}.mp4"
    
    try:
        # Download video
        file = await context.bot.get_file(video.file_id)
        await file.download_to_drive(video_path)
        
        # Run heavy inference in a separate thread so bot stays responsive
        image_path, report = await asyncio.to_thread(run_pipeline, video_path, goal)
        
        # Send results
        with open(image_path, 'rb') as photo:
            await update.message.reply_photo(photo=photo)
        await update.message.reply_text(report)
        
    except Exception as e:
        logging.error(f"Error processing video for user {user_id}: {e}", exc_info=True)
        await update.message.reply_text("❌ An error occurred during analysis. The team has been notified.")

def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token or token == "your_bot_token_here":
        print("⚠️ Warning: TELEGRAM_BOT_TOKEN not found in .env or is default.")
        return

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))

    print("🤖 Mind Agent bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
