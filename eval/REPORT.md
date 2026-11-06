# iPhone manuals: end-to-end eval (ladder mode)

LLM backend: `cli:claude` (model `CLI default`). Passed **20/20**. Median latency 7.0 s.

| id | category | expected | tier | verified citations | page hit | keywords | s | result |
|---|---|---|---|---|---|---|---|---|
| ug_wifi | doc | rag/hybrid | rag | 1/1 | exact | 50% | 7.0 | PASS |
| ug_control_center | doc | rag/hybrid | rag | 1/1 | exact | 100% | 3.0 | PASS |
| ug_lost_iphone | doc | rag/hybrid | rag | 2/2 | exact | 100% | 6.6 | PASS |
| ug_burst | doc | rag/hybrid | rag | 3/3 | exact | 100% | 5.6 | PASS |
| ug_screenshot | doc | rag/hybrid/web | rag | 2/2 | exact | 100% | 10.3 | PASS |
| ug_force_restart | doc | rag/hybrid/web | rag | 2/2 | exact | 67% | 6.0 | PASS |
| rm_thermal_event | doc | rag/hybrid | hybrid | 12/12 | exact | 67% | 28.0 | PASS |
| rm_broken_glass | doc | rag/hybrid | rag | 1/1 | exact | 67% | 8.1 | PASS |
| rm_diagnostics_requirements | doc | rag/hybrid | rag | 4/4 | exact | 100% | 7.4 | PASS |
| rm_reuse_screws | doc | rag/hybrid | rag | 2/2 | exact | 100% | 6.5 | PASS |
| rm_flex_cable_bend | doc | rag/hybrid | hybrid | 1/1 | exact | 100% | 11.1 | PASS |
| rm_part_blue_torque_driver | hybrid | rag/hybrid | rag | 1/1 | exact | 50% | 7.4 | PASS |
| rm_part_grounding_spring_screw | hybrid | rag/hybrid | rag | 1/1 | exact | 100% | 4.2 | PASS |
| rm_adjustable_torque_range | hybrid | rag/hybrid | rag | 1/1 | exact | 100% | 6.6 | PASS |
| know_usb | knowledge | knowledge | knowledge | 0/0 | - | - | 1.4 | PASS |
| know_ram | knowledge | knowledge | knowledge | 0/0 | - | - | 1.6 | PASS |
| know_boiling_point | knowledge | knowledge | knowledge | 0/0 | - | - | 3.9 | PASS |
| web_newest_iphone | web | web | web | 3/3 | - | - | 17.6 | PASS |
| web_latest_ios | web | web | web | 3/3 | - | - | 17.3 | PASS |
| web_apple_revenue | web | web | web | 3/3 | - | - | 11.6 | PASS |

## Answers

### ug_wifi: How do I connect my iPhone to a Wi-Fi network?

Tier: rag

To connect your iPhone to a Wi-Fi network, go to Settings > Wi-Fi and turn Wi-Fi on [1]. Then tap one of the listed networks and enter its password if asked [1].

**Sources**
- [1] iphone_user_guide.pdf, p. 16 ✓ — “Go to Settings > Wi-Fi, then turn Wi-Fi on or off. (You can also turn Wi-Fi on or off in Control Center.) • Choose a network: Tap one of the listed networks, then enter the password, if asked.”

<details><summary>Trace</summary>

- Plan: route=documents — This is a procedure for the iPhone, which the user guide documents directly, and the closest passage on p. 16 covers Wi-Fi connection.
- Tier 1 · RAG (dense): 11 chunks (iphone_user_guide.pdf p. 16, 17, 18, 40, 41, 20) → judge: sufficient
- Reasoning: Source [iphone_user_guide.pdf, p. 16] gives the core steps: go to Settings > Wi-Fi, turn Wi-Fi on, then tap a listed network and enter its password if asked. Source [iphone_user_guide.pdf, p. 17] adds how to join a closed network, which is optional detail beyond the basic question.
- Generate (with the judge): 1 citations
- Verify: 1/1 citations verified

</details>

### ug_control_center: How do I open Control Center on my iPhone?

Tier: rag

To open Control Center, swipe up from the bottom edge of any screen, even the Lock screen [1].

**Sources**
- [1] iphone_user_guide.pdf, p. 35 ✓ — “Open Control Center. Swipe up from the bottom edge of any screen (even the Lock screen).”

