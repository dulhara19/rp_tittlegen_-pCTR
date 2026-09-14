"""Shared test fixtures — 10 synthetic transcripts spanning content types.

Reused across Sprint 2 (Analyzer), Sprint 3 (Generator), and Sprint 5
(API integration tests), per the implementation plan.
"""

from system.agents.schemas import VideoInput

TEST_VIDEO_INPUTS: list[VideoInput] = [
    VideoInput(
        video_transcript=(
            "Today I'm reviewing the new Pixel 9 Pro after using it for three weeks "
            "as my only phone. The camera takes noticeably better low-light photos "
            "than my old Pixel 7, thanks to the larger sensor. Battery life got me "
            "through a full 14-hour day of heavy use, which is about 3 hours longer "
            "than the Pixel 7 managed. The one disappointment is the price: at $999 "
            "it's $100 more than last year's model for what feels like an incremental "
            "upgrade. If you already own a Pixel 7 or 8, I don't think this is worth "
            "the upgrade. If you're coming from something older, it's a solid choice."
        ),
        video_description="Three-week real-world review of the Pixel 9 Pro.",
        video_category="Science & Technology",
        channel_stats={"subscribers": 420_000, "avg_views": 85_000},
    ),
    VideoInput(
        video_transcript=(
            "In this video I'll show you how to make authentic Neapolitan pizza "
            "dough from scratch using just four ingredients: flour, water, salt, and "
            "yeast. The key is a 72-hour cold ferment in the fridge, which develops "
            "flavor without needing any sugar or oil. I'll walk through the exact "
            "hydration ratio I use, 65 percent, and show you how to shape the dough "
            "by hand without a rolling pin, which flattens the air bubbles you want "
            "to keep. By the end you'll have dough ready for a home oven at 500 "
            "degrees, which is the hottest most home ovens go."
        ),
        video_description="Step-by-step Neapolitan pizza dough tutorial.",
        video_category="Howto & Style",
        channel_stats={"subscribers": 1_200_000, "avg_views": 300_000},
    ),
    VideoInput(
        video_transcript=(
            "Two years ago I quit my $150,000 a year job as a software engineer at "
            "a company most of you would recognize, to try making a living from "
            "woodworking full time. For the first eight months I made almost "
            "nothing, and I nearly went back to my old job twice. What changed "
            "things was posting build videos online instead of just selling "
            "finished pieces locally. Today the shop brings in more than my old "
            "salary did, but it took a full eighteen months to get there, and I "
            "want to be honest about how close I came to quitting on this."
        ),
        video_description="My personal story of leaving tech for woodworking.",
        video_category="People & Blogs",
        channel_stats={"subscribers": 68_000, "avg_views": 22_000},
    ),
    VideoInput(
        video_transcript=(
            "Here are five underrated travel destinations in Southeast Asia that "
            "get a fraction of the tourists Bali or Bangkok see. First, Kampot in "
            "Cambodia, known for its pepper farms and riverside sunsets. Second, "
            "Hoi An's countryside outside the old town, reachable by bike in twenty "
            "minutes. Third, the Banaue rice terraces in the Philippines, over two "
            "thousand years old. Fourth, Kep, a quiet former French colonial beach "
            "town also in Cambodia. Fifth, Con Dao, a group of islands off Vietnam "
            "that used to be a prison colony and now has some of the clearest water "
            "I've seen anywhere in the region."
        ),
        video_description="Five lesser-known Southeast Asia travel spots.",
        video_category="Travel & Events",
        channel_stats={"subscribers": 310_000, "avg_views": 95_000},
    ),
    VideoInput(
        video_transcript=(
            "This week in tech news: a major cloud provider had a six-hour outage "
            "that took down several large apps, the EU proposed new rules requiring "
            "third-party app stores on mobile devices by next year, and a startup "
            "raised 40 million dollars for battery recycling technology that claims "
            "to recover 95 percent of lithium from used batteries, well above the "
            "industry average of around 50 percent. We'll also cover the antitrust "
            "ruling handed down against a major ad-tech company this week and what "
            "it could mean for how ads are sold online going forward."
        ),
        video_description="Weekly tech news recap.",
        video_category="News & Politics",
        channel_stats={"subscribers": 890_000, "avg_views": 210_000},
    ),
    VideoInput(
        video_transcript=(
            "Why does ice float on water when almost every other solid sinks in "
            "its own liquid? The answer is in how water molecules arrange "
            "themselves as they freeze. Unlike most substances, water molecules "
            "form an open hexagonal lattice when frozen, which is actually less "
            "dense than liquid water. That's why ice is about 9 percent less dense "
            "than liquid water, and why icebergs float with roughly one-tenth of "
            "their mass above the surface. If water behaved like most other "
            "liquids, lakes would freeze from the bottom up, which would have "
            "made most aquatic life on Earth impossible."
        ),
        video_description="A short explainer on why ice floats.",
        video_category="Education",
        channel_stats={"subscribers": 2_100_000, "avg_views": 540_000},
    ),
    VideoInput(
        video_transcript=(
            "I spent 100 hours trying to beat this game without taking a single "
            "point of damage, and today I'm finally showing you the run that "
            "worked. The hardest part wasn't the final boss, it was a jump section "
            "two hours into the run where one mistimed input meant restarting from "
            "scratch. I died 340 times total getting here. In this video I'll break "
            "down the exact strategy, frame-perfect tricks, and the route I used, "
            "including two skips most players don't know about."
        ),
        video_description="No-damage speedrun attempt and full breakdown.",
        video_category="Gaming",
        channel_stats={"subscribers": 540_000, "avg_views": 180_000},
    ),
    VideoInput(
        video_transcript=(
            "This is a 20-minute full-body workout you can do with zero equipment, "
            "built around five compound movements: squats, push-ups, lunges, "
            "plank rows using a towel, and mountain climbers. I'll do each move "
            "for 40 seconds with 20 seconds rest, four rounds total. This targets "
            "your legs, chest, back, and core in one session, which research "
            "suggests is roughly as effective for beginners as a split routine "
            "spread across multiple days, as long as you're consistent three times "
            "a week."
        ),
        video_description="No-equipment full-body home workout.",
        video_category="Howto & Style",
        channel_stats={"subscribers": 780_000, "avg_views": 160_000},
    ),
    VideoInput(
        video_transcript=(
            "I bought the three most popular robot vacuums under $300 and tested "
            "them side by side for a month in the same apartment. The Eufy X9 Pro "
            "picked up the most debris in our carpet test, collecting 94 grams "
            "compared to 71 grams for the Roborock Q5 and 58 grams for the "
            "Shark AI. However, the Roborock had the best mapping software and "
            "never got stuck, while both the Eufy and Shark got trapped under the "
            "same couch multiple times. For pet hair specifically, the Eufy pulled "
            "ahead again, clearing 89 percent versus 75 and 70 percent."
        ),
        video_description="Head-to-head robot vacuum comparison under $300.",
        video_category="Science & Technology",
        channel_stats={"subscribers": 205_000, "avg_views": 60_000},
    ),
    VideoInput(
        video_transcript=(
            "I paid off $42,000 in credit card debt in 19 months on a $55,000 "
            "salary, and I want to walk through exactly how, because most advice "
            "online assumes you can just earn more. I used the debt avalanche "
            "method, paying minimums on everything except the highest-interest "
            "card, which was at 24.99 percent. I also picked up a part-time "
            "weekend job for the first ten months that added about $600 a month. "
            "The biggest mistake I made early on was still using one card for "
            "emergencies, which added another $1,800 I hadn't planned for."
        ),
        video_description="How I paid off $42K in credit card debt.",
        video_category="People & Blogs",
        channel_stats={"subscribers": 145_000, "avg_views": 48_000},
    ),
]
