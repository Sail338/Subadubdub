import io
import os
import re
import string
import fuzzy
from pydub import AudioSegment
import  script_sanitzer
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import storage



class Node:
    """
        :param words a dictrionary containing the word and its specfic start_time and end time and other word specfic information in the actual script
        :param sentence the sentence that this node represents
        :param start the overall start time of the sentence
        :param end the overall end time of the sentence
    """
    def __init__(self,words,sentence,start,end):
        self.words = words
        self.sentence = sentence
        self.start = start
        self.end = end

def gen_transcript(filename:str,script_path:str):
    """generates a transcript"""
    client = speech.SpeechClient()
    #upload to gcp
    uri_ = upload_to_gcp(filename)
    audio = speech.types.RecognitionAudio(uri=uri_)

    characters, sentences = script_sanitzer.santize(script_path,['*,*','[,]','(,)'])
    phrases_ = [x[0] if  len(x[0]) < 100 else x[0][:100] for x in sentences]
    config = speech.types.RecognitionConfig(
         encoding='FLAC',
         language_code='en-US',
         model='video',
         sample_rate_hertz=16000,
         enable_word_time_offsets=True)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    result_data = operation.result(timeout=1000)
    merged_transcript = ""
    merged_words = []

    for result in result_data.results:
         alternative = result.alternatives[0]
         merged_transcript += alternative.transcript
         for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            word_tup = (word,start_time.seconds + start_time.nanos * 1e-9,end_time.seconds + end_time.nanos * 1e-9)
    #        print('Word: {}, start_time: {}, end_time: {}'.format(
     #           word,
      #          start_time.seconds + start_time.nanos * 1e-9,
       #         end_time.seconds + end_time.nanos * 1e-9))
            merged_words.append(word_tup)
    #santize the script
    print(merged_words)
    empty_queue = []
    transcript_ptr = 0
    start = -1.1
    end = -1.1
    for sentence in sentences:
        print(transcript_ptr)
        start = -1.0
        end = -1.0
        found = False
        for word in sentence[0].split(" "):
            if(found):
                break
            for word2 in merged_words[transcript_ptr:len(sentence[0])]:
                #find start
                if check_words_equal(word,word2[0]):
                    start = word2[1]
                    found = True
                    break
                    
        found = False 
        for word in sentence[0].split(" ")[::-1]:
            if(found):

                break
            for word2 in range(len(merged_words[transcript_ptr:len(sentence)]),-1,-1):
                #find start
                if check_words_equal(word,merged_words[word2][0]):
                    end = merged_words[word2][2]
                    transcript_ptr = word2 + 1
                    found = True
                    break
        if start < 0 or end <0:
            raise Exception
        else:
            empty_queue.append((start,end,sentence))
    print(empty_queue)
        
        

    #search for the first word

def check_words_equal(word1,word2):
    #remove punctuation from word1
    word1_mod = word1.translate(str.maketrans("","",string.punctuation))
    word2_mod = word2.translate(str.maketrans("","", string.punctuation))
    d_meta = fuzzy.DMetaphone()
    #fuzzy match
    return d_meta(word1_mod) == d_meta(word2)

def upload_to_gcp(filename:str):
    """
    Upload to GCP
    """
    storage_client = storage.Client()
    bucket_to_use = storage_client.get_bucket('jakepaulwasamistae')
    blob = bucket_to_use.blob(filename)
    if not blob.exists():
        blob.upload_from_filename(filename)
    #return the file uri
    uri_base = "gs://jakepaulwasamistae/"
    uri = uri_base + filename
    return uri


gen_transcript("parksandrec.flac",'rickandmortyscript.txt')