<details><summary>Trace</summary>

- Plan: route=documents — This is an iPhone procedure, and the user guide's closest passage on p. 154 describes opening Control Center.
- Tier 1 · RAG (dense): 15 chunks (iphone_user_guide.pdf p. 35, 36, 154, 172, 173, 169, 41, 170) → judge: sufficient
- Reasoning: Source [iphone_user_guide.pdf, p. 35] states the direct step: swipe up from the bottom edge of any screen, even the Lock screen, to open Control Center. Nothing else is needed to answer the question.
- Generate (with the judge): 1 citations
- Verify: 1/1 citations verified

</details>

### ug_lost_iphone: I lost my iPhone, what can Find My iPhone do to help me?

Tier: rag

Find My iPhone can help you locate and secure a lost iPhone. It works from the free Find My iPhone app on another iPhone, iPad, or iPod touch, or from a web browser at www.icloud.com/find [1]. Its Activation Lock is designed to stop anyone else from using your iPhone [1]. You can use these actions:

- **Play Sound:** plays a sound at full volume for two minutes, even on silent [2].
- **Lost Mode:** locks the iPhone with a passcode, shows a contact number on screen, and tracks its location [2].
- **Erase iPhone:** removes all information and media and restores factory settings [2].

Find My iPhone must already be turned on before the phone is lost, and the iPhone must be able to connect to the Internet [1].

**Sources**
- [1] iphone_user_guide.pdf, p. 46 ✓ — “Find My iPhone can help you locate and secure your iPhone using the free Find My iPhone app”
- [2] iphone_user_guide.pdf, p. 46 ✓ — “Play Sound: Play a sound at full volume for two minutes, even if the ringer is set to silent.”

<details><summary>Trace</summary>

- Plan: route=documents — The iPhone user guide has a Find My iPhone section on p. 46 that likely answers this directly.
- Tier 1 · RAG (dense): 11 chunks (iphone_user_guide.pdf p. 46, 47, 18, 19, 191, 189) → judge: sufficient
- Reasoning: Source [iphone_user_guide.pdf, p. 46] explains Find My iPhone locates and secures a lost iPhone and includes Activation Lock. Source [iphone_user_guide.pdf, p. 46] lists the actions available: Play Sound, Lost Mode, and Erase iPhone. The evidence fully covers what the feature can do for a lost phone.
- Generate (with the judge): 2 citations
- Verify: 2/2 citations verified

</details>

### ug_burst: How do I take burst photos with the iPhone camera?

Tier: rag

To take burst photos, touch and hold the Take Picture button in Photo or Square mode. The camera takes rapid-fire photos while you hold it [1]. A counter shows how many shots you've taken until you lift your finger [2]. To choose the photos to keep, tap the thumbnail, then tap Select [3].

**Sources**
- [1] iphone_user_guide.pdf, p. 94 ✓ — “Touch and hold the Take Picture button to take rapid-fire photos in bursts (available while in Square or Photo mode).”
- [2] iphone_user_guide.pdf, p. 94 ✓ — “the counter shows how many shots you’ve taken, until you lift your finger.”
- [3] iphone_user_guide.pdf, p. 94 ✓ — “To see the suggested shots and select the photos you want to keep, tap the thumbnail, then tap Select.”

<details><summary>Trace</summary>

- Plan: route=documents — The iPhone user guide's camera section on p. 94 explicitly covers taking burst shots.
- Tier 1 · RAG (dense): 9 chunks (iphone_user_guide.pdf p. 94, 95, 92, 96) → judge: sufficient
- Reasoning: Source [iphone_user_guide.pdf, p. 94] explains the burst steps: touch and hold the Take Picture button, lift your finger to stop, then review and keep shots. This fully answers the question.
- Generate (with the judge): 3 citations
- Verify: 3/3 citations verified

</details>

### ug_screenshot: How do I take a screenshot of what is on my iPhone screen?

Tier: rag

Press the Sleep/Wake and Home buttons at the same time [1]. The screenshot is added to the Photos app [2].

**Sources**
- [1] iphone_user_guide.pdf, p. 96 ✓ — “Simultaneously press and release the Sleep/ Wake and Home buttons.”
- [2] iphone_user_guide.pdf, p. 96 ✓ — “The screenshot is added to the Photos tab in Photos”

