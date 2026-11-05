# Test corpus sources

PDFs live in `data/manuals/` (gitignored, not committed). Both come from apple.com domains. Downloaded 2026-11-06.

## 1. iphone_user_guide.pdf

- Title: iPhone User Guide for iOS 8.4 Software
- URL: https://cdsassets.apple.com/live/6GJYWVAV/user/ma1724_iphone_user_guide.pdf
- Pages: 196 (physical page N = printed page N, so question page numbers match the printed numbers)
- Size: 25,661,881 bytes (24.5 MiB)
- Downloaded: 2026-11-06 (unmodified original from Apple)
- Note: this is the newest iPhone User Guide that Apple still publishes as a PDF. Apple retired
  manuals.info.apple.com (it now redirects to support.apple.com/docs) and publishes the iOS 15 to 27
  guides only as web pages and Apple Books. The iOS 4 to iOS 8.4 PDFs are on cdsassets.apple.com, and iOS 8.4
  is the latest of them. Features added after iOS 8.4 (Face ID, Emergency SOS, force restart with volume buttons)
  are therefore not in this PDF.

## 2. iphone_16_repair_manual.pdf

- Title: iPhone 16 Repair Manual (Apple Self Service Repair, Manual ID GKPFXT), print-rendered
- URL: https://support.apple.com/en-us/120652 (manual contents page). Apple no longer offers repair-manual PDFs
  (the old manuals.info.apple.com iPhone 12/13 repair PDFs now redirect), so this PDF was built from Apple's official
  HTML manual: each of the 27 manual pages was printed to PDF with headless Chrome and concatenated in table-of-contents order.
  Images were downsampled to about 900 px at JPEG quality 45 to cut 163 MB to 10 MB. Text is unchanged.
- Pages: 214
- Size: 10,200,292 bytes (9.7 MiB)
- Downloaded and built: 2026-11-06
- Pages included (https://support.apple.com/en-us/<id>): 120623 Introduction, 100299 Battery Safety, 104942 Broken Glass Safety,
  101964 Quick Checks, 101965 Apple Diagnostics for Self Service Repair, 101969 Battery/Charging/Power, 101967 Camera,
  101966 Display, 101968 Sound, 101970 Mechanical, 120648 Internal View/Orderable Parts/Exploded View, 120649 Screws,
  120983 Tools, 100300 First Steps, 104039 SIM Tray, 119969 Heated Display Removal Fixture Operating Manual,
  120638 Back Glass, 120639 Camera, 120640 Top Speaker, 120641 TrueDepth Camera, 120642 Battery, 120643 Taptic Engine,
  120644 Bottom Speaker, 120645 Main Microphone, 120646 Display, 120654 Enclosure, 120655 USB-C Connector.
- Caveat: page text is Chrome print output, so image-heavy pages (for example part tables) extract with a different
  reading order than the web page. Part numbers sit directly above their part names on the page.
