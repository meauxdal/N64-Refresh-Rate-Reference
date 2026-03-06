# N64 Timing Reference — Deduplicated Source List
*Generated 2026-03-05. Canonical URLs only; duplicates, redundant archived versions, and bare search queries removed.*

---

## Broadcast Standards (Official/Authoritative)

- https://www.itu.int/rec/R-REC-BT — ITU-R BT index
- https://www.itu.int/rec/r-rec-bt.470/en — BT.470-6: NTSC/PAL lines, fields/sec, subcarrier frequencies
- https://www.itu.int/rec/R-REC-BT.1700/en — BT.1700: composite video signal levels, timing, sync
- https://www.itu.int/rec/R-REC-BT.1701/en — BT.1701: horizontal/vertical timing for composite video
- https://en.wikipedia.org/wiki/NTSC
- https://en.wikipedia.org/wiki/PAL
- https://en.wikipedia.org/wiki/PAL-M
- https://www.telecomponents.com/html/ntsc.htm
- https://www.telecomponents.com/html/pal.htm
- https://martin.hinner.info/vga/pal.html — community PAL timing reference (R. Salmon 1996); 288-line PAL progressive
- https://web.archive.org/web/20160512200958/http://www.pembers.freeserve.co.uk/World-TV-Standards/ — VBI/HBI amplitude diagrams, PAL 625-line field sync
- https://web.archive.org/web/20160427050012/http://www.pembers.freeserve.co.uk/World-TV-Standards/Line-Standards.html
- https://web.archive.org/web/20160502235024/http://www.pembers.freeserve.co.uk/World-TV-Standards/Colour-Standards.html
- https://web.archive.org/web/20160428232400/http://www.pembers.freeserve.co.uk/World-TV-Standards/Transmission-Systems.html
- https://www.ntsc-tv.com/
- https://danalee.ca/ttt/analog_video.htm
- https://web.archive.org/web/20171123052456/http://www.vcolor.com.br/nova/sistemas.htm
- https://web.archive.org/web/20140405033622/http://www.dtv.org.br/fndc-os-numeros-da-tv-digital-referencias-historicas/
- https://batc.org.uk/wp-content/uploads/ATVCompendium.pdf — Mike Wooding ATV Compendium; PAL-M fS = 227.25 × fH
- https://handwiki.org/wiki/Engineering:Colorburst
- https://handwiki.org/wiki/Raster%20scan
- https://handwiki.org/wiki/Raster%20graphics

---

## Nintendo Official Documentation & SDKs

- https://ultra64.ca/ — hub for all official SDK docs
- https://ultra64.ca/files/documentation/online-manuals/man-v5-2/allman52/ — OS 2.0L v5.2 online manuals
- https://ultra64.ca/files/documentation/online-manuals/functions_reference_manual_2.0i/home.html — Functions Reference Manual OS 2.0I
- https://ultra64.ca/files/documentation/online-manuals/functions_reference_manual_2.0i/os/osViSetMode.html — osViSetMode
- https://ultra64.ca/files/documentation/online-manuals/man/pro-man/start/index.html — Programming Manual OS 2.0J
- https://ultra64.ca/files/documentation/nintendo/Nintendo_64_Programming_Manual_NU6-06-0030-001G_HQ.pdf — Programming Manual REV G
- https://drive.google.com/drive/folders/1kGlB2TyX7CsmPnSyzpxGcSKpJ1F-ywal — System Service Manual NUS-06-0014-001 REV A
- https://frds.github.io/oman-archive — OMAN archive description
- https://jrra.zone/n64/doc/ — mirror of allman52 (dupe of ultra64.ca)
- https://web.archive.org/web/20161122235657/https://n64squid.com/Nintendo%20Ultra64%20Programming%20Manual+Addendums.pdf — archived addendum

---

## Schematics & Hardware

- https://github.com/RWeick/NUS-CPU-03-Nintendo-64-Motherboard — NUS-CPU-03 KiCAD schematic (primary hardware reference)
- https://kicanvas.org/?repo=https%3A%2F%2Fgithub.com%2FRWeick%2FNUS-CPU-03-Nintendo-64-Motherboard — KiCanvas viewer
- https://wiki.console5.com/tw/images/a/a2/N64_NUS-CPU-03.pdf — RDC NUS-CPU-03/04 schematic PDF
- https://forums.modretro.com/threads/schematic-nus-cpu-04-ntsc-1996-1997.11227/ — RDC schematic thread

---

## Datasheets