<details><summary>Trace</summary>

- Plan: route=documents — This is a how-to procedure for a specific iPhone, which the indexed iPhone user guide is likely to cover.
- Tier 1 · RAG (dense): 15 chunks (iphone_user_guide.pdf p. 93, 94, 96, 170; iphone_16_repair_manual.pdf p. 40, 41, 46) → judge: sufficient
- Reasoning: [iphone_user_guide.pdf, p. 96] gives the button combination and says where screenshots are saved, and [iphone_user_guide.pdf, p. 170] repeats the button press for taking a screenshot. Nothing else is needed.
- Generate (with the judge): 2 citations
- Verify: 2/2 citations verified

</details>

### ug_force_restart: How do I force restart my iPhone when it will not turn off?

Tier: rag

Hold the Sleep/Wake and Home buttons together for at least ten seconds, until the Apple logo appears [1]. Use this only when you can't turn off the iPhone normally [2].

**Sources**
- [1] iphone_user_guide.pdf, p. 187 ✓ — “Hold down the Sleep/Wake button and the Home button at the same time for at least ten seconds, until the Apple logo appears.”
- [2] iphone_user_guide.pdf, p. 187 ✓ — “Do this only if you’re unable to restart iPhone.”

<details><summary>Trace</summary>

- Plan: route=documents — The user guide's troubleshooting section likely contains the force restart procedure for an unresponsive iPhone.
- Tier 1 · RAG (dense): 12 chunks (iphone_user_guide.pdf p. 187, 188, 186, 35, 12; iphone_16_repair_manual.pdf p. 37, 38, 39, 28) → judge: sufficient
- Reasoning: [iphone_user_guide.pdf, p. 187] gives the button combination for forcing a restart and says to use it only when a normal restart is not possible. The evidence covers the question, so no further search is needed.
- Generate (with the judge): 2 citations
- Verify: 2/2 citations verified

</details>

### rm_thermal_event: What should I do if the battery starts smoking or has a thermal event while I am repairing an iPhone?

Tier: hybrid

**If the battery starts smoking, sparking, or puffing out:**

- Act immediately. The warning signs include a battery that begins to smoke or emit sparks or soot [1].
- Smother the battery or device with plenty of clean, dry sand [2]. Dump the sand all at once [3].
- Contact local fire authorities if further assistance is needed [4].
- Leave the room for 30 minutes after the reaction is contained [5]. Do not touch the device for 30 minutes [6].
- When removing the device from the sand, wear heat-resistant gloves and safety glasses with side shields [7].

**Handling the battery safely during the repair:**

- Fully discharge the battery before you begin a repair [8]. Discharge the battery fully and disconnect all cables before starting [9].
- Don't throw or drop the battery [10].
- The battery should be replaced only by Apple or an authorized service provider [11].
- Dispose of a damaged battery or device according to local laws and guidelines [12].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 5 ✓ — “The lithium-ion battery or a device that contains one begins to smoke or emit sparks or soot.”
- [2] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do smother the battery or device immediately with plenty of clean, dry sand.”
- [3] iphone_16_repair_manual.pdf, p. 5 ✓ — “Dump the sand all at once.”
- [4] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do contact local fire authorities if further assistance is needed.”
- [5] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do leave the room for 30 minutes after the reaction is contained.”
- [6] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do wait 30 minutes before touching the device.”
- [7] iphone_16_repair_manual.pdf, p. 5 ✓ — “Wear the heat-resistant gloves and safety glasses with side shields to remove the device from the sand.”
- [8] iphone_16_repair_manual.pdf, p. 5 ✓ — “Fully discharge the battery before you begin a repair.”
- [9] iphone_16_repair_manual.pdf, p. 85 ✓ — “Discharge the battery fully. Disconnect all cables.”
- [10] iphone_16_repair_manual.pdf, p. 6 ✓ — “Donʼt throw or drop the battery.”
- [11] iphone_user_guide.pdf, p. 183 ✓ — “The lithium-ion battery in iPhone should be replaced only by Apple or an authorized service provider”
- [12] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do dispose of the damaged battery or device”

<details><summary>Trace</summary>

