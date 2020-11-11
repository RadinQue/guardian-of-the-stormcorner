from io import BytesIO
from pyo import *
from os import path
import os
import requests
import subprocess
import pathlib

class SoundFilterer:

	""" Conversion """

	def ffmpeg_convert(self, input_path, output_path):
		subprocess.call([str(pathlib.Path().absolute())+'/ffmpeg.exe', '-i', input_path , output_path , '-y'], shell = True)

	""" Filtering processes """

	async def prepare_audio_file_for_filtering(self):
		self.audio_server = Server(audio="offline")
		
		# retrieving info about the sound
		self.sound_info = sndinfo("temp.wav")

		""" since right now we're bouncing everything to wav anyway this part should be simplified """
		self.sound_duration, self.sampling_rate, self.channels = self.sound_info[1], self.sound_info[2], self.sound_info[3]
		self.sound_file_format = ['WAVE', 'AIFF', 'AU', 'RAW', 'SD2', 'FLAC', 'CAF', 'OGG'].index(self.sound_info[4])
		self.samptype = ['16 bit int', '24 bit int', '32 bit int', '32 bit float', '64 bits float', 'U-Law encoded', 'A-Law encoded'].index(self.sound_info[5])
		
		# setting server parameters
		self.audio_server.setSamplingRate(self.channels)
		self.audio_server.setNchnls(self.sound_channels)
		self.audio_server.boot()
		self.audio_server.recordOptions(dur=self.sound_duration, filename="sound.wav", fileformat=self.sound_file_format, sampletype=self.samptype)
		self.sound_file = SfPlayer("temp.wav")

	async def render_filtered_audio_file(self):
		self.audio_server.start()
		self.audio_server.shutdown()
		del self.sound_file
		self.ffmpeg_convert("sound.wav","sound.mp3")

	def clean_all_temp_files(self):
		possible_temp_files = ["sound.mp3","sound.wav","temp,mp3","temp.wav"]
		for file in possible_temp_files:
			if path.exists(file):
				os.remove(file)

	""" Filters """

	async def add_yoi(self):
		await self.prepare_audio_file_for_filtering();
		lfo = Sine(freq=[.2, .25], mul=.125, add=.5)
		sound_fmed = IRFM(self.sound_file, carrier=5000, ratio=lfo, index=3, order=256).out()
		await self.render_filtered_audio_file();

	async def max_distortion(self):
		await self.prepare_audio_file_for_filtering();
		sound_distorted = Disto(self.sound_file, drive=200, slope=0.1)
		sound_mixed = Interp(self.sound_file, sound_distorted, interp=0.5, mul=0.5).out()
		await self.render_filtered_audio_file();