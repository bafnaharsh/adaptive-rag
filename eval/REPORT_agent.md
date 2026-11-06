# iPhone manuals: end-to-end eval (agent mode)

LLM backend: `cli:claude` (model `CLI default`). Passed **18/20**. Median latency 10.2 s.

| id | category | expected | tier | verified citations | page hit | keywords | s | result |
|---|---|---|---|---|---|---|---|---|
| ug_wifi | doc | rag/hybrid | hybrid | 3/3 | exact | 50% | 12.1 | PASS |
| ug_control_center | doc | rag/hybrid | hybrid | 2/2 | exact | 50% | 6.2 | PASS |
| ug_lost_iphone | doc | rag/hybrid | rag | 8/8 | exact | 100% | 12.3 | PASS |
| ug_burst | doc | rag/hybrid | rag | 5/5 | exact | 100% | 8.1 | PASS |
| ug_screenshot | doc | rag/hybrid/web | rag | 2/2 | exact | 100% | 7.0 | PASS |
| ug_force_restart | doc | rag/hybrid/web | rag | 2/2 | ±1 | 0% | 13.9 | FAIL |
| rm_thermal_event | doc | rag/hybrid | rag | 12/12 | exact | 100% | 12.8 | PASS |
| rm_broken_glass | doc | rag/hybrid | rag | 2/2 | exact | 100% | 10.2 | PASS |
| rm_diagnostics_requirements | doc | rag/hybrid | rag | 11/11 | exact | 100% | 14.7 | PASS |
| rm_reuse_screws | doc | rag/hybrid | rag | 3/3 | exact | 50% | 6.7 | PASS |
| rm_flex_cable_bend | doc | rag/hybrid | rag | 2/2 | exact | 100% | 5.9 | PASS |
| rm_part_blue_torque_driver | hybrid | rag/hybrid | hybrid | 2/2 | miss | 50% | 12.5 | FAIL |
| rm_part_grounding_spring_screw | hybrid | rag/hybrid | rag | 2/2 | exact | 100% | 3.0 | PASS |
| rm_adjustable_torque_range | hybrid | rag/hybrid | rag | 2/2 | exact | 100% | 4.9 | PASS |
| know_usb | knowledge | knowledge | knowledge | 0/0 | - | - | 1.4 | PASS |
| know_ram | knowledge | knowledge | knowledge | 0/0 | - | - | 1.3 | PASS |
| know_boiling_point | knowledge | knowledge | knowledge | 0/0 | - | - | 1.5 | PASS |
| web_newest_iphone | web | web | web | 2/2 | - | - | 19.8 | PASS |
| web_latest_ios | web | web | web | 2/2 | - | - | 20.8 | PASS |
| web_apple_revenue | web | web | web | 1/1 | - | - | 12.5 | PASS |

## Answers

### ug_wifi: How do I connect my iPhone to a Wi-Fi network?

Tier: hybrid

1. Open **Settings > Wi-Fi** and turn Wi-Fi on [1].
2. Tap one of the listed networks, then enter its password if asked [1].
3. If your network doesn't appear in the list, you can join a closed network: tap **Other**, then enter the network name. You need to know the network name, security type, and password [2].

Once connected, a Wi-Fi icon appears at the top of the screen [3].

**Sources**
- [1] iphone_user_guide.pdf, p. 16 ✓ — “Configure Wi-Fi. Go to Settings > Wi-Fi, then turn Wi-Fi on or off. (You can also turn Wi-Fi on or off in Control Center.) • Choose a network: Tap one of the listed networks, then enter the password, if asked.”
- [2] iphone_user_guide.pdf, p. 17 ✓ — “Join a closed Wi-Fi network: Tap Other, then enter the name of the closed network. You need to know the network name, security type, and password.”
- [3] iphone_user_guide.pdf, p. 16 ✓ — “If appears at the top of the screen, you’re connected to a Wi-Fi network.”

<details><summary>Trace</summary>

- Round 1 · think: Checking your iPhone user guide for the steps to join a Wi-Fi network.
- Round 1 · search_documents(quick) “how to connect iPhone to a Wi-Fi network Settings Wi-Fi join network” → 8 chunks (iphone_user_guide.pdf p. 16, 17, 18, 40, 187)
- Round 1 · search_documents(deep) “Wi-Fi settings iPhone join network password” → 16 chunks (iphone_user_guide.pdf p. 17, 40, 41, 16, 187, 15, 52, 45, 27; iphone_16_repair_manual.pdf p. 15)
- Round 2 · think: The user guide gives the steps, so I can answer from the documents now.
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>