- Plan: route=documents — This is a safety procedure specific to the documented iPhone 16, and the repair manual has relevant passages on swollen or overheating batteries.
- Tier 1 · RAG (dense): 14 chunks (iphone_16_repair_manual.pdf p. 28, 29, 85, 86, 87, 5, 6, 7, 4) → judge: insufficient — Specific steps to take at the moment a battery starts smoking or overheating during a repair. → next: documents ['battery swelling smoke overheating what to do immediately'], web []
- Reasoning: Sources 522 and 518 cover hissing or popping batteries, ventilation, and the risk of a thermal event, but give no direct response for smoke. Sources 687 and 523 cover disconnecting cables, discharging the battery, and safe handling, which answers the handling part. The immediate emergency response is not stated anywhere in the evidence.
- Tier 2 · Hybrid (BM25+dense, reranked): 2 queries (What should I do if the battery starts smoking or has a thermal event while I am repairing an iPhone? | battery swelling smoke overheating what to do immediately) → 14 chunks (iphone_16_repair_manual.pdf p. 5, 6, 4, 85, 28, 118, 145, 31; iphone_user_guide.pdf p. 183) → judge: sufficient
- Reasoning: Source 520 gives the immediate response to a thermal event: smother with dry sand, contact fire authorities, and stay away for 30 minutes. Sources 521 and 687 cover discharging the battery and disconnecting cables before repair, and 523, 465 and 521 cover careful handling and disposal. Every part is answered directly by the evidence.
- Generate (with the judge): 12 citations
- Verify: 12/12 citations verified

</details>

### rm_broken_glass: What protective gear do I need before repairing an iPhone with a broken display glass?

Tier: rag

Before repairing a broken display glass, put on safety glasses with side shields and cut-resistant gloves [1].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 7 ✓ — “Put on safety glasses with side shields and the cut-resistant gloves.”

<details><summary>Trace</summary>

- Plan: route=documents — The repair manual's broken glass safety and display repair pages list the protective gear required for this exact task.
- Tier 1 · RAG (dense): 15 chunks (iphone_16_repair_manual.pdf p. 7, 8, 10, 170, 171, 107, 108, 118, 48, 1) → judge: sufficient
- Reasoning: [iphone_16_repair_manual.pdf, p. 7] states directly that before handling broken display glass you should put on safety glasses with side shields and cut-resistant gloves. It also lists an ESD-safe vacuum and protective cover as tools, but the gear question is answered fully by the glasses and gloves. No further sources are needed.
- Generate (with the judge): 1 citations
- Verify: 1/1 citations verified

</details>

### rm_diagnostics_requirements: What do I need to run Apple Diagnostics for Self Service Repair on an iPhone?

Tier: rag

To run Apple Diagnostics for Self Service Repair, you need an iPhone 12 or later that can start up in iOS [1]. The device being tested must have iOS 17 or later [2]. You also need a secondary device, such as a Mac running macOS Catalina 10.15 or later with Safari [3], and a Wi-Fi connection on the device being tested [4].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 21 ✓ — “An iPhone 12 or later to be tested that can turn on and start up in iOS.”
- [2] iphone_16_repair_manual.pdf, p. 21 ✓ — “The device youʼre testing must have iOS 17 or iPadOS 17 or later to run Apple Diagnostics for Self Service Repair on a web browser.”
- [3] iphone_16_repair_manual.pdf, p. 22 ✓ — “A Mac running macOS Catalina 10.15 or later with Safari”
- [4] iphone_16_repair_manual.pdf, p. 22 ✓ — “A Wi-Fi connection on the device to be tested”

<details><summary>Trace</summary>

- Plan: route=documents — The closest passages in the iPhone 16 Repair Manual directly list the requirements for running Apple Diagnostics for Self Service Repair.
- Tier 1 · RAG (dense): 10 chunks (iphone_16_repair_manual.pdf p. 21, 22, 16, 17, 18) → judge: sufficient
- Reasoning: [iphone_16_repair_manual.pdf, p. 21] lists the device requirements: an iPhone 12 or later on iOS 17 or later, and a web browser on a secondary device. [iphone_16_repair_manual.pdf, p. 22] covers the secondary device and Wi-Fi connection needed. Together these answer the question fully.
- Generate (with the judge): 4 citations
- Verify: 4/4 citations verified

</details>

### rm_reuse_screws: Can I reuse the old screws when I put an iPhone back together?