- https://www.datasheets360.com/part/detail/mx8350/-7133688394404043430/ — Macronix MX8350 dual clock synthesizer
- https://www.datasheets360.com/part/detail/mx8330mc/-2428964985180354578/ — Macronix MX8330MC single clock synthesizer
- *(local)* MX9911MC datasheet (PM0463 REV. 1.2, AUG 12 1997) — Macronix MX9911MC single clock synthesizer; functionally equivalent to MX8330MC
- *(local)* Rohm BA7242F datasheet — ENC-NUS (U5); YOUT/VOUT/COUT; SCIN level; NT/PAL logic
- *(local)* Mitsumi PST91XX datasheet — U3 voltage supervisor/reset IC; PST9128 variant identified on NUS-CPU-03
- https://www.alldatasheet.com/datasheet-pdf/view/93083/MITSUMI/PST9128.html — PST9128 datasheet (alldatasheet)
- *(local)* TI SN74LV125A datasheet — U8 quad bus buffer (LC125); CSYNC buffering on early revisions
- https://people.ece.cornell.edu/land/courses/ece4760/ideas/saa1101.pdf — SAA1101 sync generator; corroborates PAL-M fS = 227.25 × fH
- https://web.archive.org/web/20160707115958/http://www.datasheetarchive.com/dl/Scans-064/DSA2IH00157976.pdf — RDRAM RAC timing (1/8 RCLK relationship)
- https://utsource.net/itm/p/260745.html — Rohm 178M05 (voltage regulator) datasheet hunt
- https://upup.utsource.net/pdfjs/index.html?pdf/17/173425_ROHM_178M18CP — Rohm 178Mxx family sheet (possibly correct)
- https://wiki.console5.com/wiki/BA6596F — S-RGB A (BA6596F) pinout ASCII

### Failed datasheet hunts (BU9801F / VDC-NUS)
- https://www.worldwayelec.com/pro/mill-max-mfg-corp/bu9801f/3619554
- https://www.alldatasheet.net/view.jsp?Searchword=BU9801F
- https://www.excesschip.cn/product/details/BU9801F
- https://www.jotrin.com/product/parts/BU9801F

---

## Patents

- https://patents.google.com/patent/US6556197B1/en — Programmable Video Timing Registers
- https://patents.google.com/patent/US4054919A/en — Video Image Positioning Control
- https://patents.google.com/patent/US6454652B2/en
- https://patents.google.com/?inventor=Shigeru+Miyamoto
- https://patents.google.com/?q=(video)&assignee=Nintendo+Co.%2c+Ltd.&num=100&oq=assignee:(Nintendo+Co.%2c+Ltd.)+video&sort=old&page=2&clustered=true

---

## Board Revisions & Component Identification

- https://forums.modretro.com/threads/nintendo-64-motherboard-revisions-serials-info-request.1417/ — Link83 et al; primary revision/serial reference
- https://forums.benheck.com/viewtopic.php?f=58&t=27684 — Ben Heck Forums mirror of Link83 thread
- https://consolemods.org/wiki/N64:N64_Model_Differences — revision summary (cites io55.net)
- https://io55.net/wiki/eop/video_game_consoles-home/5th_generation/nintendo_64
- https://nfggames.com/forum2/index.php?topic=3083.0 — kwyjibo et al; NUS-CPU(R)-01 / French PAL / S-RGB A
- https://nfggames.com/forum2/index.php?msg=21925 — NUS-CPU(R)-01 board image
- https://nfggames.com/forum2/index.php?topic=3525.0 — datasheet links thread; BA7242F identification
- https://nfggames.com/forum2/index.php?topic=5223.0 — CPU upgrade investigation (RobIvy64)
- https://web.archive.org/web/20170107112600/http://nfggames.com/forum2/index.php?topic=5223.0 — archived version with Ultra 64 Dev Board image
- https://web.archive.org/web/20150926190309/http://nintendo64.wikia.com/wiki/NUS-CPU(P)-01
- https://web.archive.org/web/20141114122131/http://nintendo64.wikia.com:80/wiki/NUS-CPU(P)-02
- https://web.archive.org/web/20141103210228/http://nintendo64.wikia.com:80/wiki/NUS-CPU(P)-03
- https://web.archive.org/web/20140316153804/http://nintendo64.wikia.com:80/wiki/NUS-CPU-02
- https://web.archive.org/web/20141123084430/http://nintendo64.wikia.com:80/wiki/NUS-CPU-03
- https://web.archive.org/web/20141026032754/http://nintendo64.wikia.com:80/wiki/NUS-CPU-05
- https://web.archive.org/web/20141102082931/http://nintendo64.wikia.com:80/wiki/NUS-CPU-05-1
- https://web.archive.org/web/20160417025559/http://nintendo64.wikia.com/wiki/NUS-CPU-06
- https://web.archive.org/web/20160419054350/http://nintendo64.wikia.com/wiki/NUS-CPU-07
- https://web.archive.org/web/20141028010439/http://nintendo64.wikia.com/wiki/NUS-CPU-08
- https://web.archive.org/web/20160414201604/http://nintendo64.wikia.com:80/wiki/NUS-CPU-08-1
- https://web.archive.org/web/20141026021843/http://nintendo64.wikia.com:80/wiki/NUS-CPU-09
- https://web.archive.org/web/20160401003207/http://forums.modretro.com/viewtopic.php?f=33&t=1622&p=26734#p26734 — XCVG revision info
- https://web.archive.org/web/20151105192150/http://forums.modretro.com/viewtopic.php?f=33&t=1417 — archived Link83 thread
- https://web.archive.org/web/20241012072747/https://forums.modretro.com/threads/differences-between-ntsc-and-pal-n64s.14138/
- https://web.archive.org/web/20241010145036/https://forums.modretro.com/threads/ntsc-n64-rgb-mod-with-amplifier.11144/ — NUS-CPU-03/04 serial info
- https://www.tapatalk.com/groups/nintendo_64_forever/do-funtastic-consoles-have-better-video-display-t2744-s200.html
- https://gamingdoc.org/repairs/consoles/nintendo-64/components/ — repair component reference
- https://web.archive.org/web/20170626183850/https://circuit-board.de/forum/index.php/Thread/13913-STRIP-CLUB-PCB-Scans/?pageNo=1 — PCB scans including NUS-CPU(P)-01 (German)
- https://circuit-board.de/forum/index.php/Thread/37226-Erledigt-Probleme-mit-S-Video-beim-N64-an-Grundig-R%C3%B6hre/?postID=1108762#post1108762

