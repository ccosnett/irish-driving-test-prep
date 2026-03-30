# Irish Driving Test Prep

Verified and organized study materials for passing the Irish Category B driving test first time.

Last reviewed: 2026-03-30

## Goal

Pass the Irish driving test first time, as soon as possible, using:

- the materials sent by Stephen Fitzsimons
- current official RSA guidance
- an Anki-first study system

## What Is In This Folder

- `stephens_materials/`
  - original PDF and image materials sent by Stephen Fitzsimons
- `ladybird_driving_test_questions.txt`
  - a practical-test-style question list
- `irish_driving_theory_anki.txt`
  - a tab-separated Q/A deck in a format that can be imported into Anki

## Verification Summary

Short version: these do **not** appear to be an official RSA-issued list of exact driving test questions.

What I verified from official sources:

- The RSA says the driving test includes questions on the Rules of the Road, including identifying road signs, plus hand signals and vehicle controls/checks.
- The RSA marking guidelines show that poor answers to Rules/Checks and Technical Checks can cost marks.
- The RSA tells learners to study the official Rules of the Road and the RSA preparation/checklist booklets.
- I found official RSA question banks for the **theory test**, but I did **not** find an official public RSA bank of exact practical-test oral questions for the car driving test.

Practical conclusion:

- Stephen's materials look like legitimate **prep material** built around the real RSA syllabus and common practical-test questioning.
- They look useful.
- They should be treated as **unofficial but relevant**, not as the final official wording of every question.

## Best Official Sources

Checked on 2026-03-30:

- RSA driving test overview:
  - <https://www.rsa.ie/services/learner-drivers/the-driving-test/what-it-is>
- RSA Rules of the Road:
  - <https://www.rsa.ie/services/learner-drivers/resources/rules-of-the-road>
- RSA marking guidelines:
  - <https://www.rsa.ie/docs/default-source/services/s3.2-adi/making-your-mark-marking-guidelines-for-the-driving-test.pdf?sfvrsn=548e1e7d_7>
- RSA practical-test checklist:
  - <https://www.rsa.ie/docs/default-source/services/s1.5-driving-test/checklist-for-your-driving-test.pdf>
- RSA rural speed limit update:
  - <https://www.rsa.ie/road-safety/campaigns/rural-speed-limit>
- Official theory-test materials:
  - <https://theorytest.ie/revision-material/>

## What The RSA Officially Confirms

From the RSA driving test page:

- the test checks knowledge of the Rules of the Road
- you must answer questions on the Rules of the Road, including road signs
- you must demonstrate hand signals
- your use of secondary controls is assessed

From the RSA marking guidelines:

- weak performance in `Rules/Checks` can be marked
- inability to describe technical checks can also be marked

This matters because the oral part is not random trivia. It is tied to:

- road signs
- road markings
- right of way
- speed limits
- lights and crossings
- parking and overtaking rules
- basic roadworthiness and vehicle checks

## Important Corrections For 2026

Your materials are broadly useful, but some items should be treated with care.

### 1. Speed-limit cards need updating

The biggest issue is any card that implies a simple universal answer like:

- `single carriageway = 80 km/h`
- `rural road = 80 km/h`

That is too broad now.

The RSA says that from **7 February 2025**, the default speed limit on many **rural local roads** changed from **80 km/h** to **60 km/h**. So any Anki card that treats `80 km/h` as the default answer for all rural or single-carriageway situations is risky.

Safer study rule:

- local rural roads: many are now 60 km/h by default
- regional roads: commonly 80 km/h
- national roads: commonly 100 km/h
- motorways: commonly 120 km/h
- always obey the posted limit if different

### 2. Contra-flow bus lane wording needs nuance

One of the Ladybird cards says a contra-flow bus lane is reserved only for buses and that no other traffic may use it day or night.

The official Rules of the Road is slightly more precise:

- a contra-flow bus lane is generally reserved only for buses
- **unless signs authorise its use by cyclists**

