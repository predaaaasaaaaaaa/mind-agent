import numpy as np
from nilearn import datasets

def load_atlas() -> dict:
    """
    Load the Destrieux surface atlas for fsaverage5.
    Returns a dictionary with 'map_left', 'map_right', and 'labels'.
    """
    return datasets.fetch_atlas_surf_destrieux()

def voxels_to_regions(preds: np.ndarray) -> dict[str, float]:
    """
    Map raw voxel predictions (shape: n_seconds, 20484) to named brain regions.
    Returns a dictionary mapping region name -> mean activation.
    """
    atlas = load_atlas()
    
    # fsaverage5 has 10242 vertices per hemisphere, total 20484
    # The left and right hemisphere maps
    map_left = atlas['map_left']
    map_right = atlas['map_right']
    labels = atlas['labels']
    
    # Concatenate the maps to match the 20484 voxels
    full_map = np.concatenate([map_left, map_right])
    
    # Aggregate predictions across time (mean across time axis)
    mean_preds = np.mean(preds, axis=0)
    
    region_activations = {}
    
    # Calculate mean activation per region
    for i, label_bytes in enumerate(labels):
        label = label_bytes.decode('utf-8') if isinstance(label_bytes, bytes) else str(label_bytes)
        
        # Region 0 is usually 'Unknown' or 'Medial Wall', we can skip it or keep it
        if i == 0 or "Unknown" in label:
            continue
            
        region_mask = (full_map == i)
        if np.any(region_mask):
            region_activations[label] = float(np.mean(mean_preds[region_mask]))
            
    return region_activations

def top_k_regions(region_activations: dict, k: int = 10) -> list[tuple[str, float]]:
    """
    Return the top k regions by activation.
    """
    sorted_regions = sorted(region_activations.items(), key=lambda item: item[1], reverse=True)
    return sorted_regions[:k]

if __name__ == "__main__":
    # Fake data: 20 seconds of 20484 voxels
    fake_preds = np.random.randn(20, 20484)
    print("Testing region mapping with fake data...")
    # Because nilearn might download the dataset here, we just call the function
    activations = voxels_to_regions(fake_preds)
    top_10 = top_k_regions(activations, k=10)
    
    print("\nTop 10 regions:")
    for rank, (region, val) in enumerate(top_10, 1):
        print(f"{rank}. {region}: {val:.3f}")
