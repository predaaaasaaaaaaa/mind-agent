import argparse
import sys
from datetime import datetime
from pathlib import Path

from src.inference import BrainPredictor
from src.brain_viz import render_brain_heatmap
from src.report_builder import build_analysis_report
from src.goal_mapping import map_goal_to_regions
from src.goal_targeting import compute_gap, build_targeting_report
from src.config import OUTPUTS_DIR

def main():
    parser = argparse.ArgumentParser(description="Run real TRIBE v2 inference pipeline")
    parser.add_argument("--video", required=True, help="Path to input video file")
    parser.add_argument("--goal", help="Optional goal string (e.g., 'excitement')")
    args = parser.parse_args()

    video_path = Path(args.video)
    if not video_path.exists():
        print(f"❌ Error: Video file not found at {video_path}")
        sys.exit(1)

    print(f"🚀 Starting Real Inference on {video_path}")
    print("⏳ Loading model and running TRIBE v2 (this will take time on CPU)...")
    
    predictor = BrainPredictor()
    preds = predictor.predict(video_path)
    print(f"✅ Inference complete. Predictions shape: {preds.shape}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_img = OUTPUTS_DIR / f"real_brain_{timestamp}.png"
    out_report = OUTPUTS_DIR / f"real_report_{timestamp}.txt"
    
    print("\n🎨 Rendering heatmap...")
    render_brain_heatmap(preds, out_img, title="Real Brain Activation")
    print(f"   Saved to {out_img}")
    
    report_text = ""
    if args.goal:
        print(f"\n🎯 Target Goal: '{args.goal}'")
        target_regions = map_goal_to_regions(args.goal)
        if target_regions:
            gap = compute_gap(preds, target_regions)
            report_text = build_targeting_report(gap, args.goal)
        else:
            print(f"⚠️ Goal '{args.goal}' not recognized. Falling back to general analysis.")
            report_text = build_analysis_report(preds)
    else:
        print("\n📊 Generating general analysis report...")
        report_text = build_analysis_report(preds)
        
    with open(out_report, "w") as f:
        f.write(report_text)
        
    print(f"   Saved report to {out_report}")
    
    print("\n--- REPORT OUTPUT ---")
    print(report_text)
    print("---------------------\n")
    print("✅ Pipeline finished successfully.")

if __name__ == "__main__":
    main()
