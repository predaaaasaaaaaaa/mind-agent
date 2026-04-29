import numpy as np
from src.region_mapping import voxels_to_regions

SUGGESTIONS = {
    "amygdala": "Add faster cuts, louder audio peaks, or high-contrast, unexpected visuals to increase emotional arousal.",
    "ventral_striatum": "Introduce clear rewards, gamification elements, or positive upbeat music.",
    "anterior_cingulate": "Create moments of conflict or cognitive dissonance (e.g., unexpected plot twists) to grab attention.",
    "hippocampus": "Use strong narrative structures, clear character arcs, and repetitive motifs for better memory encoding.",
    "entorhinal_cortex": "Provide clearer spatial contexts or establishing shots to ground the scene.",
    "parahippocampal_gyrus": "Include highly detailed, recognizable environments and rich contextual scenes.",
    "dorsolateral_prefrontal_cortex": "Present structured, logical information, facts, and problem-solving scenarios.",
    "intraparietal_sulcus": "Use visual pointers, highlight important numbers, and guide visual attention explicitly.",
    "insula": "Focus on relatable human experiences, pain points, or close-ups on facial expressions of emotion.",
    "ventromedial_prefrontal_cortex": "Emphasize personal relevance, core values, and trustworthy figures to build resonance.",
    "temporoparietal_junction": "Show complex social interactions, empathetic moments, and multiple perspectives.",
    "orbitofrontal_cortex": "Highlight tangible benefits, clear value propositions, and choices with positive outcomes.",
    "nucleus_accumbens": "Build anticipation leading up to a big reveal or satisfying resolution.",
    "ventral_tegmental_area": "Use highly salient and novel stimuli, such as vibrant colors and dynamic motion.",
    "broca_area": "Use clear, articulate voiceovers and engaging dialogue.",
    "wernicke_area": "Ensure speech is easy to understand, avoiding overly complex jargon or overlapping audio.",
    "superior_temporal_gyrus": "Improve audio quality, add compelling sound design, and use distinct linguistic cues."
}

def compute_gap(preds: np.ndarray, target_regions: list[str]) -> dict:
    """
    Compare actual activation against target regions.
    Returns {region: {"actual": float, "delta_from_max": float}}
    """
    activations = voxels_to_regions(preds)
    
    if not activations:
        return {}
        
    max_activation = max(activations.values())
    
    gap = {}
    for target in target_regions:
        # Match target region by substring
        actual_val = 0.0
        matched_key = None
        for key, val in activations.items():
            if target in key.lower() or key.lower() in target:
                if val > actual_val:
                    actual_val = val
                    matched_key = key
        
        delta = max_activation - actual_val
        gap[target] = {
            "actual": actual_val,
            "delta_from_max": delta,
            "matched_region": matched_key
        }
        
    return gap

def suggest_video_changes(gap: dict, goal: str) -> list[str]:
    """
    Provide hardcoded suggestions per region if there is a significant gap.
    """
    suggestions = []
    for region, data in gap.items():
        # Only suggest if delta is relatively large (> 0.5 for example, or just if it exists)
        # We'll provide it as a general suggestion for improvement if delta is positive
        if data["delta_from_max"] > 0.1: 
            if region in SUGGESTIONS:
                suggestions.append(f"To boost {region}: {SUGGESTIONS[region]}")
    return suggestions

def build_targeting_report(gap: dict, goal: str) -> str:
    """
    Format a report with gaps and suggestions.
    """
    report = []
    report.append(f"🎯 GOAL TARGETING ANALYSIS: {goal.upper()}")
    report.append("Target Regions Gap Analysis:\n")
    
    for region, data in gap.items():
        actual = data['actual']
        delta = data['delta_from_max']
        matched = data['matched_region'] or 'Not found'
        report.append(f"• {region} (mapped to {matched}):")
        report.append(f"  Actual Activation: {actual:.3f}")
        report.append(f"  Gap from Peak: {delta:.3f}\n")
        
    suggestions = suggest_video_changes(gap, goal)
    if suggestions:
        report.append("🎬 VIDEO EDITING SUGGESTIONS:")
        for sug in suggestions:
            report.append(f"- {sug}")
    else:
        report.append("🎬 VIDEO EDITING SUGGESTIONS: Activation is optimal, no major changes needed.")
        
    return "\n".join(report)

if __name__ == "__main__":
    fake_preds = np.random.randn(20, 20484)
    target_regions = ["amygdala", "ventral_striatum", "anterior_cingulate"] # Excitement
    gap = compute_gap(fake_preds, target_regions)
    print(build_targeting_report(gap, "excitement"))
