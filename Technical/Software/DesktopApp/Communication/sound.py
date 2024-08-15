import pyaudio
import threading
import socket
from tkinter import messagebox
from global_variables import get_audio,set_audio
input_index=0
output_index=0
p = pyaudio.PyAudio()
for ii in range(p.get_device_count()):
	if p.get_device_info_by_index(ii).get('name') == "Microsoft Sound Mapper - Input":
		input_index=ii
	elif p.get_device_info_by_index(ii).get('name') == "Microsoft Sound Mapper - Output":
		output_index=ii


input_stream=p.open(format=pyaudio.paInt16,
				input_device_index=input_index,
				channels=2,
				rate=44100,
				input=True,
				frames_per_buffer=4096,
				)
input_stream.stop_stream()
output_stream=p.open(format=pyaudio.paInt16,
                output_device_index=output_index,
				channels=2,
				rate=44100,
				output=True,
				frames_per_buffer=4096,
				)
output_stream.stop_stream()

def audio_connect(target_ip,target_port,ui):
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((target_ip, target_port))
	except:
		messagebox.showerror("Error!","Audio Not Activated")
		return
	print("connected To Audio")

	receive_thread = threading.Thread(target=receive_server_data,args=[s,ui]).start()
	send_thread = threading.Thread(target=send_server_data,args=[s,ui]).start()
	#send_server_data(s,ui)


def receive_server_data(s,ui):
	output_stream.start_stream()
	while get_audio():
		try:
			data = s.recv(4096)
			if not data:
				break
			output_stream.write(data)

		except:
			pass
	s.close()
	# change audio text if necessary
	output_stream.stop_stream()
	#ui.unlock_audio_button()
	#clear all socket resources



def send_server_data(s,ui):
	input_stream.start_stream()
	while get_audio():
		data = input_stream.read(4096,exception_on_overflow=False)
		s.sendall(data)
	s.close()
	input_stream.stop_stream()
	#ui.unlock_audio_button()
	#clear


#to close stream permanently stream_close and then p.terminate()
