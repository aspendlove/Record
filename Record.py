import pyaudio
import requests

chunk = 320  # Number of frames per audio chunk
sample_format = pyaudio.paInt16  # 16-bit signed integer format
channels = 1  # Mono channel
rate = 16000  # Sample rate of 16000 Hz
seconds = 5

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=rate,
                frames_per_buffer=chunk,
                input=True)

frames = bytearray()  # Initialize array to store frames

# Store data in chunks for 3 seconds
for i in range(0, int(rate / chunk * seconds)):
    data = stream.read(chunk)
    frames.extend(data)

# Stop and close the stream
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording')

# Define the server URL for your POST request
server_url = "http://127.0.0.1:2100/"

# Set headers (optional, but content type can be helpful for the server)
headers = {"Content-Type": "audio/wav", "Connection": "Close"}  # Indicate WAV data

# Send the POST request with the WAV data as the body
response = requests.post(server_url, data=frames, headers=headers)

# Check the response status for success
if response.status_code == 200:
    print("WAV data uploaded successfully!")
else:
    print("Error uploading WAV data:", response.status_code)
    print(response.text)  # Access error message from response body (if applicable)
