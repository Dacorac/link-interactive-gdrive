import socket
import subprocess
import time

buffersize = 1024

serverIP = '10.1.1.3'
severport = 5000
retry_number = 0


def execute_python_command(command):
  # Run command in shell
  subprocess.call(command, shell=True)

def receive_udp_message_and_execute_python_command():
  try:
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind to port 5000
    sock.bind((serverIP, severport))

    print('Listening...')

    while True:
      # Waiting for message
      data, addr = sock.recvfrom(buffersize)

      # Decode message 
      command = data.decode('utf-8')

      print(command)
      print(addr[0])
      
      if command == 'hello':
        messageFromServer = 'Hello from server'
      elif command == 'take photo':
        execute_python_command('python3 /home/pi/link-interactive-webcam/webcam.py')
        messageFromServer = 'Webcam script executed.'
      elif command == 'close':
        messageFromServer = 'Bye from server'
        break

      # Send response to client
      bytestosend = messageFromServer.encode('utf-8')
      sock.sendto(bytestosend, addr)

    succesfull_message = "Script exceuted succesfully"
    success_to_send = succesfull_message.encode('utf-8')

    sock.sendto(success_to_send, addr)
  except Exception as ex:
    if retry_number < 5:
      retry_number = retry_number + 1
      time.sleep(10)
      receive_udp_message_and_execute_python_command()
    else :
      error_message = f"An error has ocurred while processing command: {str(ex)}"
      error_to_send = error_message.encode('utf-8')
      retry_number = 0
      sock.sendto(error_to_send, addr)
    
    

if __name__ == "__main__":
  receive_udp_message_and_execute_python_command()