from pydub import AudioSegment
import scipy.fftpack as sf
import numpy as np
import queue
import sys
import os


def loudness(q):
	audio = AudioSegment.from_file(os.getcwd() + '/output.flac')
	if(not audio):
		print('no audio found with that name')
		sys.exit(1)

	size = q.qsize()
	dBs = []
	for i in range (0, size):
		node = q.pop()
		#Pydub slicing is in ms, so multiply all times by 1000 
		start = node.start * 1000
		end = node.end * 1000
		slice = audio[start:end]
		
		length = slice.duration_seconds
		max_dB = slice.max_dBFS
		dB = slice.dBFS
		dBs.append(dB)
	
	return dBs
	

def pitch(q):
	pitches = []
	'''
	Iterate through time slices
		Run autocorellation w/ FFT
		Extract pitches from max peaks
		Update pitches list
	'''
	return pitches
