#!/usr/bin/env python3
"""Generate Ogulcan blues jazz song with ACE-Step 1.5."""
import sys
sys.path.insert(0, "ACE-Step-1.5")

from acestep.inference import ACEStepInference

pipe = ACEStepInference(checkpoint_dir="ACE-Step-1.5/checkpoints")

result = pipe.generate_music(
    prompt="blues jazz, male vocals, soulful, groovy, electric guitar, saxophone, piano, warm bass, slow tempo, smoky bar",
    lyrics="""[verse]
Midnight streets are empty and cold
Ogulcan walks alone through the smoke
Everyone turns to watch him pass
His shadow hits harder than the bass

[verse]
Bartender pours a double straight
Women whisper table to table
Who is that man they always ask
Ogulcan they say the whole room shakes

[chorus]
Big dick Ogulcan came tonight
Blues pumping through his every stride
The whole damn bar gets on its feet
Big dick Ogulcan takes the beat

[verse]
Saxophone screams the solo breaks
Piano moans the drums explode
Ogulcan grabs the microphone
One look is all he needs to own

[chorus]
Big dick Ogulcan came tonight
Jazz flowing through his every breath
The walls are shaking left and right
Big dick Ogulcan owns the set

[outro]
Last call pours as dawn rolls in
Ogulcan tips his hat and grins
The crowd erupts behind his back
The legend never ends it just takes a break""",
    duration=180,
    language="en",
    output_dir="ACE-Step-1.5/output",
)
print("Done!", result)
