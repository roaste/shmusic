from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip, ffmpeg_extract_audio
import random
import vk_api
import os
import sys
import requests
import json
import re
from bs4 import BeautifulSoup
from acrcloud.recognizer import ACRCloudRecognizer


class backend():
	'''Бэкэнд сайта'''
	def __init__(self, request):
		'''Инициализация реквест запроса'''
		self.request = request 
		self.name = self.generate_name()
		self.result = ''
	def generate_name(self):
		'''Генерация имени файла'''
		generate_array = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j', 'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
		name = ''
		for i in range(40):
			name += generate_array[random.randint(0, len(generate_array) - 1)]
		return name 


	def valid_time(self, time):
		'''Валидация времени'''
		timespl = time.split(':')
		if len(timespl) != 2:
			return 'error'
		else:
			try:
				time1 = int(timespl[0])
				time2 = int(timespl[1])
			except:
				return 'error'
			if time1 <= 59 and time1 >= 0 and time2 <= 59 and time2 >= 0:
				return 'ok'
			else:
				return 'error' 


	def validator(self):
		'''Валидация'''
		if 'timeof' in self.request.GET and 'timeto' in self.request.GET and 'link' in self.request.GET:
			timeof = self.request.GET['timeof']
			timeto = self.request.GET['timeto']
			timeofvalid = self.valid_time(timeof)
			timetovalid = self.valid_time(timeto)
			if timeofvalid == 'ok' and timetovalid == 'ok':
				time = True
			else:
				return 'time_error'

			if self.request.GET['link'][0: 24] == 'https://www.youtube.com/' and time == True:
				youtube = self.install_youtube()
				if youtube == 'ok':
					check = self.check_music()
					if check == 'ok':
						return 'ok|' + self.result
				elif youtube == 'link_error':
					return 'link_error'
				elif youtube == 'time_error':
					return 'time_error'
				
			elif self.request.GET['link'][0: 17] == 'https://youtu.be/' and time == True:
				youtube = self.install_youtube()
				if youtube == 'ok':
					check = self.check_music()
					if check == 'ok':
						return 'ok|' + self.result
				elif youtube == 'link_error':
					return 'link_error'
				elif youtube == 'time_error':
					return 'time_error'
	
			elif self.request.GET['link'][0: 20] == 'https://vk.com/video' and time == True:
				vk = self.install_vk()
				if vk == 'ok':
					check = self.check_music()
					if check == 'ok':
						return 'ok|' + self.result
				elif vk == 'link_error':
					return 'link_error'
				elif vk == 'time_error':
					return 'time_error'

			elif self.request.GET['link'][0: 26] == 'https://www.instagram.com/' and time == True:
				insta = self.install_insta()
				if insta == 'ok':
					check = self.check_music()
					if check == 'ok':
						return 'ok|' + self.result
				elif insta == 'link_error':
					return 'link_error'
				elif insta == 'time_error':
					return 'time_error'	
			else:
				return 'error'
		else:
			return 'error'

	def install_youtube(self):
		'''Скачивание видео из ютуба'''
		link = self.request.GET['link']
		timeof = self.request.GET['timeof'].split(':')
		timeto = self.request.GET['timeto'].split(':')
		timeof_seconds = int(timeof[0]) * 60 + int(timeof[1])
		timeto_seconds = int(timeto[0]) * 60 + int(timeto[1])
		if timeto_seconds - timeof_seconds > 30 and timeto_seconds - timeof_seconds < 1:
			return 'link_error'
		try:
			stream = YouTube(link).streams.filter(only_audio=True, mime_type='audio/mp4').desc().first().url
			print(stream)
		except:
			return 'link_error'
		ffmpeg_extract_subclip(stream, timeof_seconds, timeto_seconds, targetname="audio/{}.mp4".format(self.name))
		return 'ok'

	def install_vk(self):
		'''Скачивание видео из вк'''
		videos = self.request.GET['link'].strip('https://vk.com/video')
		videos = videos.split('?')[0]
		token = 'ae1f79f5b6f3ff797737b9462904dc1c0b531fb8a95e3cff8d8ea45d2dab94fb223ba4a814879dfc7c829'
		vk = vk_api.VkApi(token=token)
		vk._auth_token()
		video_url = vk.method("video.get", 
		{
		'videos' : videos,
		'extended': True,
		})	
		if len(video_url['items']) > 0:
			url = video_url['items'][0]['files']['mp4_240']
		else:
			return 'link_error'
		timeof = self.request.GET['timeof'].split(':')
		timeto = self.request.GET['timeto'].split(':')
		timeof_seconds = int(timeof[0]) * 60 + int(timeof[1])
		timeto_seconds = int(timeto[0]) * 60 + int(timeto[1])
		if timeto_seconds - timeof_seconds > 30 and timeto_seconds - timeof_seconds < 1:
			return 'time_error'
		ffmpeg_extract_subclip(url, timeof_seconds, timeto_seconds, targetname="audio/{}.mp4".format(self.name))# + '000'
		# ffmpeg_extract_audio("audio/{}.mp4".format(self.name + '000'), "audio/{}.mp4".format(self.name), bitrate=3000, fps=44100)
		# path = os.path.join(os.path.abspath(os.getcwd()), 'audio/{}.mp4'.format(self.name + '000'))
		# os.remove(path)
		return 'ok'

	def install_insta(self):
		'''Скачивание видео из инстаграма''' 
		link_to_video = self.request.GET['link']
		response = requests.get(link_to_video)
		text_for_parser = response.content
		text_for_parser = str(text_for_parser)
		regxp =  '(http[^"]+mp4)'
		result = []
		result = re.findall(regxp, text_for_parser)
		try:
			url = result[0]
		except:
			return 'link_error'
		timeof = self.request.GET['timeof'].split(':')
		timeto = self.request.GET['timeto'].split(':')
		timeof_seconds = int(timeof[0]) * 60 + int(timeof[1])
		timeto_seconds = int(timeto[0]) * 60 + int(timeto[1])
		if timeto_seconds - timeof_seconds > 30 and timeto_seconds - timeof_seconds < 1:
			return 'time_error'
		link = link_to_video.split('?')[0] + '?__a=1'
		response = requests.get(link_to_video).text
		soup = BeautifulSoup(response, 'lxml')
		for heading in soup.find_all(re.compile("^script")):
			if heading.text.strip()[0:18] == 'window._sharedData':
				arr_link = heading.text.strip('window._sharedData = ').split('video_url')[1].split('"')[2].strip().split('\\u0026')
				url = ''
				for i in arr_link:
					url += i + '&'
		ffmpeg_extract_subclip(url, timeof_seconds, timeto_seconds, targetname="audio/{}.mp4".format(self.name))
		return 'ok'

	def check_music(self):
		'''Проверка музыки'''
		config = {
		    'host': 'identify-eu-west-1.acrcloud.com',
		    'access_key': 'a18a4f6a76f4a6edf47e3204266f8692',
		    'access_secret': 'iGKRisfMUvAex9mFKTlOloMPPqf3BrMmfxjzL85g',
		    'debug': False,
		    'timeout': 10,
		}
		
		acrcloud = ACRCloudRecognizer(config)
		
		data = acrcloud.recognize_by_file(file_path = 'audio/{}.mp4'.format(self.name), start_seconds = 0)
		data = json.loads(data)
		path = os.path.join(os.path.abspath(os.getcwd()), 'audio/{}.mp4'.format(self.name))
		os.remove(path)
		try:
			name_artist = data['metadata']['music'][0]['artists'][0]['name']
			name_song = data['metadata']['music'][0]['title']
			self.result = str(name_artist) + ' - ' + str(name_song)
			return 'ok'
		except:
			result_error = data['status']['msg']
			if result_error == 'Missing/Invalid Access Key':
				self.result = 'Ошибка на стороне сервера'
				return 'ok'
			elif result_error == 'No result':
				self.result = 'Песня не найдена'
				return 'ok'