### ug_control_center: How do I open Control Center on my iPhone?

Tier: hybrid

Swipe up from the bottom edge of any screen, including the Lock screen [1]. You can also do this when iPhone is locked or when you're using another app [2].

To close Control Center, swipe down, tap the top of the screen, or press the Home button [1].

The guide doesn't describe a different gesture for iPhone models without a Home button, so I can't confirm how it works on those models from these documents.

**Sources**
- [1] iphone_user_guide.pdf, p. 35 ✓ — “Swipe up from the bottom edge of any screen (even the Lock screen).”
- [2] iphone_user_guide.pdf, p. 13 ✓ — “swipe up from the bottom edge of the screen to open Control Center.”

<details><summary>Trace</summary>

- Round 1 · think: Checking your iPhone user guide for how to open Control Center.
- Round 1 · search_documents(quick) “how to open Control Center on iPhone swipe down from top right corner” → 15 chunks (iphone_user_guide.pdf p. 154, 169, 173, 35, 155, 172)
- Round 1 · search_documents(deep) “Control Center iPhone open swipe gesture” → 16 chunks (iphone_user_guide.pdf p. 154, 35, 36, 172, 173, 170, 138, 155, 93, 13)
- Round 2 · think: The guide explains how to open Control Center by swiping up from the bottom edge.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### ug_lost_iphone: I lost my iPhone, what can Find My iPhone do to help me?

Tier: rag

Find My iPhone can help you find and secure a lost iPhone in these ways:

- **Locate it on a map:** You can locate your iPhone on a map [1]. It can also tell you where the phone has been: "iPhone tracks and reports its location, so you can see where it’s been when you check the Find My iPhone app." [2]
- **Play a sound:** "Play a sound at full volume for two minutes, even if the ringer is set to silent." [3]
- **Lost Mode:** "Immediately lock your missing iPhone with a passcode and send it a message displaying a contact number." [4]
- **Erase iPhone:** "Protect your privacy by erasing all the information and media on your iPhone and restoring it to its original factory settings." [5]
- **Activation Lock:** "Find My iPhone includes Activation Lock, which is designed to prevent anyone else from using your iPhone if you ever lose it." [6]

There are two limits to keep in mind. First, the features only work if Find My iPhone was already on before the loss: "To use Find My iPhone features, Find My iPhone must be turned on before your iPhone is lost." [7] Second, if the battery runs out, the phone can still report a last location, but only when "Send Last Location in Settings is turned on." [8]

To use these features, open the Find My iPhone app on another iOS device or go to www.icloud.com/find on a computer [6].

The guide does not describe how to find a phone that is offline or has no battery, and it does not cover newer Find My features.

**Sources**
- [1] iphone_user_guide.pdf, p. 18 ✓ — “Locate your iPhone on a map, display a message, play a sound, lock the screen”
- [2] iphone_user_guide.pdf, p. 46 ✓ — “iPhone tracks and reports its location, so you can see where it’s been when you check the Find My iPhone app.”
- [3] iphone_user_guide.pdf, p. 46 ✓ — “Play a sound at full volume for two minutes, even if the ringer is set to silent.”
- [4] iphone_user_guide.pdf, p. 46 ✓ — “Immediately lock your missing iPhone with a passcode and send it a message displaying a contact number.”
- [5] iphone_user_guide.pdf, p. 46 ✓ — “Protect your privacy by erasing all the information and media on your iPhone and restoring it to its original factory settings.”
- [6] iphone_user_guide.pdf, p. 46 ✓ — “Find My iPhone includes Activation Lock, which is designed to prevent anyone else from using your iPhone if you ever lose it.”
- [7] iphone_user_guide.pdf, p. 46 ✓ — “To use Find My iPhone features, Find My iPhone must be turned on before your iPhone is lost.”
- [8] iphone_user_guide.pdf, p. 46 ✓ — “iPhone sends its last location prior to the battery running out when Send Last Location in Settings is turned on.”

<details><summary>Trace</summary>

- Round 1 · think: Checking your iPhone user guide for what Find My can do when a phone is lost.
- Round 1 · search_documents(quick) “Use Find My iPhone to locate a lost iPhone on a map, play a sound, or enable Lost Mode” → 12 chunks (iphone_user_guide.pdf p. 46, 47, 18, 19, 103, 34)
- Round 1 · search_documents(quick) “Find My iPhone Lost Mode play sound erase iPhone remotely” → 15 chunks (iphone_user_guide.pdf p. 46, 47, 18, 19, 75, 76, 35, 36, 13)
- Round 2 · think: Your guide covers locating, sounding, locking, and erasing the phone, so I have enough to answer.
- Generate: 8 citations
- Verify: 8/8 citations verified

