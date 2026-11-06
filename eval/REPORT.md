# iPhone manuals: end-to-end eval

LLM backend: `cli:claude` (model `CLI default`). Passed **19/20**. Median latency 7.9 s.

| id | category | expected | tier | verified citations | page hit | keywords | s | result |
|---|---|---|---|---|---|---|---|---|
| ug_wifi | doc | rag/hybrid | rag | 3/3 | exact | 50% | 12.3 | PASS |
| ug_control_center | doc | rag/hybrid | rag | 2/2 | exact | 100% | 7.9 | PASS |
| ug_lost_iphone | doc | rag/hybrid | rag | 10/10 | exact | 33% | 15.3 | FAIL |
| ug_burst | doc | rag/hybrid | rag | 1/1 | exact | 100% | 5.0 | PASS |
| ug_screenshot | doc | rag/hybrid/web | rag | 2/2 | exact | 100% | 7.0 | PASS |
| ug_force_restart | doc | rag/hybrid/web | web | 4/4 | exact | 67% | 38.7 | PASS |
| rm_thermal_event | doc | rag/hybrid | hybrid | 4/4 | exact | 67% | 19.9 | PASS |
| rm_broken_glass | doc | rag/hybrid | rag | 3/3 | exact | 100% | 7.6 | PASS |
| rm_diagnostics_requirements | doc | rag/hybrid | rag | 7/7 | exact | 100% | 13.5 | PASS |
| rm_reuse_screws | doc | rag/hybrid | rag | 2/2 | exact | 100% | 4.9 | PASS |
| rm_flex_cable_bend | doc | rag/hybrid | hybrid | 3/3 | exact | 100% | 34.5 | PASS |
| rm_part_blue_torque_driver | hybrid | rag/hybrid | rag | 2/2 | exact | 50% | 6.8 | PASS |
| rm_part_grounding_spring_screw | hybrid | rag/hybrid | rag | 2/2 | exact | 100% | 6.7 | PASS |
| rm_adjustable_torque_range | hybrid | rag/hybrid | rag | 1/1 | exact | 100% | 7.4 | PASS |
| know_usb | knowledge | knowledge | knowledge | 0/0 | - | - | 1.6 | PASS |
| know_ram | knowledge | knowledge | knowledge | 0/0 | - | - | 1.6 | PASS |
| know_boiling_point | knowledge | knowledge | knowledge | 0/0 | - | - | 1.6 | PASS |
| web_newest_iphone | web | web | web | 3/3 | - | - | 17.4 | PASS |
| web_latest_ios | web | web | web | 3/3 | - | - | 15.8 | PASS |
| web_apple_revenue | web | web | web | 2/2 | - | - | 13.5 | PASS |

## Answers

### ug_wifi: How do I connect my iPhone to a Wi-Fi network?

Tier: rag

To connect your iPhone to a Wi-Fi network, go to **Settings > Wi-Fi** and turn Wi-Fi on [1]. Then tap one of the listed networks and enter the password if asked [1]. Once connected, **Wi-Fi** appears at the top of the screen [2].

If the network you want isn't listed (a closed network), tap **Other** and enter the network's name. You need to know the network name, security type, and password [3].

**Sources**
- [1] iphone_user_guide.pdf, p. 16 ✓ — “Go to Settings > Wi-Fi, then turn Wi-Fi on or off.”
- [2] iphone_user_guide.pdf, p. 16 ✓ — “If appears at the top of the screen, you’re connected to a Wi-Fi network.”
- [3] iphone_user_guide.pdf, p. 17 ✓ — “Tap Other, then enter the name of the closed network. You need to know the network name, security type, and password.”

<details><summary>Trace</summary>

- Plan: route=documents — This is a procedure for the documented iPhone, and the user guide has a Connect to Wi-Fi section.
- Tier 1 · RAG (dense): 11 chunks (iphone_user_guide.pdf p. 16, 17, 18, 40, 41, 20) → judge: sufficient
- Reasoning: Source [iphone_user_guide.pdf, p. 16] states the steps: go to Settings > Wi-Fi, turn Wi-Fi on, tap a listed network, and enter the password if asked. Source [iphone_user_guide.pdf, p. 17] adds how to join a closed network (Tap Other and enter the network name, security type, and password). Together these cover connecting to a Wi-Fi network completely.
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>

### ug_control_center: How do I open Control Center on my iPhone?

Tier: rag

To open Control Center, swipe up from the bottom edge of any screen, including the Lock screen. [1]

The same steps are also shown for accessibility: with VoiceOver on, select any item in the status bar, then swipe up with three fingers. [2]

**Sources**
- [1] iphone_user_guide.pdf, p. 35 ✓ — “Swipe up from the bottom edge of any screen (even the Lock screen).”
- [2] iphone_user_guide.pdf, p. 154 ✓ — “Select any item in the status bar, then swipe up with three fingers.”

