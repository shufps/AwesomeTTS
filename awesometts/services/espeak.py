# -*- coding: utf-8 -*-

#import awesometts.config as config

from PyQt4 import QtGui,QtCore

#Supported Languages       
# code , Language
slanguages = [['af', 'Afrikaans'],
['sq', 'Albanian'],
['hy', 'Armenian'],
['bs', 'Bosnian'],
['ca', 'Catalan'],
['zh-yue', 'Chinese Cantonese'],
['zh', 'Chinese Mandarin'],
['hr', 'Croatian'],
['cs', 'Czech'],
['da', 'Danish'],
['nl', 'Dutch'],
['en', 'English'],
['eo', 'Esperanto'],
['fi', 'Finnish'],
['fr', 'French'],
['ka', 'Georgian'],
['de', 'German'],
['el', 'Greek'],
['grc', 'Greek (Ancient)'],
['hi', 'Hindi'],
['is', 'Icelandic'],
['id', 'Indonesian'],
['it', 'Italian'],
['kn', 'Kannada'],
['ku', 'Kurdish'],
['la', 'Latin'],
['lv', 'Latvian'],
['jbo', 'Lojban'],
['mk', 'Macedonian'],
['no', 'Norwegian'],
['pl', 'Polish'],
['pt', 'Portuguese (Brazil)'],
['pt-pt', 'Portuguese (Europeans)'],
['ro', 'Romanian'],
['ru', 'Russian'],
['sr', 'Serbian'],
['sk', 'Slovak'],
['es', 'Spanish'],
['es-la', 'Spanish - Latin America'],
['sw', 'Swahihi'],
['sv', 'Swedish'],
['ta', 'Tamil'],
['tr', 'Turkish'],
['vi', 'Vietnamese'],
['cy', 'Welsh']]


TTS_ADDRESS = 'http://translate.google.com/translate_tts'


import os, re, subprocess
from anki.utils import stripHTML
from urllib import quote_plus
import awesometts.config as config
import awesometts.util as util
from subprocess import Popen, PIPE, STDOUT


def playEspeakTTS(text, language):
	text = re.sub("\[sound:.*?\]", "", stripHTML(text.replace("\n", "")).encode('utf-8'))
	subprocess.Popen(['espeak', '-v', language, text], stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()

def playfromtagEspeakTTS(fromtag):
	for item in fromtag:
		match = re.match("(.*?):(.*)", item, re.M|re.I)
		playEspeakTTS(match.group(2), match.group(1))

def playfromHTMLtagEspeakTTS(fromtag):
	for item in fromtag:
		text = ''.join(item.findAll(text=True))
		voice = item['voice']
		playEspeakTTS(text, voice)

def get_language_id(language_code):
	x = 0
	for d in slanguages:
		if d[0]==language_code:
			return x
		x = x + 1


def recordEspeakTTS(text, language):
	text = re.sub("\[sound:.*?\]", "", stripHTML(text.replace("\n", "")).encode('utf-8'))
	filename = util.generateRandomName()+'.mp3'
	espeak_exec = subprocess.Popen(['espeak', '-v', language, text, '--stdout'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
	lame_exec = Popen(["lame", "-", filename], stdin=espeak_exec.stdout, stdout = PIPE)
	espeak_exec.stdout.close()
	result = lame_exec.communicate()[0]
	espeak_exec.wait()

	md5fn = util.hashfileMD5(filename)+'.mp3'
	os.rename(filename_mp3, md5fn)	

	return md5fn

def filegenerator_layout(form):
	global DefaultEspeakVoice
	verticalLayout = QtGui.QVBoxLayout()
	textEditlabel = QtGui.QLabel()
	textEditlabel.setText("Language:")
	form.comboBoxEspeak = QtGui.QComboBox()
	form.comboBoxEspeak.addItems([d[0] +' - '+ d[1] for d in slanguages])
	form.comboBoxEspeak.setCurrentIndex(DefaultEspeakVoice) # get Default

	verticalLayout.addWidget(textEditlabel)
	verticalLayout.addWidget(form.comboBoxEspeak)
	return verticalLayout

def recordEspeakTTS_form(form, text):
	global DefaultEspeakVoice
	DefaultEspeakVoice = form.comboBoxEspeak.currentIndex() #set new Default
	return recordEspeakTTS(text, slanguages[form.comboBoxEspeak.currentIndex()][0])

def filegenerator_run(form):
	global DefaultEspeakVoice
	DefaultEspeakVoice = form.comboBoxEspeak.currentIndex() #set new Default
	return recordEspeakTTS(unicode(form.texttoTTS.toPlainText()), slanguages[form.comboBoxEspeak.currentIndex()][0])

def filegenerator_preview(form):
	return playEspeakTTS(unicode(form.texttoTTS.toPlainText()), slanguages[form.comboBoxEspeak.currentIndex()][0])


DefaultEspeakVoice = get_language_id('en')

TTS_service = {'espeak' : {
'name': 'Espeak',
'play' : playEspeakTTS,
'playfromtag' : playfromtagEspeakTTS,
'playfromHTMLtag' : playfromHTMLtagEspeakTTS,
'record' : recordEspeakTTS_form,
'filegenerator_layout': filegenerator_layout,
'filegenerator_preview': filegenerator_preview,
'filegenerator_run': filegenerator_run}}




