# iPhone manuals: end-to-end eval (ladder mode)

LLM backend: `cli:claude` (model `CLI default`). Passed **20/20**. Median latency 7.6 s.

| id | category | expected | tier | verified citations | page hit | keywords | s | result |
|---|---|---|---|---|---|---|---|---|
| ug_wifi | doc | rag/hybrid | rag | 2/2 | exact | 50% | 13.8 | PASS |
| ug_control_center | doc | rag/hybrid | rag | 1/1 | exact | 100% | 3.4 | PASS |
| ug_lost_iphone | doc | rag/hybrid | rag | 3/3 | exact | 100% | 7.2 | PASS |
| ug_burst | doc | rag/hybrid | rag | 1/1 | exact | 100% | 3.5 | PASS |
| ug_screenshot | doc | rag/hybrid/web | rag | 2/2 | exact | 100% | 7.8 | PASS |
| ug_force_restart | doc | rag/hybrid/web | rag | 2/2 | exact | 67% | 4.8 | PASS |
| rm_thermal_event | doc | rag/hybrid | hybrid | 8/8 | exact | 100% | 34.0 | PASS |
| rm_broken_glass | doc | rag/hybrid | rag | 1/1 | exact | 67% | 8.5 | PASS |
| rm_diagnostics_requirements | doc | rag/hybrid | rag | 3/3 | exact | 100% | 4.4 | PASS |
| rm_reuse_screws | doc | rag/hybrid | rag | 2/2 | exact | 100% | 8.8 | PASS |
| rm_flex_cable_bend | doc | rag/hybrid | hybrid | 1/1 | exact | 100% | 14.2 | PASS |
| rm_part_blue_torque_driver | hybrid | rag/hybrid | rag | 1/1 | exact | 50% | 7.6 | PASS |
| rm_part_grounding_spring_screw | hybrid | rag/hybrid | rag | 1/1 | exact | 100% | 3.9 | PASS |
| rm_adjustable_torque_range | hybrid | rag/hybrid | rag | 1/1 | exact | 100% | 6.9 | PASS |
| know_usb | knowledge | knowledge | knowledge | 0/0 | - | - | 1.5 | PASS |
| know_ram | knowledge | knowledge | knowledge | 0/0 | - | - | 1.7 | PASS |
| know_boiling_point | knowledge | knowledge | knowledge | 0/0 | - | - | 4.3 | PASS |
| web_newest_iphone | web | web | web | 3/3 | - | - | 12.4 | PASS |
| web_latest_ios | web | web | web | 3/3 | - | - | 21.5 | PASS |
| web_apple_revenue | web | web | web | 2/2 | - | - | 10.8 | PASS |

## Answers

### ug_wifi: How do I connect my iPhone to a Wi-Fi network?

Tier: rag

1. Open **Settings > Wi-Fi** and turn Wi-Fi on. You can also turn it on or off in Control Center [1].
2. Tap one of the listed networks, then enter its password if asked [1].

To join a hidden network, tap **Other** and enter the network name. You need the network name, security type, and password [2].

When connected, **Wi-Fi** appears at the top of the screen [1].

**Sources**
- [1] iphone_user_guide.pdf, p. 16 ✓ — “Go to Settings > Wi-Fi, then turn Wi-Fi on or off. (You can also turn Wi-Fi on or off in Control Center.)”
- [2] iphone_user_guide.pdf, p. 17 ✓ — “Join a closed Wi-Fi network: Tap Other, then enter the name of the closed network.”

<details><summary>Trace</summary>

- Plan: route=documents — This is a procedure specific to the documented iPhone, and the user guide passages cover Wi-Fi connection.
- Tier 1 · RAG (dense): 11 chunks (iphone_user_guide.pdf p. 16, 17, 18, 40, 41, 20) → judge: sufficient
- Reasoning: Source [iphone_user_guide.pdf, p. 16] states the steps: go to Settings > Wi-Fi, turn Wi-Fi on, then tap one of the listed networks and enter the password if asked. Source [iphone_user_guide.pdf, p. 17] adds that tapping Other lets you join a closed network, which needs its name, security type, and password. The question asks how to connect, and [iphone_user_guide.pdf, p. 16] answers the core procedure completely.
- Generate (with the judge): 2 citations
- Verify: 2/2 citations verified

