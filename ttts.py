from google.cloud import texttospeech

# Instantiates a client
client = texttospeech.TextToSpeechClient()
#ben, leslie, andy
characters = {"Ben": "en-US-Wavenet-A", "Leslie": "en-US-Wavenet-C", "Andy": "en-US-Wavenet-B"}



def generate(characters):
        # Set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text="Hello, World!")

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        #voice = texttospeech.types.VoiceSelectionParams(
        #    language_code='en-US',
        #    ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

        ben_voice = texttospeech.types.VoiceSelectionParams(name=characters["Ben"],
        language_code="en-US")

        andy_voice = texttospeech.types.VoiceSelectionParams(name=characters["Andy"],
        language_code="en-US")

        leslie_voice = texttospeech.types.VoiceSelectionParams(name=characters["Leslie"],
        language_code="en-US")

        client = texttospeech.TextToSpeechClient()
        ben_input = texttospeech.types.SynthesisInput(text="Hello, I'm Ben")
        leslie_input = texttospeech.types.SynthesisInput(text="Hello, I'm Leslie")
        andy_input = texttospeech.types.SynthesisInput(text="Hello, I'm Andy")

        audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type

        ben_response = client.synthesize_speech(ben_input, ben_voice, audio_config)
        leslie_response = client.synthesize_speech(leslie_input, leslie_voice, audio_config)
        andy_response = client.synthesize_speech(andy_input, andy_voice, audio_config)


        # The response's audio_content is binary.
        with open('output.mp3', 'wb') as out:
        # Write the response to the output file.
            out.write(ben_response.audio_content)
            print('Audio content written to file "ben_output.mp3"')
        
        with open('leslie_output.mp3', 'wb') as out:
        # Write the response to the output file.
            out.write(leslie_response.audio_content)
            print('Audio content written to file "leslie_output.mp3"')

        with open('andy_output.mp3', 'wb') as out:
        # Write the response to the output file.
            out.write(andy_response.audio_content)
            print('Audio content written to file "andy_output.mp3"')
        


generate(characters)
