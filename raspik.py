#! /usr/bin/env python
# encoding: utf-8
# -*- coding: utf8 -*-

# sudo apt-get install mplayer portaudio19-dev libcurl3-gnutls libcurl4-gnutls-dev libc6 libgnutls30 libssl-dev alsamixer pulse audio twinkle
# pip install SpeechRecognition
# pip install pyaudio
# pip install gtts
# pip install google-api-python-client
# pip install setuptools
# pip install pycurl

#RIPRODUZIONE SU RASP
# wget http://omxplayer.sconde.net/builds/omxplayer_0.3.7~git20170130~62fb580_armhf.deb
# dpkg -i mxplayer_0.3.7~git20170130~62fb580_armhf.deb            (  sudo apt-get -f install  ) if you have problem with dependencies

from RPLCD.gpio import CharLCD
from modules import act
from gtts import gTTS
import sys, os, subprocess,urllib, pycurl, time
import speech_recognition as sr

def rec():
  with sr.Microphone() as source:
    #s.system('clear')
    print("Parla!")
    audio = r.listen(source, phrase_time_limit=3)
    r.adjust_for_ambient_noise(source)
    try:
      data=r.recognize_google(audio, language="it-IT")
      print("Hai detto: " + data)
    except sr.UnknownValueError:
      data=""
    except sr.RequestError as e:
      print("Non si capisce un cazzo; {0}".format(e))
      fase(1)
  return data
  
def fase(a):
  d=''
  i=0
  if (a==1):
    lcd.clear()
    lcd.write_string("      zZz....zZz")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("(^_^)")
    while (d!='stop'):
      if(d=='ciao peppino'):
        fase(2)
      elif(d=='chiudi peppino'):
        act.ripeti("telefonata terminata")
        os.system('twinkle --cmd "bye"')
        fase(1)
      else:
        d=rec().lower()
    act.ripeti("Addio")
    exit()
  elif (a==2):
    lcd.clear()
    lcd.write_string("Puoi parlare...")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("....ti ascolto")
    act.ripeti("Ciao Maura, cosa posso fare per te?")
    while (d!='stop'):
      d=rec().lower()
      if(d=='saluta'):
        act.ripeti('vaffanculo')
        lcd.clear()
        lcd.write_string("VAFFANCULO")
        fase(1)
      elif(d=='che ore sono'):
        t1= time.localtime(time.time())
        lcd.clear()
        lcd.write_string("Sono le ore :")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("%s" %time.strftime("%H:%M:%S"))
        act.ripeti("sono le ore "+str(t1.tm_hour)+"e"+str(t1.tm_min)+"minuti")
        time.sleep(2)
        fase(1)
      elif(d=='chiama'):
        act.ripeti('chi devo chiamare?')
        nom=rec().lower()
        if (nom=='cristian'):
          lcd.clear()
          lcd.write_string("Sto chiamando...")
          lcd.cursor_pos = (1, 0)
          lcd.write_string("....Cristian")
          os.system('twinkle --cmd "call sip:+393456819655@sip.linphone.org"')
          time.sleep(3)
          fase(1)
        elif(nom=='antonella'):
          lcd.clear()
          lcd.write_string("Sto chiamando...")
          lcd.cursor_pos = (1, 0)
          lcd.write_string("...Antonella")
          os.system('twinkle --cmd "call sip:+393806972730@sip.linphone.org"')
          fase(1)
        elif(nom=='claudia'):
          lcd.clear()
          lcd.write_string("Sto chiamando...")
          lcd.cursor_pos = (1, 0)
          lcd.write_string("....Claudia")
          os.system('twinkle --cmd "call sip:+41762969098@sip.linphone.org"')
          fase(1)
        else:
          act.ripeti("il numero non esiste")
          fase(1)
      elif(d=='ricerca'):
        act.ripeti('chi devo cercare?')
        nom=rec()
        lcd.clear()
        lcd.write_string(nom[:16])
        act.ripeti('dove si trova?')
        cit=rec()
        lcd.cursor_pos = (1, 0)
        lcd.write_string(cit[:16])
        act.find_num(nom, cit)
        fase(1)
      elif(i>5):
        act.ripeti("ritorno a riposare")
        fase(1)
      else:
        i+=1
    act.ripeti("Addio")
    exit()

try:
  lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])
  with open(os.devnull, 'wb') as devnull:
    subprocess.Popen(['twinkle','-f cristian -c'], stdout=subprocess.PIPE, universal_newlines=True)  
  r=sr.Recognizer()
  fase(1)
except KeyboardInterrupt:
  lcd.clear()

