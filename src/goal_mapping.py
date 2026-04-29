GOAL_TO_REGIONS = {
    "excitement": ["amygdala", "ventral_striatum", "anterior_cingulate"],
    "memory": ["hippocampus", "entorhinal_cortex", "parahippocampal_gyrus"],
    "attention": ["dorsolateral_prefrontal_cortex", "intraparietal_sulcus"],
    "emotion": ["amygdala", "insula", "ventromedial_prefrontal_cortex"],
    "trust": ["ventromedial_prefrontal_cortex", "temporoparietal_junction"],
    "decision": ["orbitofrontal_cortex", "ventromedial_prefrontal_cortex"],
    "reward": ["nucleus_accumbens", "ventral_tegmental_area", "orbitofrontal_cortex"],
    "language": ["broca_area", "wernicke_area", "superior_temporal_gyrus"],
}

def map_goal_to_regions(goal: str) -> list[str]:
    """
    Map a user-provided goal string to target brain regions.
    Uses fuzzy matching against the predefined goals.
    """
    goal_lower = goal.lower()
    for known_goal, regions in GOAL_TO_REGIONS.items():
        if known_goal in goal_lower:
            return regions
    return []

def available_goals() -> list[str]:
    """
    Return the list of available goal categories.
    """
    return list(GOAL_TO_REGIONS.keys())

if __name__ == "__main__":
    print("Available goals:", available_goals())
    print("Mapping 'I want them to feel excited':", map_goal_to_regions("I want them to feel excited"))
    print("Mapping 'unknown goal':", map_goal_to_regions("unknown goal"))
