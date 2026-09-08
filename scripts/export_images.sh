#!/bin/bash

# Script to copy all high-resolution AI regenerated images to your report folder.
# Run this from your macOS Terminal.

SOURCE_DIR="/Users/t.anh/.gemini/antigravity-ide/brain/4709b981-ff2b-4ed7-bc3a-86a274a9c99f"
DEST_DIR="/Users/t.anh/Downloads/BÁO CÁO THỰC TẬP NHÓM 10/image"

# Create target directory if it doesn't exist
mkdir -p "$DEST_DIR"

echo "Copying high-resolution AI images to report folder..."

cp "$SOURCE_DIR/ptit_logo_1780373859565.png" "$DEST_DIR/image1.png"
cp "$SOURCE_DIR/fpt_logo_1780373904001.png" "$DEST_DIR/image2.png"
cp "$SOURCE_DIR/sgon_org_chart_1780373923474.png" "$DEST_DIR/image3.png"
cp "$SOURCE_DIR/corp_org_chart_1780373950314.png" "$DEST_DIR/image4.png"
cp "$SOURCE_DIR/fb_insights_nov_2w_1780373973873.png" "$DEST_DIR/image5.png"
cp "$SOURCE_DIR/fin_perf_charts_1780374002313.png" "$DEST_DIR/image6.png"
cp "$SOURCE_DIR/fb_insights_dec_2w_1780374022932.png" "$DEST_DIR/image7.png"
cp "$SOURCE_DIR/fb_insights_nov_4w_1780374042275.png" "$DEST_DIR/image8.png"
cp "$SOURCE_DIR/fb_insights_jan_2w_1780374075021.png" "$DEST_DIR/image9.png"
cp "$SOURCE_DIR/fb_insights_jan_4w_1780374105707.png" "$DEST_DIR/image10.png"
cp "$SOURCE_DIR/fb_insights_dec_4w_1780374140605.png" "$DEST_DIR/image11.png"
cp "$SOURCE_DIR/similarweb_nov_jan_1780374169052.png" "$DEST_DIR/image12.png"
cp "$SOURCE_DIR/similarweb_channels_nov_jan_1780374197304.png" "$DEST_DIR/image13.png"
cp "$SOURCE_DIR/similarweb_28days_1780374230003.png" "$DEST_DIR/image14.png"
cp "$SOURCE_DIR/similarweb_channels_jan_original_1780374522104.png" "$DEST_DIR/image15.png"

echo "All images successfully exported to $DEST_DIR"