</details>

### ug_burst: How do I take burst photos with the iPhone camera?

Tier: rag

Burst photos take rapid-fire shots while you hold the button:

1. Open Camera and choose **Photo** mode. Burst is available in Square or Photo mode [1].
2. Touch and hold the Take Picture button. "The shutter sound is different, and the counter shows how many shots you’ve taken, until you lift your finger." [2]
3. To choose the shots you keep, tap the thumbnail, then tap **Select**. "The gray dot(s) mark the suggested photos." [3]
4. To keep one photo from the burst as a separate photo, tap the circle in the lower-right corner of that photo [4].
5. To delete the whole burst, tap it, then tap the delete icon [5].

The guide says burst shooting needs an iPhone 5s or later [1]. The guide does not say whether Burst is on by default, how to turn it off, or what the delete icon looks like, because the icon is not in the text I found.

**Sources**
- [1] iphone_user_guide.pdf, p. 94 ✓ — “(iPhone 5s or later) Touch and hold the Take Picture button to take rapid-fire photos in bursts”
- [2] iphone_user_guide.pdf, p. 94 ✓ — “The shutter sound is different, and the counter shows how many shots you’ve taken, until you lift your finger.”
- [3] iphone_user_guide.pdf, p. 94 ✓ — “The gray dot(s) mark the suggested photos.”
- [4] iphone_user_guide.pdf, p. 94 ✓ — “To copy a photo from the burst as a separate photo in your Bursts album in Photos, tap the circle in the lower-right corner of the photo.”
- [5] iphone_user_guide.pdf, p. 94 ✓ — “To delete the burst of photos, tap it”

<details><summary>Trace</summary>

- Round 1 · think: Searching your iPhone guide for how to take burst photos with the camera.
- Round 1 · search_documents(quick) “Take burst photos with the iPhone camera by holding the shutter button or using Volume Up” → 9 chunks (iphone_user_guide.pdf p. 94, 95, 97, 96)
- Round 1 · search_documents(quick) “burst mode camera iPhone take a burst of photos” → 11 chunks (iphone_user_guide.pdf p. 94, 95, 96, 97, 93)
- Round 2 · think: Your guide explains burst shooting clearly, so I can answer without more searching.
- Generate: 5 citations
- Verify: 5/5 citations verified

</details>

### ug_screenshot: How do I take a screenshot of what is on my iPhone screen?

Tier: rag

To take a screenshot, press two buttons at the same time: "Simultaneously press and release the Sleep/ Wake and Home buttons." [1] The screenshot is saved to your Photos app: "The screenshot is added to the Photos tab in Photos and can also be viewed in the Camera Roll album" [2]. The guide describes only the Sleep/Wake plus Home button method. It does not cover iPhone models without a Home button, so check your model's instructions if you do not have one.

**Sources**
- [1] iphone_user_guide.pdf, p. 96 ✓ — “Simultaneously press and release the Sleep/ Wake and Home buttons.”
- [2] iphone_user_guide.pdf, p. 96 ✓ — “The screenshot is added to the Photos tab in Photos and can also be viewed in the Camera Roll album”

<details><summary>Trace</summary>

- Round 1 · think: Searching the iPhone user guide for the screenshot steps.
- Round 1 · search_documents(quick) “how to take a screenshot on iPhone screen side button volume up button” → 15 chunks (iphone_user_guide.pdf p. 170, 171, 173, 154, 96, 172, 93)
- Round 2 · think: Found the screenshot steps in the iPhone guide; answering now.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### ug_force_restart: How do I force restart my iPhone when it will not turn off?

Tier: rag

The user guide covers a normal restart, not a forced one. It says to hold the Sleep/Wake button until the power-off slider appears [1].

The iPhone 16 repair manual mentions forcing a restart, but the retrieved text doesn't include the button sequence [2].

I couldn't find the force-restart button steps in the indexed documents, so I can't give them from these sources. Apple's support site or the iPhone 16 support page would have them.

**Sources**
- [1] iphone_user_guide.pdf, p. 186 ✓ — “Hold down the Sleep/Wake button until the slider appears.”
- [2] iphone_16_repair_manual.pdf, p. 59 ✓ — “force restart the iPhone”