---

## Motherboard Images

- https://forums.modretro.com/threads/nintendo-64-motherboard-revisions-serials-info-request.1417/ — Link83 (primary)
- https://bitbuilt.net/forums/threads/n64-rev-3-1-compendium.7053/
- https://bitbuilt.net/forums/threads/n64-rev-9-1-compendium.4762/
- https://bitbuilt.net/forums/threads/open64-a-work-in-progress-open-source-n64-motherboard-recreation.6874/
- https://bitbuilt.net/forums/threads/crazygadgets-first-n64-portable-nsight64.5937/
- https://bitbuilt.net/forums/threads/help-with-an-n64-board-no-video-audio-output-no-everdrive64-led-activity.4616/ — clean NUS-CPU-03 photo
- https://bitbuilt.net/forums/threads/first-n64-portable.3231/ — printsmith3d NUS-CPU-05
- https://bitbuilt.net/forums/threads/first-n64-portable-pal.7119/ — Glimmerman PAL board
- https://bitbuilt.net/forums/threads/slow-progress-on-my-first-n64-portable.2020/
- https://bitbuilt.net/forums/threads/ramslot-ramcard.7107/
- https://bitbuilt.net/forums/threads/n64-expansion-paks-ram-part-numbers.3943/ — Miceeno RAM part numbers
- https://nfggames.com/forum2/index.php?msg=21925 — NUS-CPU(R)-01 image
- https://imgur.com/a/B4uPSNF — meauxdal (Elle) motherboard image dump

---

## RGB Mods & Video Output

- http://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html — Tim Worthington N64RGB (original URL, likely dead)
- https://web.archive.org/web/20240430210859/https://members.optusnet.com.au/eviltim/n64rgb/n64rgb.html — archived (canonical archive version)
- https://gamesx.com/wiki/doku.php?id=av:n64rgb-ntsc — Tim Worthington NUS-CPU-03 video circuit schematic
- https://gamesx.com/wiki/doku.php?id=av:n64rgb-amp
- https://gamesx.com/wiki/doku.php?id=av:nintendomultiav — Nintendo Multi-AV connector pinout
- https://consolemods.org/wiki/Nintendo_Multi_Out
- https://consolemods.org/wiki/N64:Connector_Pinouts
- https://consolemods.org/wiki/N64:RGB-Compatible_Systems
- https://retrorgb.com/n64rgbcompatible.html
- https://github.com/borti4938/n64rgb_project_overview
- https://github.com/borti4938/n64adv2_fw
- https://etim.net.au/n64rgb/
- https://etim.net.au/n64rgb/instructions-new/
- https://github.com/mrehkopf/n64rgb
- https://web.archive.org/web/20130130062716/http://free-for-all.ath.cx:80/daten/n64rgbmod.html — QUAKEMASTER NUS-CPU(R)-01 RGB mod (German)
- https://web.archive.org/web/20120830195043/http://www.mmmonkey.co.uk/ntsc-nintendo-64-rgb/ — Mmmonkey RGB mod
- https://web.archive.org/web/20190406032415/http://pakupakustory.blogspot.com/2011/12/docteur-switch-en-direct-de-latelier-le.html — French mod blog (marginal relevance)
- https://web.archive.org/web/20241013224314/https://forums.modretro.com/threads/miceenos-rgb-vga-monitor-n64-portable.15234/
- https://wiki.voultar.com/n64/n64
- https://junkerhq.net/xrgb/index.php?title=Optimal_timings
- https://videogameperfection.com/forums/topic/nintendo-64-de-blur/
- https://web.archive.org/web/20241010145036/https://forums.modretro.com/threads/ntsc-n64-rgb-mod-with-amplifier.11144/