</details>

### ug_control_center: How do I open Control Center on my iPhone?

Tier: rag

Swipe up from the bottom edge of any screen, even the Lock screen, to open Control Center [1].

Control Center gives quick access to the camera, calculator, AirPlay, audio playback controls, and other features such as brightness and AirDrop [1].

**Sources**
- [1] iphone_user_guide.pdf, p. 35 ✓ — “Open Control Center. Swipe up from the bottom edge of any screen (even the Lock screen).”

<details><summary>Trace</summary>

- Plan: route=documents — The question is a procedure for the documented iPhone, and the user guide has a passage describing how to open Control Center.
- Tier 1 · RAG (dense): 15 chunks (iphone_user_guide.pdf p. 35, 36, 154, 172, 173, 169, 41, 170) → judge: sufficient
- Reasoning: Source [iphone_user_guide.pdf, p. 35] directly states the procedure: swipe up from the bottom edge of any screen, even the Lock screen, to open Control Center. [iphone_user_guide.pdf, p. 35] also explains what Control Center provides. The question asks only how to open it, and [iphone_user_guide.pdf, p. 35] answers that completely.
- Generate (with the judge): 1 citations
- Verify: 1/1 citations verified

</details>

### ug_lost_iphone: I lost my iPhone, what can Find My iPhone do to help me?

Tier: rag

Find My iPhone can help you locate and secure a lost iPhone in several ways:

- **Locate it on a map:** You can see where your iPhone is using the Find My iPhone app on another iOS device or at www.icloud.com/find [1].
- **Play a sound:** It plays a sound at full volume for two minutes, even if the ringer is set to silent [2].
- **Lost Mode:** It locks the phone with a passcode and shows a contact number on screen. It also keeps tracking the phone's location so you can see where it has been [2].
- **Display a message or remotely wipe:** You can display a message on the device or remotely wipe its data [3].
- **Erase iPhone:** It erases all information and media and restores factory settings [2].
- **Activation Lock:** This prevents anyone else from using your iPhone, since your Apple ID and password are required to turn off Find My iPhone or erase and reactivate it [1].

Two conditions apply. Find My iPhone must be turned on before the phone is lost [1], and the iPhone must be able to connect to the Internet to be located or secured [1].

**Sources**
- [1] iphone_user_guide.pdf, p. 46 ✓ — “Find My iPhone must be turned on before your iPhone is lost”
- [2] iphone_user_guide.pdf, p. 46 ✓ — “Play a sound at full volume for two minutes, even if the ringer is set to silent”
- [3] iphone_user_guide.pdf, p. 18 ✓ — “display a message, play a sound, lock the screen, temporarily suspend or permanently remove your credit and debit cards”

<details><summary>Trace</summary>

- Plan: route=documents — The question asks for documented procedures and features of Find My iPhone, which the iPhone User Guide covers directly.
- Standalone question: What can Find My iPhone do to help me locate or secure my iPhone after I lost it?
- Tier 1 · RAG (dense): 11 chunks (iphone_user_guide.pdf p. 46, 47, 18, 19, 44; iphone_16_repair_manual.pdf p. 98) → judge: sufficient
- Reasoning: Sources [iphone_user_guide.pdf, p. 46] and [iphone_user_guide.pdf, p. 46] describe Play Sound, Lost Mode, Erase iPhone, and the requirement that Find My iPhone be on before loss and the phone be online. [iphone_user_guide.pdf, p. 18] adds locating on a map, displaying a message, and remote wipe. Activation Lock is covered in [iphone_user_guide.pdf, p. 46]. Together these answer the question fully.
- Generate (with the judge): 3 citations
- Verify: 3/3 citations verified

