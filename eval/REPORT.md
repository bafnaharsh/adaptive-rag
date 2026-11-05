# iPhone manuals: end-to-end eval

LLM backend: `cli:claude` (model `CLI default`). Passed **20/20**. Median latency 12.6 s.

| id | category | expected | tier | verified citations | page hit | keywords | s | result |
|---|---|---|---|---|---|---|---|---|
| ug_wifi | doc | rag/hybrid | rag | 1/1 | exact | 50% | 12.9 | PASS |
| ug_control_center | doc | rag/hybrid | rag | 2/2 | exact | 100% | 7.4 | PASS |
| ug_lost_iphone | doc | rag/hybrid | rag | 9/9 | exact | 100% | 13.4 | PASS |
| ug_burst | doc | rag/hybrid | rag | 1/1 | exact | 100% | 4.5 | PASS |
| ug_screenshot | doc | rag/hybrid/web | rag | 2/2 | exact | 100% | 7.1 | PASS |
| ug_force_restart | doc | rag/hybrid/web | web | 4/4 | exact | 67% | 43.6 | PASS |
| rm_thermal_event | doc | rag/hybrid | hybrid | 3/3 | exact | 100% | 23.5 | PASS |
| rm_broken_glass | doc | rag/hybrid | rag | 3/3 | exact | 100% | 10.1 | PASS |
| rm_diagnostics_requirements | doc | rag/hybrid | rag | 6/6 | exact | 100% | 12.6 | PASS |
| rm_reuse_screws | doc | rag/hybrid | rag | 3/3 | exact | 100% | 4.5 | PASS |
| rm_flex_cable_bend | doc | rag/hybrid | hybrid | 2/2 | exact | 100% | 20.4 | PASS |
| rm_part_blue_torque_driver | hybrid | rag/hybrid | rag | 1/1 | exact | 50% | 7.6 | PASS |
| rm_part_grounding_spring_screw | hybrid | rag/hybrid | hybrid | 2/2 | exact | 100% | 20.4 | PASS |
| rm_adjustable_torque_range | hybrid | rag/hybrid | rag | 2/2 | exact | 100% | 8.7 | PASS |
| know_usb | knowledge | knowledge | knowledge | 0/0 | - | - | 1.7 | PASS |
| know_ram | knowledge | knowledge | knowledge | 0/0 | - | - | 1.8 | PASS |
| know_boiling_point | knowledge | knowledge | knowledge | 0/0 | - | - | 4.5 | PASS |
| web_newest_iphone | web | web | web | 3/3 | - | - | 38.4 | PASS |
| web_latest_ios | web | web | web | 3/3 | - | - | 13.9 | PASS |
| web_apple_revenue | web | web | web | 2/2 | - | - | 15.0 | PASS |

## Answers

### ug_wifi: How do I connect my iPhone to a Wi-Fi network?

Tier: rag

To connect your iPhone to a Wi-Fi network:

1. Go to **Settings > Wi-Fi**, then turn Wi-Fi on [1]. You can also turn Wi-Fi on or off in Control Center [1].
2. Tap one of the listed networks [1].
3. Enter the password if asked [1].

Once connected, **Connect to Wi-Fi** appears at the top of the screen [1]. iPhone reconnects anytime you return to the same location [1].

**Sources**
- [1] iphone_user_guide.pdf, p. 16 ✓ — “Go to Settings > Wi-Fi, then turn Wi-Fi on or off. (You can also turn Wi-Fi on or off in Control Center.) • Choose a network: Tap one of the listed networks, then enter the password, if asked.”

<details><summary>Trace</summary>

- Plan: route=documents — The question is about connecting an iPhone to Wi-Fi, which is the subject of the indexed iPhone user guide.
- Tier 1 · RAG (dense): 6 chunks (iphone_user_guide.pdf p. 16, 17, 40, 20) → judge: sufficient
- Reasoning: doc:29 (p. 16) states the core steps directly: go to Settings > Wi-Fi, turn Wi-Fi on, tap one of the listed networks, and enter the password if asked. It also notes that Wi-Fi can be toggled from Control Center and that iPhone reconnects when you return to the same location. doc:31 and doc:32 (p. 17) add that iPhone prefers the most recently used available network, and that it shows a list of networks in range if you need to choose one. doc:96 and doc:97 cover sharing a connection through Personal Hotspot and are not relevant to joining a Wi-Fi network. doc:44 covers Wi-Fi syncing with iTunes and is not relevant either. Together, doc:29 and doc:31/32 answer the question completely and accurately.
- Generate: 1 citations
- Verify: 1/1 citations verified

</details>

### ug_control_center: How do I open Control Center on my iPhone?

Tier: rag

To open Control Center, swipe up from the bottom edge of any screen, including the Lock screen [1].

For VoiceOver users, select any item in the status bar, then swipe up with three fingers [2].

**Sources**
- [1] iphone_user_guide.pdf, p. 35 ✓ — “Swipe up from the bottom edge of any screen (even the Lock screen).”
- [2] iphone_user_guide.pdf, p. 154 ✓ — “Select any item in the status bar, then swipe up with three fingers.”

<details><summary>Trace</summary>

- Plan: route=documents — The question asks about a feature of the iPhone, which is the subject of the indexed iPhone user guide.
- Tier 1 · RAG (dense): 6 chunks (iphone_user_guide.pdf p. 35, 154, 172, 169, 41, 170) → judge: sufficient
- Reasoning: The question asks how to open Control Center on an iPhone. Source doc:77 (iphone_user_guide.pdf, p. 35) states the answer directly under 'Open Control Center': swipe up from the bottom edge of any screen, including the Lock screen. Its closing-method details (swipe down, tap the top of the screen, or press the Home button) are extra and not needed for the question. Source doc:371 and doc:432 describe VoiceOver and AssistiveTouch routes, which are alternatives for accessibility users and not required for the standard answer. Nothing in the question goes unanswered, so no further search is needed.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### ug_lost_iphone: I lost my iPhone, what can Find My iPhone do to help me?

