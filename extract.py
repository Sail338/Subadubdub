import io
import os
import re
import string
import fuzzy
import translate
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
    def __init__(self,speaker,sentence,start,end):
        self.sentence = sentence
        self.start = start
        self.end = end
        self.speaker = speaker
    def __repr__(self):
        a = "\n\nSentence: " + self.sentence +  "\nStart:  " + str(self.start) + "\nend: " + str(self.end) + "\nSpeaker: " + self.speaker +"\n\n"
        return a
        

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
    prev_start = start
    prev_end = end
    for sentence in sentences:
        actualSize = findSize(sentence[0])
        print(transcript_ptr)
        prev_start = start
        prev_end = end
        start = -1.0
        end = -1.0
        found = False
        for word in sentence[0].split(" "):
            if word.isspace():
                continue
            if(found):
                break
            for word2 in merged_words[transcript_ptr:transcript_ptr+actualSize]:
                #find start
                if check_words_equal(word,word2[0]):
                    start = word2[1]
                    found = True
                    break
                    
        found = False 
        for word in sentence[0].split(" ")[::-1]:
            print("WORD: "+str(word))
            if word.isspace():
                continue
            if(found):

                break
            for word2 in range(transcript_ptr+actualSize,transcript_ptr-1,-1):
                if(word2 >= len(merged_words)):
                    continue
                print(actualSize)
                print(sentence[0].split(" "))
                #find start
                print(word2)
                print(len(merged_words))
                print("WORD 2:     "+str(merged_words[word2][0]))
                if check_words_equal(word,merged_words[word2][0]):
                    end = merged_words[word2][2]
                    transcript_ptr = word2 + 1
                    found = True
                    break
        #Could not find the correct start or end times for first and last words
        #Time to estimate!
        if start < 0 or end <0:
            '''
               We know that, if all previous sentences were calculated correctly,
               The start and end time of this sentence must be after the previous
               end time of the last sentence (somewhere near the first word after the last sentence)
               or 0 if its the first sentence. Once we have the start we will calculate the average
               talking speed (wpm) of the characters. Using this speed we can define a low ball
               estimate for how long the sentence that couldnt be defined will take, allowing us
               to define the end time. If this is the first sentence we will attempt to use the
               average persons wpm (150 wpm).
            '''

            #No previous sentences 
            if len(empty_queue) == 0:
                start = merged_words[0][1]
                end = actualSize * (14/6)
                transcript_ptr = actualSize - int(actualSize*1/4)
            else:
                start = merged_words[transcript_ptr][1]
                avg_wpm = findAverageWPM(empty_queue)
                end = actualSize * avg_wpm
                transcript_ptr += actualSize - int(actualSize * 1/4)


            
        else:
            #create nodes
            node_to_add = Node(sentence[1],translate.translate_phrase(sentence[0],'de'),start,end)
            empty_queue.append(node_to_add)
    print(empty_queue)
        
        

    #search for the first word
def findAverageWPM(queue):
    words = 0
    total_time = 0.0
    for x in empty_queue:
        total_time += abs(x.end - x.start)
        words += findSize(x.sentence)
    return words/total_time



def check_words_equal(word1,word2):
    #remove punctuation from word1
    word1_mod = word1.translate(str.maketrans("","",string.punctuation))
    word2_mod = word2.translate(str.maketrans("","", string.punctuation))
    d_meta = fuzzy.DMetaphone()
    #fuzzy match
    return d_meta(word1_mod) == d_meta(word2)

def findSize(sentence):
    count = 0
    for x in sentence.split(" "):
        if not x == '':
            count += 1
    return count



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
