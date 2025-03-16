import os
import cv2

# Path to the extracted frames
frames_dir = "sign_language_data/datasets/Custom/frames"
output_dir = "sign_language_data/datasets/Custom/processed_frames"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Resize dimensions
IMG_SIZE = (224, 224)

def resize_frames():
    if not os.path.exists(frames_dir):
        print(f"Error: Frames directory '{frames_dir}' not found.")
        return

    for img_name in os.listdir(frames_dir):
        img_path = os.path.join(frames_dir, img_name)
        img = cv2.imread(img_path)
        
        if img is None:
            print(f"Warning: Skipping {img_name} (Not a valid image)")
            continue
        
        img_resized = cv2.resize(img, IMG_SIZE)
        output_path = os.path.join(output_dir, img_name)
        cv2.imwrite(output_path, img_resized)

    print("✅ Frames resized and saved successfully.")

if __name__ == "__main__":
    resize_frames()