That is a small nuance, but exactly the kind of nuance worth keeping correct.

### 3. Some cards are better learned as "topic answers" rather than exact scripts

Because these are not official RSA-issued exact practical-test questions, do not overfit to one exact wording. Learn each topic so you can answer:

- in your own words
- clearly
- quickly
- without sounding memorized

## What To Focus On For A First-Time Pass

If the goal is first-time pass, fastest route, prioritize:

1. Road signs
2. Road markings
3. Speed limits
4. Right of way at junctions and roundabouts
5. Traffic lights and pedestrian crossings
6. Parking distances and parking restrictions
7. Overtaking rules
8. Hand signals
9. Secondary controls
10. Basic technical checks

These are the highest-yield oral-question areas and they also reinforce the practical drive itself.

## Anki Strategy

### Cleaned deck in this repo

Use this file for your main import:

- `irish_driving_test_2026_safe_anki.tsv`
- `irish_driving_test_2026_visual_anki.tsv`
- `irish_driving_test_2026_web_remote_anki.tsv`
- `irish_driving_test_easy_mode_core30.tsv`
- `irish_driving_test_easy_mode_pics.tsv`

It is a cleaned version of the current notes with:

- 2026-safe wording
- corrected speed-limit cards
- deduped overlap
- Anki tags in the third field

The visual deck:

- adds an image to each card
- uses images copied from `stephens_materials/`
- is best when you want stronger visual memory for signs and markings

The web-remote deck:

- adds an internet image URL to each card
- does not rely on the local Stephen image files
- is backed by `web_image_sources.csv`, which records the query and source used for each question

The easy-mode deck:

- trims the deck to 30 high-yield cards
- uses shorter prompts
- adds a memory cue before the answer
- is meant for fast recall when full wording feels heavy

The easy-mode picture deck:

- keeps the same 30-card easy deck
- adds a picture to the front of each card
- uses Irish sign images for the sign-heavy cards
- uses conceptual images for the rule cards

### Recommended deck structure

Use three decks or subdecks:

- `Irish Driving Test::Official Core`
  - only cards you are confident are current and official-aligned
- `Irish Driving Test::Stephen Questions`
  - cards from Stephen/Ladybird materials
- `Irish Driving Test::Corrections 2026`
  - any cards you rewrite because of rule changes or nuance

### Best card types

- Basic front/back for factual rules
- Cloze deletions for numbers:
  - speed limits
  - parking distances
  - tread depth
  - penalty-point thresholds
- Image occlusion for road-sign sheets

### Import notes

`irish_driving_theory_anki.txt` is already in a useful tab-separated format for Anki import.

`irish_driving_test_2026_safe_anki.tsv` is the better file to import first.

`irish_driving_test_2026_visual_anki.tsv` is the version with images embedded in the answer side.

`irish_driving_test_2026_web_remote_anki.tsv` is the version that points each card at a web image URL instead of a local image file.

`irish_driving_test_easy_mode_core30.tsv` is the simplest file to use when you are tired or overloaded.

`irish_driving_test_easy_mode_pics.tsv` is the easiest picture-cued version of the short deck.

Recommended import settings:

- note type: `Basic`
- field separator: `Tab`
- map field 1 -> `Front`
- map field 2 -> `Back`
- map field 3 -> `Tags`
- deck: `Irish Driving Test::Official Core`

Recommended first step after import:

- suspend or delete older cards from `irish_driving_theory_anki.txt` that conflict with the cleaned 2026 deck

Media note:

- the image files for the visual deck were copied into `~/Library/Application Support/Anki2/User 1/collection.media/` on this Mac
- if you use AnkiWeb and sync, the media should sync too

## 10-Day Sprint Plan

If you want the fastest realistic route, use this.

