import os
import datetime
import subprocess
import requests
import base64
import io
import re 

# def create_blob_from_base64(image_base64):
#     try:
#         # Add padding if necessary
#         padded_base64 = image_base64 + '=' * (-len(image_base64) % 4)
        
#         # Decode the base64 string
#         image_bytes = base64.b64decode(padded_base64)
        
#         # Convert the bytes to a blob
#         with io.BytesIO(image_bytes) as image_bytes_io:
#             blob = image_bytes_io.getvalue()
#             return blob
#         # image_bytes = base64.b64decode(image_base64)
#         # with io.BytesIO(image_bytes) as image_bytes_io:
#         #     blob = image_bytes_io.getvalue()
#         #     return blob

#     except Exception as e:
#         raise RuntimeError("Failed to create Blob from base64 image:", str(e)) from e

def capture_image():
    # call the .sh to capture the image
    try:
        '/home/pi/link-interactive-webcam/webcam.sh' 
        output = subprocess.check_output(['/home/pi/link-interactive-webcam/webcam.sh'], stderr=subprocess.STDOUT, text=True)
        # output = subprocess.check_output(['/home/juliangonzalez/Documentos/link-interactice-gdrive-py/webcam.sh'], stderr=subprocess.STDOUT, text=True) #JULI

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

        print('Image data')
        print(image_data)

        return image_data, rel_path
    except Exception as e:
        raise RuntimeError(str(e)) from e

async def upload_image(image_data):
    try:
        # Assuming `image_data` contains the file path or binary data of the image
        files = {'image': open(image_data, 'rb')}  # Use 'image' instead of 'file'

        response = requests.post('http://localhost:3000/upload', files=files)

        # Verificar el resultado de la solicitud
        if response.status_code == 200:
            print('El archivo se ha enviado exitosamente.')
        else:
            print('Hubo un problema al enviar el archivo:', response.status_code)

        data = response.json()
        
        print('Image uploaded:', data)
        os.remove(image_data)
        return data

    except requests.exceptions.RequestException as error:
        print('Error uploading image:', error)
        raise

    except Exception as error:
        print('Error taking picture:', error)
        raise

async def main():
    # capture image
    image_data, rel_path = capture_image()

    # convert image to blob
    # blob = create_blob_from_base64(image_data)
    # upload image
    await upload_image(image_data)

    # print the response
    print()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())