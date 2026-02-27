#!/usr/bin/env bash
# generate-tracks.sh - Generate 48 diverse MP3 tracks using ffmpeg synthesis
set -euo pipefail

OUTDIR="/Volumes/SRC-9/SRC Musical Intelligence/My Musical Mind (Monetizing)/public/music"
mkdir -p "$OUTDIR"

gen() {
  local num=$1 dur=$2 fc=$3
  local name
  name=$(printf "lib-%02d.mp3" "$num")
  echo "  Generating $name (${dur}s)..."
  ffmpeg -y -loglevel error -filter_complex "$fc" -map "[out]" -t "$dur" -ar 44100 -ac 2 -b:a 128k "$OUTDIR/$name"
}

echo "=== Generating 48 tracks ==="
echo ""

echo "[1/9] Classical / Neo-Classical / Cinematic (01-06)"
# Classical C major triad with tremolo and echo
gen 1 75 'sine=f=261.63:d=75[c1];sine=f=329.63:d=75[c2];sine=f=392:d=75[c3];sine=f=523.25:d=75[c4];[c1][c2]amix=inputs=2[m1];[c3][c4]amix=inputs=2[m2];[m1][m2]amix=inputs=2,tremolo=f=2:d=0.3,volume=0.4,aecho=0.8:0.7:60:0.3[mono];[mono]aformat=channel_layouts=stereo[out]'
# Neo-classical A harmonics with vibrato
gen 2 70 'sine=f=220:d=70[a1];sine=f=440:d=70[a2];sine=f=660:d=70[a3];sine=f=880:d=70[a4];[a1]volume=0.5[v1];[a2]volume=0.3[v2];[a3]volume=0.15[v3];[a4]volume=0.1[v4];[v1][v2][v3][v4]amix=inputs=4,vibrato=f=4:d=0.2,aecho=0.8:0.6:80:0.25[mono];[mono]aformat=channel_layouts=stereo[out]'
# Cinematic low E+B drone
gen 3 85 'sine=f=82.41:d=85[e1];sine=f=123.47:d=85[b1];sine=f=164.81:d=85[e2];[e1]volume=0.5[v1];[b1]volume=0.35[v2];[e2]volume=0.2[v3];[v1][v2][v3]amix=inputs=3,tremolo=f=0.5:d=0.5,aecho=0.8:0.8:120:0.4,aecho=0.6:0.5:200:0.2,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'
# D minor chord with chorus
gen 4 72 'sine=f=293.66:d=72[d1];sine=f=349.23:d=72[f1];sine=f=440:d=72[a1];sine=f=587.33:d=72[d2];[d1]volume=0.4[v1];[f1]volume=0.3[v2];[a1]volume=0.25[v3];[d2]volume=0.15[v4];[v1][v2][v3][v4]amix=inputs=4,chorus=0.5:0.9:50|60|40:0.4|0.32|0.3:0.25|0.4|0.3:2|2.3|1.3,volume=0.45[mono];[mono]aformat=channel_layouts=stereo[out]'
# Orchestral swell G major
gen 5 80 'sine=f=196:d=80[g1];sine=f=246.94:d=80[b1];sine=f=293.66:d=80[d1];sine=f=392:d=80[g2];[g1]volume=0.4[v1];[b1]volume=0.3[v2];[d1]volume=0.25[v3];[g2]volume=0.15[v4];[v1][v2][v3][v4]amix=inputs=4,vibrato=f=5:d=0.15,aecho=0.8:0.7:100:0.3,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'
# Cinematic tension tritone C+F#
gen 6 78 'sine=f=130.81:d=78[c1];sine=f=185:d=78[fs1];sine=f=261.63:d=78[c2];sine=f=370:d=78[fs2];[c1]volume=0.4[v1];[fs1]volume=0.35[v2];[c2]volume=0.2[v3];[fs2]volume=0.15[v4];[v1][v2][v3][v4]amix=inputs=4,tremolo=f=1.5:d=0.6,aecho=0.8:0.6:150:0.35,volume=0.4[mono];[mono]aformat=channel_layouts=stereo[out]'

