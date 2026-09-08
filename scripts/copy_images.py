import shutil
import os

source_dir = "/Users/t.anh/.gemini/antigravity-ide/brain/4709b981-ff2b-4ed7-bc3a-86a274a9c99f"
dest_dir = "/Users/t.anh/Downloads/BÁO CÁO THỰC TẬP NHÓM 10/image"

mapping = {
    "ptit_logo_1780373859565.png": "image1.png",
    "fpt_logo_1780373904001.png": "image2.png",
    "sgon_org_chart_1780373923474.png": "image3.png",
    "corp_org_chart_1780373950314.png": "image4.png",
    "fb_insights_nov_2w_1780373973873.png": "image5.png",
    "fin_perf_charts_1780374002313.png": "image6.png",
    "fb_insights_dec_2w_1780374022932.png": "image7.png",
    "fb_insights_nov_4w_1780374042275.png": "image8.png",
    "fb_insights_jan_2w_1780374075021.png": "image9.png",
    "fb_insights_jan_4w_1780374105707.png": "image10.png",
    "fb_insights_dec_4w_1780374140605.png": "image11.png",
    "similarweb_nov_jan_1780374169052.png": "image12.png",
    "similarweb_channels_nov_jan_1780374197304.png": "image13.png",
    "similarweb_28days_1780374230003.png": "image14.png",
    "similarweb_channels_jan_1780374255581.png": "image15.png"
}

# Create backup directory in workspace
backup_dir = "/Users/t.anh/.gemini/antigravity-ide/scratch/goha-seo-main/tmp/backup"

os.makedirs(backup_dir, exist_ok=True)

print("Starting file copy operation...")

for src_name, dest_name in mapping.items():
    src_path = os.path.join(source_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    
    if os.path.exists(src_path):
        # Backup original if it exists and backup doesn't have it yet
        orig_backup_path = os.path.join(backup_dir, dest_name)
        if os.path.exists(dest_path) and not os.path.exists(orig_backup_path):
            shutil.copy2(dest_path, orig_backup_path)
            print(f"Backed up original {dest_name} to backup directory")
            
        shutil.copy2(src_path, dest_path)
        print(f"Successfully copied {src_name} -> {dest_name}")
    else:
        print(f"Warning: source file {src_name} not found!")

print("All copies completed.")