<details><summary>Trace</summary>

- Round 1 · think: Searching both iPhone manuals for the force restart steps.
- Round 1 · search_documents(quick) “how to force restart iPhone when it will not turn off” → 12 chunks (iphone_user_guide.pdf p. 187, 188, 186, 35, 36, 12; iphone_16_repair_manual.pdf p. 37, 28)
- Round 1 · search_documents(quick) “force restart iPhone hold side button and volume button until Apple logo appears” → 15 chunks (iphone_16_repair_manual.pdf p. 59, 60, 63; iphone_user_guide.pdf p. 187, 188, 173, 170, 186)
- Round 2 · think: The guide's method is for Home-button models; I'll check the manual for newer iPhones.
- Round 2 · search_documents(quick) “force restart iPhone 16 press volume up then volume down then hold side button Apple logo” → 15 chunks (iphone_user_guide.pdf p. 170, 171, 173, 154, 186; iphone_16_repair_manual.pdf p. 51, 52, 53, 58)
- Round 3 · think: The indexed guides don't include the force-restart button steps, so I'll say what they do cover.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### rm_thermal_event: What should I do if the battery starts smoking or has a thermal event while I am repairing an iPhone?

Tier: rag

**Signs of a thermal event:** the battery or device may smoke, emit sparks or soot, puff out, or hiss or pop [1][2].

**What to do right away:**
- Smother the battery or device immediately with plenty of clean, dry sand [3].
- Dump all the sand at once, because timing is critical [4].
- Contact local fire authorities if you need further help [5].
- Leave the room for 30 minutes after the reaction is contained, and ventilate the area [6].
- Wait 30 minutes before touching the device [7].
- Wear heat-resistant gloves and safety glasses with side shields to remove the device from the sand [8].
- Wipe the affected area with water first, then with an ESD-safe cleaning solution [9].
- Dispose of the damaged battery or device and any sand debris according to local environmental laws [10].

**Prevention:** fully discharge the battery before you begin a repair [11], and keep a sand container within reach of the workspace [12].

The evidence does not cover what to do if you have no sand, or first aid for injuries.

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 5 ✓ — “The lithium-ion battery or a device that contains one begins to smoke or emit sparks or soot.”
- [2] iphone_16_repair_manual.pdf, p. 5 ✓ — “The battery pouch suddenly and quickly puffs out.”
- [3] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do smother the battery or device immediately with plenty of clean, dry sand.”
- [4] iphone_16_repair_manual.pdf, p. 5 ✓ — “Dump the sand all at once.”
- [5] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do contact local fire authorities if further assistance is needed.”
- [6] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do leave the room for 30 minutes after the reaction is contained. Ventilate the area.”
- [7] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do wait 30 minutes before touching the device.”
- [8] iphone_16_repair_manual.pdf, p. 5 ✓ — “Wear the heat-resistant gloves and safety glasses with side shields to remove the device from the sand.”
- [9] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do wipe the affected area with water first.”
- [10] iphone_16_repair_manual.pdf, p. 5 ✓ — “Do dispose of the damaged battery or device (including any debris removed from the sand) according to local environmental laws and guidelines.”
- [11] iphone_16_repair_manual.pdf, p. 5 ✓ — “Fully discharge the battery before you begin a repair.”
- [12] iphone_16_repair_manual.pdf, p. 4 ✓ — “Sand container within reach (2 feet) on both sides of the workspace”

<details><summary>Trace</summary>

- Round 1 · think: I'll search both manuals for battery safety and overheating steps during repair.
- Round 1 · search_documents(quick) “iPhone 16 battery swelling smoking overheating thermal event during repair safety procedure” → 15 chunks (iphone_16_repair_manual.pdf p. 4, 5, 143, 144, 145, 146, 55, 87, 56; iphone_user_guide.pdf p. 183, 184)
- Round 1 · search_documents(quick) “iPhone 16 battery damaged handling precautions stop repair fire hazard dispose” → 12 chunks (iphone_16_repair_manual.pdf p. 143, 144, 145, 107, 108, 146, 148, 85; iphone_user_guide.pdf p. 183)
- Round 2 · think: The manuals cover the thermal-event response well, so I'll answer now.
- Generate: 12 citations
- Verify: 12/12 citations verified

</details>

### rm_broken_glass: What protective gear do I need before repairing an iPhone with a broken display glass?

Tier: rag