<details><summary>Trace</summary>

- Plan: route=documents — This is a procedure for the documented iPhone, and the user guide's passages mention opening Control Center.
- Tier 1 · RAG (dense): 15 chunks (iphone_user_guide.pdf p. 35, 36, 154, 172, 173, 169, 41, 170) → judge: sufficient
- Reasoning: Source [iphone_user_guide.pdf, p. 35] states the answer directly: swipe up from the bottom edge of any screen, including the Lock screen. The question asks only how to open Control Center, and no part of it is left unanswered.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### ug_lost_iphone: I lost my iPhone, what can Find My iPhone do to help me?

Tier: rag

Find My iPhone can help you in these ways:

- **Locate and secure your phone:** You can use it from the free Find My iPhone app on another iOS device, or from a web browser at www.icloud.com/find [1].
- **Play a sound:** It can make your phone play a sound at full volume, even if the ringer is silenced [2].
- **Lost Mode:** It can immediately lock your phone with a passcode and display a contact number on the screen [3]. It also tracks and reports the phone's location [4].
- **Erase the phone:** You can erase all information and media on the phone to protect your privacy [5]. Note that erasing also removes Apple Pay payment ability.
- **Apple Pay:** Lost Mode suspends the use of your credit and debit cards for Apple Pay [6].
- **Activation Lock:** This is designed to stop anyone else from using your iPhone if you lose it [7].
- **Last known location:** If Send Last Location is turned on, the phone sends its last location before the battery runs out [8].

There are two requirements. Find My iPhone must be turned on before the phone is lost [9], and the phone must be able to connect to the Internet for you to locate and secure it [10].

The evidence does not cover other steps, such as contacting your carrier or reporting the loss.

**Sources**
- [1] iphone_user_guide.pdf, p. 46 ✓ — “Find My iPhone can help you locate and secure your iPhone”
- [2] iphone_user_guide.pdf, p. 46 ✓ — “Play a sound at full volume for two minutes, even if the ringer is set to silent.”
- [3] iphone_user_guide.pdf, p. 46 ✓ — “Immediately lock your missing iPhone with a passcode and send it a message displaying a contact number.”
- [4] iphone_user_guide.pdf, p. 46 ✓ — “iPhone tracks and reports its location”
- [5] iphone_user_guide.pdf, p. 46 ✓ — “Protect your privacy by erasing all the information and media on your iPhone”
- [6] iphone_user_guide.pdf, p. 46 ✓ — “Lost Mode also suspends the use of your credit and debit cards used for Apple Pay”
- [7] iphone_user_guide.pdf, p. 46 ✓ — “Find My iPhone includes Activation Lock, which is designed to prevent anyone else from using your iPhone if you ever lose it.”
- [8] iphone_user_guide.pdf, p. 46 ✓ — “iPhone sends its last location prior to the battery running out when Send Last Location in Settings is turned on.”
- [9] iphone_user_guide.pdf, p. 46 ✓ — “To use Find My iPhone features, Find My iPhone must be turned on before your iPhone is lost.”
- [10] iphone_user_guide.pdf, p. 46 ✓ — “iPhone must be able to connect to the Internet for you to locate and secure the device.”

<details><summary>Trace</summary>

- Plan: route=documents — The closest passages from the Apple iPhone User Guide describe the Find My iPhone features directly, so the documents likely contain the answer.
- Tier 1 · RAG (dense): 11 chunks (iphone_user_guide.pdf p. 46, 47, 18, 19, 191, 189) → judge: sufficient
- Reasoning: Sources [iphone_user_guide.pdf, p. 46] and [iphone_user_guide.pdf, p. 46] list what Find My iPhone can do: play a sound, Lost Mode with a passcode and contact message, and Erase iPhone, plus Activation Lock and location tracking ([iphone_user_guide.pdf, p. 46] notes it must be turned on beforehand and needs internet). The evidence covers the lost-phone features well, so the answer is substantially complete.
- Generate: 10 citations
- Verify: 10/10 citations verified

</details>

### ug_burst: How do I take burst photos with the iPhone camera?

Tier: rag

To take burst photos with the iPhone camera:

1. Make sure the camera is in Square or Photo mode, since burst shooting is available only in those modes [1].
2. Touch and hold the Take Picture button to take rapid-fire photos in a burst. The counter shows how many shots you have taken [1].
3. Lift your finger to stop the burst [1].
4. To see the suggested shots and choose which to keep, tap the thumbnail, then tap Select. Gray dots mark the suggested photos [1].
5. To save one photo from the burst as a separate photo in your Bursts album, tap the circle in its lower-right corner [1].

Burst shooting requires iPhone 5s or later [1].

**Sources**
- [1] iphone_user_guide.pdf, p. 94 ✓ — “Touch and hold the Take Picture button to take rapid-fire photos in bursts (available while in Square or Photo mode).”

