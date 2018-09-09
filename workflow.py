import ttts
import extract_audio
import time
#starts the workflow to 
def begin_workflow(script_path,video_path,lang_code):
    extract_audio.extract(video_path)
    time.sleep(2)
    q = ttts.generate_mp3("input.flac",script_path,lang_code)
    
