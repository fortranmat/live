# YouTube Live Stream Template (Relaxing / Sleep / Meditation)

Starter file structure for running and scaling a relaxing music livestream channel.

## Folder Structure

```text
live/
├── .env.example
├── 01_branding/
│   ├── channel-art/
│   ├── logos/
│   ├── thumbnails/
│   └── README.md
├── 02_audio/
│   ├── licenses/
│   ├── mastered/
│   ├── tracks_looped/
│   ├── tracks_raw/
│   └── README.md
├── 03_visuals/
│   ├── backgrounds/
│   ├── loops/
│   ├── overlays/
│   └── README.md
├── 04_stream_setup/
│   └── obs/
│       ├── filters/
│       │   └── README.md
│       ├── profiles/
│       │   └── README.md
│       └── scenes/
│           └── README.md
├── 05_automation/
│   ├── scheduler/
│   │   └── stream_schedule_template.csv
│   └── scripts/
├── 06_monetization/
│   ├── gumroad/
│   ├── links/
│   └── products/
│       └── product_catalog_template.md
├── 07_content_plan/
│   ├── descriptions/
│   │   └── description_template.md
│   ├── themes/
│   └── titles/
│       └── title_ideas.md
├── 08_operations/
│   ├── analytics/
│   ├── checklists/
│   │   ├── post_stream_checklist.md
│   │   └── pre_stream_checklist.md
│   └── logs/
│       └── stream_log.md
├── 09_legal/
│   ├── disclaimers/
│   │   └── health_disclaimer.md
│   └── music_licenses/
├── 10_archive/
│   └── past_streams/
└── 11_user_input/
    ├── audio/
    ├── images/
    ├── output/
    └── README.md
```

## Quick Start

1. Copy `.env.example` to `.env` and fill values.
2. Add audio into `02_audio/tracks_raw/`, then export loops to `02_audio/tracks_looped/`.
3. Put visual loops/backgrounds in `03_visuals/`.
4. Export OBS profiles/scenes into `04_stream_setup/obs/`.
5. Use `08_operations/checklists/pre_stream_checklist.md` before going live.

## Notes

- Keep music license proofs in `02_audio/licenses/` and `09_legal/music_licenses/`.
- Store product and monetization links in `06_monetization/`.
- Log every stream in `08_operations/logs/stream_log.md` to improve consistency.

## Build Long Video from MP3 + Image(s)

1. Put exactly one MP3 in `11_user_input/audio/`.
2. Put one or more images in `11_user_input/images/`.
3. Run:

```bash
python3 05_automation/scripts/build_live_video.py --project-root . --hours 8 --hold-seconds 12 --output-name live_8h_1080p.mp4
```

Output video is saved to `11_user_input/output/`.

### 10-Minute Sample

```bash
bash 05_automation/scripts/make_10min_sample.sh
```

## OBS Runtime Note

- If you stream directly from OBS, OBS must stay running for the full live duration (1h, 8h, etc.).
- If you upload a pre-rendered long video and run a scheduled/premiere-style workflow, your local OBS runtime is not required for that playback.