</details>

### ug_burst: How do I take burst photos with the iPhone camera?

Tier: rag

To take burst photos, touch and hold the Take Picture button in Square or Photo mode. The counter shows how many shots you've taken until you lift your finger [1]. Afterward, tap the thumbnail, then tap Select to see the suggested shots. Gray dots mark the suggested photos [1]. To keep one photo from the burst as a separate photo, tap the circle in its lower-right corner [1].

**Sources**
- [1] iphone_user_guide.pdf, p. 94 ✓ — “Touch and hold the Take Picture button to take rapid-fire photos in bursts”

<details><summary>Trace</summary>

- Plan: route=documents — The closest passage on page 94 of the iPhone User Guide describes taking Burst shots with the camera, so the documents likely contain the procedure.
- Tier 1 · RAG (dense): 9 chunks (iphone_user_guide.pdf p. 94, 95, 92, 96) → judge: sufficient
- Reasoning: [iphone_user_guide.pdf, p. 94] states the burst procedure: touch and hold the Take Picture button in Square or Photo mode, the counter shows shots until you lift your finger. It also explains selecting suggested shots and copying one to the Bursts album. This fully answers how to take burst photos.
- Generate (with the judge): 1 citations
- Verify: 1/1 citations verified

</details>

### ug_screenshot: How do I take a screenshot of what is on my iPhone screen?

Tier: rag

To take a screenshot, press the Sleep/Wake and Home buttons at the same time and release them quickly [1]. The screenshot is saved to your Photos app, where you can also find it in the Camera Roll or All Photos album [2].

**Sources**
- [1] iphone_user_guide.pdf, p. 96 ✓ — “Simultaneously press and release the Sleep/ Wake and Home buttons.”
- [2] iphone_user_guide.pdf, p. 96 ✓ — “The screenshot is added to the Photos tab in Photos and can also be viewed in the Camera Roll album”

<details><summary>Trace</summary>

- Plan: route=documents — The iPhone user guide almost certainly documents the screenshot procedure, which is product-specific.
- Tier 1 · RAG (dense): 15 chunks (iphone_user_guide.pdf p. 93, 94, 96, 170; iphone_16_repair_manual.pdf p. 40, 41, 46) → judge: sufficient
- Reasoning: Source [iphone_user_guide.pdf, p. 96] states the screenshot method directly: pressing the Sleep/Wake and Home buttons together. It also says where the screenshot is saved. Nothing else is needed to answer the question.
- Generate (with the judge): 2 citations
- Verify: 2/2 citations verified

</details>

### ug_force_restart: How do I force restart my iPhone when it will not turn off?

Tier: rag

Hold down the Sleep/Wake button and the Home button at the same time for at least ten seconds, until the Apple logo appears [1]. Use this only if you can't restart the iPhone normally [2].

**Sources**
- [1] iphone_user_guide.pdf, p. 187 ✓ — “Hold down the Sleep/Wake button and the Home button at the same time for at least ten seconds, until the Apple logo appears.”
- [2] iphone_user_guide.pdf, p. 187 ✓ — “Do this only if you’re unable to restart iPhone.”

<details><summary>Trace</summary>

- Plan: route=documents — The user guide's appendix covers forcing restarts and troubleshooting an unresponsive iPhone, which is model-specific procedure.
- Tier 1 · RAG (dense): 12 chunks (iphone_user_guide.pdf p. 187, 188, 186, 35, 12; iphone_16_repair_manual.pdf p. 37, 38, 39, 28) → judge: sufficient
- Reasoning: Source [iphone_user_guide.pdf, p. 187] gives the force restart method: hold Sleep/Wake and Home together for at least ten seconds until the Apple logo appears. It also says to use this only if the iPhone can't be restarted normally. That covers the question fully.
- Generate (with the judge): 2 citations
- Verify: 2/2 citations verified