echo "[2/9] Electronic / IDM / Synthwave / D&B / Trance (07-14)"
# Synthwave saw-like stacked harmonics
gen 7 65 'sine=f=110:d=65[s1];sine=f=220:d=65[s2];sine=f=330:d=65[s3];sine=f=440:d=65[s4];sine=f=550:d=65[s5];[s1]volume=0.35[v1];[s2]volume=0.3[v2];[s3]volume=0.2[v3];[s4]volume=0.15[v4];[s5]volume=0.1[v5];[v1][v2][v3][v4][v5]amix=inputs=5,chorus=0.6:0.9:25|35:0.4|0.3:0.3|0.4:2|3,flanger=delay=3:depth=3:speed=0.5,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'
# IDM detuned beating with flanger
gen 8 62 'sine=f=185:d=62[a1];sine=f=187.5:d=62[a2];sine=f=370:d=62[a3];sine=f=277.18:d=62[a4];[a1][a2]amix=inputs=2[beat];[a3]volume=0.3[v3];[a4]volume=0.25[v4];[beat][v3][v4]amix=inputs=3,tremolo=f=8:d=0.7,flanger=delay=2:depth=4:speed=2,volume=0.45[mono];[mono]aformat=channel_layouts=stereo[out]'
# D&B deep bass with hi-hat tremolo
gen 9 68 'sine=f=55:d=68[bass];sine=f=110:d=68[sub];sine=f=880:d=68[hi];[bass]volume=0.6[v1];[sub]volume=0.3[v2];[hi]volume=0.1,tremolo=f=14.5:d=0.9[v3];[v1][v2][v3]amix=inputs=3,flanger=delay=1:depth=2:speed=4,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'
# Trance E minor pad with chorus echo
gen 10 75 'sine=f=164.81:d=75[e1];sine=f=196:d=75[g1];sine=f=246.94:d=75[b1];sine=f=329.63:d=75[e2];[e1]volume=0.35[v1];[g1]volume=0.3[v2];[b1]volume=0.25[v3];[e2]volume=0.2[v4];[v1][v2][v3][v4]amix=inputs=4,chorus=0.7:0.9:20|30|45:0.5|0.4|0.3:0.3|0.5|0.4:2|3|1.5,aecho=0.8:0.5:60:0.35,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'
# Synthwave retro A minor vibrato
gen 11 70 'sine=f=220:d=70[a1];sine=f=261.63:d=70[c1];sine=f=329.63:d=70[e1];sine=f=440:d=70[a2];sine=f=660:d=70[a3];[a1]volume=0.4[v1];[c1]volume=0.3[v2];[e1]volume=0.25[v3];[a2]volume=0.15[v4];[a3]volume=0.08[v5];[v1][v2][v3][v4][v5]amix=inputs=5,vibrato=f=6:d=0.4,flanger=delay=5:depth=3:speed=0.3,volume=0.45[mono];[mono]aformat=channel_layouts=stereo[out]'
# Electronic pulse stacked fifths
gen 12 64 'sine=f=146.83:d=64[d1];sine=f=220:d=64[a1];sine=f=293.66:d=64[d2];sine=f=440:d=64[a2];[d1]volume=0.4[v1];[a1]volume=0.3[v2];[d2]volume=0.2[v3];[a2]volume=0.1[v4];[v1][v2][v3][v4]amix=inputs=4,tremolo=f=5.5:d=0.8,chorus=0.5:0.7:30:0.3:0.4:2,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'
# Acid squelch high harmonics
gen 13 60 'sine=f=311.13:d=60[e1];sine=f=622.25:d=60[e2];sine=f=933.38:d=60[e3];sine=f=1244.5:d=60[e4];sine=f=1555.6:d=60[e5];[e1]volume=0.3[v1];[e2]volume=0.25[v2];[e3]volume=0.2[v3];[e4]volume=0.15[v4];[e5]volume=0.1[v5];[v1][v2][v3][v4][v5]amix=inputs=5,vibrato=f=8:d=0.6,flanger=delay=1:depth=5:speed=3,tremolo=f=4:d=0.5,volume=0.4[mono];[mono]aformat=channel_layouts=stereo[out]'
# Techno minimal low drone hi tick
gen 14 66 'sine=f=73.42:d=66[bass];sine=f=146.83:d=66[mid];sine=f=1760:d=66[tick];[bass]volume=0.5[v1];[mid]volume=0.3[v2];[tick]volume=0.08,tremolo=f=11:d=0.95[v3];[v1][v2][v3]amix=inputs=3,flanger=delay=2:depth=2:speed=1.5,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'

