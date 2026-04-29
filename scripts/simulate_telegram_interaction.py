import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import asyncio
import numpy as np
from unittest.mock import MagicMock, AsyncMock

# Mock BrainPredictor before importing telegram_bot because src.inference is empty
class FastFakePredictor:
    def predict(self, path):
        print(f"\n   [System: FakePredictor processing {path} (simulated 15s)...]")
        # Simulate a specific scenario: high visual activation but low emotion (amygdala) 
        # to trigger an interesting gap analysis.
        preds = np.random.randn(15, 20484) * 0.1
        # Add a strong peak somewhere else, say visual cortex, to create a gap
        preds[:, 1000] = 5.0 # Fake strong peak to force a delta > 0.1
        return preds

mock_inference = MagicMock()
mock_inference.BrainPredictor = FastFakePredictor
sys.modules['src.inference'] = mock_inference

import src.telegram_bot

async def run_simulation():
    print("="*60)
    print("📱 TELEGRAM BOT SIMULATION: WATCH COMMERCIAL")
    print("="*60)

    # Mock Update and Context
    update = MagicMock()
    context = MagicMock()
    
    # Define common mocks
    update.message.reply_text = AsyncMock()
    update.message.reply_photo = AsyncMock()
    context.bot.get_file = AsyncMock()
    mock_file = AsyncMock()
    context.bot.get_file.return_value = mock_file

    # 1. Test /start
    print("\n🧑 You: /start")
    await src.telegram_bot.start_command(update, context)
    print(f"🤖 Bot:\n{update.message.reply_text.call_args[0][0]}\n")

    # 2. Test sending a video with a goal
    print("-" * 60)
    print("🧑 You: [Uploaded a 15s video of a new luxury smartwatch commercial]")
    print("🧑 You (caption): I want the viewer to feel excitement and prestige.")
    
    update.message.video.duration = 15
    update.message.video.file_id = "mock_luxury_watch_video"
    update.message.caption = "I want the viewer to feel excitement and prestige."
    update.message.from_user.id = 77777
    
    # Reset call history
    update.message.reply_text.reset_mock()

    # Run the handle_video function
    await src.telegram_bot.handle_video(update, context)

    # Print the immediate wait message
    first_reply = update.message.reply_text.call_args_list[0][0][0]
    print(f"🤖 Bot: {first_reply}")

    # Print the final photo and report
    if update.message.reply_photo.called:
        photo_arg = update.message.reply_photo.call_args[1].get('photo')
        photo_name = photo_arg.name if hasattr(photo_arg, 'name') else "image_file"
        print(f"🤖 Bot: [Sent Image: {photo_name}]")

    if len(update.message.reply_text.call_args_list) > 1:
        final_report = update.message.reply_text.call_args_list[1][0][0]
        print(f"🤖 Bot Report:\n{final_report}")
        
    print("="*60)

if __name__ == "__main__":
    asyncio.run(run_simulation())