Tier: rag

Find My iPhone can help you locate and secure your iPhone, using the free Find My iPhone app on another Apple device or icloud.com/find in a browser [1]. Its options include:

- **Play Sound:** Plays a sound at full volume for two minutes, even if the ringer is set to silent [2].
- **Lost Mode:** Locks the iPhone with a passcode and shows it a message with a contact number [3]. The iPhone tracks and reports its location, so you can see where it has been [4].
- **Erase iPhone:** Erases all information and media and restores the factory settings [5].

There are conditions. Find My iPhone must have been turned on before the phone was lost [6], and the iPhone must be able to connect to the Internet [7]. If Send Last Location was on, the iPhone sends its last location before the battery runs out [8]. Activation Lock is designed to prevent anyone else from using the iPhone if you lose it [9].

The guide does not describe any steps for physically recovering the phone beyond these features.

**Sources**
- [1] iphone_user_guide.pdf, p. 46 ✓ — “Find My iPhone can help you locate and secure your iPhone using the free Find My iPhone app”
- [2] iphone_user_guide.pdf, p. 46 ✓ — “Play Sound: Play a sound at full volume for two minutes, even if the ringer is set to silent.”
- [3] iphone_user_guide.pdf, p. 46 ✓ — “Lost Mode: Immediately lock your missing iPhone with a passcode and send it a message displaying a contact number.”
- [4] iphone_user_guide.pdf, p. 46 ✓ — “iPhone tracks and reports its location, so you can see where it’s been when you check the Find My iPhone app.”
- [5] iphone_user_guide.pdf, p. 46 ✓ — “Erase iPhone: Protect your privacy by erasing all the information and media on your iPhone and restoring it to its original factory settings.”
- [6] iphone_user_guide.pdf, p. 46 ✓ — “To use Find My iPhone features, Find My iPhone must be turned on before your iPhone is lost.”
- [7] iphone_user_guide.pdf, p. 46 ✓ — “iPhone must be able to connect to the Internet for you to locate and secure the device.”
- [8] iphone_user_guide.pdf, p. 46 ✓ — “iPhone sends its last location prior to the battery running out when Send Last Location in Settings is turned on.”
- [9] iphone_user_guide.pdf, p. 46 ✓ — “Find My iPhone includes Activation Lock, which is designed to prevent anyone else from using your iPhone if you ever lose it.”

<details><summary>Trace</summary>

- Plan: route=documents — The question is about Find My iPhone, which the indexed iPhone user guide covers directly on page 46.
- Tier 1 · RAG (dense): 6 chunks (iphone_user_guide.pdf p. 46, 18, 191, 189) → judge: sufficient
- Reasoning: doc:116 says Find My iPhone helps locate and secure a lost iPhone and includes Activation Lock, which prevents others from using it, but only if Find My iPhone was turned on before the loss and the iPhone can reach the Internet. It also notes that Send Last Location sends the last location before the battery runs out. doc:117 lists the actions available from the app or icloud.com/find: Play Sound (full volume for two minutes, even on silent), Lost Mode (locks the phone with a passcode, shows a contact number, and tracks its location), and Erase iPhone (wipes all data and restores factory settings). doc:37 adds that you can locate the iPhone on a map, display a message, lock the screen, suspend Apple Pay cards, or remotely wipe data. Together these cover what Find My iPhone can do for a lost phone. The guide is for an older iOS version, so some details may differ on current devices, but the question is answered from the evidence provided.
- Generate: 9 citations
- Verify: 9/9 citations verified

</details>

### ug_burst: How do I take burst photos with the iPhone camera?

Tier: rag

To take burst photos on an iPhone 5s or later, open Camera and choose Photo or Square mode, since burst shots are available in those modes [1]. Then touch and hold the Take Picture button [1]. The camera takes rapid-fire photos and shows a counter of shots until you lift your finger [1].

To review the burst, tap the thumbnail and then tap Select to see the suggested shots, which are marked with gray dots [1]. To keep a photo from the burst as a separate photo in your Bursts album, tap the circle in its lower-right corner [1]. To delete the whole burst, tap it, then tap the delete control [1].

**Sources**
- [1] iphone_user_guide.pdf, p. 94 ✓ — “Touch and hold the Take Picture button to take rapid-fire photos in bursts (available while in Square or Photo mode).”

<details><summary>Trace</summary>

- Plan: route=documents — The question is about iPhone camera burst shots, which is the subject of the indexed iPhone user guide.
- Tier 1 · RAG (dense): 6 chunks (iphone_user_guide.pdf p. 94, 95, 92, 96) → judge: sufficient
- Reasoning: doc:239 directly answers the question: on iPhone 5s or later, touch and hold the Take Picture button in Square or Photo mode to take rapid-fire burst photos, and the burst continues until you lift your finger. It also explains how to review suggested shots, keep individual photos, and delete a burst. doc:238 confirms that Photo mode is chosen by dragging or tapping the mode labels, and doc:242 and doc:244 add context about other camera modes and the capture timer, but none of that is needed to answer. The question is fully answered by doc:239.
- Generate: 1 citations
- Verify: 1/1 citations verified

</details>

### ug_screenshot: How do I take a screenshot of what is on my iPhone screen?

Tier: rag

To take a screenshot of what is on your iPhone screen, press the Sleep/Wake and Home buttons at the same time and release them [1]. The screenshot is saved to the Photos tab in Photos, and you can also find it in the Camera Roll album or the All Photos album if you use iCloud Photo Library [1]. The iPhone user guide's menu of hardware actions gives the same combination: pressing the Home and Sleep/Wake buttons simultaneously takes a screenshot [2].