</details>

### rm_thermal_event: What should I do if the battery starts smoking or has a thermal event while I am repairing an iPhone?

Tier: hybrid

**If the battery smokes or has a thermal event, act immediately.**

1. Watch for the warning signs, including smoke, sparks, or soot. [1]
2. Smother the battery or device with plenty of clean, dry sand. [2]
3. Dump all the sand at once, because speed matters. [3]
4. Contact local fire authorities if you need further help. [4]
5. Leave the room for at least 30 minutes after the reaction is contained, and ventilate the area. Don't return until it is clear of smoke. [5]
6. Wait 30 minutes before you touch the device. [6]
7. Wear heat-resistant gloves and safety glasses with side shields to remove the device from the sand. [7]
8. Dispose of the damaged battery or device, including any debris from the sand, according to local laws and guidelines. [8]

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 5 ✓ — “The lithium-ion battery or a device that contains one begins to smoke or emit sparks or soot.”
- [2] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do smother the battery or device immediately with plenty of clean, dry sand.”
- [3] iphone_16_repair_manual.pdf, p. 5 ✓ — “Dump the sand all at once.”
- [4] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do contact local fire authorities if further assistance is needed.”
- [5] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do leave the room for 30 minutes after the reaction is contained.”
- [6] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do wait 30 minutes before touching the device.”
- [7] iphone_16_repair_manual.pdf, p. 5 ✓ — “Wear the heat-resistant gloves and safety glasses with side shields to remove the device from the sand.”
- [8] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do dispose of the damaged battery or device (including any debris removed from the sand) according to local environmental laws and guidelines.”

<details><summary>Trace</summary>

- Plan: route=documents — This is a battery safety procedure that the iPhone 16 repair manual likely covers, and the closest passages mention hissing, popping, and disconnecting the battery.
- Tier 1 · RAG (dense): 14 chunks (iphone_16_repair_manual.pdf p. 28, 29, 85, 86, 87, 5, 6, 7, 4) → judge: insufficient — The immediate steps to take when a battery smokes or has a thermal event during repair, such as moving away, extinguishing, or calling emergency services. → next: documents ['battery begins to smoke or has a thermal event what to do', 'battery swelling venting fire safety workspace extinguisher emergency'], web []
- Reasoning: Sources 522 and 518 warn that hissing, popping, or overheating can lead to a battery thermal event or fire, and 522 says to disconnect external cables. None of them says what to do once smoke or a thermal event actually starts, such as where to move or what to use to extinguish it.
- Tier 2 · Hybrid (BM25+dense, reranked): 3 queries (What should I do if the battery starts smoking or has a thermal event while I am repairing an iPhone? | battery begins to smoke or has a thermal event what to do | battery swelling venting fire safety workspace extinguisher emergency) → 16 chunks (iphone_16_repair_manual.pdf p. 5, 6, 4, 7, 85, 87, 143, 28, 107, 31; iphone_user_guide.pdf p. 183) → judge: sufficient
- Reasoning: Source 520 gives the core response: smother the battery with dry sand, pour it all at once, contact fire authorities if needed, leave the room, and wait 30 minutes before touching the device. Source 521 lists the warning signs (smoke, sparks, soot, a puffing pouch) and says to dispose of the damaged battery, so every part of the question is covered.
- Generate (with the judge): 8 citations
- Verify: 8/8 citations verified

</details>

### rm_broken_glass: What protective gear do I need before repairing an iPhone with a broken display glass?

Tier: rag

Before repairing a broken display glass, put on **safety glasses with side shields** and **cut-resistant gloves** [1].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 7 ✓ — “Put on safety glasses with side shields and the cut-resistant gloves.”

<details><summary>Trace</summary>