Before repairing an iPhone 16 with broken display glass, the manual says to put on safety glasses with side shields and cut-resistant gloves [1]. The same tool list also includes a display protective cover and an ESD-safe vacuum cleaner for removing glass pieces [2]. The evidence does not list any other protective gear for this step.

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 7 ✓ — “Put on safety glasses with side shields and the cut-resistant gloves.”
- [2] iphone_16_repair_manual.pdf, p. 7 ✓ — “Display protective cover ESD-safe vacuum cleaner”

<details><summary>Trace</summary>

- Round 1 · think: I'll check the iPhone 16 repair manual for the protective gear required when handling broken display glass.
- Round 1 · search_documents(quick) “iPhone 16 broken display glass safety protective gear required before repair” → 15 chunks (iphone_16_repair_manual.pdf p. 170, 171, 7, 8, 10, 107, 108, 143, 183, 56)
- Round 1 · search_documents(quick) “Broken Glass Safety iPhone 16 safety glasses cut-resistant gloves display repair” → 14 chunks (iphone_16_repair_manual.pdf p. 7, 10, 107, 108, 170, 171, 143, 8, 87)
- Round 2 · think: The manual's broken display glass steps list the protective gear, so I can answer from it directly.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### rm_diagnostics_requirements: What do I need to run Apple Diagnostics for Self Service Repair on an iPhone?

Tier: rag

- **Device to test:** an iPhone 12 or later that can turn on and start up in iOS [1].
- **Software:** iOS 17 or later is required to run it in a web browser [2]. Refer to the update instructions and keep the device's software up to date [3].
- **Secondary device:** you need a separate device with a web browser and internet access to act as the diagnostic console [4]. Supported browsers include Chrome, Firefox, or Edge on a PC, for example "A PC with Chrome 55 or later, Firefox 59 or later, or Microsoft Edge 12 or later" [5].
- **Wi-Fi:** the device being tested needs a Wi-Fi connection [6].
- **Before you start:** unplug all accessories [7], remove any case or cover [8], and write down the device serial number [9].
- **Diagnostics mode:** press and hold both volume buttons while plugging the device into a power adapter [10][11].

The evidence does not describe any additional tools or costs for this procedure.

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 21 ✓ — “An iPhone 12 or later to be tested that can turn on and start up in iOS.”
- [2] iphone_16_repair_manual.pdf, p. 21 ✓ — “iOS 17 or iPadOS 17 or later to run Apple Diagnostics for Self Service Repair on a web browser.”
- [3] iphone_16_repair_manual.pdf, p. 21 ✓ — “Refer to Update your iPhone or iPad for instructions to update the device.”
- [4] iphone_16_repair_manual.pdf, p. 16 ✓ — “a separate, secondary device with a web browser and internet access.”
- [5] iphone_16_repair_manual.pdf, p. 22 ✓ — “A PC with Chrome 55 or later, Firefox 59 or later, or Microsoft Edge 12 or later”
- [6] iphone_16_repair_manual.pdf, p. 22 ✓ — “A Wi-Fi connection on the device to be tested”
- [7] iphone_16_repair_manual.pdf, p. 22 ✓ — “Unplug all accessories from the device.”
- [8] iphone_16_repair_manual.pdf, p. 22 ✓ — “Remove any case or cover from the device.”
- [9] iphone_16_repair_manual.pdf, p. 22 ✓ — “Write down the device serial number.”
- [10] iphone_16_repair_manual.pdf, p. 18 ✓ — “Press and hold both the volume up and volume down buttons.”
- [11] iphone_16_repair_manual.pdf, p. 18 ✓ — “plug the device into a 20W or higher power adapter”

<details><summary>Trace</summary>

- Round 1 · think: I need to search the repair manual for what Apple Diagnostics for Self Service Repair requires.
- Round 1 · search_documents(quick) “Apple Diagnostics Self Service Repair requirements to run diagnostics on iPhone” → 11 chunks (iphone_16_repair_manual.pdf p. 21, 22, 16, 17, 18)
- Round 1 · search_documents(quick) “Apple Diagnostics Self Service Repair iPhone 16 what you need before running diagnostics” → 11 chunks (iphone_16_repair_manual.pdf p. 21, 22, 16, 17, 18)
- Round 2 · think: The manual lists the device, software, and secondary-device requirements, so I can answer from it directly.
- Generate: 11 citations
- Verify: 11/11 citations verified

</details>

### rm_reuse_screws: Can I reuse the old screws when I put an iPhone back together?