echo "[3/9] Ambient / Post-Rock / Trip-Hop / Dark Ambient (15-20)"
# Pure ambient F major slow echo
gen 15 90 'sine=f=174.61:d=90[f1];sine=f=261.63:d=90[c1];sine=f=349.23:d=90[f2];[f1]volume=0.2[v1];[c1]volume=0.15[v2];[f2]volume=0.1[v3];[v1][v2][v3]amix=inputs=3,aecho=0.8:0.9:250:0.4,aecho=0.6:0.7:400:0.25,volume=0.4[mono];[mono]aformat=channel_layouts=stereo[out]'
# Dark ambient low drones pink noise
gen 16 88 'sine=f=41.2:d=88[low];sine=f=61.74:d=88[mid];anoisesrc=d=88:c=pink:a=0.02[noise];[low]volume=0.35[v1];[mid]volume=0.25[v2];[v1][v2][noise]amix=inputs=3,tremolo=f=0.3:d=0.4,aecho=0.8:0.8:300:0.35,volume=0.35[mono];[mono]aformat=channel_layouts=stereo[out]'
# Post-rock shimmer high chorus
gen 17 82 'sine=f=659.25:d=82[e1];sine=f=783.99:d=82[g1];sine=f=987.77:d=82[b1];[e1]volume=0.2[v1];[g1]volume=0.15[v2];[b1]volume=0.12[v3];[v1][v2][v3]amix=inputs=3,chorus=0.8:0.9:40|55|70:0.3|0.25|0.2:0.4|0.3|0.5:1|1.5|0.8,aecho=0.8:0.7:180:0.4,volume=0.35[mono];[mono]aformat=channel_layouts=stereo[out]'
# Trip-hop mellow bass airy
gen 18 76 'sine=f=98:d=76[bass];sine=f=196:d=76[mid];sine=f=784:d=76[hi];anoisesrc=d=76:c=pink:a=0.01[air];[bass]volume=0.35,tremolo=f=1.2:d=0.4[v1];[mid]volume=0.2[v2];[hi]volume=0.08,vibrato=f=3:d=0.3[v3];[v1][v2][v3][air]amix=inputs=4,aecho=0.7:0.6:120:0.3,volume=0.4[mono];[mono]aformat=channel_layouts=stereo[out]'
# Ambient drift slow cluster
gen 19 90 'sine=f=130.81:d=90[c1];sine=f=138.59:d=90[cs1];sine=f=155.56:d=90[eb1];[c1]volume=0.2[v1];[cs1]volume=0.15[v2];[eb1]volume=0.15[v3];[v1][v2][v3]amix=inputs=3,chorus=0.8:0.9:60|80:0.3|0.25:0.5|0.4:0.5|0.7,aecho=0.8:0.8:350:0.3,volume=0.35[mono];[mono]aformat=channel_layouts=stereo[out]'
# Dark ambient industrial noise sub
gen 20 85 'sine=f=36.71:d=85[sub];sine=f=73.42:d=85[bass];anoisesrc=d=85:c=brown:a=0.03[noise];sine=f=1480:d=85[metal];[sub]volume=0.3[v1];[bass]volume=0.2[v2];[metal]volume=0.04,flanger=delay=5:depth=5:speed=0.2[v3];[v1][v2][noise][v3]amix=inputs=4,tremolo=f=0.2:d=0.5,aecho=0.7:0.7:200:0.4,volume=0.3[mono];[mono]aformat=channel_layouts=stereo[out]'

