#!/bin/bash

IMAGES_DIR="../_images"
POSTS_DIR="_posts"

DATE=$(date +"%Y-%m-%d")
TIME=$(date +"%H:%M:%S")
POST_FILE="$POSTS_DIR/$DATE-image-gallery.md"

mkdir -p "$POSTS_DIR"

echo "Creating $POST_FILE"

cat <<EOF > "$POST_FILE"
---
title: "Image Gallery"
date: $DATE $TIME
layout: post
---

EOF

# Loop through images (jpg, jpeg, png, webp, gif)
find "$IMAGES_DIR" -type f \( \
  -iname "*.jpg" -o \
  -iname "*.jpeg" -o \
  -iname "*.png" -o \
  -iname "*.webp" -o \
  -iname "*.gif" \
\) | sort | while read -r img; do
  echo "![${img##*/}](/$img)" >> "$POST_FILE"
  echo "" >> "$POST_FILE"
done

echo "Done. All images added to one post."