Tier: rag

No. The repair manual says you should never reuse iPhone screws. Install only new screws during reassembly [1]. The screws are covered with an adhesive that can't be reused [1]. Each repair comes with screw trays that include all the new screws needed for that repair [2]. The manual's repair steps also call for new screws, such as "one new trilobe screw (923- 11712)" for the bottom speaker [3].

The documents do not cover the specific steps for every model or every screw type, so check the screw tray for the exact count and placement for your repair.

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 73 ✓ — “Never reinstall a screw after it has been removed. Install only new screws. iPhone screws are covered with an adhesive that canʼt be reused.”
- [2] iphone_16_repair_manual.pdf, p. 76 ✓ — “Screw trays include all the new screws needed for each repair.”
- [3] iphone_16_repair_manual.pdf, p. 158 ✓ — “install one new trilobe screw (923- 11712) into the bottom speaker.”

<details><summary>Trace</summary>

- Round 1 · think: I'll search the repair manual for guidance on reusing screws during iPhone reassembly.
- Round 1 · search_documents(quick) “reuse screws reassembly iPhone 16 replace screws do not reuse” → 15 chunks (iphone_16_repair_manual.pdf p. 73, 74, 75, 76, 158, 159, 160, 161, 169, 170, 171, 153, 148, 56)
- Round 1 · search_documents(quick) “iPhone 16 security screws replacement reinstall screws torque reassembly” → 15 chunks (iphone_16_repair_manual.pdf p. 73, 74, 75, 76, 153, 154, 155, 156, 158, 159, 160, 161, 85, 56, 169)
- Round 2 · think: Evidence covers the manual's warnings and screw-tray notes, but not the bottom-speaker or microphone steps fully; the rules are clear enough to answer now.
- Generate: 3 citations
- Verify: 3/3 citations verified

</details>

### rm_flex_cable_bend: How far may I bend back the flex cables when removing the USB-C connector from the iPhone 16?

Tier: rag

The manual says not to bend the flex cables back more than 90 degrees. The caution appears in the USB-C connector removal steps, next to the logic board screw removal [1].

The caution is attached to steps that refer to the flex cables on the logic board, so the documents don't say whether the same limit applies to the USB-C connector flex cable itself. The removal step for that cable says to "lift the end of the USB-C connector flex cable as shown" but gives no bend angle [2]. Follow the 90-degree limit as the safest guidance, and check the manual's diagrams for the exact motion.

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 200 ✓ — “Donʼt bend back the flex cables more than 90 degrees.”
- [2] iphone_16_repair_manual.pdf, p. 206 ✓ — “Lift the end of the USB-C connector flex cable as shown”

<details><summary>Trace</summary>

- Round 1 · think: The manual likely covers the USB-C connector's flex cable limits, so I'll search it quickly and in depth.
- Round 1 · search_documents(quick) “iPhone 16 USB-C connector flex cable removal bend back limit” → 14 chunks (iphone_16_repair_manual.pdf p. 110, 111, 112, 113, 206, 207, 208, 199, 200, 201, 202, 43, 85, 209)
- Round 1 · search_documents(quick) “iPhone 16 USB-C connector flex cable do not bend degrees removal” → 14 chunks (iphone_16_repair_manual.pdf p. 110, 111, 112, 113, 206, 207, 208, 85, 86, 87, 43, 209; iphone_user_guide.pdf p. 186)
- Round 2 · think: The manual gives a 90-degree limit for flex cables in the USB-C connector removal steps. I'll answer with that and note the limits of the evidence.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### rm_part_blue_torque_driver: What is the part number of the blue torque driver (0.65 kgf cm) in the iPhone 16 tools list?

Tier: hybrid

The indexed repair manual lists the tool as "Torque driver (blue, 0.65 kgf cm)" in the top speaker tool list [1], but none of the retrieved passages give a part number for it. The manual points to a separate full tools list for all repairs [2], and that list is not among the retrieved passages, so the part number may be there. I can't confirm the part number from the evidence I have.

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 130 ✓ — “3. Torque driver (blue, 0.65 kgf cm)”
- [2] iphone_16_repair_manual.pdf, p. 170 ✓ — “Tools Refer to a full list of tools required for all repairs.”

<details><summary>Trace</summary>

