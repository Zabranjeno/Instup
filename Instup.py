from instagrapi import Client
import os
import time
import random
import json

# Instagram credentials
USERNAME = "insta_username"
PASSWORD = "insta_password"  # Replace with your password
TWO_FACTOR_CODE = "000000"  # Replace with your 2FA code if needed

# Folder containing media files
MEDIA_FOLDER = "driveltter:/folder/subfolder"
# Caption for all posts
CAPTION = "Posted via Python script! #Instagram #Automation"
# Progress file to track uploaded files
PROGRESS_FILE = "upload_progress.json"
# Maximum uploads per session before pausing
BATCH_SIZE = 10
# Delay range (seconds)
MIN_DELAY = 15
MAX_DELAY = 30

def load_progress():
    """Load progress from file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_progress(uploaded_files):
    """Save progress to file."""
    with open(PROGRESS_FILE, "w") as f:
        json.dump(list(uploaded_files), f)

def login_to_instagram():
    """Log in to Instagram and return client object."""
    cl = Client()
    try:
        cl.login(USERNAME, PASSWORD, verification_code=TWO_FACTOR_CODE)
        print("Logged in successfully!")
        return cl
    except Exception as e:
        print(f"Login failed: {e}")
        return None

def upload_media(client, file_path, caption):
    """Upload a single media file to Instagram."""
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in [".jpg", ".jpeg", ".png"]:
            client.photo_upload(file_path, caption=caption)
            print(f"Uploaded photo: {file_path}")
            return True
        elif ext == ".mp4":
            client.video_upload(file_path, caption=caption)
            print(f"Uploaded video: {file_path}")
            return True
        else:
            print(f"Unsupported file type: {file_path}")
            return False
    except Exception as e:
        print(f"Failed to upload {file_path}: {e}")
        return False

def bulk_upload():
    """Bulk upload media files with batch processing and error handling."""
    client = login_to_instagram()
    if not client:
        return

    if not os.path.exists(MEDIA_FOLDER):
        print(f"Media folder '{MEDIA_FOLDER}' not found!")
        return

    # Load previously uploaded files
    uploaded_files = load_progress()
    media_files = [
        f for f in os.listdir(MEDIA_FOLDER)
        if os.path.isfile(os.path.join(MEDIA_FOLDER, f))
        and f not in uploaded_files
    ]

    if not media_files:
        print("No new media files found in the folder!")
        return

    total_files = len(media_files)
    print(f"Found {total_files} new media files to upload.")

    batch_count = 0
    for idx, file in enumerate(media_files, 1):
        if batch_count >= BATCH_SIZE:
            print("Batch limit reached. Pausing and re-logging in...")
            client.logout()
            time.sleep(60)  # Wait 1 minute before re-login
            client = login_to_instagram()
            if not client:
                print("Re-login failed. Stopping.")
                break
            batch_count = 0

        file_path = os.path.join(MEDIA_FOLDER, file)
        print(f"Uploading {idx}/{total_files}: {file}")
        success = upload_media(client, file_path, CAPTION)

        if success:
            uploaded_files.add(file)
            save_progress(uploaded_files)
            batch_count += 1
        else:
            print(f"Skipping {file} due to upload failure.")

        # Random delay to avoid rate limits
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        print(f"Waiting {delay:.2f} seconds...")
        time.sleep(delay)

    print("Bulk upload completed!")
    client.logout()

if __name__ == "__main__":
    bulk_upload()
