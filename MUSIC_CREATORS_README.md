# MUSIC CREATORS README (WIP)

Refer to mfvitools docs at https://github.com/emberling/mfvitools/wiki for help with MML syntax.
This guide is a work in progress.
To do list:
* Explain jdm devtools and features
* Info on folder structure, uniqueness rules, using variants within jdm etc.
* Info on playlist files
* Info on creating dancing mad tiers
* Quickstart for adding music using sqspcmml
* Guide to using/obtaining custom samples for your MML

## JOHNNYDMAD STYLE GUIDE for sample selection (WIP)

THE HIGHEST PRIORITY IS SOUNDING GOOD. The second priority is sounding "right", meaning either the original mood, melodic line, and whatever accompaniment is feasible is preserved, or you as the arranger chose to change one or more of those things and the arrangement owns those changes; it should be obvious that any changes are not a mistake. The below sample selection guidelines should be followed only to the point that they don't endanger those first two priorities.

On sounding "right", though, a caveat: this stays within the context of late SNES RPG music. While we do want to do our best to preserve the *mood* of the source, be it from NES, PC MIDI, one of the various FM chips, or a live orchestra, or even from a SNES game with significantly more memory limitations or very different aesthetic requirements. We don't want a reproduction; we want the "Fight Against Culex" version, something that incorporates both the style of the original and the mood and sensibility of the surrounding game. NES tracks should be orchestral, for example, instead of or in addition to mimicking the NES sound capabilities using our own triangle and pulse wave samples. Natively orchestral tracks may have to add bass or rethink percussion in order to preserve a sense of impact, rhythm, or bombast that SPC700 isn't really capable of imitating in original form. And SNES original tracks with lower quality, heavily artifacted or FM-derived samples -- piano being the most common offender -- should aim for using the higher quality, more naturalistic equivalents, not imitating the originals.

### PIANOS:
* The standard multisampled piano is:
  * `C7+   06 LQPiano8 (sounds +3oct)`
  * `C6-B6 01 GrandPiano6 (sounds +1oct)`
  * `C5-B5 02 GrandPiano5`
  * `C4-B4 03 GrandPiano4`
  * `  -B3 11 BrightPiano3`
