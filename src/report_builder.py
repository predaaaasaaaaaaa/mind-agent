import numpy as np
from src.region_mapping import voxels_to_regions, top_k_regions

INTERPRETATION_HINTS = {
    "amygdala": "High emotional arousal and potential fear or excitement responses detected.",
    "ventral_striatum": "Strong reward processing and positive anticipation engaged.",
    "anterior_cingulate": "Increased attention and conflict monitoring present.",
    "hippocampus": "Significant memory encoding and recall taking place.",
    "entorhinal_cortex": "Spatial memory and navigation processing activated.",
    "parahippocampal_gyrus": "Contextual scene recognition and memory retrieval observed.",
    "dorsolateral_prefrontal_cortex": "High working memory load and executive control engaged.",
    "intraparietal_sulcus": "Focused visual attention and numeric processing detected.",
    "insula": "Heightened interoceptive awareness and subjective feeling state.",
    "ventromedial_prefrontal_cortex": "Value-based decision making and personal relevance processed.",
    "temporoparietal_junction": "Social cognition and theory of mind processing activated.",
    "orbitofrontal_cortex": "Expected reward evaluation and decision making taking place.",
    "nucleus_accumbens": "Intense reward anticipation and pleasure responses observed.",
    "ventral_tegmental_area": "Dopaminergic reward pathways significantly engaged.",
    "broca_area": "Active language production and syntactic processing.",
    "wernicke_area": "Speech comprehension and semantic processing underway.",
    "superior_temporal_gyrus": "Auditory processing and language perception detected."
}

def build_analysis_report(preds: np.ndarray, top_k: int = 5) -> str:
    """
    Build a human-readable text report from raw voxel predictions.
    """
    n_seconds = preds.shape[0] if preds.ndim == 2 else 1
    total_voxels = preds.shape[1] if preds.ndim == 2 else preds.shape[0]
    
    activations = voxels_to_regions(preds)
    top_regions = top_k_regions(activations, k=top_k)
    
    report = []
    report.append("🧠 BRAIN ACTIVATION ANALYSIS")
    report.append(f"Duration: {n_seconds}s")
    report.append(f"Total voxels analyzed: {total_voxels:,}\n")
    
    report.append(f"Top {len(top_regions)} most activated regions:")
    for rank, (region, val) in enumerate(top_regions, 1):
        report.append(f"{rank}. {region} — activation: {val:.3f}")
        
    report.append("\n💡 Interpretation:")
    interpretations = []
    for region, _ in top_regions:
        # Match hint by substring since exact nilearn region names might be complex
        for key, hint in INTERPRETATION_HINTS.items():
            if key in region.lower() or region.lower() in key:
                if hint not in interpretations:
                    interpretations.append(hint)
                break
    
    if interpretations:
        report.append(" ".join(interpretations[:3])) # limit to 3 sentences
    else:
        report.append("General widespread cortical activation observed.")
        
    return "\n".join(report)

if __name__ == "__main__":
    fake_preds = np.random.randn(20, 20484)
    print(build_analysis_report(fake_preds, top_k=5))
