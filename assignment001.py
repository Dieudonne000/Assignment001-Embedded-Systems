import os
import time
import shutil
import subprocess

# Folders
camera_folder = "captures"  # Folder to monitor (update this to your camera's folder path)
uploaded_folder = "uploaded"  # Separate folder to store uploaded images

# Create the 'uploaded' folder if it doesn't exist
if not os.path.exists(uploaded_folder):
    os.makedirs(uploaded_folder)

# URL for uploading
upload_url = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"

# Function to upload an image using curl
def upload_image(file_path):
    try:
        # Construct the curl command
        command = [
            "curl", "-X", "POST", upload_url,
            "-F", f"imageFile=@{file_path}"
        ]
        
        # Execute the curl command
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Check if the upload was successful
        if result.returncode == 0:
            print(f"Successfully uploaded: {file_path}")
            return True
        else:
            print(f"Failed to upload {file_path}: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")
        return False

# Function to monitor the folder
def monitor_and_upload():
    while True:
        try:
            # List all files in the folder
            files = [f for f in os.listdir(camera_folder) if os.path.isfile(os.path.join(camera_folder, f))]
            
            for file_name in files:
                file_path = os.path.join(camera_folder, file_name)

                # Wait 30 seconds before processing the file
                time.sleep(30)

                # Upload the file
                if upload_image(file_path):
                    # Move the file to the 'uploaded' folder
                    shutil.move(file_path, os.path.join(uploaded_folder, file_name))
                    print(f"Moved {file_name} to the 'uploaded' folder.")
        except Exception as e:
            print(f"Error: {e}")

        # Wait before checking the folder again
        time.sleep(5)

# Start monitoring the folder
if __name__ == "__main__":
    print("Monitoring folder for new images...")
    monitor_and_upload()