- Round 1 · think: The part number for the blue torque driver should be in the manual's tools list, so I'll search for it exactly and by meaning.
- Round 1 · search_documents(deep) “blue torque driver (0.65 kgf cm) iPhone 16 tools list part number” → 16 chunks (iphone_16_repair_manual.pdf p. 130, 131, 132, 133, 170, 171, 184, 185, 186, 187, 107, 160, 199, 155)
- Round 1 · search_documents(quick) “iPhone 16 torque driver blue 0.65 kgf cm tools required” → 15 chunks (iphone_16_repair_manual.pdf p. 199, 200, 201, 202, 184, 185, 186, 187, 130, 131, 132, 133, 160, 150, 73)
- Round 2 · think: The manual names the blue torque driver but gives no part number, so I'll report that.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### rm_part_grounding_spring_screw: What is the part number of the grounding spring screw for the iPhone 16?

Tier: rag

The iPhone 16 repair manual lists the grounding spring screw part number as 923-11184 [1]. The same screw appears as "10 grounding springs 923-11184" in the parts list [2]. The evidence does not say which specific repair step uses this screw.

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 75 ✓ — “Grounding spring screw part number: 923-11184”
- [2] iphone_16_repair_manual.pdf, p. 68 ✓ — “10 grounding springs 923-11184”

<details><summary>Trace</summary>

- Round 1 · think: I'll search the repair manual for the grounding spring screw part number, using both deep and quick searches.
- Round 1 · search_documents(quick) “iPhone 16 grounding spring screw part number” → 15 chunks (iphone_16_repair_manual.pdf p. 74, 75, 76, 78, 68, 69, 70, 71, 79, 80, 81, 82, 158, 155, 150)
- Round 1 · search_documents(quick) “grounding spring screw iPhone 16 repair manual part number” → 14 chunks (iphone_16_repair_manual.pdf p. 74, 75, 76, 78, 79, 80, 81, 82, 155, 156, 157, 150, 123, 158)
- Round 2 · think: The manual gives the grounding spring screw part number directly, so I can answer now.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### rm_adjustable_torque_range: What is the torque range of the adjustable torque driver used for screws outlined in black/green?

Tier: rag

The adjustable torque driver used for screws outlined in black/green has a range of **10–34 Ncm** [1]. The manual's tool list also gives this range for the driver [2].

**Sources**
- [1] iphone_16_repair_manual.pdf, p. 75 ✓ — “Use the adjustable torque driver (10–34 Ncm) for screws outlined in black/green.”
- [2] iphone_16_repair_manual.pdf, p. 79 ✓ — “Adjustable torque driver (10–34 Ncm)”

<details><summary>Trace</summary>

- Round 1 · think: I'll search the repair manual for the adjustable torque driver range used with black/green screws.
- Round 1 · search_documents(quick) “adjustable torque driver screws outlined in black/green iPhone 16” → 15 chunks (iphone_16_repair_manual.pdf p. 184, 185, 186, 187, 73, 74, 75, 76, 199, 200, 201, 202, 85, 150, 170)
- Round 1 · search_documents(quick) “adjustable torque driver (10–34 Ncm) for screws outlined in black/green” → 15 chunks (iphone_16_repair_manual.pdf p. 75, 76, 78, 79, 167, 168, 169, 170, 83, 84, 85, 137, 152, 165)
- Round 2 · think: The manual gives the adjustable driver's range as 10–34 Ncm; I have the quotes I need.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### know_usb: What does USB stand for?

Tier: knowledge

*Answered from the model's general knowledge; no documents or web sources were consulted.*

USB stands for **Universal Serial Bus**. It is a standard for connecting devices to computers and for transferring data and power.

<details><summary>Trace</summary>

- Round 1 · think: USB is a well-known term, so I can answer directly from general knowledge.

</details>

### know_ram: What does RAM stand for in a computer?

Tier: knowledge

*Answered from the model's general knowledge; no documents or web sources were consulted.*

RAM stands for **Random Access Memory**. It is the computer's short-term working memory, where data and programs in active use are stored so the processor can reach them quickly.

<details><summary>Trace</summary>

- Round 1 · think: RAM is a common computing term, so I can answer directly from general knowledge.

</details>

### know_boiling_point: At what temperature in Celsius does water boil at sea level?

Tier: knowledge

*Answered from the model's general knowledge; no documents or web sources were consulted.*

Water boils at **100 °C** (212 °F) at sea level, at standard atmospheric pressure of 1 atmosphere.

<details><summary>Trace</summary>

- Round 1 · think: This is a well-known physical fact, so I can answer directly from general knowledge.

</details>

### web_newest_iphone: What is the newest iPhone model Apple sells right now?