---

## Community Documentation & Wiki

- https://n64brew.dev/ — N64brew wiki hub
- https://n64brew.dev/wiki/Video_Interface
- https://n64brew.dev/wiki/Video_DAC
- https://n64brew.dev/wiki/Libultra
- https://n64.readthedocs.io/ — hardware reference for emulator devs
- https://www.retroreversing.com/n64/
- https://www.retroreversing.com/n64-sdk
- https://www.retroreversing.com/n64-sdk-setup
- https://www.retroreversing.com/n64-3d-modelling
- https://www.retroreversing.com/n64sound
- https://crashoveride95.github.io/modernsdk/index.html
- https://www.copetti.org/writings/consoles/nintendo-64/ — Rodrigo Copetti architecture overview
- https://web.archive.org/web/20260119215039/https://pastebin.com/pJG5SBnW — Zoinkity VI settings Pastebin (237/474 line libultra behavior)
- https://www.moria.us/tags/nintendo-64 — libultra dev blog

---

## SDKs & Libraries

- https://libdragon.dev/
- https://github.com/DragonMinded/libdragon
- https://github.com/DragonMinded/libdragon/blob/trunk/src/vi.h — LEAP register values
- https://github.com/ModernN64SDKArchives/n64sdkmod
- https://github.com/mark-temporary/hkz-libn64 — direct VI register-level mappings
- https://github.com/mikeryan/n64dev

---

## Emulators & FPGA

- https://github.com/ares-emulator/ares/tree/master/ares/n64
- https://github.com/ares-emulator/ares/blob/master/ares/n64/vi/vi.cpp
- https://github.com/mamedev/mame/blob/master/src/mame/nintendo/n64.cpp
- https://github.com/n64dev/cen64
- https://github.com/MiSTer-devel/N64_MiSTer — Robert Peip FPGA VI timing
- *(note: gopher64, RMG, Project64, mupen64plus — no specific URLs yet)*

---

## Test ROMs

- https://github.com/lemmy-64/n64-systemtest
- https://github.com/rasky/n64_pi_dma_test
- https://github.com/PeterLemon/N64

---

## Overclocking / Hardware Research

- https://web.archive.org/web/20170107155232/http://assemblergames.com/l/threads/mapping-n64-overclockability-achieved-3-0x-multiplier-but-not-3-0x-speed.51656/
- http://www.shootersforever.com/forums_message_boards/viewtopic.php?t=6627

---

## Misc / Not Directly Relevant

- https://github.com/TinyRetroWarehouse/PicoCart64
- https://github.com/jombo23/N64-Tools — GoldeneyeVault tools archive
- https://github.com/TinyRetroWarehouse/Awesome-Retro-Docs/blob/master/Consoles/Nintendo%20-%20Super%20Nintendo/pinout_av_multiout.pdf — SNES Multi-Out pinout
- https://web.archive.org/web/20020614123954/http://www.snsys.com/n64.htm — archived SN Systems dev kit page
- https://x.com/hard4games/status/1960445877476098168 — Hard4Games repair docs leak announcement
- https://www.youtube.com/watch?v=2VlSf7d9LJo — Hard4Games repair docs leak video
- https://web.archive.org/web/20140915191434/http://www.nesretro.com/cgi-bin/yabb2/YaBB.pl?num=1354381429 — French forum, duplicate info

---

## Personal / Working Resources

- https://docs.google.com/spreadsheets/d/1A0djJNITvrgbucCVMT6spz2m31yxDv8idIDtCiyBgVs/edit?gid=0#gid=0 — meauxdal (Elle) crystal stamp codes + board revision tracking spreadsheet
- https://imgur.com/a/B4uPSNF — meauxdal (Elle) motherboard image dump

---

## Notes / Still Unresolved

- BU9801F (VDC-NUS) datasheet: not found. All leads exhausted so far.
- Rohm 178M05 datasheet: partial; 178Mxx family sheet may cover it.
- NUS-CPU-06 U7 clock chip: unconfirmed from board photos.
- arthur2425 on N64brew Discord has an MPAL machine (potential test resource).
