from google.cloud import translate
import six

def translate_phrase(input_string:str, target:str):
    translate_client = translate.Client()
    if isinstance(input_string, six.binary_type):
        input_string = input_string.decode('utf-8')
    result = translate_client.translate(
        input_string, target_language=target)

    return result['translatedText']


