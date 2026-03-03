#!/usr/bin/env bash
set -euo pipefail

python3 05_automation/scripts/build_live_video.py \
  --project-root . \
  --hours 0.1667 \
  --hold-seconds 12 \
  --output-name sample_10min_1080p.mp4

echo "Created: 11_user_input/output/sample_10min_1080p.mp4"