<details><summary>Trace</summary>

- Plan: route=documents — The question asks for a documented iPhone camera procedure, and the user guide has a passage on taking burst shots.
- Tier 1 · RAG (dense): 9 chunks (iphone_user_guide.pdf p. 94, 95, 92, 96) → judge: sufficient
- Reasoning: Source [iphone_user_guide.pdf, p. 94] (p. 94) states the exact procedure: touch and hold the Take Picture button in Square or Photo mode to take rapid-fire burst photos, lift the finger to stop, then tap the thumbnail and Select to choose shots. It also covers copying a single photo out of the burst and deleting the burst. Nothing in the evidence is missing for the question of how to take burst photos.
- Generate: 1 citations
- Verify: 1/1 citations verified

</details>

### ug_screenshot: How do I take a screenshot of what is on my iPhone screen?

Tier: rag

To take a screenshot, simultaneously press and release the Sleep/Wake and Home buttons [1]. The screenshot is then added to the Photos tab in Photos and can also be viewed in the Camera Roll album or All Photos album (if you're using iCloud Photo Library) [2].

**Sources**
- [1] iphone_user_guide.pdf, p. 96 ✓ — “Simultaneously press and release the Sleep/ Wake and Home buttons.”
- [2] iphone_user_guide.pdf, p. 96 ✓ — “The screenshot is added to the Photos tab in Photos and can also be viewed in the Camera Roll album or All Photos album”

<details><summary>Trace</summary>

- Plan: route=documents — This is a documented iPhone procedure, and the iPhone user guide likely covers it.
- Tier 1 · RAG (dense): 15 chunks (iphone_user_guide.pdf p. 93, 94, 96, 170; iphone_16_repair_manual.pdf p. 40, 41, 46) → judge: sufficient
- Reasoning: Source [iphone_user_guide.pdf, p. 170] (iphone_user_guide.pdf, p. 170) states that pressing the Home and Sleep/Wake buttons simultaneously takes a screenshot, and [iphone_user_guide.pdf, p. 96] (p. 96) gives the same button combination and says the screenshot is saved to Photos. Together these fully answer how to take a screenshot. The question has no remaining part that the evidence leaves unanswered.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### ug_force_restart: How do I force restart my iPhone when it will not turn off?

Tier: web

To force restart an iPhone 16, press and quickly release Volume Up, then press and quickly release Volume Down, then press and hold the Side button until the Apple logo appears [1]. Keep holding the Side button until the logo shows, which usually takes about 10 seconds [2]. This method is also reported to work on iPhone 8 through iPhone 17 running iOS 26 [4].

If your iPhone has a Home button, the user guide instead says to hold the Sleep/Wake button and the Home button together for at least ten seconds, until the Apple logo appears [3].

The evidence does not say which iPhone model you have, so check which of these two methods matches your device.

**Sources**
- [1] [How To Restart iPhone 16 — Easy Step-By-Step Guide!](https://thetechgorilla.com/how-to-restart-iphone-16/) ✓ — “For a force restart on a frozen iPhone 16, press Volume Up, then Volume Down, then hold the Side button until the Apple logo appears.”
- [2] [How To Restart iPhone 16 — Easy Step-By-Step Guide!](https://thetechgorilla.com/how-to-restart-iphone-16/) ✓ — “Finally, press and hold the Side button until the Apple logo appears — usually about 10 seconds.”
- [3] iphone_user_guide.pdf, p. 187 ✓ — “Hold down the Sleep/Wake button and the Home button at the same time for at least ten seconds, until the Apple logo appears.”
- [4] [How to Fix Unresponsive iPhone When Nothing Works (2026)](https://www.appleheadlines.com/how-to-fix-unresponsive-iphone/) ✓ — “This force restart works on every iPhone 8 through iPhone 17 running iOS 26”

<details><summary>Trace</summary>

- Plan: route=documents — The closest passage in the user guide covers forcing restart and turning off the iPhone, so the documents likely contain the procedure.
- Tier 1 · RAG (dense): 12 chunks (iphone_user_guide.pdf p. 187, 188, 186, 35, 12; iphone_16_repair_manual.pdf p. 37, 38, 39, 28) → judge: insufficient — Force-restart steps for iPhone models without a Home button, which the user's model may need. → next: documents ['force restart iPhone without Home button volume up volume down side button'], web []
- Reasoning: [iphone_user_guide.pdf, p. 187] directly answers the question for iPhones with a Home button: hold the Sleep/Wake and Home buttons together for at least ten seconds until the Apple logo appears. [iphone_user_guide.pdf, p. 186] and [iphone_user_guide.pdf, p. 187] cover the normal restart, and [iphone_user_guide.pdf, p. 187] notes a reset is only for when restart fails. No source gives the force-restart steps for iPhones without a Home button, such as the iPhone 16 in [iphone_16_repair_manual.pdf, p. 37] to [iphone_16_repair_manual.pdf, p. 38], so the answer depends on the user's model.
- Tier 2 · Hybrid (BM25+dense, reranked): 2 queries (How do I force restart my iPhone when it will not turn off? | force restart iPhone without Home button volume up volume down side button) → 16 chunks (iphone_user_guide.pdf p. 187, 188, 186, 35, 170, 12; iphone_16_repair_manual.pdf p. 63, 64, 65, 59, 12, 37) → judge: insufficient — Force-restart button sequence for iPhone models without a Home button. → next: documents ['force restart iPhone 16 press volume up then volume down hold side button until Apple logo appears'], web []
- Reasoning: [iphone_user_guide.pdf, p. 187] gives the force-restart steps for iPhones with a Home button: hold Sleep/Wake and Home together for at least ten seconds until the Apple logo appears. [iphone_user_guide.pdf, p. 186] covers a normal restart, and [iphone_16_repair_manual.pdf, p. 63], [iphone_16_repair_manual.pdf, p. 12], and [iphone_16_repair_manual.pdf, p. 59] tell the reader to force restart but don't say how. No source gives the force-restart steps for iPhones without a Home button, such as the iPhone 16 these repair manual pages cover, so the answer depends on the user's model.
- Tier 3 · Web: “force restart iPhone 16 press volume up then volume down hold side button until Apple logo appears” → 5 chunks (https://thetechgorilla.com/how-to-restart-iphone-16/; https://www.appleheadlines.com/how-to-fix-unresponsive-iphone/; https://www.appleheadlines.com/force-restart-iphone/)
- Generate: 4 citations
- Verify: 4/4 citations verified

</details>

### rm_thermal_event: What should I do if the battery starts smoking or has a thermal event while I am repairing an iPhone?

Tier: hybrid

If the battery starts smoking or has a thermal event during an iPhone repair, the manual says to act immediately by smothering the battery or device with sand. [1] Dump all the sand at once, because speed matters for containing the reaction. [1] Contact local fire authorities if further help is needed. [1] Leave the room for 30 minutes after the reaction is contained, ventilate the area, and do not return until it is clear of smoke. [1] Wait 30 minutes before touching the device, then wear heat-resistant gloves and safety glasses with side shields to remove it from the sand. [1] Afterward, wipe the affected area with water first, then with an ESD-safe cleaning solution, and dispose of the damaged battery and any debris according to local environmental laws. [2] Before any repair, the manual also recommends setting up a workspace with sand within reach and adequate ventilation. [3] Signs that call for these steps include the battery beginning to smoke or emit sparks or soot, the pouch suddenly puffing out, or hissing or popping sounds; in those cases, disconnect all external cables and remove cases and covers. [4]

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do smother the battery or device immediately with plenty of clean, dry sand. Dump the sand all at once.”
- [2] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do wipe the affected area with water first. Then wipe the area with an ESD-safe cleaning solution. Do dispose of the damaged battery or device”
- [3] iphone_16_repair_manual.pdf, p. 4 ✓ — “Sand container within reach (2 feet) on both sides of the workspace, not above the workspace Adequate ventilation”
- [4] iphone_16_repair_manual.pdf, p. 5 ✓ — “The lithium-ion battery or a device that contains one begins to smoke or emit sparks or soot. The battery pouch suddenly and quickly puffs out.”

<details><summary>Trace</summary>

- Plan: route=documents — The repair manual's closest passage covers a battery emitting hissing or popping sounds and the steps to take during repair.
- Tier 1 · RAG (dense): 14 chunks (iphone_16_repair_manual.pdf p. 28, 29, 85, 86, 87, 5, 6, 7, 4) → judge: insufficient — Immediate response to visible smoke or a thermal event: evacuation, ventilation, emergency contact, and what extinguishing method to use or avoid. → next: documents ['battery emits smoke or fire during repair evacuate ventilate workspace', 'battery thermal event fire extinguisher emergency services lithium-ion'], web []
- Reasoning: [iphone_16_repair_manual.pdf, p. 5] says that if a battery or device starts hissing or popping, the user should disconnect external cables, remove cases and covers, and wait for the device to turn off. [iphone_16_repair_manual.pdf, p. 4] and [iphone_16_repair_manual.pdf, p. 6] warn that mishandling can cause a thermal event or fire and say not to puncture, crush, or overheat the battery. No source says what to do when smoke appears, such as evacuating, ventilating, calling emergency services, or the extinguishing method, so that part is unanswered.
- Tier 2 · Hybrid (BM25+dense, reranked): 3 queries (What should I do if the battery starts smoking or has a thermal event while I am repairing an iPhone? | battery emits smoke or fire during repair evacuate ventilate workspace | battery thermal event fire extinguisher emergency services lithium-ion) → 16 chunks (iphone_16_repair_manual.pdf p. 5, 6, 4, 7, 85, 87, 143, 118, 28; iphone_user_guide.pdf p. 183) → judge: sufficient
- Reasoning: [iphone_16_repair_manual.pdf, p. 5] lists the thermal-event signs and says to smother the device immediately with dry sand, contact fire authorities if needed, leave the room for 30 minutes, ventilate, and wait 30 minutes before touching the device. [iphone_16_repair_manual.pdf, p. 5] adds that the affected area should be wiped with water and then an ESD-safe cleaning solution, and that the damaged battery must be disposed of per local law. [iphone_16_repair_manual.pdf, p. 5] and [iphone_16_repair_manual.pdf, p. 5] also cover the smoke, sparks, and puffing signs and the immediate steps to disconnect cables and remove cases. Together these answer the question, so no further search is needed.
- Generate: 4 citations
- Verify: 4/4 citations verified

</details>

### rm_broken_glass: What protective gear do I need before repairing an iPhone with a broken display glass?

Tier: rag

Before repairing an iPhone with broken display glass, put on **safety glasses with side shields** and **cut-resistant gloves** [1]. Then use an **ESD-safe vacuum cleaner** to remove glass pieces from your workspace and the iPhone [2]. Finally, attach a **display protective cover** to the broken glass to prevent injury or scattering of glass [3].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 7 ✓ — “Put on safety glasses with side shields and the cut-resistant gloves.”
- [2] iphone_16_repair_manual.pdf, p. 7 ✓ — “Use an ESD-safe vacuum cleaner to remove glass pieces from your workspace and the iPhone.”
- [3] iphone_16_repair_manual.pdf, p. 7 ✓ — “Attach a protective cover to the broken glass to prevent injury or scattering of glass.”

<details><summary>Trace</summary>

- Plan: route=documents — This is specific to the documented iPhone 16 repair procedure, and the manual's broken glass safety section likely lists the protective gear.
- Tier 1 · RAG (dense): 15 chunks (iphone_16_repair_manual.pdf p. 7, 8, 10, 170, 171, 107, 108, 118, 48, 1) → judge: sufficient
- Reasoning: Source 524 lists the protective gear for a broken display glass: cut-resistant gloves and safety glasses with side shields, plus an ESD-safe vacuum and a protective cover. Source 524 also says to put these on before starting, and source 525 adds the cover-application steps. Every part of the question is answered directly, so no further search is needed.
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>

### rm_diagnostics_requirements: What do I need to run Apple Diagnostics for Self Service Repair on an iPhone?

Tier: rag

To run Apple Diagnostics for Self Service Repair on an iPhone, you need:

- An iPhone 12 or later that can turn on and start up in iOS [1].
- iOS 17 or later. Beta versions aren't supported [2].
- A secondary device to access the Apple Diagnostics for Self Service Repair website and diagnostic console, such as an iPhone or iPad running iOS 13 or later or iPadOS 13 or later with Safari [3], a Mac running macOS Catalina 10.15 or later with Safari, or a PC with Chrome 55 or later, Firefox 59 or later, or Microsoft Edge 12 or later [4].
- A Wi-Fi connection on the device being tested [5]. That device supports only Wi-Fi in diagnostics mode, not cellular [5].
- A Wi-Fi, cellular, or wired internet connection on the secondary device [6].

To put the iPhone into diagnostics mode, the evidence says to plug it into a 20W or higher power adapter [7].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 21 ✓ — “An iPhone 12 or later to be tested that can turn on and start up in iOS.”
- [2] iphone_16_repair_manual.pdf, p. 21 ✓ — “The device youʼre testing must have iOS 17 or iPadOS 17 or later to run Apple Diagnostics for Self Service Repair on a web browser.”
- [3] iphone_16_repair_manual.pdf, p. 22 ✓ — “An iPhone running iOS 13 or later or iPad running iPadOS 13 or later with Safari”
- [4] iphone_16_repair_manual.pdf, p. 22 ✓ — “A PC with Chrome 55 or later, Firefox 59 or later, or Microsoft Edge 12 or later”
- [5] iphone_16_repair_manual.pdf, p. 22 ✓ — “A Wi-Fi connection on the device to be tested”
- [6] iphone_16_repair_manual.pdf, p. 22 ✓ — “A Wi-Fi, cellular, or wired internet connection on the secondary device”
- [7] iphone_16_repair_manual.pdf, p. 18 ✓ — “plug the device into a 20W or higher power adapter”

<details><summary>Trace</summary>

- Plan: route=documents — The question asks for specific requirements from the indexed iPhone 16 Repair Manual, and the closest passage on page 21 lists them.
- Tier 1 · RAG (dense): 10 chunks (iphone_16_repair_manual.pdf p. 21, 22, 16, 17, 18) → judge: sufficient
- Reasoning: Source 546 lists the device requirements: an iPhone 12 or later that can start up in iOS, with iOS 17 or later for the web version. Source 547 adds a secondary device such as a Mac, PC, iPad, or iPhone with internet access, and source 548 lists supported secondary devices and browsers along with the Wi-Fi requirement. Sources 548 and 549 also cover the setup steps, including unplugging accessories, removing cases, and recording the serial number. The evidence covers the requirements fully, so nothing else is missing.
- Generate: 7 citations
- Verify: 7/7 citations verified

</details>

### rm_reuse_screws: Can I reuse the old screws when I put an iPhone back together?

Tier: rag

No. The manual says you should never reinstall a screw after it has been removed, and you should install only new screws [1]. The reason given is that iPhone screws are covered with an adhesive that can't be reused [1]. Screw trays included with new parts provide all the new screws needed for each repair [2].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 73 ✓ — “Never reinstall a screw after it has been removed. Install only new screws. iPhone screws are covered with an adhesive that canʼt be reused.”
- [2] iphone_16_repair_manual.pdf, p. 76 ✓ — “Screw trays include all the new screws needed for each repair.”

<details><summary>Trace</summary>

- Plan: route=documents — The question is about a specific repair procedure, and the repair manual passages directly address reusing screws.
- Standalone question: Can I reuse the old screws when I put an iPhone 16 back together?
- Tier 1 · RAG (dense): 15 chunks (iphone_16_repair_manual.pdf p. 73, 74, 75, 76, 158, 159, 160, 161, 169, 170, 171, 153, 56, 148) → judge: sufficient
- Reasoning: Source [iphone_16_repair_manual.pdf, p. 73] states that iPhone screws are covered with an adhesive that can't be reused, and that you should never reinstall a screw after removal and install only new screws. [iphone_16_repair_manual.pdf, p. 76] repeats that new screws must be installed and that screw trays include all the new screws needed for each repair. Together these directly answer that you should not reuse the old screws.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### rm_flex_cable_bend: How far may I bend back the flex cables when removing the USB-C connector from the iPhone 16?

Tier: hybrid

The manual says not to bend the flex cables back more than 90 degrees [1][2]. This caution appears in the earlier steps for removing the logic board and SIM assembly screws, which come before the USB-C connector is removed [1][2]. The final removal step only says to lift the flex cable and peel it from the enclosure [3], so the evidence gives no separate limit for that step.

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 200 ✓ — “Donʼt bend back the flex cables more than 90 degrees.”
- [2] iphone_16_repair_manual.pdf, p. 201 ✓ — “Donʼt bend back the flex cables more than 90 degrees.”
- [3] iphone_16_repair_manual.pdf, p. 206 ✓ — “Lift the end of the USB-C connector flex cable as shown and peel the flex cable from the enclosure.”

<details><summary>Trace</summary>

- Plan: route=documents — This asks for a specific repair value from the iPhone 16 repair manual, which the indexed documents are likely to contain.
- Tier 1 · RAG (dense): 15 chunks (iphone_16_repair_manual.pdf p. 110, 111, 112, 113, 206, 207, 208, 209, 85, 86, 87, 199, 43, 104) → judge: insufficient — A maximum bend or lift angle for the USB-C connector flex cables during removal. → next: documents ['USB-C connector flex cable bend degrees removal caution', 'avoid damaging flex cables do not bend more than degrees USB-C connector iPhone 16', 'lift USB-C connector flex cable angle damage caution'], web []
- Reasoning: Source 819 says to lift the USB-C flex cable and peel it from the enclosure, and source 710 gives a 5-degree limit only for tilting the back glass or display. No source gives a bend limit for the USB-C flex cables, so the question is not answered.
- Tier 2 · Hybrid (BM25+dense, reranked): 4 queries (How far may I bend back the flex cables when removing the USB-C connector from the iPhone 16? | USB-C connector flex cable bend degrees removal caution | avoid damaging flex cables do not bend more than degrees USB-C connector iPhone 16 | lift USB-C connector flex cable angle damage caution) → 16 chunks (iphone_16_repair_manual.pdf p. 206, 207, 208, 186, 187, 188, 189, 200, 201, 203, 209, 125, 202, 210, 205; iphone_user_guide.pdf p. 186) → judge: sufficient
- Reasoning: Source 813 (p. 200) and source 814 (p. 201) sit inside the iPhone 16 USB-C connector removal procedure and both warn not to bend back the flex cables more than 90 degrees. Source 799 and 800 repeat the same 90-degree limit for the logic board and SIM steps, and the other sources give no limit.
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>

### rm_part_blue_torque_driver: What is the part number of the blue torque driver (0.65 kgf cm) in the iPhone 16 tools list?

Tier: rag

The part number of the blue torque driver (0.65 kgf cm) is **923-0448** [1].

This item appears in the iPhone 16 tools list on page 83 of the repair manual, and the blue 0.65 kgf cm driver is also listed as a tool for the top speaker procedure [2].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 83 ✓ — “923-0448 Torque driver (blue, 0.65 kgf cm)”
- [2] iphone_16_repair_manual.pdf, p. 130 ✓ — “3. Torque driver (blue, 0.65 kgf cm)”

<details><summary>Trace</summary>

- Plan: route=documents — The part number is a specific document detail, and the iPhone 16 repair manual's tools list likely contains it.
- Tier 1 · RAG (dense): 15 chunks (iphone_16_repair_manual.pdf p. 199, 200, 201, 202, 184, 185, 186, 187, 160, 161, 162, 163, 130, 83, 150) → judge: sufficient
- Reasoning: Source [iphone_16_repair_manual.pdf, p. 83] (p. 83) lists "923-0448 Torque driver (blue, 0.65 kgf cm)" in the tools list, giving the part number directly. [iphone_16_repair_manual.pdf, p. 130] (p. 130) confirms the blue 0.65 kgf cm driver is a tool used in the iPhone 16 top speaker procedure. The question has no unanswered parts.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### rm_part_grounding_spring_screw: What is the part number of the grounding spring screw for the iPhone 16?

Tier: rag

The part number of the grounding spring screw for the iPhone 16 is **923-11184** [1].

The same number is listed under grounding springs in the parts list, which gives 10 grounding springs with part number 923-11184 [2].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 75 ✓ — “Grounding spring screw part number: 923-11184”
- [2] iphone_16_repair_manual.pdf, p. 68 ✓ — “10 grounding springs 923-11184”

<details><summary>Trace</summary>

- Plan: route=documents — The closest passages mention grounding spring screws and part numbers in the iPhone 16 repair manual, so the answer is likely there.
- Tier 1 · RAG (dense): 13 chunks (iphone_16_repair_manual.pdf p. 74, 75, 76, 68, 69, 70, 71, 155, 156, 157, 158, 65, 78) → judge: sufficient
- Reasoning: Source [iphone_16_repair_manual.pdf, p. 75] states directly: "Grounding spring screw part number: 923-11184". Source [iphone_16_repair_manual.pdf, p. 68] lists the same number under grounding springs, which confirms it. Nothing else is needed to answer the question.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### rm_adjustable_torque_range: What is the torque range of the adjustable torque driver used for screws outlined in black/green?

Tier: rag

The adjustable torque driver used for screws outlined in black/green has a torque range of **10–34 Ncm** [1].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 75 ✓ — “Use the adjustable torque driver (10–34 Ncm) for screws outlined in black/green.”

<details><summary>Trace</summary>

- Plan: route=documents — The closest passage on page 75 states the adjustable torque driver (10–34 Ncm) is used for screws outlined in black/green, so the manual likely answers this.
- Standalone question: What is the torque range of the adjustable torque driver used for screws outlined in black/green in the iPhone 16 Repair Manual?
- Tier 1 · RAG (dense): 14 chunks (iphone_16_repair_manual.pdf p. 83, 84, 85, 73, 74, 76, 150, 151, 152, 153, 123, 199, 75) → judge: sufficient
- Reasoning: Source [iphone_16_repair_manual.pdf, p. 75] says the adjustable torque driver (10–34 Ncm) is used for screws outlined in black/green, which gives the torque range directly. Sources [iphone_16_repair_manual.pdf, p. 151] and [iphone_16_repair_manual.pdf, p. 152] also show the same adjustable driver set to 10 Ncm, consistent with that range. No source is needed beyond this to answer the question.
- Generate: 1 citations
- Verify: 1/1 citations verified

</details>

### know_usb: What does USB stand for?

Tier: knowledge

*Answered from the model's general knowledge; no documents or web sources were consulted.*

USB stands for **Universal Serial Bus**.

<details><summary>Trace</summary>

- Plan: route=knowledge — USB stands for Universal Serial Bus, a well-established fact that does not depend on the documents.

</details>

### know_ram: What does RAM stand for in a computer?

Tier: knowledge

*Answered from the model's general knowledge; no documents or web sources were consulted.*

RAM stands for **Random Access Memory**. It is the computer's short-term working memory, where data and programs in active use are stored so the processor can reach them quickly.

<details><summary>Trace</summary>

- Plan: route=knowledge — RAM stands for Random Access Memory, a well-established general computing definition not specific to the documents.

</details>

### know_boiling_point: At what temperature in Celsius does water boil at sea level?

Tier: knowledge

*Answered from the model's general knowledge; no documents or web sources were consulted.*

Water boils at **100 °C** (212 °F) at sea level, under standard atmospheric pressure.

<details><summary>Trace</summary>

- Plan: route=knowledge — Water boils at 100 °C at standard sea-level pressure, a reliable physical fact unrelated to the documents.

</details>

### web_newest_iphone: What is the newest iPhone model Apple sells right now?

Tier: web

The newest iPhone Apple sells is the **iPhone 17 series**, which Apple introduced in September 2025 [1]. The lineup has four models: iPhone 17, iPhone Air, iPhone 17 Pro, and iPhone 17 Pro Max [2]. Apple also continues selling the iPhone 16 and iPhone 16e as lower-cost alternatives [3].

**Sources**
- [1] [What is the Latest iPhone? A Complete Guide to Apple’s iPhone 17 Lineup in 2026](https://www.macobserver.com/tips/round-ups/what-is-the-latest-iphone/) ✓ — “the answer is the iPhone 17 series , which Apple introduced in September 2025.”
- [2] [What is the Latest iPhone? A Complete Guide to Apple’s iPhone 17 Lineup in 2026](https://www.macobserver.com/tips/round-ups/what-is-the-latest-iphone/) ✓ — “The lineup includes four models: iPhone 17 , iPhone Air , iPhone 17 Pro , and iPhone 17 Pro Max .”
- [3] [What is the Latest iPhone? A Complete Guide to Apple’s iPhone 17 Lineup in 2026](https://www.macobserver.com/tips/round-ups/what-is-the-latest-iphone/) ✓ — “Apple also continues selling the iPhone 16 and iPhone 16e as lower-cost alternatives.”

<details><summary>Trace</summary>

- Plan: route=web — Which iPhone Apple currently sells is time-sensitive and the manuals may be out of date, so it needs a web search.
- Tier 3 · Web: “What is the newest iPhone model Apple sells right now?” → 5 chunks (https://www.macobserver.com/tips/round-ups/what-is-the-latest-iphone/; https://toolrom.com/what-iphone-is-current/)
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>

### web_latest_ios: What is the latest public version of iOS available today?

Tier: web

The latest public release of iOS is **iOS 27.2**, released on October 26, 2026 [1]. It belongs to the iOS 27 line, which became publicly available on September 14, 2026 [2]. A 27.3 beta is in testing, but beta builds are not final public releases [3].

**Sources**
- [1] [iOS 27 - Wikipedia](https://en.wikipedia.org/wiki/IOS_27) ✓ — “Latest release 27.2 [ 1 ] (October 26, 2026”
- [2] [iOS 27 - Wikipedia](https://en.wikipedia.org/wiki/IOS_27) ✓ — “became publicly available on September 14, 2026.”
- [3] [iOS 27 is available to download to your iPhone right now](https://appleinsider.com/articles/26/09/14/ios-27-is-now-available-with-big-changes-to-photos-and-siri) ✓ — “First public betas for iOS 27.3, iPadOS 27.3, and macOS 27.3 are available”

<details><summary>Trace</summary>

- Plan: route=web — The latest public iOS release changes over time and is not in the manuals, so it needs a web search.
- Tier 3 · Web: “What is the latest public version of iOS available today?” → 5 chunks (https://en.wikipedia.org/wiki/IOS_27; https://www.whistleout.com/CellPhones/Guides/what-is-the-latest-version-of-ios; https://appleinsider.com/articles/26/09/14/ios-27-is-now-available-with-big-changes-to-photos-and-siri)
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>

### web_apple_revenue: How much revenue did Apple report in its most recent quarterly earnings?

Tier: web

Apple's most recent quarterly earnings were for fiscal Q4 2026, which it reported on November 2, and posted revenue of **$114.5 billion** [1][2].

**Sources**
- [1] [Apple Reports Q4 2026 Revenue of $114.5 Billion - MacStories](https://www.macstories.net/news/apple-reports-q4-2026-revenue-of-114-5-billion/) ✓ — “Today, Apple reported its 2026 Q4 earnings, posting quarterly revenue of $114.5 billion.”
- [2] [Apple Reports 4Q 2026 Results: $30.7B Profit on $114.5B Revenue](https://www.macrumors.com/2026/11/02/apple-4q-2026-earnings/) ✓ — “For the quarter, Apple posted revenue of $114.5 billion”

<details><summary>Trace</summary>

- Plan: route=web — Apple's latest quarterly revenue is time-sensitive financial information that the iPhone manuals do not contain.
- Tier 3 · Web: “How much revenue did Apple report in its most recent quarterly earnings?” → 5 chunks (https://www.macstories.net/news/apple-reports-q3-2026-earnings/; https://www.macstories.net/news/apple-reports-q4-2026-revenue-of-114-5-billion/; https://www.apple.com/newsroom/2026/01/apple-reports-first-quarter-results/; https://9to5mac.com/2026/11/02/apple-reports-q4-2026-earnings/; https://www.macrumors.com/2026/11/02/apple-4q-2026-earnings/)
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>