- Plan: route=documents — The repair manual's broken glass safety section and display repair pages list the protective gear required for this task.
- Tier 1 · RAG (dense): 15 chunks (iphone_16_repair_manual.pdf p. 7, 8, 10, 170, 171, 107, 108, 118, 48, 1) → judge: sufficient
- Reasoning: Source [iphone_16_repair_manual.pdf, p. 7] states that before a broken-glass repair you must put on safety glasses with side shields and cut-resistant gloves. Source [iphone_16_repair_manual.pdf, p. 8] repeats the same step for broken back glass. Together these fully answer the question about protective gear, so no further search is needed.
- Generate (with the judge): 1 citations
- Verify: 1/1 citations verified

</details>

### rm_diagnostics_requirements: What do I need to run Apple Diagnostics for Self Service Repair on an iPhone?

Tier: rag

To run Apple Diagnostics for Self Service Repair, you need an iPhone 12 or later that can start up in iOS [1]. The device must have iOS 17 or later, and beta versions aren't supported [2]. You also need a secondary device with a supported browser, such as a Mac with Safari, and a Wi-Fi connection on the iPhone being tested [3].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 21 ✓ — “An iPhone 12 or later to be tested that can turn on and start up in iOS.”
- [2] iphone_16_repair_manual.pdf, p. 21 ✓ — “The device youʼre testing must have iOS 17 or iPadOS 17 or later to run Apple Diagnostics for Self Service Repair on a web browser.”
- [3] iphone_16_repair_manual.pdf, p. 22 ✓ — “A Mac running macOS Catalina 10.15 or later with Safari A PC with Chrome 55 or later”

<details><summary>Trace</summary>

- Plan: route=documents — The question asks for specific procedural requirements, which the Apple iPhone 16 Repair Manual likely covers, as shown by the matching passage on p. 21.
- Tier 1 · RAG (dense): 10 chunks (iphone_16_repair_manual.pdf p. 21, 22, 16, 17, 18) → judge: sufficient
- Reasoning: Source [iphone_16_repair_manual.pdf, p. 21] lists the requirements: an iPhone 12 or later that can start up in iOS, iOS 17 or later, and an up-to-date device. Source [iphone_16_repair_manual.pdf, p. 22] lists the secondary device options and the Wi-Fi requirement, and [iphone_16_repair_manual.pdf, p. 22] covers serial number and diagnostics mode steps. Together these cover what is needed to run the self-service diagnostics.
- Generate (with the judge): 3 citations
- Verify: 3/3 citations verified

</details>

### rm_reuse_screws: Can I reuse the old screws when I put an iPhone back together?

Tier: rag

No, don't reuse the old screws. The manual says to never reinstall a screw after removing it, so you should install only new screws [1]. The screws are also coated with an adhesive that can't be reused [2].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 73 ✓ — “Never reinstall a screw after it has been removed. Install only new screws.”
- [2] iphone_16_repair_manual.pdf, p. 73 ✓ — “iPhone screws are covered with an adhesive that canʼt be reused.”

<details><summary>Trace</summary>

- Plan: route=documents — The closest passage on p. 73 says never to reinstall a removed screw and to install only new screws, which directly covers this procedural question about the documented product.
- Standalone question: Can I reuse the old screws when I put an iPhone 16 back together?
- Tier 1 · RAG (dense): 15 chunks (iphone_16_repair_manual.pdf p. 73, 74, 75, 76, 158, 159, 160, 161, 169, 170, 171, 153, 56, 148) → judge: sufficient
- Reasoning: Source [iphone_16_repair_manual.pdf, p. 73] directly states that removed screws must never be reinstalled, that only new screws should be installed, and that the screws' adhesive cannot be reused. That answers the question completely, so no further search is needed.
- Generate (with the judge): 2 citations
- Verify: 2/2 citations verified

</details>

### rm_flex_cable_bend: How far may I bend back the flex cables when removing the USB-C connector from the iPhone 16?

Tier: hybrid

Do not bend back the flex cables more than 90 degrees while removing the USB-C connector [1].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 200 ✓ — “Caution: Donʼt bend back the flex cables more than 90 degrees.”

