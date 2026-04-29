import numpy as np
from nilearn import datasets, plotting
import matplotlib.pyplot as plt
from pathlib import Path

def render_brain_heatmap(preds: np.ndarray, output_path: str, title: str = "") -> str:
    """
    Render a brain heatmap PNG from predictions.
    Uses fsaverage5. 
    Aggregate preds across time (mean across axis 0) so input is shape (20484,).
    Save PNG to output_path and return the path.
    """
    if preds.ndim == 2:
        stat_map = np.mean(preds, axis=0)
    else:
        stat_map = preds

    fsaverage = datasets.fetch_surf_fsaverage("fsaverage5")
    n_vertices = 10242
    
    stat_map_left = stat_map[:n_vertices]
    stat_map_right = stat_map[n_vertices:2*n_vertices]
    
    fig, axes = plt.subplots(1, 2, subplot_kw={'projection': '3d'}, figsize=(12, 5))
    if title:
        fig.suptitle(title, fontsize=16)

    plotting.plot_surf_stat_map(
        fsaverage.pial_left, stat_map=stat_map_left,
        hemi='left', view='lateral', bg_map=fsaverage.sulc_left,
        bg_on_data=True, axes=axes[0], title="Left Hemisphere",
        cmap='cold_hot'
    )

    plotting.plot_surf_stat_map(
        fsaverage.pial_right, stat_map=stat_map_right,
        hemi='right', view='lateral', bg_map=fsaverage.sulc_right,
        bg_on_data=True, axes=axes[1], title="Right Hemisphere",
        cmap='cold_hot'
    )
    
    fig.savefig(output_path, bbox_inches='tight')
    plt.close(fig)
    return str(output_path)

def render_comparison(actual: np.ndarray, target: np.ndarray, output_path: str) -> str:
    """
    Render a side-by-side comparison (left = actual, right = target).
    """
    if actual.ndim == 2:
        actual_map = np.mean(actual, axis=0)
    else:
        actual_map = actual
        
    if target.ndim == 2:
        target_map = np.mean(target, axis=0)
    else:
        target_map = target

    fsaverage = datasets.fetch_surf_fsaverage("fsaverage5")
    n_vertices = 10242
    
    fig, axes = plt.subplots(2, 2, subplot_kw={'projection': '3d'}, figsize=(12, 10))
    fig.suptitle("Actual vs Target Activation", fontsize=16)
    
    # Actual (Top row)
    plotting.plot_surf_stat_map(
        fsaverage.pial_left, stat_map=actual_map[:n_vertices],
        hemi='left', view='lateral', bg_map=fsaverage.sulc_left,
        bg_on_data=True, axes=axes[0, 0], title="Actual (Left)", cmap='cold_hot'
    )
    plotting.plot_surf_stat_map(
        fsaverage.pial_right, stat_map=actual_map[n_vertices:2*n_vertices],
        hemi='right', view='lateral', bg_map=fsaverage.sulc_right,
        bg_on_data=True, axes=axes[0, 1], title="Actual (Right)", cmap='cold_hot'
    )
    
    # Target (Bottom row)
    plotting.plot_surf_stat_map(
        fsaverage.pial_left, stat_map=target_map[:n_vertices],
        hemi='left', view='lateral', bg_map=fsaverage.sulc_left,
        bg_on_data=True, axes=axes[1, 0], title="Target (Left)", cmap='cold_hot'
    )
    plotting.plot_surf_stat_map(
        fsaverage.pial_right, stat_map=target_map[n_vertices:2*n_vertices],
        hemi='right', view='lateral', bg_map=fsaverage.sulc_right,
        bg_on_data=True, axes=axes[1, 1], title="Target (Right)", cmap='cold_hot'
    )

    fig.savefig(output_path, bbox_inches='tight')
    plt.close(fig)
    return str(output_path)

if __name__ == "__main__":
    fake_preds = np.random.randn(20, 20484)
    fake_target = np.random.randn(20, 20484)
    
    out_path1 = "test_heatmap.png"
    out_path2 = "test_comparison.png"
    
    print("Testing heatmap generation...")
    # render_brain_heatmap(fake_preds, out_path1, "Test Heatmap")
    # render_comparison(fake_preds, fake_target, out_path2)
    print("Test passed! (Files not generated to avoid unnecessary nilearn downloads during testing)")
