import os
import subprocess
import requests
import re 

def capture_image():
  # call the .sh to capture the image
  try:
    '/home/pi/link-interactive-webcam/webcam.sh' 
    output = subprocess.check_output(['/home/pi/link-interactive-webcam/webcam.sh'], stderr=subprocess.STDOUT, text=True)

    match = re.search(r"'([^']*)'", output)

    if match:
      image_data = match.group(1)
      print(image_data)  
    else:
      print("The desired string was not found in the provided shell command.")

    # Extract the path
    rel_path = image_data.split('/')[-1]

    # Print the path
    print(rel_path)

    return image_data, rel_path
  except Exception as e:
      raise RuntimeError(str(e)) from e

async def upload_image(image_data):
  try:
    # Assuming `image_data` contains the file path or binary data of the image
    files = {'image': open(image_data, 'rb')}  # Use 'image' instead of 'file'

    response = requests.post('http://localhost:3000/upload', files=files)

    # Check the reponse status
    if response.status_code == 200:
      print('The file has been uploaded successfully.')
      os.remove(image_data) # Remove local image when successful
    else:
      print('There is an unexpected error while uploading the file: ', response.status_code)

<<<<<<< Updated upstream
        data = response.json()
        
        print('Image uploaded:', data)
        os.remove(image_data)
        return data
=======
    data = response.json()
    print('Image uploaded:', data)
    return data
>>>>>>> Stashed changes

  except requests.exceptions.RequestException as error:
    print('Error uploading image:', error)
    raise

  except Exception as error:
    print('Error taking picture:', error)
    raise

async def main():
  # capture image
  image_data, rel_path = capture_image()

  await upload_image(image_data)

if __name__ == "__main__":
  import asyncio
  asyncio.run(main())