Tier: rag

No. Never reinstall a screw after it has been removed. Install only new screws [1]. The screws are covered with an adhesive that can't be reused [2].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 73 ✓ — “Never reinstall a screw after it has been removed. Install only new screws.”
- [2] iphone_16_repair_manual.pdf, p. 73 ✓ — “iPhone screws are covered with an adhesive that canʼt be reused.”

<details><summary>Trace</summary>

- Plan: route=documents — The repair manual's screw warning passage directly addresses whether removed screws can be reinstalled, so the documents likely answer this.
- Standalone question: Can I reuse the old screws when I put an iPhone 16 back together?
- Tier 1 · RAG (dense): 15 chunks (iphone_16_repair_manual.pdf p. 73, 74, 75, 76, 158, 159, 160, 161, 169, 170, 171, 153, 56, 148) → judge: sufficient
- Reasoning: [iphone_16_repair_manual.pdf, p. 73] directly says never to reinstall a removed screw and to install only new screws, and that iPhone screws carry an adhesive that can't be reused. That answers the question completely, with no need for other sources.
- Generate (with the judge): 2 citations
- Verify: 2/2 citations verified

</details>

### rm_flex_cable_bend: How far may I bend back the flex cables when removing the USB-C connector from the iPhone 16?

Tier: hybrid

Do not bend the flex cables back more than 90 degrees [1].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 200 ✓ — “Donʼt bend back the flex cables more than 90 degrees.”

<details><summary>Trace</summary>

- Plan: route=documents — The repair manual covers USB-C connector removal and flex cable handling, so it likely holds the bending limit.
- Tier 1 · RAG (dense): 15 chunks (iphone_16_repair_manual.pdf p. 110, 111, 112, 113, 206, 207, 208, 209, 85, 86, 87, 199, 43, 104) → judge: insufficient — A bend or flex limit for the USB-C connector flex cable itself during removal. → next: documents ['USB-C connector flex cable avoid damaging do not bend remove'], web []
- Reasoning: [iphone_16_repair_manual.pdf, p. 104] gives a 5-degree limit for tilting the back glass or display to avoid damaging flex cables, but that is for the display, not the USB-C connector cable. [iphone_16_repair_manual.pdf, p. 206] and [iphone_16_repair_manual.pdf, p. 199] describe lifting and peeling the USB-C flex cable without giving any bend limit. The question asks for the limit specifically for the USB-C connector, so the 5-degree figure cannot be applied without guessing.
- Tier 2 · Hybrid (BM25+dense, reranked): 2 queries (How far may I bend back the flex cables when removing the USB-C connector from the iPhone 16? | USB-C connector flex cable avoid damaging do not bend remove) → 16 chunks (iphone_16_repair_manual.pdf p. 206, 207, 208, 209, 211, 212, 29, 30, 185, 183, 210, 199, 200; iphone_user_guide.pdf p. 186) → judge: sufficient
- Reasoning: [iphone_16_repair_manual.pdf, p. 200], from the USB-C connector removal section, says not to bend back the flex cables more than 90 degrees. This directly answers the bend limit for this step. The 5-degree figure in an earlier display section does not apply to the USB-C connector.
- Generate (with the judge): 1 citations
- Verify: 1/1 citations verified

</details>

### rm_part_blue_torque_driver: What is the part number of the blue torque driver (0.65 kgf cm) in the iPhone 16 tools list?

Tier: rag

The blue torque driver (0.65 kgf cm) has part number 923-0448 [1].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 83 ✓ — “923-0448 Torque driver (blue, 0.65 kgf cm)”

<details><summary>Trace</summary>

- Plan: route=documents — This asks for a specific part number from the iPhone 16 repair manual's tools list, which the documents are likely to contain.
- Tier 1 · RAG (dense): 15 chunks (iphone_16_repair_manual.pdf p. 199, 200, 201, 202, 184, 185, 186, 187, 160, 161, 162, 163, 130, 83, 150) → judge: sufficient
- Reasoning: Source [iphone_16_repair_manual.pdf, p. 83] lists the blue torque driver (0.65 kgf cm) with part number 923-0448. Source [iphone_16_repair_manual.pdf, p. 130] names the same tool but gives no part number, and no other source conflicts with it.
- Generate (with the judge): 1 citations
- Verify: 1/1 citations verified