echo "[4/9] Jazz / Fusion (21-24)"
# Jazz Cmaj7 vibrato chorus
gen 21 72 'sine=f=261.63:d=72[c1];sine=f=329.63:d=72[e1];sine=f=392:d=72[g1];sine=f=493.88:d=72[b1];sine=f=523.25:d=72[c2];[c1]volume=0.3[v1];[e1]volume=0.25[v2];[g1]volume=0.25[v3];[b1]volume=0.2[v4];[c2]volume=0.12[v5];[v1][v2][v3][v4][v5]amix=inputs=5,vibrato=f=5:d=0.2,chorus=0.4:0.5:30:0.3:0.3:2,volume=0.45[mono];[mono]aformat=channel_layouts=stereo[out]'
# Fusion Dm9 bright flanger
gen 22 68 'sine=f=146.83:d=68[d1];sine=f=174.61:d=68[f1];sine=f=220:d=68[a1];sine=f=261.63:d=68[c1];sine=f=329.63:d=68[e1];[d1]volume=0.35[v1];[f1]volume=0.25[v2];[a1]volume=0.2[v3];[c1]volume=0.2[v4];[e1]volume=0.15[v5];[v1][v2][v3][v4][v5]amix=inputs=5,vibrato=f=5.5:d=0.25,flanger=delay=4:depth=2:speed=0.4,volume=0.45[mono];[mono]aformat=channel_layouts=stereo[out]'
# Cool jazz Fmaj7#11 soft
gen 23 74 'sine=f=174.61:d=74[f1];sine=f=220:d=74[a1];sine=f=261.63:d=74[c1];sine=f=329.63:d=74[e1];sine=f=246.94:d=74[b1];[f1]volume=0.3[v1];[a1]volume=0.25[v2];[c1]volume=0.2[v3];[e1]volume=0.18[v4];[b1]volume=0.15[v5];[v1][v2][v3][v4][v5]amix=inputs=5,tremolo=f=2:d=0.15,chorus=0.5:0.6:45:0.3:0.3:1.8,aecho=0.6:0.4:80:0.2,volume=0.4[mono];[mono]aformat=channel_layouts=stereo[out]'
# Bebop stacked fourths fast vibrato
gen 24 64 'sine=f=293.66:d=64[d1];sine=f=392:d=64[g1];sine=f=523.25:d=64[c1];sine=f=698.46:d=64[f1];[d1]volume=0.3[v1];[g1]volume=0.28[v2];[c1]volume=0.22[v3];[f1]volume=0.15[v4];[v1][v2][v3][v4]amix=inputs=4,vibrato=f=7:d=0.3,tremolo=f=3.5:d=0.4,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'

echo "[5/9] Rock / Art Rock / Progressive Metal (25-30)"
# Hard rock E5 power chord harmonics
gen 25 65 'sine=f=82.41:d=65[e1];sine=f=164.81:d=65[e2];sine=f=246.94:d=65[b1];sine=f=329.63:d=65[e3];sine=f=493.88:d=65[b2];sine=f=659.25:d=65[e4];[e1]volume=0.4[v1];[e2]volume=0.35[v2];[b1]volume=0.3[v3];[e3]volume=0.2[v4];[b2]volume=0.15[v5];[e4]volume=0.1[v6];[v1][v2][v3][v4][v5][v6]amix=inputs=6,tremolo=f=6:d=0.7,volume=0.55[mono];[mono]aformat=channel_layouts=stereo[out]'
# Art rock dissonant cluster flanger
gen 26 70 'sine=f=233.08:d=70[bb1];sine=f=277.18:d=70[cs1];sine=f=369.99:d=70[fs1];sine=f=466.16:d=70[bb2];sine=f=554.37:d=70[cs2];[bb1]volume=0.35[v1];[cs1]volume=0.3[v2];[fs1]volume=0.25[v3];[bb2]volume=0.15[v4];[cs2]volume=0.1[v5];[v1][v2][v3][v4][v5]amix=inputs=5,flanger=delay=2:depth=4:speed=1.5,tremolo=f=4:d=0.6,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'
# Progressive metal complex harmonics
gen 27 68 'sine=f=55:d=68[low];sine=f=110:d=68[e1];sine=f=164.81:d=68[e2];sine=f=220:d=68[a1];sine=f=440:d=68[a2];sine=f=880:d=68[a3];[low]volume=0.5[v1];[e1]volume=0.35[v2];[e2]volume=0.3[v3];[a1]volume=0.2[v4];[a2]volume=0.1[v5];[a3]volume=0.05,tremolo=f=7:d=0.8[v6];[v1][v2][v3][v4][v5][v6]amix=inputs=6,tremolo=f=3.5:d=0.5,flanger=delay=1:depth=3:speed=2,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'
# Grunge wall midrange noise
gen 28 66 'sine=f=196:d=66[g1];sine=f=293.66:d=66[d1];sine=f=392:d=66[g2];anoisesrc=d=66:c=pink:a=0.04[noise];[g1]volume=0.4[v1];[d1]volume=0.35[v2];[g2]volume=0.25[v3];[v1][v2][v3][noise]amix=inputs=4,tremolo=f=5:d=0.65,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'
# Post-punk B minor fast tremolo
gen 29 63 'sine=f=123.47:d=63[b1];sine=f=146.83:d=63[d1];sine=f=185:d=63[fs1];sine=f=246.94:d=63[b2];sine=f=369.99:d=63[fs2];[b1]volume=0.4[v1];[d1]volume=0.3[v2];[fs1]volume=0.25[v3];[b2]volume=0.15[v4];[fs2]volume=0.1[v5];[v1][v2][v3][v4][v5]amix=inputs=5,tremolo=f=8:d=0.75,flanger=delay=1:depth=2:speed=3,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'
# Stoner rock detuned heavy low
gen 30 72 'sine=f=61.74:d=72[b0];sine=f=63:d=72[b0d];sine=f=123.47:d=72[b1];sine=f=185:d=72[fs1];[b0]volume=0.45[v1];[b0d]volume=0.4[v2];[b1]volume=0.3[v3];[fs1]volume=0.2[v4];[v1][v2][v3][v4]amix=inputs=4,tremolo=f=2.5:d=0.6,flanger=delay=4:depth=5:speed=0.3,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'