<details><summary>Trace</summary>

- Plan: route=documents — This asks for a specific procedural limit from the iPhone 16 repair manual, and the closest passage on removing the USB-C connector flex cable is in that manual.
- Tier 1 · RAG (dense): 15 chunks (iphone_16_repair_manual.pdf p. 110, 111, 112, 113, 206, 207, 208, 209, 85, 86, 87, 199, 43, 104) → judge: insufficient — The maximum bend or angle allowed for the USB-C connector flex cable when removing the USB-C connector from the iPhone 16. → next: documents ['USB-C connector flex cable caution avoid bending or tearing the flex cable iPhone 16', 'iPhone 16 USB-C connector removal flex cable bend angle caution'], web []
- Reasoning: Source [iphone_16_repair_manual.pdf, p. 206] describes lifting and peeling the USB-C flex cable, and [iphone_16_repair_manual.pdf, p. 104] gives a 5-degree tilt limit for the back glass or display, which is not a bend limit for the USB-C flex cable. No source states how far the USB-C flex cables may be bent.
- Tier 2 · Hybrid (BM25+dense, reranked): 3 queries (How far may I bend back the flex cables when removing the USB-C connector from the iPhone 16? | USB-C connector flex cable caution avoid bending or tearing the flex cable iPhone 16 | iPhone 16 USB-C connector removal flex cable bend angle caution) → 16 chunks (iphone_16_repair_manual.pdf p. 110, 111, 112, 113, 209, 211, 212, 206, 207, 208, 125, 199, 183, 200, 186; iphone_user_guide.pdf p. 186) → judge: sufficient
- Reasoning: Source [iphone_16_repair_manual.pdf, p. 200] is in the iPhone 16 USB-C connector removal procedure and states the flex cable bend limit directly. Source [iphone_16_repair_manual.pdf, p. 186] gives the same 90-degree limit for a different procedure, which is not needed.
- Generate (with the judge): 1 citations
- Verify: 1/1 citations verified

</details>

### rm_part_blue_torque_driver: What is the part number of the blue torque driver (0.65 kgf cm) in the iPhone 16 tools list?

Tier: rag

The part number of the blue torque driver (0.65 kgf cm) is **923-0448** [1].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 83 ✓ — “923-0448 Torque driver (blue, 0.65 kgf cm)”

<details><summary>Trace</summary>

- Plan: route=documents — The question asks for a specific part number from the iPhone 16 repair manual's tools list, which the indexed documents likely contain.
- Tier 1 · RAG (dense): 15 chunks (iphone_16_repair_manual.pdf p. 199, 200, 201, 202, 184, 185, 186, 187, 160, 161, 162, 163, 130, 83, 150) → judge: sufficient
- Reasoning: Source [iphone_16_repair_manual.pdf, p. 83] (p. 83) is a parts list that pairs each part number with its tool name, and it gives "923-0448" directly before "Torque driver (blue, 0.65 kgf cm)". Source [iphone_16_repair_manual.pdf, p. 130] confirms the blue 0.65 kgf cm driver is a tool in the manual but gives no part number. The question is fully answered by [iphone_16_repair_manual.pdf, p. 83].
- Generate (with the judge): 1 citations
- Verify: 1/1 citations verified

</details>

### rm_part_grounding_spring_screw: What is the part number of the grounding spring screw for the iPhone 16?

Tier: rag

The part number for the grounding spring screw on the iPhone 16 is **923-11184** [1].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 75 ✓ — “Grounding spring screw part number: 923-11184”

<details><summary>Trace</summary>

- Plan: route=documents — The closest passages show a grounding spring screws section in the iPhone 16 repair manual, which likely lists the part number.
- Tier 1 · RAG (dense): 13 chunks (iphone_16_repair_manual.pdf p. 74, 75, 76, 68, 69, 70, 71, 155, 156, 157, 158, 65, 78) → judge: sufficient
- Reasoning: Source [iphone_16_repair_manual.pdf, p. 75] (p. 75) states the grounding spring screw part number directly as 923-11184. Source [iphone_16_repair_manual.pdf, p. 68] lists the same number next to grounding springs, which is a minor labeling difference but does not change the answer. Nothing else is needed.
- Generate (with the judge): 1 citations
- Verify: 1/1 citations verified

