"""Manual review runner for Sprint 2 exit criteria (PLAN §2.6).

Prints transcript -> VideoBrief pairs for a human to eyeball:
  - is core_promise factually accurate?
  - does any key_entity NOT actually appear in the transcript?

Flags (does not hard-fail) any key_entity with no substring overlap with
the transcript, since legitimate paraphrases won't match verbatim but
should still be reviewed.

Run: python -m system.tests.manual_check_analyzer
"""

import asyncio

from system.agents import analyzer
from system.tests.fixtures import TEST_VIDEO_INPUTS


def _looks_unsupported(entity: str, transcript: str) -> bool:
    transcript_lower = transcript.lower()
    entity_lower = entity.lower()
    if entity_lower in transcript_lower:
        return False
    # loose check: any individual word of the entity appears in the transcript
    words = [w for w in entity_lower.split() if len(w) > 2]
    if words and any(w in transcript_lower for w in words):
        return False
    return True


async def main():
    for i, video_input in enumerate(TEST_VIDEO_INPUTS, start=1):
        brief = await analyzer.run(video_input)

        print(f"\n{'=' * 80}")
        print(f"[{i}/10] category={video_input.video_category}")
        print(f"TRANSCRIPT:\n{video_input.video_transcript}")
        print(f"\nCORE PROMISE: {brief.core_promise}")
        print(f"EMOTIONAL POTENTIAL: {brief.emotional_potential}")
        print(f"TRIGGER CANDIDATES: {brief.trigger_candidates}")
        print("KEY ENTITIES:")
        for entity in brief.key_entities:
            flag = " <-- REVIEW: not found in transcript" if _looks_unsupported(
                entity, video_input.video_transcript
            ) else ""
            print(f"  - {entity}{flag}")


if __name__ == "__main__":
    asyncio.run(main())
