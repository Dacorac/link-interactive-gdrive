import os
import datetime
import sys
import time
import subprocess
import requests
import base64
import io

async def create_blob_from_base64(image_base64):
    image_bytes = base64.b64decode(image_base64)

    try:
        with io.BytesIO(image_bytes) as image_bytes_io:
            blob = image_bytes_io.getvalue()
            return blob

    except Exception as e:
        raise RuntimeError("Failed to create Blob from base64 image:", str(e)) from e

def capture_image():
    # call the .sh to capture the image
    image_data = subprocess.check_output(['/home/pi/link-interactive-webcam/webcam.sh'], stderr=subprocess.STDOUT, text=True)

    # generate a timestamped filename
    currentdate = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    rel_path = currentdate + ".jpg"

    # construct the full file path
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, rel_path)

    print('Image data')
    print(image_data)

    return abs_file_path, image_data

def upload_image(image_data):
    try:
        headers = {'Content-Type': 'image/jpeg'}
        files = {'image': ('image.jpg', image_data)}
        response = requests.post('http://localhost:3000/upload', headers=headers, files=files)
        response.raise_for_status() # Raise an exception for non-200 status codes

        data = response.json()
        print('Image uploaded:', data)
        return data

    except requests.exceptions.RequestException as error:
        print('Error uploading image:', error)
        raise

    except Exception as error:
        print('Error taking picture:', error)
        raise

async def main():
    # capture image
    abs_file_path, image_data = capture_image()

    # convert image to blob
    blob = await create_blob_from_base64(image_data)

    # upload image
    upload_image(image_data)

    # print the response
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())