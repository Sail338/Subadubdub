from google.cloud import texttospeech
import generate_transcript as gt
from pydub import AudioSegment 

#eventually make this more configurable
def generate_characters():

        
#        ben_voice = texttospeech.types.VoiceSelectionParams(name='de-DE-Wavenet-B',
 #       language_code="en-US")
  #      andy_voice = texttospeech.types.VoiceSelectionParams(name='de-DE-Wavenet-D',
   #     language_code="en-US")
    #    leslie_voice = texttospeech.types.VoiceSelectionParams(name='de-DE-Wavenet-A',
     #   language_code="en-US")

        characters = {"Ben": 'de-DE-Wavenet-B', "Leslie": 'de-DE-Wavenet-A', "Andy": 'de-DE-Wavenet-D'}

        return characters

def generate_audio_clip(client, node, node_num, language_code, characters):
        audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        snippet = configure_speaker_snippet(node, characters, client, language_code, audio_config)
        

        output_file = "media/output"+str(node_num)+".mp3"
        # The response's audio_content is binary.
        with open(output_file, 'wb') as out:
        # Write the response to the output file.
            out.write(snippet.audio_content)
            print('Audio content written to output file ' + str(node_num))
        time_delta = node.end - node.start        
        audio = AudioSegment.from_file(output_file)
        audio.duration_seconds = time_delta
        audio.export(output_file, format='mp3')

def configure_speaker_snippet(node, character_voices, client, language_code, audio_config):
    voice = configure_voice(node, character_voices, language_code)    
    synthesis_input = texttospeech.types.SynthesisInput(text=node.sentence)
    snippet = client.synthesize_speech(synthesis_input, voice, audio_config)
    return snippet

def configure_voice(node, character_voices, language_code):
    voice = texttospeech.types.VoiceSelectionParams(name=character_voices[node.speaker], language_code=language_code)
    return voice


def generate_mp3(source_audio,script,lang_code):
    #Get timed audio transcript
    transcript = gt.gen_transcript(source_audio, script,lang_code)

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()
    node_num = 1

    characters = generate_characters()

    #eventually adapt this to take command line input for dynamic language change
    for node in transcript:
        generate_audio_clip(client, node, node_num, lang_code, characters)
        node_num = node_num + 1
    return transcript