</details>

### rm_part_grounding_spring_screw: What is the part number of the grounding spring screw for the iPhone 16?

Tier: rag

The grounding spring screw part number for the iPhone 16 is 923-11184 [1].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 75 ✓ — “Grounding spring screw part number: 923-11184”

<details><summary>Trace</summary>

- Plan: route=documents — The closest passages cover grounding spring screws and parts numbers in the iPhone 16 repair manual, so the answer is likely there.
- Tier 1 · RAG (dense): 13 chunks (iphone_16_repair_manual.pdf p. 74, 75, 76, 68, 69, 70, 71, 155, 156, 157, 158, 65, 78) → judge: sufficient
- Reasoning: Source [iphone_16_repair_manual.pdf, p. 75] states the grounding spring screw part number directly as 923-11184. Source [iphone_16_repair_manual.pdf, p. 68] lists the same number, though under the grounding springs heading.
- Generate (with the judge): 1 citations
- Verify: 1/1 citations verified

</details>

### rm_adjustable_torque_range: What is the torque range of the adjustable torque driver used for screws outlined in black/green?

Tier: rag

The adjustable torque driver has a range of 10–34 Ncm and is used for screws outlined in black or green [1].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 75 ✓ — “Use the adjustable torque driver (10–34 Ncm) for screws outlined in black/green.”

<details><summary>Trace</summary>

- Plan: route=documents — The question asks for a specific torque value from the iPhone 16 repair manual, which the closest passages appear to contain.
- Tier 1 · RAG (dense): 15 chunks (iphone_16_repair_manual.pdf p. 75, 76, 78, 79, 83, 84, 85, 167, 168, 169, 170, 137, 165, 152) → judge: sufficient
- Reasoning: Source [iphone_16_repair_manual.pdf, p. 75] directly states that the adjustable torque driver (10–34 Ncm) is used for screws outlined in black/green. Nothing else in the question is left unanswered, so no further searches are needed.
- Generate (with the judge): 1 citations
- Verify: 1/1 citations verified

</details>

### know_usb: What does USB stand for?

Tier: knowledge

*Answered from the model's general knowledge; no documents or web sources were consulted.*

USB stands for **Universal Serial Bus**. It is a standard for connecting devices to computers and other electronics for data transfer, charging, and power.

<details><summary>Trace</summary>

- Plan: route=knowledge — This is a well-established definition that I know reliably and that is not time-sensitive.

</details>

### know_ram: What does RAM stand for in a computer?

Tier: knowledge

*Answered from the model's general knowledge; no documents or web sources were consulted.*

**RAM** stands for **Random Access Memory**. It is a type of computer memory that stores data and programs the processor is actively using. It is fast to read and write, but its contents are lost when the power is turned off.

<details><summary>Trace</summary>

- Plan: route=knowledge — RAM is a standard computing term that I know reliably and it is not time-sensitive.

</details>

### know_boiling_point: At what temperature in Celsius does water boil at sea level?

Tier: knowledge

*Answered from the model's general knowledge; no documents or web sources were consulted.*

Water boils at **100 °C** (212 °F) at sea level, when the air pressure is standard atmospheric pressure (1 atm).

<details><summary>Trace</summary>

- Plan: route=knowledge — This is a well-established, non-time-sensitive physics fact unrelated to the documents.

</details>

### web_newest_iphone: What is the newest iPhone model Apple sells right now?

Tier: web

The newest iPhone lineup Apple sells is the **iPhone 17 series** [1]. It includes four models: iPhone 17, iPhone Air, iPhone 17 Pro, and iPhone 17 Pro Max [2]. Apple also continues selling the iPhone 16 and iPhone 16e as lower-cost alternatives [3].