</details>

### rm_adjustable_torque_range: What is the torque range of the adjustable torque driver used for screws outlined in black/green?

Tier: rag

The adjustable torque driver ranges from **10–34 Ncm** for screws outlined in black or green. [1]

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 75 ✓ — “Use the adjustable torque driver (10–34 Ncm) for screws outlined in black/green.”

<details><summary>Trace</summary>

- Plan: route=documents — The closest passages from the iPhone 16 repair manual cover torque drivers for black- and green-outlined screws.
- Tier 1 · RAG (dense): 15 chunks (iphone_16_repair_manual.pdf p. 75, 76, 78, 79, 83, 84, 85, 167, 168, 169, 170, 137, 165, 152) → judge: sufficient
- Reasoning: Source [iphone_16_repair_manual.pdf, p. 75] states the adjustable torque driver range directly: 10–34 Ncm for screws outlined in black/green. Source [iphone_16_repair_manual.pdf, p. 79] repeats the same 10–34 Ncm range in the tools list. The question has no other part, so nothing is missing.
- Generate (with the judge): 1 citations
- Verify: 1/1 citations verified

</details>

### know_usb: What does USB stand for?

Tier: knowledge

*Answered from the model's general knowledge; no documents or web sources were consulted.*

**USB** stands for **Universal Serial Bus**. It is a standard for connecting devices to computers and other electronics, for data transfer, charging, and power.

<details><summary>Trace</summary>

- Plan: route=knowledge — This is a well-established abbreviation that I know reliably, and it is not specific to the documented product.

</details>

### know_ram: What does RAM stand for in a computer?

Tier: knowledge

*Answered from the model's general knowledge; no documents or web sources were consulted.*

**RAM** stands for **Random Access Memory**. It is the computer's short-term working memory, where data and programs in use are stored so the processor can access them quickly. RAM is usually volatile, meaning it loses its contents when power is turned off.

<details><summary>Trace</summary>

- Plan: route=knowledge — RAM is a well-established computing term that I know reliably, and the question is general rather than specific to the documented iPhone.

</details>

### know_boiling_point: At what temperature in Celsius does water boil at sea level?

Tier: knowledge

*Answered from the model's general knowledge; no documents or web sources were consulted.*

Water boils at **100 °C** (212 °F) at sea level, under standard atmospheric pressure of 1 atm (101.325 kPa).

<details><summary>Trace</summary>

- Plan: route=knowledge — This is a well-established physical fact that does not depend on the documents or on current information.

</details>

### web_newest_iphone: What is the newest iPhone model Apple sells right now?

Tier: web

The newest iPhone lineup is the iPhone 17 series, which includes the iPhone 17, iPhone Air, iPhone 17 Pro, and iPhone 17 Pro Max. [1] Apple also continues to sell the iPhone 16 and iPhone 16e as lower-cost alternatives. [2] Prices start at $799 and go up to $1,999, depending on model and storage. [3]

