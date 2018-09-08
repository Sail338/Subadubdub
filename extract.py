import io
import os
from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import storage


def gen_transcript_and_tag_audio(filename:str):
    client = speech.SpeechClient()
    #upload to gcp
    uri_ = upload_to_gcp(filename)
    audio = speech.types.RecognitionAudio(uri=uri_)
    config = speech.types.RecognitionConfig(
         encoding='FLAC',
         language_code='en-US',
         model='video',
         sample_rate_hertz=16000,
         enable_word_time_offsets=True)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    result_data = operation.result(timeout=1000)
    for result in result_data.results:
         alternative = result.alternatives[0]
         print(u'Transcript: {}'.format(alternative.transcript))
         print('Confidence: {}'.format(alternative.confidence))
         for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            print('Word: {}, start_time: {}, end_time: {}'.format(
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9))

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