echo "[6/9] Hip-Hop / R&B / Neo-Soul / Funk (31-36)"
# Hip-hop boom bap deep bass rhythm
gen 31 70 'sine=f=55:d=70[bass];sine=f=110:d=70[sub];sine=f=440:d=70[hi];[bass]volume=0.5,tremolo=f=2.8:d=0.7[v1];[sub]volume=0.3[v2];[hi]volume=0.06,tremolo=f=5.6:d=0.9[v3];[v1][v2][v3]amix=inputs=3,aecho=0.6:0.4:60:0.25,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'
# R&B smooth Abmaj7 chorus
gen 32 72 'sine=f=207.65:d=72[ab1];sine=f=261.63:d=72[c1];sine=f=311.13:d=72[eb1];sine=f=392:d=72[g1];[ab1]volume=0.35[v1];[c1]volume=0.28[v2];[eb1]volume=0.22[v3];[g1]volume=0.18[v4];[v1][v2][v3][v4]amix=inputs=4,chorus=0.6:0.7:35|50:0.3|0.25:0.4|0.3:2|2.5,vibrato=f=4:d=0.15,volume=0.45[mono];[mono]aformat=channel_layouts=stereo[out]'
# Neo-soul Ebmaj9 warm deep
gen 33 76 'sine=f=155.56:d=76[eb1];sine=f=196:d=76[g1];sine=f=233.08:d=76[bb1];sine=f=293.66:d=76[d1];sine=f=349.23:d=76[f1];[eb1]volume=0.35[v1];[g1]volume=0.28[v2];[bb1]volume=0.22[v3];[d1]volume=0.18[v4];[f1]volume=0.12[v5];[v1][v2][v3][v4][v5]amix=inputs=5,tremolo=f=1.5:d=0.25,chorus=0.5:0.6:40:0.3:0.35:2,volume=0.4[mono];[mono]aformat=channel_layouts=stereo[out]'
# Funk E9 rhythmic staccato
gen 34 65 'sine=f=164.81:d=65[e1];sine=f=207.65:d=65[gs1];sine=f=246.94:d=65[b1];sine=f=293.66:d=65[d1];sine=f=185:d=65[fs1];[e1]volume=0.4[v1];[gs1]volume=0.25[v2];[b1]volume=0.2[v3];[d1]volume=0.18[v4];[fs1]volume=0.15[v5];[v1][v2][v3][v4][v5]amix=inputs=5,tremolo=f=6:d=0.8,flanger=delay=1:depth=1:speed=4,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'
# Lo-fi hip-hop vinyl crackle
gen 35 74 'sine=f=174.61:d=74[f1];sine=f=220:d=74[a1];sine=f=261.63:d=74[c1];anoisesrc=d=74:c=pink:a=0.015[vinyl];[f1]volume=0.3[v1];[a1]volume=0.22[v2];[c1]volume=0.18[v3];[v1][v2][v3][vinyl]amix=inputs=4,tremolo=f=1:d=0.2,aecho=0.5:0.4:100:0.2,volume=0.4[mono];[mono]aformat=channel_layouts=stereo[out]'
# Trap sub bass hi-hat tremolo
gen 36 66 'sine=f=36.71:d=66[sub];sine=f=73.42:d=66[bass];sine=f=7040:d=66[hat];[sub]volume=0.5[v1];[bass]volume=0.35[v2];[hat]volume=0.03,tremolo=f=12:d=0.95[v3];[v1][v2][v3]amix=inputs=3,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'