**Sources**
- [1] iphone_user_guide.pdf, p. 96 ✓ — “Simultaneously press and release the Sleep/ Wake and Home buttons. The screenshot is added to the Photos tab in Photos and can also be viewed in the Camera Roll album or All Photos album”
- [2] iphone_user_guide.pdf, p. 170 ✓ — “Press the Home and Sleep/Wake buttons simultaneously to take a screenshot”

<details><summary>Trace</summary>

- Plan: route=documents — The question concerns iPhone functionality, which the indexed iPhone user guide likely covers, so the documents should be searched.
- Tier 1 · RAG (dense): 6 chunks (iphone_user_guide.pdf p. 93, 96, 170; iphone_16_repair_manual.pdf p. 40, 46) → judge: sufficient
- Reasoning: The question asks how to take a screenshot on an iPhone. Source doc:244 (iphone_user_guide.pdf, p. 96) states directly: 'Simultaneously press and release the Sleep/Wake and Home buttons,' and notes that the screenshot is added to the Photos tab and the Camera Roll or All Photos album. Source doc:432 (p. 170) confirms the same button combination ('Press the Home and Sleep/Wake buttons simultaneously to take a screenshot'). The other sources (doc:237, doc:600, doc:619, doc:599) concern the camera, repair, and display diagnostics and do not bear on the question. The answer is complete and accurate from the evidence, with no guessing required.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### ug_force_restart: How do I force restart my iPhone when it will not turn off?

Tier: web

Your question doesn't say which iPhone model you have, so the method depends on whether your iPhone has a Home button.

**If your iPhone has no Home button (iPhone 8 through iPhone 17 per these sources):** Press and quickly release Volume Up, then press and quickly release Volume Down, then press and hold the Side button until the Apple logo appears [1][2][3]. The web sources say this works on every iPhone 8 through iPhone 17 running iOS 26 [2], and one of them describes the same sequence for iPhone 16 [1].

**If your iPhone has a Home button:** Hold down the Sleep/Wake button and the Home button at the same time for at least ten seconds, until the Apple logo appears [4]. The iPhone user guide says to use this reset only if you're unable to restart iPhone [4].

The evidence does not state which models use which method beyond the iPhone 8 through 17 range, so if neither method works, check your model's Home-button status before trying the other.