| Day | Focus | Output |
| --- | --- | --- |
| 1 | Import existing deck, suspend doubtful cards, study core road signs | 100% setup done |
| 2 | Speed limits, road markings, yellow/white lines, box junctions | 25 to 40 solid cards |
| 3 | Junctions, right of way, roundabouts, crossroads | Oral recall without notes |
| 4 | Traffic lights, crossings, filter arrows, school wardens | Fast answers under pressure |
| 5 | Parking rules, overtaking, hard shoulder, motorway rules | No hesitation on restrictions |
| 6 | Vehicle controls, lights, tyres, horn, breakdown procedure | Technical-check confidence |
| 7 | Hand signals plus mixed mock questioning | 1 full oral mock |
| 8 | Weak-area repair day | Rewrite weak cards |
| 9 | Full mixed review + practical lesson/pretest if possible | Smooth recall in the car |
| 10 | Light review only + sleep + test-day checklist | Arrive calm and sharp |

## Daily Study Routine

Do this every day until the test:

- 20 to 30 minutes Anki reviews
- 15 to 20 new cards only
- 10 minutes saying answers out loud without looking
- 10 minutes studying signs/markings visually
- 1 short driving-test oral mock with a friend, instructor, or voice note

Rule:

- do not add huge numbers of new cards once reviews start ballooning
- prioritize perfect recall of high-yield cards over deck size

## How To Use Stephen's Materials Well

Best use:

- treat them as a strong shortlist of likely topics
- use the photos for visual sign recognition
- use the Ladybird PDF/questions for oral practice

Do not assume:

- exact wording will match the RSA tester
- every answer is perfectly current without checking

## Test-Day Oral Strategy

When asked a question:

- answer directly first
- keep the first sentence short
- add one clarifying detail if useful
- stop talking once the answer is complete

Good pattern:

`What does a continuous white line mean?`

`You must stay to the left of it and you must not cross it except in limited situations such as access or an emergency.`

That style is usually stronger than a one-word answer.

## Personal Recommendation

If the goal is to pass first time as fast as possible:

- keep Anki
- trim or rewrite any outdated speed-limit cards immediately
- spend as much time on oral recall and sign recognition as on pure card review
- combine the deck with at least one proper pretest drive close to the exam

## Research Verdict

My best evidence-based conclusion is:

- the Stephen/Ladybird materials are **good unofficial preparation materials**
- they are **not** the official RSA-published practical driving test question bank
- they are still worth studying because they map closely to what the RSA says is examined
- they should be cleaned up slightly for 2026 accuracy, especially around speed limits

## Printables

- `WALL_SHEET.md` is the compact wall version built from the easy 30-card deck.
- `printables/irish-driving-test-wall-sheet.pdf` is the wall PDF.
- `printables/irish-driving-test-all-questions.pdf` is the full cleaned question-set PDF.
- `python3 scripts/build_printables.py` regenerates the wall sheet, PDFs, and the question appendix below.
- `.github/workflows/build-printables.yml` rebuilds the printables in GitHub Actions and uploads them as an artifact.

## All Questions

<!-- ALL_QUESTIONS_START -->

Generated from `irish_driving_test_2026_safe_anki.tsv`.

This is the full cleaned 2026-safe question set grouped by topic.

### Speed Limits

- **What speed limit usually applies in a built-up area in Ireland?**
  Answer: 50 km/h unless a different posted limit applies.
- **Since 7 February 2025, what is the default speed limit on many rural local roads?**
  Answer: 60 km/h.
- **What speed limit commonly applies on regional roads?**
  Answer: 80 km/h unless signs show otherwise.
- **What speed limit commonly applies on national roads?**
  Answer: 100 km/h unless signs show otherwise.
- **What speed limit commonly applies on motorways?**
  Answer: 120 km/h unless signs show otherwise.
- **If a posted speed limit is different from the default limit, which must you obey?**
  Answer: The posted speed limit.

### Right Of Way

- **Who has right of way at a roundabout?**
  Answer: Traffic already on the roundabout.
- **Who has priority at an unmarked crossroads where roads are of equal importance?**
  Answer: Give way to traffic from the right and to traffic already on the junction.

### Junctions

- **What must you do at a stop sign?**
  Answer: Come to a complete stop and yield before moving off.
