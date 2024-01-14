#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

# capture the image
image_data=$(fswebcam -r 1280x720 --no-banner -q /home/pi/$DATE.jpg)

# return the image data
echo $image_data


#ESTO ES PARA LA EJECUCION DE JULI
# DATE=$(date +"%Y-%m-%d_%H%M")

# # capture the image using cheese and save it to a file
# fswebcam /home/juliangonzalez/Documentos/$DATE.jpg

# # return the image file path
# echo "/home/juliangonzalez/Documentos/$DATE.jpg"