echo "[7/9] Indie Folk / Singer-Songwriter / Bossa Nova (37-40)"
# Indie folk G major gentle
gen 37 78 'sine=f=196:d=78[g1];sine=f=246.94:d=78[b1];sine=f=293.66:d=78[d1];sine=f=392:d=78[g2];[g1]volume=0.3[v1];[b1]volume=0.22[v2];[d1]volume=0.18[v3];[g2]volume=0.12[v4];[v1][v2][v3][v4]amix=inputs=4,chorus=0.3:0.4:25:0.2:0.3:2,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'
# Singer-songwriter C/G vibrato
gen 38 80 'sine=f=196:d=80[g1];sine=f=261.63:d=80[c1];sine=f=329.63:d=80[e1];sine=f=392:d=80[g2];sine=f=523.25:d=80[c2];[g1]volume=0.3[v1];[c1]volume=0.28[v2];[e1]volume=0.22[v3];[g2]volume=0.15[v4];[c2]volume=0.08[v5];[v1][v2][v3][v4][v5]amix=inputs=5,vibrato=f=4.5:d=0.15,aecho=0.5:0.3:70:0.2,volume=0.4[mono];[mono]aformat=channel_layouts=stereo[out]'
# Bossa nova Dm7b5 gentle rhythm
gen 39 76 'sine=f=146.83:d=76[d1];sine=f=174.61:d=76[f1];sine=f=207.65:d=76[ab1];sine=f=261.63:d=76[c1];[d1]volume=0.3[v1];[f1]volume=0.25[v2];[ab1]volume=0.22[v3];[c1]volume=0.18[v4];[v1][v2][v3][v4]amix=inputs=4,tremolo=f=3:d=0.2,vibrato=f=5:d=0.12,chorus=0.4:0.5:30:0.2:0.3:2,volume=0.42[mono];[mono]aformat=channel_layouts=stereo[out]'
# Acoustic waltz A major
gen 40 74 'sine=f=220:d=74[a1];sine=f=277.18:d=74[cs1];sine=f=329.63:d=74[e1];sine=f=440:d=74[a2];[a1]volume=0.32[v1];[cs1]volume=0.25[v2];[e1]volume=0.2[v3];[a2]volume=0.12[v4];[v1][v2][v3][v4]amix=inputs=4,tremolo=f=2:d=0.35,aecho=0.4:0.3:60:0.15,volume=0.45[mono];[mono]aformat=channel_layouts=stereo[out]'

echo "[8/9] Experimental / Noise / Drone / Glitch (41-44)"
# Noise white+pink modulated
gen 41 65 'anoisesrc=d=65:c=white:a=0.08[n1];anoisesrc=d=65:c=pink:a=0.06[n2];[n1]tremolo=f=3:d=0.7[v1];[n2]flanger=delay=3:depth=5:speed=1[v2];[v1][v2]amix=inputs=2,volume=0.35[mono];[mono]aformat=channel_layouts=stereo[out]'
# Drone microtonal cluster
gen 42 90 'sine=f=100:d=90[a1];sine=f=101.5:d=90[a2];sine=f=103:d=90[a3];sine=f=150:d=90[b1];sine=f=151.2:d=90[b2];[a1]volume=0.25[v1];[a2]volume=0.25[v2];[a3]volume=0.25[v3];[b1]volume=0.2[v4];[b2]volume=0.2[v5];[v1][v2][v3][v4][v5]amix=inputs=5,tremolo=f=0.15:d=0.3,aecho=0.8:0.8:400:0.3,volume=0.35[mono];[mono]aformat=channel_layouts=stereo[out]'
# Glitch rapid hi tremolo noise
gen 43 62 'sine=f=2000:d=62[hi1];sine=f=3150:d=62[hi2];anoisesrc=d=62:c=white:a=0.04[glitch];[hi1]volume=0.1,tremolo=f=15:d=0.95[v1];[hi2]volume=0.08,tremolo=f=11:d=0.9[v2];[glitch]tremolo=f=7:d=0.85[v3];[v1][v2][v3]amix=inputs=3,flanger=delay=0.5:depth=5:speed=5,volume=0.35[mono];[mono]aformat=channel_layouts=stereo[out]'
# Experimental atonal detuned noise
gen 44 70 'sine=f=137:d=70[a1];sine=f=211:d=70[a2];sine=f=347:d=70[a3];sine=f=509:d=70[a4];anoisesrc=d=70:c=brown:a=0.03[noise];[a1]volume=0.2,vibrato=f=9:d=0.5[v1];[a2]volume=0.18,tremolo=f=6:d=0.6[v2];[a3]volume=0.12,flanger=delay=2:depth=4:speed=2[v3];[a4]volume=0.08[v4];[v1][v2][v3][v4][noise]amix=inputs=5,aecho=0.6:0.5:150:0.3,volume=0.35[mono];[mono]aformat=channel_layouts=stereo[out]'

