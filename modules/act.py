#! /usr/bin/env python
# encoding: utf-8
# -*- coding: utf8 -*-

from RPLCD.gpio import CharLCD
import requests, os, subprocess, time, base64
import speech_recognition as sr
from lxml import html
from gtts import gTTS



def ripeti(frase):
	tts = gTTS(text=unicode(frase),lang="it")
	tts.save("output.mp3")
	with open(os.devnull, 'wb') as devnull:
		subprocess.call(['mplayer', 'output.mp3'], stdout=devnull, stderr=subprocess.STDOUT)

def find_num(nome, citta):
	lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])
	
	stringa='{"CurrentPage":1,"RecordsPerPage":0,"CountryCode":null,"BusinessType":2,"SortBy":null,"SearchTerm":null,"SearchLocation":"'+citta+'","ResidentialSearchTerm":"'+nome+'","SearchCategories":null,"CategoryCode":null,"CategoryLevel":0,"IsMeta":false,"Latitude":"37.9418631","Longitude":"15.3624647","Order08":"083089","Order09":null,"NearBy":null,"StrictLocation":false,"CategorySearch":false,"TopCitiesNumber":0,"TopCitiesArea":0,"TopCategoriesNumber":0,"TopCompetitorsNumber":0,"TopCompetitorsArea":0,"ValidForEncryption":false,"LocationWithProvince":false}'
	tok=base64.b64encode(bytes(stringa))
	url = "https://www.infobel.com/it/italy/Search/ResidentialResults"
	querystring = {"token":tok}
	headers = {
		'Cache-Control': "no-cache",
		'Postman-Token': "d1e4a0ee-fe5f-44ff-8164-296623e2a9af"
		}
	response = requests.request("GET", url, headers=headers, params=querystring)

	tree = html.fromstring(response.content)
	nom = tree.xpath('//h1[@class="customer-item-name"]//a/text()')
	tel = tree.xpath('//span[@class="customer-info-detail"]//span[@class="detail-text"]/text()')
	add = tree.xpath('//span[@class="customer-info-detail highlighted address"]//span[@class="detail-text"]/text()')

	i=0
	k=0
	for key in nom:
		k+=1
	if (k>0):
		if (k==1):
			ripeti("c'e una persona con questo nome")
		else:
			ripeti('ci sono '+str(k)+'persone con questo nome')
		for key in nom:
			''.join(e for e in nom[i] if e.isalnum())
			''.join(f for f in tel[i] if f.isalnum())    
			tel[i]=tel[i].strip()
			lcd.write_string(nom[i])
			lcd.cursor_pos = (1, 0)
			lcd.write_string(tel[i])
			ripeti(nom[i]+" "+ tel[i])
			time.sleep(1)
			i+=1
	else:
		ripeti('Mi dispiace non trovo la persona che cerchi')