- **What does a yield sign mean?**
  Answer: Give way to traffic with priority and stop if necessary.

### Traffic Lights

- **What does a flashing amber traffic light mean?**
  Answer: Proceed with caution only if the crossing or junction is clear; pedestrians have priority.
- **What should you do at a steady amber traffic light?**
  Answer: Stop unless it is unsafe to do so.
- **What do flashing red lights at a railway crossing mean?**
  Answer: Stop; a train is approaching or the crossing is operating.
- **What is a filter light?**
  Answer: A green or amber arrow that lets you proceed in that direction if it is safe and the way is clear.
- **When should you use dipped headlights?**
  Answer: When meeting traffic, following closely, on continuously lit roads, and in fog, snow, dusk, dawn, or poor visibility.
- **What should you do if you are dazzled by headlights?**
  Answer: Slow down and stop if necessary; watch for pedestrians or cyclists and look towards the left verge if the dazzle is from oncoming traffic.

### Crossings

- **What do white zig-zag lines at a zebra crossing mean?**
  Answer: No parking and no overtaking.
- **How far from a pedestrian crossing should you not park?**
  Answer: Within 15 metres before it or 5 metres after it.
- **What must you do when a school warden shows the STOP sign?**
  Answer: Stop and wait until children have crossed and the warden allows traffic to move again.
- **What is the difference between a pelican crossing and a zebra crossing?**
  Answer: A pelican crossing is controlled by lights; a zebra crossing uses flashing amber beacons and pedestrian priority.
- **What does an island in the middle of a pedestrian crossing mean?**
  Answer: Treat each side of a zebra crossing as separate; a staggered pelican crossing is also treated as two crossings.

### Road Markings

- **What are the rules for a yellow box junction?**
  Answer: Do not enter unless you can clear it without stopping, except when turning right and waiting for a safe gap without blocking traffic with priority.
- **What does a broken white line in the centre of the road mean?**
  Answer: You may cross it only if it is safe to do so.
- **What does a continuous white line in the centre of the road mean?**
  Answer: Keep left and do not cross it except for access or in an emergency.
- **What do double broken white lines along the centre of the road mean?**
  Answer: They warn that continuous white lines are ahead; do not cross them unless it is safe.
- **If there is a continuous and a broken white line together, which line do you obey?**
  Answer: The line nearest to you.
- **What does a broken yellow line along the side of the road mean?**
  Answer: It marks a hard shoulder, normally for pedestrians and cyclists; you may pull in briefly to let faster traffic pass if it is safe.
- **What does a single continuous yellow line along the side of the road mean?**
  Answer: No parking during the times shown.
- **What do double continuous yellow lines at the side of the road mean?**
  Answer: No parking at any time.
- **What are the road markings for no entry?**
  Answer: A continuous and a broken white line with the words NO ENTRY.

### Parking

- **How far from a junction should you not park?**
  Answer: Within 5 metres of the junction.
- **How close to the kerb should you normally park?**
  Answer: Within 45 cm.

### Signs

- **What shape are warning signs in Ireland?**
  Answer: Diamond-shaped with a yellow background.
- **What shape are most regulatory signs in Ireland?**
  Answer: Circular.
- **What colour are motorway signs?**
  Answer: Blue.
- **What colour are national road signs?**
  Answer: Green.
- **What colour are regional and local road signs?**
  Answer: White with black text.

### Overtaking

- **When another driver is overtaking you, what must you not do?**
  Answer: Increase your speed.
- **When may you overtake on the left?**
  Answer: When the driver ahead has moved right and signalled right, when you have signalled left, or in slow-moving traffic where the left lane is moving faster.
- **Give examples of places where you should not overtake.**
  Answer: Near a bend, hill crest, hump-back bridge, continuous white line, entrance, taxi rank, or where the road is too narrow or visibility is poor.

### Motorway

- **When may you use the hard shoulder on a motorway?**
  Answer: In an emergency only.
