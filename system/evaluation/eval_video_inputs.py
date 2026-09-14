"""20 diverse video inputs for Sprint 6 system-level evaluation (SOT §19.1;
PLAN §6.2). Reuses the 10 synthetic transcripts from Sprint 2/3's test
fixtures (system/tests/fixtures.py) and adds 10 more spanning the
categories the original 10 didn't cover, so all 15 categories in
category_map.py get at least one representative across the combined 20.
"""

from system.agents.schemas import VideoInput
from system.tests.fixtures import TEST_VIDEO_INPUTS

_NEW_VIDEO_INPUTS: list[VideoInput] = [
    VideoInput(
        video_transcript=(
            "This short film follows a paper airplane that gets caught in a storm "
            "drain and has to navigate its way back to the kid who folded it, "
            "using nothing but wind currents and a lot of luck. It's a five-minute "
            "animated short I made entirely alone over eight months, frame by "
            "frame, using free software. There's no dialogue, just music and "
            "sound design, because I wanted it to work in any language. The "
            "hardest part was animating water realistically with almost no "
            "budget for reference footage, so I filmed my own bathtub for two "
            "weeks to get the ripple physics right."
        ),
        video_description="An 8-month solo animated short about a paper airplane.",
        video_category="Film & Animation",
        channel_stats={"subscribers": 34_000, "avg_views": 12_000},
    ),
    VideoInput(
        video_transcript=(
            "I bought a salvage-title 2015 pickup truck for $4,200 at auction and "
            "spent the next three months rebuilding the engine after it threw a "
            "rod. Total parts cost came to $2,100, plus about 90 hours of my own "
            "labor. In this video I walk through the full teardown, what actually "
            "went wrong inside the block, and the exact torque specs I used on "
            "reassembly. By the end the truck passed inspection and now has "
            "142,000 miles on the original frame, running better than it did "
            "before the failure."
        ),
        video_description="Rebuilding a salvage-title truck engine from scratch.",
        video_category="Autos & Vehicles",
        channel_stats={"subscribers": 156_000, "avg_views": 41_000},
    ),
    VideoInput(
        video_transcript=(
            "This is the full breakdown of how I wrote and recorded a song in 24 "
            "hours for a songwriting challenge, starting from a single chord "
            "progression I had saved on my phone. I'll walk through the lyric "
            "writing process, why I scrapped the entire chorus at hour 14, and "
            "how I mixed the final track using only free plugins. The song ended "
            "up placing third out of 200 entries, and I'm breaking down exactly "
            "what the judges said worked and what they said was weak about the "
            "bridge section."
        ),
        video_description="Writing and recording a full song in 24 hours.",
        video_category="Music",
        channel_stats={"subscribers": 89_000, "avg_views": 27_000},
    ),
    VideoInput(
        video_transcript=(
            "My rescue dog Biscuit was terrified of other dogs for the first six "
            "months I had him, to the point where he'd shake and hide behind my "
            "legs on every walk. This video documents the exact desensitization "
            "process our trainer had us follow over 12 weeks, including the "
            "specific distance thresholds we used and why rushing the process "
            "backfired the one time we tried to speed it up. Today he can play "
            "off-leash with other dogs at the park, and I'm showing the actual "
            "footage from week 1 versus week 12 side by side."
        ),
        video_description="12-week journey helping a fearful rescue dog around other dogs.",
        video_category="Pets & Animals",
        channel_stats={"subscribers": 212_000, "avg_views": 68_000},
    ),
    VideoInput(
        video_transcript=(
            "I ran the numbers on every marathon I've finished in the last four "
            "years, all nine of them, and today I'm breaking down exactly why my "
            "time improved from 4 hours 12 minutes to 3 hours 21 minutes. It "
            "wasn't just training volume, it was three specific changes: fixing "
            "my carb intake during the race, switching to a run-walk strategy for "
            "the last 10K, and finally addressing a hip imbalance a physio caught "
            "in year two. I'll show the actual pace splits from each race so you "
            "can see where the time came from."
        ),
        video_description="Four years of marathon data and what actually improved my time.",
        video_category="Sports",
        channel_stats={"subscribers": 178_000, "avg_views": 52_000},
    ),
    VideoInput(
        video_transcript=(
            "I tried to write a stand-up set entirely out of complaints my mom "
            "has texted me over the past year, unedited, word for word, in the "
            "order she sent them. Some of these are genuinely unhinged, like the "
            "47-message thread about a parking spot that ends with her comparing "
            "herself to a Roman general. This is the full 8-minute set I "
            "performed at an open mic, plus the crowd reactions, plus the two "
            "jokes that completely bombed and why I think they didn't land."
        ),
        video_description="An 8-minute stand-up set built entirely from my mom's texts.",
        video_category="Comedy",
        channel_stats={"subscribers": 95_000, "avg_views": 31_000},
    ),
    VideoInput(
        video_transcript=(
            "We spent six months following three street performers in the same "
            "subway station to see how much they actually make in a single "
            "shift, and the numbers surprised all of us. The violinist averaged "
            "$38 an hour on weekday evenings, more than double what the "
            "guitarist made in the same spot on weekends. We also tracked how "
            "much a single viral moment can spike earnings, after one performer's "
            "clip got 2 million views and his next three shifts brought in triple "
            "his usual take."
        ),
        video_description="Six months tracking what subway street performers actually earn.",
        video_category="Entertainment",
        channel_stats={"subscribers": 410_000, "avg_views": 120_000},
    ),
    VideoInput(
        video_transcript=(
            "Our nonprofit spent the last year building a well in a village in "
            "rural Malawi that previously required a 3-hour round trip walk for "
            "clean water, mostly done by kids instead of going to school. This "
            "video documents the full process: the geological survey that found "
            "the water table, the community labor that dug the borehole, and the "
            "first day the pump was tested, including the reaction from the "
            "village elder who initially doubted the project would work. School "
            "attendance in the area rose 22% within two months of the well "
            "opening."
        ),
        video_description="Building a well that changed school attendance in a Malawian village.",
        video_category="Nonprofits & Activism",
        channel_stats={"subscribers": 63_000, "avg_views": 19_000},
    ),
    VideoInput(
        video_transcript=(
            "Why do some bridges sway visibly in high wind while others barely "
            "move at all, even when they're built from similar materials? The "
            "answer comes down to a concept called resonant frequency, and I'll "
            "walk through the famous 1940 Tacoma Narrows Bridge collapse as the "
            "clearest real-world example of what happens when a structure's "
            "natural frequency matches the frequency of the forces acting on it. "
            "Using a scale model and a fan, I'll actually recreate the same "
            "oscillation pattern that brought the real bridge down, at a much "
            "smaller and safer scale."
        ),
        video_description="Why some bridges sway in wind and others don't -- a resonance explainer.",
        video_category="Education",
        channel_stats={"subscribers": 890_000, "avg_views": 230_000},
    ),
    VideoInput(
        video_transcript=(
            "I played through the entire original Doom on the hardest difficulty "
            "using only a keyboard from 1993, no mouse, to see how much harder "
            "aiming actually was for players at launch. It took me 11 attempts "
            "to clear the first episode, compared to roughly 2 attempts with "
            "modern mouse-look controls. I'm breaking down exactly which fights "
            "become dramatically harder without free aiming, and why the game's "
            "original level design seems to account for keyboard-only movement "
            "in ways I hadn't noticed before."
        ),
        video_description="Beating the original Doom keyboard-only, the way players did in 1993.",
        video_category="Gaming",
        channel_stats={"subscribers": 267_000, "avg_views": 74_000},
    ),
]

EVAL_VIDEO_INPUTS: list[VideoInput] = list(TEST_VIDEO_INPUTS) + _NEW_VIDEO_INPUTS
