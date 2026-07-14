RESEARCH_DATASETS = {
    "atm_iv": {
        "enabled": True,
        "status": "production",
    },
    "smile_near": {
        "enabled": True,
        "status": "production",
    },
    "surface_near": {
        "enabled": True,
        "status": "production",
    },
    "term_structure": {
        "enabled": True,
        "status": "production",
    },
}


def list_research_datasets():
    return list(RESEARCH_DATASETS.keys())


def enabled_research_datasets():
    return [
        name
        for name, cfg in RESEARCH_DATASETS.items()
        if cfg["enabled"]
    ]


def get_research_dataset(name):
    if name not in RESEARCH_DATASETS:
        raise KeyError(name)
    return RESEARCH_DATASETS[name]