**Sources**
- [1] [How To Restart iPhone 16 — Easy Step-By-Step Guide!](https://thetechgorilla.com/how-to-restart-iphone-16/) ✓ — “For a force restart on a frozen iPhone 16, press Volume Up, then Volume Down, then hold the Side button until the Apple logo appears.”
- [2] [How to Fix Unresponsive iPhone When Nothing Works (2026)](https://www.appleheadlines.com/how-to-fix-unresponsive-iphone/) ✓ — “This force restart works on every iPhone 8 through iPhone 17 running iOS 26”
- [3] [How To Restart iPhone 16 — Easy Step-By-Step Guide!](https://thetechgorilla.com/how-to-restart-iphone-16/) ✓ — “Press and quickly release Volume Up. Then press and quickly release Volume Down. Finally, press and hold the Side button until the Apple logo appears”
- [4] iphone_user_guide.pdf, p. 187 ✓ — “Hold down the Sleep/Wake button and the Home button at the same time for at least ten seconds, until the Apple logo appears.”

<details><summary>Trace</summary>

- Plan: route=documents — This is about iPhone troubleshooting, which the indexed iPhone user guide and repair manual cover, so the documents should be searched.
- Tier 1 · RAG (dense): 6 chunks (iphone_user_guide.pdf p. 187, 186, 35, 12; iphone_16_repair_manual.pdf p. 37, 28) → judge: insufficient — The force-restart procedure for iPhone models without a Home button (iPhone X and later, including iPhone 16), which uses the volume and side buttons instead of Sleep/Wake plus Home. The evidence only covers Home-button models.
- Reasoning: Source doc:480 (iphone_user_guide.pdf, p. 187) directly answers the core question: to force restart, hold down the Sleep/Wake button and the Home button at the same time for at least ten seconds, until the Apple logo appears. It also says this reset should be used only if iPhone can't be restarted normally. Source doc:479 (p. 186) covers the normal restart (hold Sleep/Wake until the slider appears), which is the step to try before a force restart. Source doc:17 (p. 12) covers turning iPhone on and off with the Sleep/Wake button, and doc:564 and doc:594 are repair-manual material on no-power troubleshooting and Diagnostics Mode. Doc:79 is unrelated (Do Not Disturb). The question asks how to force restart 'my iPhone' without naming a model. The only force-restart method in the evidence depends on a Home button. The evidence includes an iPhone 16 repair manual, and the iPhone 16 has no Home button, so the method in doc:480 may not apply to the user's device. No source gives the force-restart method for Home-button-less models (such as pressing Volume Up, then Volume Down, then holding the side button), so answering for the user's likely device would require guessing.
- Tier 2 · Hybrid (BM25+dense, reranked): 4 queries (How do I force restart my iPhone when it will not turn off? | force restart iPhone 16 without Home button volume up volume down side button | how to force restart iPhone that won't turn off Apple support | iPhone X or later force restart press and release volume up then volume down hold side button) → 12 chunks (iphone_user_guide.pdf p. 187, 186, 35, 170; iphone_16_repair_manual.pdf p. 63, 59, 37, 36, 12, 56) → judge: insufficient — The force-restart button sequence for iPhone models without a Home button (iPhone X and later, including iPhone 16), which uses the volume and side buttons. The evidence only gives the Home-button method.
- Reasoning: Source doc:480 (iphone_user_guide.pdf, p. 187) gives the only force-restart steps in the evidence: hold the Sleep/Wake and Home buttons together for at least ten seconds, until the Apple logo appears. This applies only to iPhones with a Home button. Source doc:479 (p. 186) covers a normal restart, which should be tried first. The new repair-manual sources (doc:665, doc:654, doc:653, doc:644, doc:530) all tell the reader to 'force restart the iPhone' but never describe how. Doc:591 mentions the Sleep/Wake or Side button only as a way to turn the device back on after an unexpected shutoff, not as a force-restart procedure. Doc:432 covers a simulator's screenshot shortcut, which is unrelated. Doc:594, doc:593, doc:564, doc:17, and doc:79 add no force-restart steps. The question does not name a model. The iPhone 16 repair manual covers models with no Home button, and for those the method in doc:480 does not apply. No source gives the button sequence for those models, so answering would require guessing.
- Tier 3 · Web: “force restart iPhone 16 press volume up release volume down hold side button” → 5 chunks (https://thetechgorilla.com/how-to-restart-iphone-16/; https://www.youtube.com/watch?v=n-lT1WXyLJU; https://www.appleheadlines.com/how-to-fix-unresponsive-iphone/)
- Generate: 4 citations
- Verify: 4/4 citations verified

</details>

### rm_thermal_event: What should I do if the battery starts smoking or has a thermal event while I am repairing an iPhone?

Tier: hybrid

If the battery starts smoking or has a thermal event during an iPhone repair, the manual says to act immediately. Smother the battery or device with plenty of clean, dry sand, and dump all of the sand at once, because timing is critical [1]. Contact local fire authorities if further assistance is needed [1]. Leave the room for 30 minutes after the reaction is contained, ventilate the area, and do not return until the area is clear of smoke [1]. Wait 30 minutes before touching the device, then use heat-resistant gloves and safety glasses with side shields to remove it from the sand [1][2]. Afterward, wipe the affected area with water first, then with an ESD-safe cleaning solution [2]. Dispose of the damaged battery or device, including any debris removed from the sand, according to local environmental laws and guidelines [2].

The signs that should trigger this response include the battery beginning to smoke or emit sparks or soot, the battery pouch suddenly puffing out, and hissing or popping sounds [2][3]. The manual also says to disconnect all external cables and remove cases and covers [3].

The evidence does not say whether water should be used to put out the fire. The manual's cleanup step says to wipe with water, but it does not give guidance on using water as an extinguishing agent, so I cannot say more about that without guessing.

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do smother the battery or device immediately with plenty of clean, dry sand. Dump the sand all at once.”
- [2] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do wipe the affected area with water first. Then wipe the area with an ESD-safe cleaning solution.”
- [3] iphone_16_repair_manual.pdf, p. 5 ✓ — “The lithium-ion battery or a device that contains one begins to smoke or emit sparks or soot.”

<details><summary>Trace</summary>

- Plan: route=documents — This concerns iPhone repair and battery safety, which is the subject of the indexed iPhone 16 repair manual and user guide, so it should be answered from the documents.
- Tier 1 · RAG (dense): 6 chunks (iphone_16_repair_manual.pdf p. 28, 85, 5, 29, 4) → judge: insufficient — Explicit emergency response steps for a smoking or thermally venting iPhone battery during repair: immediate actions (move away, evacuate, ventilate), appropriate extinguishing method and what to avoid, when to call emergency services, and safe handling or containment of the damaged battery afterward. The complete text of the hissing/popping instruction on doc:522 p.5 is also missing.
- Reasoning: doc:522 (p.5) covers prevention and partial response. It warns that a lithium-ion battery or device may begin to emit hissing or popping sounds, and it says not to puncture, strike, or crush batteries to avoid fumes or a thermal event. It also says to disconnect external cables, remove cases, and keep the iPhone in a well-ventilated area, and it notes the flashlight produces heat. However, the sentence that opens the hissing/popping guidance is cut off, so the action it prescribes is missing. doc:518 (p.4) says improper handling or failure to discharge the battery can cause overheating, swelling, venting, leaking, or a thermal event that could cause fire, injury, or death, and it says to be prepared for all outcomes. It does not say what to do when smoke or a thermal event occurs. doc:687 (p.85) covers pre-repair steps such as discharging the battery, disconnecting cables, and using an ESD setup, which are prevention rather than response. doc:564, doc:563, doc:565, and doc:529-style troubleshooting sources cover diagnostics and battery replacement, not emergencies. Part of the question is covered: prevention, and a few immediate actions (disconnect cables, ventilate, don't puncture or crush). Not covered: the explicit response to active smoke or a thermal event, such as stepping away, evacuating, what to use or avoid for extinguishing (e.g., water versus Class D extinguisher or sand), when to call emergency services, and whether to keep the battery in a non-combustible container. Answering these would require guessing.
- Tier 2 · Hybrid (BM25+dense, reranked): 4 queries (What should I do if the battery starts smoking or has a thermal event while I am repairing an iPhone? | iPhone battery smoking or thermal event during repair what to do Apple repair manual | lithium-ion battery thermal runaway smoke immediate response extinguish Class D water sand | damaged lithium-ion battery containment after thermal event store in non-combustible container call emergency services) → 12 chunks (iphone_16_repair_manual.pdf p. 4, 5, 85, 87, 36, 118, 31, 28; iphone_user_guide.pdf p. 183) → judge: sufficient
- Reasoning: doc:520 (p.5) directly answers the response question. It defines a battery thermal event and says to act immediately if signs appear. It instructs the user to smother the battery or device at once with plenty of clean, dry sand, dumped all at once, and to contact local fire authorities if further help is needed. It says to leave the room for 30 minutes after the reaction is contained, ventilate the area, and not return until smoke has cleared. It also says to wait 30 minutes before touching the device, then remove it from the sand with heat-resistant gloves and safety glasses. doc:521 (p.5) completes the aftercare: wipe the affected area with water first, then with an ESD-safe cleaning solution, and dispose of the damaged battery and debris according to local environmental laws. doc:521 also gives the warning signs (smoke, sparks, soot, pouch puffing out, hissing or popping), and doc:522 (p.5) adds to disconnect external cables, remove cases, and keep the iPhone in a well-ventilated area. doc:517 and doc:518 (p.4) define the hazard and the risk of fire and injury. Together these cover the question: immediate action (sand, not water), when to call fire services, evacuation and ventilation, waiting before handling, safe handling of the device, and disposal. The only gap is that doc:521 says to wipe with water after sand, which seems to conflict with using water as an extinguisher, but the manual's guidance is explicit about the sequence, so no guessing is needed to answer. The snippet of doc:522 is truncated at the start, but the sign list is covered by doc:521. Evidence is sufficient.
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>

### rm_broken_glass: What protective gear do I need before repairing an iPhone with a broken display glass?

Tier: rag

Before repairing an iPhone with broken display glass, wear **safety glasses with side shields** and **cut-resistant gloves** [1]. The manual says to put these on first, then use an ESD-safe vacuum to clear glass from the workspace and the iPhone [2]. A protective cover is also attached to the broken glass, but that is a repair supply, not worn gear [1]. The manual also says to read the Broken Glass Safety section before starting the display repair [3].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 7 ✓ — “Put on safety glasses with side shields and the cut-resistant gloves.”
- [2] iphone_16_repair_manual.pdf, p. 7 ✓ — “Use an ESD-safe vacuum cleaner to remove glass pieces from your workspace and the iPhone.”
- [3] iphone_16_repair_manual.pdf, p. 170 ✓ — “Read Broken Glass Safety before you begin.”

<details><summary>Trace</summary>

- Plan: route=documents — The question concerns iPhone repair procedures covered by the indexed iPhone 16 Repair Manual, which has passages on broken glass safety and display repair.
- Tier 1 · RAG (dense): 6 chunks (iphone_16_repair_manual.pdf p. 7, 170, 107, 118, 48, 1) → judge: sufficient
- Reasoning: Question: what protective gear is needed before repairing an iPhone with broken display glass. doc:524 (p. 7) answers this directly. Its Broken Display Glass steps say to put on safety glasses with side shields and cut-resistant gloves before starting. The same section lists a display protective cover and an ESD-safe vacuum cleaner, which are used to contain and clear glass rather than worn as personal protection. doc:779 (p. 170) confirms that the Broken Glass Safety section must be read before the display repair, and its tool list has no additional protective gear. doc:713 (p. 107) lists cut-resistant and heat-resistant gloves, but that is for the back glass repair, not the display. No part of the question is left unanswered: the personal protective gear for a broken-display repair is safety glasses with side shields and cut-resistant gloves.
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>

### rm_diagnostics_requirements: What do I need to run Apple Diagnostics for Self Service Repair on an iPhone?

Tier: rag

To run Apple Diagnostics for Self Service Repair on an iPhone, you need:

- An iPhone 12 or later that can turn on and start up in iOS [1].
- iOS 17 or later to run it on a web browser [2]. Beta versions aren't supported [3].
- Software that is up to date before you continue [4].
- A secondary device, such as a Mac, PC, iPad, or iPhone, to access the Apple Diagnostics for Self Service Repair website and diagnostic console [5].
- The serial number of the device you're testing, which you write down before starting [6].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 21 ✓ — “An iPhone 12 or later to be tested that can turn on and start up in iOS.”
- [2] iphone_16_repair_manual.pdf, p. 21 ✓ — “The device youʼre testing must have iOS 17 or iPadOS 17 or later to run Apple Diagnostics for Self Service Repair on a web browser.”
- [3] iphone_16_repair_manual.pdf, p. 21 ✓ — “Beta versions of iOS and iPadOS arenʼt supported.”
- [4] iphone_16_repair_manual.pdf, p. 21 ✓ — “Ensure that the deviceʼs software is up to date before continuing.”
- [5] iphone_16_repair_manual.pdf, p. 21 ✓ — “A secondary device such as a Mac, PC, iPad, or iPhone to access the Apple Diagnostics for Self Service Repair website and diagnostic console.”
- [6] iphone_16_repair_manual.pdf, p. 22 ✓ — “Write down the device serial number.”

<details><summary>Trace</summary>

- Plan: route=documents — The question concerns Apple Diagnostics for Self Service Repair, which is covered in the indexed iPhone 16 Repair Manual, so it should be answered from the documents.
- Tier 1 · RAG (dense): 6 chunks (iphone_16_repair_manual.pdf p. 21, 16, 22) → judge: sufficient
- Reasoning: doc:546 lists the device requirements: an iPhone 12 or later that can turn on and start up in iOS, running iOS 17 or later (beta versions not supported), with software updated. doc:547 says a secondary device such as a Mac, PC, iPad, or iPhone is needed to access the Apple Diagnostics for Self Service Repair website and diagnostic console. doc:549 and doc:550 add setup steps that depend on these items: a Wi-Fi network, the device serial number, and a diagnostics session. The question asks what is needed to run the tool, and all of these requirements are stated in the evidence, so nothing essential is missing.
- Generate: 6 citations
- Verify: 6/6 citations verified

</details>

### rm_reuse_screws: Can I reuse the old screws when I put an iPhone back together?

Tier: rag

No. The manual says you should not reuse the old screws. It warns that you should "Never reinstall a screw after it has been removed" [1]. It also says to "Install only new screws" [1]. The reason given is that "iPhone screws are covered with an adhesive that canʼt be reused" [1]. The reassembly steps match this, calling for "one new trilobe screw" and "two new crosshead screws" [2][3].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 73 ✓ — “Never reinstall a screw after it has been removed. Install only new screws.”
- [2] iphone_16_repair_manual.pdf, p. 158 ✓ — “install one new trilobe screw (923- 11712) into the bottom speaker”
- [3] iphone_16_repair_manual.pdf, p. 153 ✓ — “install two new crosshead screws (923-11202) into the Taptic Engine connector cowling”

<details><summary>Trace</summary>

- Plan: route=documents — The question concerns iPhone repair and the indexed iPhone 16 Repair Manual covers screw reuse, so it should be answered from the documents.
- Standalone question: Can I reuse the old screws when I put an iPhone 16 back together?
- Tier 1 · RAG (dense): 6 chunks (iphone_16_repair_manual.pdf p. 73, 158, 169, 153, 56, 148) → judge: sufficient
- Reasoning: doc:676 directly answers the question: it says to never reinstall a screw after it has been removed, to install only new screws, and that iPhone screws are covered with an adhesive that can't be reused. The other sources (doc:767, doc:762, doc:778, doc:643, doc:757) describe reassembly steps that call for installing new screws (for example, 'install one new trilobe screw' and 'install two new crosshead screws') but do not add anything beyond what doc:676 states. Nothing in the evidence suggests an exception to the rule, so the question is fully answered.
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>

### rm_flex_cable_bend: How far may I bend back the flex cables when removing the USB-C connector from the iPhone 16?

Tier: hybrid

You may bend back the flex cables no more than 90 degrees. The removal procedure starts by lifting the ends of three flex cables off the logic board connectors [1], and the caution on the next page says not to bend the flex cables back more than 90 degrees while removing the logic board screws [2].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 199 ✓ — “Lift the ends of the three flex cables off the connectors on the logic board.”
- [2] iphone_16_repair_manual.pdf, p. 200 ✓ — “Caution: Donʼt bend back the flex cables more than 90 degrees.”

<details><summary>Trace</summary>

- Plan: route=documents — The question concerns the iPhone 16 repair procedure covered by the indexed repair manual, so it should be answered from the documents.
- Tier 1 · RAG (dense): 6 chunks (iphone_16_repair_manual.pdf p. 110, 206, 85, 199, 43, 104) → judge: insufficient — A maximum bend angle or bend distance, or a caution, for the USB-C connector flex cable(s) during removal of the USB-C connector on the iPhone 16.
- Reasoning: Source doc:812 (p. 199) introduces the USB-C connector removal and lists the prerequisite parts, and doc:819 (p. 206) says to lift the USB-C connector flex cable and peel it from the enclosure. Neither gives a bend limit. Doc:710 (p. 104) gives a 5-degree tilt limit, but it applies to tilting the back glass or display to protect flex cables during the earlier step, not to bending the flex cables during USB-C connector removal. Doc:688 and doc:611 cover alignment and reseating, not bend distance. Doc:718 covers disconnecting the battery and back glass flex cables, not the USB-C flex cables. No source states how far the USB-C flex cables may be bent back.
- Tier 2 · Hybrid (BM25+dense, reranked): 4 queries (How far may I bend back the flex cables when removing the USB-C connector from the iPhone 16? | iPhone 16 USB-C connector flex cable bend limit degrees removal | iPhone 16 repair manual USB-C connector caution do not bend flex cable | iPhone 16 USB-C connector flex cable bend radius replacement guide) → 12 chunks (iphone_16_repair_manual.pdf p. 199, 183, 209, 110, 206, 200, 186, 180, 108, 65, 29; iphone_user_guide.pdf p. 186) → judge: sufficient
- Reasoning: Doc:812 (p. 199) opens the USB-C Connector removal procedure and its step 1 says to lift the ends of the three flex cables off the logic board connectors. Doc:813 (p. 200) continues that procedure, with step 2 removing a trilobe screw from the logic board and step 3 a crosshead screw, and both steps carry the caution 'Donʼt bend back the flex cables more than 90 degrees.' Doc:819 (p. 206) and doc:822 (p. 209) cover later USB-C flex cable and connector steps, but neither gives a bend limit. Doc:799 (p. 186) has the same 90-degree caution, but it belongs to a different section, so it doesn't add to the USB-C answer. The answer is that the flex cables may be bent back no more than 90 degrees.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### rm_part_blue_torque_driver: What is the part number of the blue torque driver (0.65 kgf cm) in the iPhone 16 tools list?

Tier: rag

The part number of the blue torque driver (0.65 kgf cm) is **923-0448** [1]. In the parts list, the number appears before the tool name.

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 83 ✓ — “923-0448 Torque driver (blue, 0.65 kgf cm)”

<details><summary>Trace</summary>

- Plan: route=documents — The question asks about a specific tool listed in the iPhone 16 Repair Manual, which is one of the indexed documents.
- Tier 1 · RAG (dense): 6 chunks (iphone_16_repair_manual.pdf p. 199, 184, 160, 130, 83, 150) → judge: sufficient
- Reasoning: Source doc:685 (p. 83) is a parts list that gives the blue torque driver as "923-0448 Torque driver (blue, 0.65 kgf cm)". The part number is written before the tool name, so the number 923-0448 belongs to the blue 0.65 kgf cm driver. Source doc:737 (p. 130) confirms the same blue 0.65 kgf cm driver is used in the Top Speaker procedure, though it does not give the part number. The question is fully answered by doc:685.
- Generate: 1 citations
- Verify: 1/1 citations verified

</details>

### rm_part_grounding_spring_screw: What is the part number of the grounding spring screw for the iPhone 16?

Tier: hybrid

The grounding spring screw for the iPhone 16 is part number **923-11184**. The manual's grounding spring screws page states this directly [1], and the grounding spring replacement step confirms it by naming the new trilobe screw as 923-11184 [2].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 75 ✓ — “Grounding spring screw part number: 923-11184”
- [2] iphone_16_repair_manual.pdf, p. 175 ✓ — “install the new trilobe screw or screws (923-11184) into the grounding spring”

<details><summary>Trace</summary>

- Plan: route=documents — The question asks for a part number from the iPhone 16 Repair Manual, which is one of the indexed documents.
- Tier 1 · RAG (dense): 6 chunks (iphone_16_repair_manual.pdf p. 74, 68, 155, 158, 65, 78) → judge: insufficient — A source that explicitly names the part number of the grounding spring screw(s) for the iPhone 16, linking the 'Grounding spring screws' heading to a specific 923- number.
- Reasoning: doc:677 (p.74) has a heading 'Grounding spring screws' but no part number, so it confirms only that the section exists. doc:671 (p.68) lists grounding springs as 923-11702, 923-11703, 923-11704 and 10 grounding springs as 923-11184, but these are spring part numbers, not screw part numbers. The same parts list includes screw entries (923-11188, 923-11194, 923-11707, 923-11712) that are not labeled as grounding spring screws, so they cannot be matched to that heading without guessing. doc:767 (p.158) gives 923-11712 as the trilobe screw for the bottom speaker, and doc:764 (p.155) warns about grounding springs near the bottom speaker, but neither identifies 923-11712 as the grounding spring screw. doc:668 and doc:680 contain no relevant part information. No source directly states the grounding spring screw's part number.
- Tier 2 · Hybrid (BM25+dense, reranked): 4 queries (What is the part number of the grounding spring screw for the iPhone 16? | iPhone 16 grounding spring screws part number 923 | iPhone 16 grounding spring screw Apple self service repair parts list | iPhone 16 screw tray grounding spring screws trilobe part number) → 12 chunks (iphone_16_repair_manual.pdf p. 158, 155, 79, 68, 150, 175, 74, 75, 192, 123, 66, 121) → judge: sufficient
- Reasoning: doc:677 (p.74) is the heading 'Grounding spring screws' with no part number. doc:678 (p.75) states directly: 'Grounding spring screw part number: 923-11184', which answers the question. doc:787 (p.175) supports this: when replacing a grounding spring, it says to install 'the new trilobe screw or screws (923-11184) into the grounding spring.' doc:671 (p.68) also lists 923-11184 as '10 grounding springs' in the parts list, which is consistent with that number, though the listing is less clear. The other sources (doc:767, doc:764, doc:759, doc:805, doc:730, doc:728, doc:681, doc:669) either concern other components (bottom speaker, Taptic Engine, logic board, camera, security screws) or contain no grounding spring screw part number. doc:767's 923-11712 is the bottom speaker screw, not the grounding spring screw. Since doc:678 explicitly labels 923-11184 as the grounding spring screw part number, the question can be answered completely from the evidence without guessing.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### rm_adjustable_torque_range: What is the torque range of the adjustable torque driver used for screws outlined in black/green?

Tier: rag

The adjustable torque driver used for screws outlined in black/green has a torque range of **10–34 Ncm** [1]. The manual specifies this driver for those screws: "Use the adjustable torque driver (10–34 Ncm) for screws outlined in black/green" [1]. The same range is listed for the adjustable torque driver in the tool lists for other procedures [2].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 75 ✓ — “Use the adjustable torque driver (10–34 Ncm) for screws outlined in black/green.”
- [2] iphone_16_repair_manual.pdf, p. 150 ✓ — “Adjustable torque driver (10–34 Ncm)”

<details><summary>Trace</summary>

- Plan: route=documents — The question concerns the iPhone 16 repair manual, which is indexed, so it should be answered from the documents.
- Standalone question: What is the torque range of the adjustable torque driver used for screws outlined in black/green in the iPhone 16 Repair Manual?
- Tier 1 · RAG (dense): 6 chunks (iphone_16_repair_manual.pdf p. 83, 73, 150, 123, 199, 75) → judge: sufficient
- Reasoning: The question asks for the torque range of the adjustable torque driver used for screws outlined in black/green. Source doc:678 (p. 75) states directly: "Use the adjustable torque driver (10–34 Ncm) for screws outlined in black/green." That gives the exact range, so no guessing is needed. Source doc:730 and doc:759 also list the adjustable torque driver as 10–34 Ncm, which corroborates the figure but is not required. Source doc:685 lists fixed-value drivers in kgf cm and does not cover the adjustable driver. Source doc:676 is a general warning about torque drivers and adds nothing to the range. Every part of the question is answered by doc:678.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### know_usb: What does USB stand for?

Tier: knowledge

*Answered from the model's general knowledge; no documents or web sources were consulted.*

**USB** stands for **Universal Serial Bus**. It is a standard for connecting devices to computers and other electronics for data transfer, charging, and power.

<details><summary>Trace</summary>

- Plan: route=knowledge — This is a well-established general-knowledge definition not tied to the indexed Apple documents or time-sensitive.

</details>

### know_ram: What does RAM stand for in a computer?

Tier: knowledge

*Answered from the model's general knowledge; no documents or web sources were consulted.*

**RAM** stands for **Random Access Memory**. It is a computer's short-term working memory, which stores data and instructions that the processor is actively using. RAM is volatile, so its contents are lost when the power is turned off.

<details><summary>Trace</summary>

- Plan: route=knowledge — This is a well-established general-knowledge definition that is not tied to the indexed Apple documents and is not time-sensitive.

</details>

### know_boiling_point: At what temperature in Celsius does water boil at sea level?

Tier: knowledge

*Answered from the model's general knowledge; no documents or web sources were consulted.*

Water boils at **100 °C** (212 °F) at sea level, at standard atmospheric pressure of 1 atm.

<details><summary>Trace</summary>

- Plan: route=knowledge — This is a well-established physical fact that is not covered by the indexed Apple documents and is not time-sensitive.

</details>

### web_newest_iphone: What is the newest iPhone model Apple sells right now?

Tier: web

The evidence doesn't establish a single newest iPhone that Apple sells. Retailer listings name the **iPhone 18 Pro, iPhone 18 Pro Max, and iPhone Duo** as current models [1], and Flipkart describes them as the "latest series of iPhones" [2]. These listings come from third-party retailers, and Apple's own page only says it sells "the latest iPhone models" without naming any [3]. The evidence also doesn't say how the iPhone Duo ranks against the iPhone 18 Pro models, so I can't identify one newest model from it.

**Sources**
- [1] [Newest Apple iPhones: iPhone 18 Pro, 18 Pro Max & iPhone Duo - AT&T](https://www.att.com/buy/phones/browse/apple/) ✓ — “the iPhone 18 Pro, 18 Pro Max and iPhone Duo today”
- [2] [Apple iPhones Online at Best Prices in India - Flipkart](https://www.flipkart.com/mobiles/apple~brand/pr?sid=tyy,4io) ✓ — “Check the latest series of iPhones”
- [3] [Buy iPhone - Apple](https://www.apple.com/shop/buy-iphone) ✓ — “Shop the latest iPhone models and accessories.”

<details><summary>Trace</summary>

- Plan: route=documents — The question concerns iPhone models, which is the subject of the indexed Apple documents, and it is time-sensitive, so it should not be answered from general knowledge.
- Tier 1 · RAG (dense): 6 chunks (iphone_user_guide.pdf p. 10, 2; iphone_16_repair_manual.pdf p. 45, 36, 78, 214) → judge: insufficient — A current list of iPhone models Apple sells, with release dates or availability status, to identify the newest model on sale as of today (2026-11-06).
- Reasoning: The sources list many iPhone models (iPhone 16e, iPhone 17 models, iPhone Air, iPhone 17e, iPhone 18 Pro and Pro Max) and mention Apple's support pages, but none says which model is newest or which models Apple currently sells. Several of the sources are unrelated to availability, such as the screen-issue troubleshooting list and the page footers. The question asks about current sales, which the documents cannot establish, so the answer would require guessing.
- Tier 2 · Hybrid (BM25+dense, reranked): 4 queries (What is the newest iPhone model Apple sells right now? | Apple iPhone lineup currently available for purchase | newest iPhone model sold by Apple Store now | iPhone 18 Pro release date and availability) → 7 chunks (iphone_16_repair_manual.pdf p. 45, 23, 87, 53, 41, 58) → judge: insufficient — Current Apple sales lineup as of 2026-11-06, with release dates or availability status, to identify the newest iPhone model Apple sells.
- Reasoning: The sources name many models, including iPhone 18 Pro, iPhone 18 Pro Max, iPhone 17e, iPhone Air, and iPhone 16e, and some group them as "iPhone 18 models." None of them says which model is newest or which models Apple currently sells. The repair and troubleshooting passages only describe service procedures, and the user guide and page footers contain no sales or release information. Answering would require assuming that the model with the highest number is the newest one on sale, which the evidence does not establish.
- Tier 3 · Web: “Apple iPhone models available to buy today” → 5 chunks (https://www.att.com/buy/phones/browse/apple/; https://www.bestbuy.com/site/shop/apple-iphones; https://www.apple.com/shop/buy-iphone; https://www.flipkart.com/mobiles/apple~brand/pr?sid=tyy,4io; https://www.bestbuy.com/site/mobile-cell-phones/iphone/pcmcat305200050000.c?id=pcmcat305200050000/)
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>

### web_latest_ios: What is the latest public version of iOS available today?

Tier: web

The evidence indicates the latest public version is **iOS 27**. Apple has released it to the public [1], and it is available to download to iPhones now [2]. A WhistleOut guide also describes it as "iOS 27, the newest version of the iPhone's operating system" [3]. The evidence doesn't specify a point release number (such as 27.x) or confirm the exact date of this answer, so it can't rule out a later update.

**Sources**
- [1] [iOS 27 is available to download to your iPhone right now](https://appleinsider.com/articles/26/09/14/ios-27-is-now-available-with-big-changes-to-photos-and-siri) ✓ — “Apple has released iOS 27 to the public”
- [2] [iOS 27 is available to download to your iPhone right now](https://appleinsider.com/articles/26/09/14/ios-27-is-now-available-with-big-changes-to-photos-and-siri) ✓ — “iOS 27 is available to download to your iPhone right now”
- [3] [What Is the Current iOS Version for iPhones? | WhistleOut](https://www.whistleout.com/CellPhones/Guides/what-is-the-latest-version-of-ios) ✓ — “iOS 27, the newest version of the iPhone's operating system”

<details><summary>Trace</summary>

- Plan: route=web — This is time-sensitive, and the indexed iPhone guides cover iOS 8.4 and repair procedures, so they cannot answer which version is current today.
- Tier 3 · Web: “What is the latest public version of iOS available today?” → 5 chunks (https://www.whistleout.com/CellPhones/Guides/what-is-the-latest-version-of-ios; https://appleinsider.com/articles/26/09/14/ios-27-is-now-available-with-big-changes-to-photos-and-siri; https://www.yournavi.com/posts/latest-ios-version; https://osreleases.dev/)
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>

### web_apple_revenue: How much revenue did Apple report in its most recent quarterly earnings?

Tier: web

Apple reported **$114.5 billion** in revenue for its fiscal fourth quarter of 2026 [1]. That was a 12 percent increase year over year [2].

**Sources**
- [1] [Apple Reports Q4 2026 Revenue of $114.5 Billion - MacStories](https://www.macstories.net/news/apple-reports-q4-2026-revenue-of-114-5-billion/) ✓ — “Today, Apple reported its 2026 Q4 earnings, posting quarterly revenue of $114.5 billion.”
- [2] [Apple Hits Record $114.5 Billion Revenue In Q4 2026 Earnings](https://www.macobserver.com/news/apple-hits-record-114-5-billion-revenue-in-q4-2026-earnings/) ✓ — “Total revenue reached $114.48 billion, representing a 12 percent increase year over year.”

<details><summary>Trace</summary>

- Plan: route=web — This needs current financial data, which is time-sensitive and not in the indexed iPhone user guide or repair manual, whose matches are only copyright footers.
- Tier 3 · Web: “How much revenue did Apple report in its most recent quarterly earnings?” → 5 chunks (https://www.macstories.net/news/apple-reports-q4-2026-revenue-of-114-5-billion/; https://www.macrumors.com/2026/11/02/apple-4q-2026-earnings/; https://hypebeast.com/2026/11/apple-posts-record-114-5-billion-q4-revenue; https://www.macobserver.com/news/apple-hits-record-114-5-billion-revenue-in-q4-2026-earnings/)
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>
