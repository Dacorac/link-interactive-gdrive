import socket
import subprocess

buffersize = 1024

serverIP = '10.1.1.3'
severport = 5000

def execute_python_command(command):
  # Run command in shell
  subprocess.call(command, shell=True)

def receive_udp_message_and_execute_python_command():
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

if __name__ == "__main__":
  receive_udp_message_and_execute_python_command()