* However, different tracks have different needs, and this is very demanding on memory. Feel free to use any combination that works and produces a generally natural piano sound; avoid using samples significantly above or below their ideal octave. The overly bright, artificial piano timbre found in many, particularly early, SNES games - think FF4 or Breath of Fire - should not be duplicated unless it's integral to the nature of the song (e.g. Lufia 2's casino theme) or unless a natural version proves unfeasible.
* For bass piano parts (single held notes that fill the low end and stay around O3 or below), 08 (Chrono Trigger) is preferred. 05 is provided as an alternative that meshes better with the 01-02-03 piano, as they have the same source (SD3), though 05 doesn't slide cleanly into 03. 04, though a different source entirely, can *sort of* smooth over this transition if needed.
* Most SNES piano parts that aren't that awful bright crap are recorded in the O6-O7 range and 01/09 is a good fit for them. 09 is a lower sample rate version of 01 (taken from Front Mission). The quality difference is mostly unimportant for a single sample, but the transition from 02 to 09 is too rough to recommend using it multisampled. (It's already unfortunate with 02 to 01; you can hear it in some SD3 tracks such as Fable.)
* If you MUST with the bright crap, 05 to its max at A5 then 04 above that seems relatively seamless and has a more natural timbre than 04 alone.
* Be aware of 13 (CT 12-string guitar that sounds like honky-tonk) and C5 (piano pad), which could fill some piano parts.
* Note that 06 sounds significantly better ingame (with echo) than in SF2 audition.
### OTHER ZITHERS/E.PIANOS:
* Not much to note; use what fits and aggressively replace not-quite-harpsichord originals with harpsichord if it sounds better that way. 13 can sub as a honky-tonk-type piano, as it does extensively in CT.
* No "clean" electric piano is provided because @3 exists, as well as D0 (sine) and D1 (triangle).
* 52 is not any instrument in particular but can sub in for many of this style of timbre; it's basically midway between electric piano and clavinet, though the ADSR may need some tweaking for this use case. (The origin of this sample is a tone similar to @3 with a serendipitous typo in its loop point; it's technically closer to e.piano than bass.)
* A budget rhodes-type piano may be included in the future but I'm not currently happy with the options I have in that area.
### CHROMATIC PERC.:
* Use 20 for music box parts; octaved with the lower octave delayed by 2 ticks seems effective, if possible.
* It can be hard to tell what is what but try your best to match instrument types rather than just using whatever. Marimba/xylophone should be considered one type (it's all marimba, really) and 23/24 (labelled marimba) should be preferred if feasible.
* 28 is the preferred tubular bell.
### ACOUSTIC GUITARS:
* 34 (steel guitar) is the preferred acoustic guitar; even if it's not a match for the original, give it a shot. After that, try 36, then fall back to 35. 
* 33 rarely fits anything but when it does fit it's great - and it can play a wide variety of roles - so just keep it in mind in general. Not necessarily as a guitar.
* 35 plays a good stand-in for a bass guitar in busier soundscapes that drown out its high partials; it can be useful if the standard electric bass is a bit too emphatic.
### ELECTRIC GUITARS:
* A bit of an anything goes area; there's too much variation to make hard rules. If the original sample is a power chord (5th), even faintly, and there's no spare channel, use 44 unless it sucks. Favor the palm-mute combo (48-49) and the S50 guitar variants (41-44) in the rare circumstances that they're actually appropriate, but understand that those *are* rare; this isn't RotDS, and that sound makes a janky lead. If circumstances permit, aggressively split guitar parts into multiple timbres, particularly lead (39/40/maybe 43/etc), harmonic parts (46/47/43), and the crunchy almost-percussive low end (42/41/45/48-49), either by using different samples at different times or by using different samples in different channels at the same time.
* Note that as good as 39 is, 40 holds up better in lower octaves.
* E0, E1, and E2 may also be of use in unusual situations, industrial tinged, skirting the line between guitar and sound effect. Note that E0 sounds much more atonal ingame than SF2, more just the suggestion of tone over noise, but it could fit a super-distorted industrial riff sort of role.
### BASS:
* 50 is the only provided acoustic bass, but in the event it fails, 52, 35, and 57 might work as stand-ins.
* 51 is the canonical electric bass. It should be used for any standard picked/fingered bass parts unless the situation strongly calls for something else.
* If a more fingered and less picked sound is required, 52 and 35 are available, though they each have cases in which they fail hard: 52 when the bass part dips into higher notes, and 35 if the instrumentation is fairly sparse and fails to drown out its upper overtones.
* 54 should be considered the canonical synth bass over 55.
* 55 is a broadly useful sound for various purposes, thickening and layering, as well as certain synth 'blip' sounds, but should be AVOIDED when possible for standard bass guitar / synth bass parts. Try to keep use of this sample to subtler and not immediately recognizable uses.
* Note C6 as a synth-bass-like filter sweep synth, and D1 Triangle Wave as a NES-style bass. C1 also can serve as a particularly spicy synth bass if you've got enough going on above it.
### PIZZICATO:
* 58 (octave pizzicato) is another one of those "use this whenever possible, even when inaccurate to the original, but ONLY if it sounds good, which it usually won't" samples. Beyond that, use what works. 57 and 59 both work for most purposes, so pick whichever fits the desired character and the memory limitations.
### HARP:
* 60 (FF6) is the canonical harp.
* 61 is discouraged in most situations; the exception is when it is a close or exact match to the game's original sound. If the original sound matches 61, then ignore the discouragement and treat 60 and 61 as equal priority, going with what sounds best. I've identified FF4, Lufia 2, RS2, Terranigma, and Rudra no Hihou as using this harp or a very close equivalent, and though the sample differs, I consider Chrono Trigger a close enough sound to consider using this as well.
### STRING ENSEMBLES:
* I've identified a few varied considerations with string samples. 65 should be the rough "default" with 66 and 67 as memory-saving fallbacks, but there are other concerns to watch.
* First is that, to my ear, SNES string samples can be roughly divided into smooth, airy sounds that remind me of fluffy clouds or mist, and rough textured sounds that feel like polished wood grain. On higher notes, the textured style can sound overly noisy, and the smooth style tends to sound indistinct and muddy in medium to low ranges. Chrono Trigger, especially, has only the smooth style of strings, and often high notes will sound weird and breathy with 65. 62 is provided as an attempt to fill this role.
* Second is the baked-in attack time of the samples. Many SNES string samples start directly in the main loop and don't contain the sound of the initial contact between string and bow. Chrono Trigger and Lufia 2 are examples of games with instant-on samples. Usually, these will use the SPC700 attack instead and it becomes moot, but in some cases, especially very short notes, low notes, and especially especially short low notes, you need to reproduce that instant attack. 66 and 67 are instant attack samples, though both have a short attack time applied through ADSR that you may want to adjust to match the target.
* 64 also works very well for those short low notes; if you have the space, it's preferable to use this alongside 65 or 66, taking over the lowest string part (as vanilla FF6 did extensively).
* 63 is for combining two parts separated by one octave, and should swap relatively seamlessly with 65/66/67 when those parts diverge. 67 may need a volume change, as it runs a bit louder than the others.
* C4 is a synth string pad that should primarily be used to represent parts that are clearly intended for synth string pads -- e.g. the lead on Mako Reactor -- but can work as a fallback for normal strings if none of the other options are working out. Like 64, it has a pretty snappy low end, though it isn't instant-on.
* C5 is piano+synth strings and could be conceivably used as another string option with ADSR cropping out the piano hit.
* C3 can also be treated as an alternative fallback to the airy type of strings, though it's inescapably synthetic.
### SOLO STRINGS:
* Mostly a use-whatever-works-best area. 72 can be considered the default but it's a very soft default.
* Generally, in my experience, mid/lower octave solo string parts, like cellos, can be very hard to get to sound "right" and most samples will just sound wrong. Rather than trying to include a large enough variety of samples to fit every situation, it should just be expected that in some cases you will have to load an external sample for this.
* Oboe, bassoon, bagpipe, harmonica type sounds may also serve as replacements either if you're desperate or if the original is a synthetic or ambiguous sound.
### VOX/CHOIR:
* 75 is the default or canonical choir sound.
* Use 73 and 74 to match original source timbres or to aim for a more "realistic" sound, particularly if two or three of these are used for separate parts. Do not use these if the original part is more of a standard SNES or synthesized choir sound.
* Use 78 to match original source (at even priority to 75, not higher), or if a more synthetic sound than 75 is needed, or if a fuller sound at low octaves is needed and 73/74 aren't appropriate, or as a single-octave match to 79 if you need to octave-merge choir parts.
* 77 can also be used (with ADSR) for vox pad type sounds, or (ADSR optional) for many of the synth accent timbres with names like "Halo", "Goblins", "Brightness" and so forth.
* 76 is an odd one that should be avoided for any standard chorus/vox sound. Only use it if you strongly need the "oooh" rather than "ahh" sound, or if the original is also this style of janky '90s General MIDI "Voice Doohs" patch, or (most likely) use it not as a voice sound but as a synthetic alternative pan flute, either above ~ octave 5, or with an attack, so that the 'doo" sound is indistinct.
* B7 is an organ/vox hybrid that may be partially or completely based on the same original sound as 74 (either combined with a rock organ type sample or just cleverly edited). With attack it serves as a LQ version of 74.
### BRASS:
* 81 is the canonical trumpet. Two issues to watch out for: first, it has a relatively slow attack, so if you're using short staccato notes at all, go ahead and lower the sustain level and raise the volume accordingly. %s5 and 1.33x volume usually works well. (Decay defaults to 0 to facilitate this.) Second, it can sometimes induce some weird artifacting at higher notes, especially with vibrato; feel free to replace it if this gets too bad.
* You are also encouraged to consider replacing original "trumpet" parts with the weightier 83 or more enthusiastic and extra 87 if it feels appropriate to the song.
* Use 82 as a single-octave match of 80, or as a versatile second brass timbre if you're already using 81, or to save space, or if 81 proves too problematic.
* 84 is the canonical horn; afterward, there is a clear priority: 84 > 85 > 86 > 7F. Both 84 and 85 are intended to be signature sounds of this sample set. Horn parts vary a lot in character and how well they need to either blend with or distinguish themselves from the surrounding sounds; expect to use this sample frequently, but also reject it frequently. This is the FF7 horn sound and significantly more of a foreground sort of sound than most horn patches. Note that, like 81, this has a slower attack. The default ADSR already starts at %s5 and you may need to bring that even lower, e.g. %s3 / 1.5x, for staccato notes. (It's also a loud sample and at sustain 5 approximately matches other samples' volumes at sustain 7.)
* 85 is a really big-sounding horn that can add a sense of epic scale: the horn of the army approaching on the horizon. It's relatively quiet and blendy for all its dynamism, making it sound like something really big off in the distance. Try not to use without at least a light vibrato, as the transition from onset to loop is jarring without.
* 86 is a more unassuming and mellow horn. It's both blendy and not very dynamic, but its simplicity can lead to its own problems. Approaches a flutelike sound at higher octaves. Like 81, may need adjustment for shorter notes.
* 7F ... if you must. This is provided as a match for those annoying ambiguous timbres in SNES games that sound somewhere between a horn and an oboe -- for instance, the first lead in FF6's Under Martial Law. (Did you realize the lead changes from horn to oboe when the chord changes in that song? I didn't!) In the interest of having our horn parts sound like they're being played by horns, ideally if memory and channels permit this should be subtly layered with one of the horns that sound like horns.
* 88 should be favored over 89 when feasible. Try to watch closely whether the source is octaved and use 87 or 88 accordingly; don't swap it around heedlessly.
    
    
## LEGACY SAMPLE CONVERSION SUGGESTIONS:
* `01` (Acoustic Guitar) -> try 34 > 36 > 35. No clear match though. Note: 35 sounds one octave lower.
* `02` (Bass Guitar) -> 51. Note: sounds one octave higher.
* `03` (Pan Flute) -> A3
* `04` (Banjo) -> 31 (or 17, 14, 33, 32, 12). Most sound one octave higher. You'll want to add some harsh ADSR.
* `05` (Cello) -> 70, 72, or re-import this sample. Alternatives sound one octave higher.
* `06` (Choir) -> 75. Sounds one octave higher.
* `07` (Flute) -> A5, or A7 for space. Same timbre (A7 is same sample).
* `08` (Horn) -> Priority 84 > 85 > 86 > 7F. At least one of those should work.
* `09` (Atma Synth) -> Import.
* `0A` (Oboe) -> Ideally multisample between 91 through 94. If not, 92 is the same timbre and sounds one octave higher.
* `0B` (Perc organ) -> B4. Same sample.
* `0C` (Piano) -> 01, 06, or various multisample arrangements. 01 sounds one octave higher. 06 sounds three octaves higher and should only be used if the part stays around o6 or higher.
* `0D` (Strings) -> 65, or 66/67 to save space. Same sample, or same timbre for the alternatives.
* `0E` (Trumpet) -> Consider using 83. If not, priority 81 > 82. 81 and 82 sound one octave higher.
* `0F` (closed hihat) -> 3A. Same sample.
* `10` (mouth harp) -> AF. Same timbre, sounds two octaves higher.
* `11` (open hihat) -> 3C.
* `12` (crash cymbal) -> 2D. Will generally want to sound on a higher note (12 was native A4 while 2D is native A5, but many custom songs used 12 on higher notes so blanket shifting up an octave may not be advisable.)
* `13` (breath sfx) -> import
* `14` (march snare) -> 1A is preferred over 1B. 1B is same sample.
* `15` (pat) -> try 6E
* `16` (timpani) -> 5A is preferred over 5B. (5A same timbre/one octave lower; 5B same sample.)
* `17` (tom) -> 4B is same sample. 4A is a much less memory intensive variation.
* `18` (ac. bass) -> 50. Sounds one octave higher. May need to play with the ADSR some.
* `19` (pizzicato) -> 59 is a clean replacement, but go ahead and experiment with 57 and 58. They sound one octave lower.
* `1A` (tuba) -> 83. Same timbre, sounds one octave higher.
* `1B` (harp) -> 60. Same sample.
* `1C` (synth bass) -> 55 is the same sample, but please see if you can use 54 instead.
* `1D` (bouzouki) -> 32, same timbre.
* `1E` (dist guitar) -> 41, same sample, but experiment with 42/43/literally anything.
* `1F` (ocarina) -> If it's being used as a thin flute, A4 (sounds one octave higher). If it's being used as a whistle, A6 (sounds one lower) or D0 with a bit of attack.
* `20` (rhodes) -> 19 if you can swing the cost (sounds one higher), maybe 20 if you can't, or 22 (sounds one higher).
* `21` (hard snare) -> 1D
* `22` (kick) -> 0A, same sample.
* `23` (cowbell) -> 9D or 9C.
* `24` (tubular bells) -> 28, or 29 if it doesn't work out. Will probably need to fiddle with octaves, but there's no definitive answer for how much.
* `25` (church organ) -> B0.
* `26` (cuica) -> AB.
* `27-29` (cho-co-bo) import.
* `2A` (fingersnap) -> 8E.
* `2B` (side stick) -> 8A.
* `2C` (contrabass) -> 64, same sample.
* `2D` (guiro) -> 9B. Will need fiddling.
* `2E` (conga) -> 7A.
* `2F` (shaker) -> 6B, or 6A for space saving.
* `30` (wood block) -> 8C.
* `31` (dulcimer) -> try 14, 13, or 6. 14/13 sound one octave below, 6 sounds two above.
* `32` (ac. guitar) -> 36 is closest, but try 34 > 36 > 35.
* `33` (bagpipe) -> 99, same sample.
* `34` (shakuhachi) -> A4 is probably closest; use legato to imitate the initial trill.
* `35` (recorder) -> This is pretty close to a pure sine with some attack. If that's what you're after, use A6 (sounds one higher), D0 (two higher), or D1 (one higher) with attack added. But if you want to lean into the recorder sound with something breathier, use A1 (two higher). And if you want a smooth, ambiguous woodwind, go with the clarinet at 95 (one higher). All else equal, I prefer the clarinet. C3 is also a decent match if you're looking for something atmospheric.
* `36` (recorder/tin whistle) -> This usually gets used as "flute with prominent attack", so A4 (two higher) or A3 (one higher) are the most likely replacements. Again, though, I encourage pivoting to recorder (A1, one higher) or especially clarinet (95).
* `37` (sleigh bells) -> 6D.
* `38` (Ralse) -> 73, or if you absolutely must, the same sample is available at F0.
* `39` (Draco) -> 73, or if you absolutely must, the same sample is available at F1.
* `3A` (Maria) -> 75 or 74, or if you absolutely must, the same sample is available at F2.
* `3B` (pipe organ) -> B0. Same sample, sounds one octave higher.
* `3C` (bonk!) -> 4E maybe?
* `3D` (crane sfx) -> treat this as an import, so only use if you specifically need it, but it's at FA.
* `3E` (marimba) -> 23, same sample.
* `3F` (crowd sfx) -> FC, treat it as an import, do not break glass unless there is a fire etc.
* `40` (oboe) -> Use multisample if you can, but if you can't, this is same timbre as 94.
* `41` (brightness FX) -> 77, same sample.
* `42` (vibraphone) -> 22, same sample.
* `43` (RS3 strings 2) -> 62, probably, or 65/66/67/C4. All sound one octave lower. Maybe C3, which doesn't.
* `44` (12str. Guitar?) -> 33, same sample.
* `45` (CT strings) -> 62 or 66 are the most likely replacements, depending on whether you need instant-onset with 66 or clear airy high notes with 62. Feel free to use both. C4 can be a lifesaver as an alternative. All sound one octave lower.
* `46` (RnH strings) -> 67, generally.
* `47` (melodic bell) -> 27, same sample.
* `48` (sitar) -> 30.
* `49` (RS3 strings 1) -> 65, or maybe 62, or maybe one of the other strings. Sounds one octave lower.
* `4A` (slap bass) -> 56. Sounds one octave higher.
* `4B` (2300AD glass synth) -> if this is the original sound, import it (it's a fifth, so you need to). if it's just there to be fancy, try ... just about anything in the choir/organ/synth sections, really (7x/Bx/Cx). C5 is probably closest.
* `4C` (gong) -> 2F, same sample.
* `4D` (fretless bass) -> 53, sounds one octave higher.
* `4E` (violin) -> 71, or 70/72 (sounds one higher) or import.
* `4F` (sax) -> 98, same sample.
* `50` (crash cymbal) -> 2D.
* `51` (clap) -> 8F, same sample.
* `52` (od.guitar) -> 
* `53` (piano) ->
* `54` (ac.guitar) -> 34 > 36 > 35
* `55` (tambourine) -> 6C.
* `56` (snare) -> 1C, same sample.
* `57` (conga) -> 
* `58` (cembalo) -> 
* `59` (trance kick) -> 0D, same sample.
* `5A` (open hihat) -> 3B, same sample.
* `5B` (conga + gliss) ->
* `5C` (ultra pulse) -> C1, same sample.
* `5D` (od.guitar) -> 
* `5E` (wood block) ->
* `5F` (shaker) -> 