- **Which lane should you normally use on a motorway?**
  Answer: The left-hand lane unless overtaking or directed otherwise by signs or road markings.
- **What should you do if you break down on a motorway?**
  Answer: Pull onto the hard shoulder if possible, use your hazard lights, get help, and do not attempt roadside repairs unless it is necessary and safe.

### Safe Driving

- **What is the 2-second rule?**
  Answer: Leave at least 2 seconds in dry conditions, at least 4 seconds in wet conditions, and more in ice or poor conditions.
- **How does wet weather affect braking distance?**
  Answer: It can at least double braking distance.
- **What is aquaplaning?**
  Answer: When a layer of water causes the tyres to lose contact with the road, reducing steering and braking control.
- **What is tailgating?**
  Answer: Driving too close to the vehicle in front.

### Technical Checks

- **What is the legal minimum tyre tread depth for a car?**
  Answer: 1.6 mm across the central three-quarters of the tread.
- **Name 3 technical checks you should be able to describe for the test.**
  Answer: Examples: tyres, lights and indicators, oil, coolant, brake fluid, brakes, steering, or horn.

### Secondary Controls

- **Name 3 secondary controls you may be asked to demonstrate on the test.**
  Answer: Examples: wipers, washers, demister, rear window heater, lights, or hazard lights.

### Learner Rules

- **What is the minimum age for a Category B learner permit?**
  Answer: 17.
- **What must a learner driver display on the vehicle?**
  Answer: L-plates on the front and rear.
- **Must a learner driver be accompanied?**
  Answer: Yes. By someone with a full, valid licence in the same category for at least 2 years.

### Safety Rules

- **What is the seatbelt rule in a car?**
  Answer: Everyone must wear a seatbelt where one is fitted; the driver is responsible for passengers under 17.
- **What is the rule on mobile phones while driving?**
  Answer: It is illegal to hold or use a hand-held mobile phone while driving; the safest option is not to use any phone while driving.
- **What is the alcohol limit for learner, novice, and professional drivers?**
  Answer: 20 mg of alcohol per 100 ml of blood.
- **What is the alcohol limit for most other drivers?**
  Answer: 50 mg of alcohol per 100 ml of blood.
- **What should you do before opening your car door?**
  Answer: Check mirrors, look over your shoulder, and watch for cyclists or pedestrians.

### Bus Lanes

- **What is the difference between a with-flow and a contra-flow bus lane?**
  Answer: A with-flow lane runs with the traffic and can be used by buses, bicycles and taxis; a contra-flow lane runs against the traffic and is generally only for buses unless signs also allow cyclists.

### Positioning

- **What position should you take for a right turn in a one-way street?**
  Answer: As close as practicable to the right-hand side.

### Manoeuvres

- **Where would you never make a U-turn?**
  Answer: In a one-way street, where continuous white lines apply, or where a sign prohibits it.

### Dual Carriageway

- **When following the road ahead on a multi-lane dual carriageway, which lane should you normally use?**
  Answer: Lane 1, the left-hand driving lane, unless signs or road markings say otherwise.

### Vehicle Control

- **What is coasting and why is it dangerous?**
  Answer: Coasting is driving with the clutch down or in neutral; it reduces your control of the vehicle.

### Vehicle

- **What is the purpose of the NCT?**
  Answer: It is a basic roadworthiness and safety check for vehicles over 4 years old.

### Awareness

- **What should you look out for on country roads?**
  Answer: Pedestrians, cyclists, animals, mud, concealed entrances, bends, and slow-moving farm machinery.

### Penalties

- **What is the normal penalty point disqualification threshold for most fully licensed drivers?**
  Answer: 12 points in a 3-year period.
- **What is the lower penalty point disqualification threshold for learner and novice drivers?**
  Answer: 7 points in a 3-year period.

### Signals

- **When may you use your horn?**
  Answer: Only to warn other road users of danger; do not use it in a built-up area between 11:30 pm and 7:00 am unless there is an emergency.

<!-- ALL_QUESTIONS_END -->
