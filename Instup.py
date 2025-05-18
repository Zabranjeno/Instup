from instagrapi import Client
import os
import time

# Instagram credentials
USERNAME = "your_instagram_username"
PASSWORD = "your_instagram_password"

# Folder containing media files
MEDIA_FOLDER = "media_folder"
# Caption for all posts (customize as needed)
CAPTION = "Posted via Python script! #Instagram #Automation"

def login_to_instagram():
    """Log in to Instagram and return client object."""
    cl = Client()
    try:
        cl.login(USERNAME, PASSWORD)
        print("Logged in successfully!")
        return cl
    except Exception as e:
        print(f"Login failed: {e}")
        return None

def upload_media(client, file_path, caption):
    """Upload a single media file to Instagram."""
    try:
        # Check file extension to determine media type
        ext = os.path.splitext(file_path)[1].lower()
        if ext in [".jpg", ".jpeg", ".png"]:
            # Upload photo
            client.photo_upload(file_path, caption=caption)
            print(f"Uploaded photo: {file_path}")
        elif ext == ".mp4":
            # Upload video
            client.video_upload(file_path, caption=caption)
            print(f"Uploaded video: {file_path}")
        else:
            print(f"Unsupported file type: {file_path}")
    except Exception as e:
        print(f"Failed to upload {file_path}: {e}")

def bulk_upload():
    """Bulk upload all media files in the specified folder."""
    client = login_to_instagram()
    if not client:
        return

    # Ensure media folder exists
    if not os.path.exists(MEDIA_FOLDER):
        print(f"Media folder '{MEDIA_FOLDER}' not found!")
        return

    # Get all files in the folder
    media_files = [f for f in os.listdir(MEDIA_FOLDER) if os.path.isfile(os.path.join(MEDIA_FOLDER, f))]

    if not media_files:
        print("No media files found in the folder!")
        return

    print(f"Found {len(media_files)} media files to upload.")

    # Upload each file
    for idx, file in enumerate(media_files, 1):
        file_path = os.path.join(MEDIA_FOLDER, file)
        print(f"Uploading {idx}/{len(media_files)}: {file}")
        upload_media(client, file_path, CAPTION)
        # Add delay to avoid rate limits (adjust as needed)
        time.sleep(10)

    print("Bulk upload completed!")
    client.logout()

if __name__ == "__main__":
    bulk_upload()