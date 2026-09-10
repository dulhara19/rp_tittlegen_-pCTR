"""Maps VideoInput.video_category (free text) to the numeric category_id
the pCTR model was trained on (YouTube Data API v3 category taxonomy,
US region — matches US_category_id.json from the Sprint 1 Kaggle sources).

Neither Kaggle dataset ships a category-name column at inference time, only
the numeric ID, so this mapping is maintained here as a static dict rather
than read from US_category_id.json (which isn't checked into the repo —
only the notebook's Colab session downloaded it). If US_category_id.json is
later added to system/data/raw/, this dict should be regenerated from it
directly instead of hand-maintained.
"""

# Standard YouTube Data API v3 "US" category taxonomy, restricted to the
# categories that actually appear in YouTube Trending data (the movie/show
# categories 30-44 essentially never trend and are omitted).
CATEGORY_NAME_TO_ID: dict[str, int] = {
    "Film & Animation": 1,
    "Autos & Vehicles": 2,
    "Music": 10,
    "Pets & Animals": 15,
    "Sports": 17,
    "Travel & Events": 19,
    "Gaming": 20,
    "People & Blogs": 22,
    "Comedy": 23,
    "Entertainment": 24,
    "News & Politics": 25,
    "Howto & Style": 26,
    "Education": 27,
    "Science & Technology": 28,
    "Nonprofits & Activism": 29,
}

# Fallback for a video_category that doesn't match any known name: the most
# common category in the Sprint 1 training data (Entertainment, category_id
# 24, is consistently the largest bucket in YouTube trending datasets).
DEFAULT_CATEGORY_ID = 24


def category_name_to_id(video_category: str) -> int:
    """Case-insensitive lookup with a documented fallback for unseen names."""
    normalized = video_category.strip().lower()
    for name, cid in CATEGORY_NAME_TO_ID.items():
        if name.lower() == normalized:
            return cid
    return DEFAULT_CATEGORY_ID
