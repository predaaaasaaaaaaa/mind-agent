import numpy as np
from src.region_mapping import voxels_to_regions
from src.brain_viz import render_brain_heatmap
from src.report_builder import build_analysis_report
from src.goal_mapping import map_goal_to_regions
from src.goal_targeting import compute_gap, build_targeting_report
from src.config import OUTPUTS_DIR

def simulate():
    print("🚀 Starting Mind Agent Pipeline Simulation...")
    
    # 1. Fake inference
    print("\n[1/6] Generating fake inference data...")
    preds = np.random.randn(20, 20484)
    print(f"      Generated predictions of shape: {preds.shape}")
    
    # 2. Map voxels to regions
    print("\n[2/6] Mapping voxels to regions...")
    activations = voxels_to_regions(preds)
    print(f"      Mapped {len(activations)} regions.")
    
    # 3. Visualization
    print("\n[3/6] Rendering brain heatmap...")
    out_img = str(OUTPUTS_DIR / "sim_brain.png")
    # For simulation testing without downloading heavy nilearn datasets, 
    # we wrap it in try-except in case nilearn fails offline or takes too long.
    try:
        render_brain_heatmap(preds, out_img, title="Simulation Heatmap")
        print(f"      Saved heatmap to {out_img}")
    except Exception as e:
        print(f"      [Warning] Could not render heatmap (nilearn dataset missing?): {e}")
    
    # 4. Build Analysis Report
    print("\n[4/6] Building analysis report...")
    report = build_analysis_report(preds)
    print("\n--- ANALYSIS REPORT ---")
    print(report)
    print("-----------------------\n")
    
    # 5. Map Goal
    goal_str = "excitement"
    print(f"[5/6] Mapping goal: '{goal_str}'...")
    target_regions = map_goal_to_regions(goal_str)
    print(f"      Target regions mapped: {target_regions}")
    
    # 6. Compute Gap and Target Report
    print("\n[6/6] Computing goal gap analysis...")
    gap = compute_gap(preds, target_regions)
    targeting_report = build_targeting_report(gap, goal_str)
    print("\n--- TARGETING REPORT ---")
    print(targeting_report)
    print("------------------------\n")
    
    print("✅ Simulation complete")

if __name__ == "__main__":
    simulate()