**Sources**
- [1] [What is the Latest iPhone? A Complete Guide to Apple’s iPhone 17 Lineup in 2026](https://www.macobserver.com/tips/round-ups/what-is-the-latest-iphone/) ✓ — “The newest iPhone lineup is the iPhone 17 series, consisting of the iPhone 17, iPhone Air, iPhone 17 Pro, and iPhone 17 Pro Max.”
- [2] [What is the Latest iPhone? A Complete Guide to Apple’s iPhone 17 Lineup in 2026](https://www.macobserver.com/tips/round-ups/what-is-the-latest-iphone/) ✓ — “Apple also continues selling the iPhone 16 and iPhone 16e as lower-cost alternatives.”
- [3] [What is the Latest iPhone? A Complete Guide to Apple’s iPhone 17 Lineup in 2026](https://www.macobserver.com/tips/round-ups/what-is-the-latest-iphone/) ✓ — “Prices start at $799 and go up to $1,999 depending on model and storage.”

<details><summary>Trace</summary>

- Plan: route=web — This is time-sensitive product availability that the documents cannot reliably confirm, so it needs a current web search.
- Tier 3 · Web: “What is the newest iPhone model Apple sells right now?” → 5 chunks (https://www.macobserver.com/tips/round-ups/what-is-the-latest-iphone/; https://toolrom.com/what-iphone-is-current/)
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>

### web_latest_ios: What is the latest public version of iOS available today?

Tier: web

The latest public version of iOS in the provided evidence is **iOS 27**. [1] It is available for iPhone now. [2] A later point release, iOS 27.3, has only reached public beta so far. [3] The evidence is dated September 2026, so it does not confirm whether a newer release has shipped since then.

**Sources**
- [1] [iOS 27 is available to download to your iPhone right now](https://appleinsider.com/articles/26/09/14/ios-27-is-now-available-with-big-changes-to-photos-and-siri) ✓ — “Apple has released iOS 27 to the public”
- [2] [iOS 27 now available: New features, compatible iPhones, and more - 9to5Mac](https://9to5mac.com/2026/09/14/ios-27-now-available-features-compatible-iphones/) ✓ — “iOS 27 is now available for iPhone.”
- [3] [iOS 27 is available to download to your iPhone right now](https://appleinsider.com/articles/26/09/14/ios-27-is-now-available-with-big-changes-to-photos-and-siri) ✓ — “First public betas for iOS 27.3, iPadOS 27.3, and macOS 27.3 are available”

<details><summary>Trace</summary>

- Plan: route=web — The latest public iOS release changes over time, and the indexed guides cover older versions such as iOS 8.4, so only a current web search can answer this.
- Tier 3 · Web: “What is the latest public version of iOS available today?” → 5 chunks (https://www.whistleout.com/CellPhones/Guides/what-is-the-latest-version-of-ios; https://appleinsider.com/articles/26/09/14/ios-27-is-now-available-with-big-changes-to-photos-and-siri; https://9to5mac.com/2026/09/14/ios-27-now-available-features-compatible-iphones/)
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>

### web_apple_revenue: How much revenue did Apple report in its most recent quarterly earnings?

Tier: web

Apple's most recent quarter was its fiscal 2026 fourth quarter, and it reported revenue of **$114.5 billion**. [1] MacRumors reported the same figure, along with a net quarterly profit of $30.7 billion. [2]

**Sources**
- [1] [Apple Reports Q4 2026 Revenue of $114.5 Billion - MacStories](https://www.macstories.net/news/apple-reports-q4-2026-revenue-of-114-5-billion/) ✓ — “Today, Apple reported its 2026 Q4 earnings, posting quarterly revenue of $114.5 billion.”
- [2] [Apple Reports 4Q 2026 Results: $30.7B Profit on $114.5B Revenue - MacRumors](https://www.macrumors.com/2026/11/02/apple-4q-2026-earnings/) ✓ — “For the quarter, Apple posted revenue of $114.5 billion and net quarterly profit of $30.7 billion”

<details><summary>Trace</summary>

- Plan: route=web — This asks for current financial results that change over time and are not in the Apple iPhone manuals.
- Tier 3 · Web: “How much revenue did Apple report in its most recent quarterly earnings?” → 5 chunks (https://www.macstories.net/news/apple-reports-q3-2026-earnings/; https://www.macstories.net/news/apple-reports-q4-2026-revenue-of-114-5-billion/; https://www.macrumors.com/2026/11/02/apple-4q-2026-earnings/; https://www.apple.com/newsroom/2025/10/apple-reports-fourth-quarter-results/)
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>