echo "[9/9] World / Afrobeat / Flamenco / Indian (45-48)"
# Afrobeat polyrhythmic pentatonic
gen 45 72 'sine=f=146.83:d=72[d1];sine=f=174.61:d=72[f1];sine=f=196:d=72[g1];sine=f=220:d=72[a1];sine=f=261.63:d=72[c1];[d1]volume=0.35,tremolo=f=4:d=0.6[v1];[f1]volume=0.25,tremolo=f=3:d=0.5[v2];[g1]volume=0.2,tremolo=f=5:d=0.5[v3];[a1]volume=0.15,tremolo=f=6:d=0.4[v4];[c1]volume=0.1,tremolo=f=4.5:d=0.5[v5];[v1][v2][v3][v4][v5]amix=inputs=5,flanger=delay=2:depth=2:speed=0.8,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'
# Flamenco Phrygian tremolo picking
gen 46 68 'sine=f=164.81:d=68[e1];sine=f=174.61:d=68[f1];sine=f=196:d=68[g1];sine=f=220:d=68[a1];sine=f=329.63:d=68[e2];[e1]volume=0.35[v1];[f1]volume=0.28[v2];[g1]volume=0.2[v3];[a1]volume=0.18[v4];[e2]volume=0.12,tremolo=f=10:d=0.6[v5];[v1][v2][v3][v4][v5]amix=inputs=5,vibrato=f=6:d=0.25,aecho=0.5:0.3:50:0.2,volume=0.5[mono];[mono]aformat=channel_layouts=stereo[out]'
# Indian raga Sa+Pa drone vibrato
gen 47 80 'sine=f=130.81:d=80[sa];sine=f=196:d=80[pa];sine=f=261.63:d=80[sa2];sine=f=293.66:d=80[re2];sine=f=392:d=80[pa2];[sa]volume=0.35[v1];[pa]volume=0.3[v2];[sa2]volume=0.15,vibrato=f=6:d=0.4[v3];[re2]volume=0.1,vibrato=f=7:d=0.5[v4];[pa2]volume=0.08[v5];[v1][v2][v3][v4][v5]amix=inputs=5,aecho=0.6:0.5:100:0.25,volume=0.42[mono];[mono]aformat=channel_layouts=stereo[out]'
# World percussion layered rhythmic
gen 48 70 'sine=f=98:d=70[low];sine=f=440:d=70[mid];sine=f=1760:d=70[hi];sine=f=880:d=70[mid2];anoisesrc=d=70:c=pink:a=0.02[perc];[low]volume=0.35,tremolo=f=3.5:d=0.7[v1];[mid]volume=0.12,tremolo=f=7:d=0.8[v2];[hi]volume=0.04,tremolo=f=5:d=0.9[v3];[mid2]volume=0.08,tremolo=f=4.5:d=0.6[v4];[perc]tremolo=f=6:d=0.7[v5];[v1][v2][v3][v4][v5]amix=inputs=5,flanger=delay=2:depth=3:speed=1.2,volume=0.45[mono];[mono]aformat=channel_layouts=stereo[out]'

echo ""
echo "=== Generation complete ==="
echo ""

# Verify all files
count=0
total_size=0
for i in $(seq 1 48); do
  name=$(printf "lib-%02d.mp3" "$i")
  path="$OUTDIR/$name"
  if [ -f "$path" ]; then
    size=$(stat -f%z "$path" 2>/dev/null || stat --format=%s "$path" 2>/dev/null)
    size_kb=$((size / 1024))
    count=$((count + 1))
    total_size=$((total_size + size))
    echo "  OK  $name  (${size_kb}KB)"
  else
    echo "  MISSING  $name"
  fi
done

total_mb=$((total_size / 1024 / 1024))
echo ""
echo "Generated: $count / 48 files"
echo "Total size: ~${total_mb}MB"
