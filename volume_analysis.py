from pydub import AudioSegment
import scipy.fftpack as sf
import numpy as np
import pysptk.sptk
import queue
import sys
import os

class TimeNode:
	def __init__(self, start, end):
		self.start = start
		self.end = end

def create_q():
	a = TimeNode(0, 10)
	b = TimeNode(10, 15)
	c = TimeNode(15, 20)
	q = queue.Queue()
	q.put(a)
	q.put(b)
	q.put(c)
	return q

def loudness(q):
	audio = AudioSegment.from_file(os.getcwd() + '/output.flac')
	if(not audio):
		print('no audio found with that name')
		sys.exit(1)

	size = q.qsize()
	dBs = []
	for i in range (0, size):
		node = q.get()
		#Pydub slicing is in ms, so multiply all times by 1000 
		start = node.start * 1000
		end = node.end * 1000
		slice = audio[start:end]
		
		length = slice.duration_seconds
		max_dB = slice.max_dBFS
		dB = slice.dBFS
		dBs.append(dB)
		return dBs
		'''	
		sample_freq = 16000
		hop_size = 1
		pitch = pysptk.sptk.rapt(slice, sample_freq, hop_size, otype='pitch')
		print (pitch)
	
q = create_q()
loudness(q)
		'''