**Sources**
- [1] [What is the Latest iPhone? A Complete Guide to Apple’s iPhone 17 Lineup in 2026](https://www.macobserver.com/tips/round-ups/what-is-the-latest-iphone/) ✓ — “the answer is the iPhone 17 series”
- [2] [What is the Latest iPhone? A Complete Guide to Apple’s iPhone 17 Lineup in 2026](https://www.macobserver.com/tips/round-ups/what-is-the-latest-iphone/) ✓ — “Apple now offers iPhone 17, iPhone Air, iPhone 17 Pro, and iPhone 17 Pro Max.”
- [3] [What is the Latest iPhone? A Complete Guide to Apple’s iPhone 17 Lineup in 2026](https://www.macobserver.com/tips/round-ups/what-is-the-latest-iphone/) ✓ — “Apple also continues selling the iPhone 16 and iPhone 16e as lower-cost alternatives.”

<details><summary>Trace</summary>

- Plan: route=web — This is a current, time-sensitive product question that the documents, which cover older guides and repair procedures, are unlikely to answer.
- Tier 3 · Web: “What is the newest iPhone model Apple sells right now?” → 5 chunks (https://www.macobserver.com/tips/round-ups/what-is-the-latest-iphone/; https://toolrom.com/what-iphone-is-current/)
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>

### web_latest_ios: What is the latest public version of iOS available today?

Tier: web

The latest public version of iOS in the evidence is iOS 27, which Apple has released to the public [1]. The 9to5Mac article confirms that "iOS 27 is officially here" [2] and is dated September 14, 2026 [3]. The evidence does not mention any later iOS 27 point release, so it cannot confirm that iOS 27 is still the newest version as of today.

**Sources**
- [1] [iOS 27 is available to download to your iPhone right now](https://appleinsider.com/articles/26/09/14/ios-27-is-now-available-with-big-changes-to-photos-and-siri) ✓ — “Apple has released iOS 27 to the public”
- [2] [iOS 27 now available: New features, compatible iPhones, and more](https://9to5mac.com/2026/09/14/ios-27-now-available-features-compatible-iphones/) ✓ — “iOS 27 is officially here.”
- [3] [iOS 27 now available: New features, compatible iPhones, and more](https://9to5mac.com/2026/09/14/ios-27-now-available-features-compatible-iphones/) ✓ — “Zac Hall | Sep 14 2026”

<details><summary>Trace</summary>

- Plan: route=web — This is a current, time-sensitive software release question, and the indexed guides cover older iOS versions and repair procedures, so they are unlikely to answer it.
- Tier 3 · Web: “What is the latest public version of iOS available today?” → 5 chunks (https://9to5mac.com/2026/09/14/ios-27-now-available-features-compatible-iphones/; https://www.yournavi.com/posts/latest-ios-version; https://appleinsider.com/articles/26/09/14/ios-27-is-now-available-with-big-changes-to-photos-and-siri; https://www.macworld.com/article/2986799/ios-27-features-compatiblity-siri-ai-updates.html)
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>

### web_apple_revenue: How much revenue did Apple report in its most recent quarterly earnings?

Tier: web

Apple's most recent quarterly results, for its fiscal fourth quarter of 2026 reported on November 2, showed revenue of $114.5 billion [1]. Net profit was $30.71 billion [2], and revenue rose 12 percent from the same period last year [3].

**Sources**
- [1] [Apple reports Q4 2026 earnings: $114.5 billion in revenue, up ...](https://9to5mac.com/2026/11/02/apple-reports-q4-2026-earnings/) ✓ — “The company reported $114.5 billion in revenue”
- [2] [Apple reports Q4 2026 earnings: $114.5 billion in revenue, up ...](https://9to5mac.com/2026/11/02/apple-reports-q4-2026-earnings/) ✓ — “and $30.71 billion in net profit”
- [3] [Apple Hits Record $114.5 Billion Revenue In Q4 2026 Earnings](https://www.macobserver.com/news/apple-hits-record-114-5-billion-revenue-in-q4-2026-earnings/) ✓ — “Apple saw a 12 percent jump compared to the same period last year”

<details><summary>Trace</summary>

- Plan: route=web — This asks for Apple's latest quarterly revenue, a current figure that changes over time and is not in the iPhone manuals.
- Tier 3 · Web: “How much revenue did Apple report in its most recent quarterly earnings?” → 5 chunks (https://www.macrumors.com/2026/11/02/apple-4q-2026-earnings/; https://hypebeast.com/2026/11/apple-posts-record-114-5-billion-q4-revenue; https://9to5mac.com/2026/11/02/apple-reports-q4-2026-earnings/; https://www.macobserver.com/news/apple-hits-record-114-5-billion-revenue-in-q4-2026-earnings/; https://www.apple.com/newsroom/2025/10/apple-reports-fourth-quarter-results/)
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>