Tier: web

The most recent source I found lists the iPhone 18 Pro and Pro Max as current Apple models [1]. It also says the iPhone Duo is upcoming, not yet sold, and that a regular iPhone 18 is not expected until spring 2027 [1]. Another guide calls the iPhone 17 series the newest lineup [2], so the sources conflict. The 2026 listing is the more recent of the two, but I could not confirm current availability on Apple's own store, so check apple.com for the final answer.

**Sources**
- [1] [Every iPhone Apple Sells in 2026: Complete Lineup and Buying Guide](https://applescoop.org/story/every-iphone-apple-sells-2026-complete-lineup-buying-guide) ✓ — “Apple's current U.S. lineup contains six families: iPhone 16, iPhone 17e, iPhone 17, iPhone Air, iPhone 18 Pro and Pro Max, and the upcoming iPhone Duo”
- [2] [What is the Latest iPhone? A Complete Guide to Apple’s iPhone 17 Lineup in 2026](https://www.macobserver.com/tips/round-ups/what-is-the-latest-iphone/) ✓ — “The newest iPhone lineup is the iPhone 17 series, consisting of the iPhone 17, iPhone Air, iPhone 17 Pro, and iPhone 17 Pro Max”

<details><summary>Trace</summary>

- Round 1 · think: Checking Apple's current lineup online, since my own knowledge may be out of date.
- Round 1 · search_web(web) “Apple iPhone lineup currently sold on apple.com newest iPhone model available now” → 5 chunks (https://applescoop.org/story/every-iphone-apple-sells-2026-complete-lineup-buying-guide; https://www.macobserver.com/tips/round-ups/what-is-the-latest-iphone/)
- Round 2 · think: Two sources disagree, so I'll report the newer 2026 listing and flag the conflict.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### web_latest_ios: What is the latest public version of iOS available today?

Tier: web

iOS 27 is the newest major iOS release I found. A September 2026 article said Apple announced that it "will launch next Monday, September 14" [1]. Wikipedia's iOS 26 page lists iOS 27 as its successor [2]. The sources do not confirm the latest iOS 27 point release or build number as of today, so check Settings > General > Software Update on your iPhone for the exact current version.

**Sources**
- [1] [iOS 27: Here are Apple’s full release notes - 9to5Mac](https://9to5mac.com/2026/09/09/ios-27-here-are-apples-full-release-notes/) ✓ — “Today Apple announced that iOS 27 will launch next Monday, September 14.”
- [2] [iOS 26 - Wikipedia](https://en.wikipedia.org/wiki/IOS_26) ✓ — “Preceded by iOS 18 Succeeded by iOS 27”

<details><summary>Trace</summary>

- Round 1 · think: Latest iOS release changes often, so I'll check current web sources.
- Round 1 · search_web(web) “latest public iOS version released by Apple for iPhone, current release and update notes” → 5 chunks (https://9to5mac.com/2026/09/09/ios-27-here-are-apples-full-release-notes/; https://en.wikipedia.org/wiki/IOS_26)
- Round 2 · think: iOS 27 appears to be the newest major release; I'll note what I could not confirm.
- Generate: 2 citations
- Verify: 2/2 citations verified

</details>

### web_apple_revenue: How much revenue did Apple report in its most recent quarterly earnings?

Tier: web

Apple's most recent quarterly results were for the fiscal 2026 fourth quarter, which ended September 26, 2026. Apple reported quarterly revenue of $114.5 billion, up 12 percent year over year [1]. The evidence does not cover revenue by product line or by region.

**Sources**
- [1] [Apple reports fourth quarter results - Apple](https://www.apple.com/newsroom/2026/11/apple-reports-fourth-quarter-results/) ✓ — “The Company posted quarterly revenue of $114.5 billion, up 12 percent year over year.”

<details><summary>Trace</summary>

- Round 1 · think: Earnings figures change each quarter and the manuals won't have them, so I'll search the web.
- Round 1 · search_web(web) “Apple most recent quarterly earnings revenue results” → 5 chunks (https://www.apple.com/newsroom/2026/11/apple-reports-fourth-quarter-results/; https://www.apple.com/newsroom/2025/10/apple-reports-fourth-quarter-results/; https://www.marketbeat.com/earnings/reports/2026-7-30-apple-inc-stock/)
- Round 2 · think: The latest press release gives the answer, so I can respond now.
- Generate: 1 citations
- Verify: 1/1 citations verified

</details>
