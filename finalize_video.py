import ttts
from pydub import AudioSegment
import moviepy.editor as mpe



def finalize_video(audio_file,script_file,lang_code):
    
    queue = ttts.generate_mp3(audio_file,script_file,lang_code)
    original_sound = AudioSegment.from_file(audio_file,"flac")
    SECONDS = 1000
    QUIET = 5
    size_of_original = len(original_sound)
    overlay_sound = AudioSegment.silent(duration=size_of_original)
    outputFilePtr =1 
    #The ptr represents where we are in the mp3 in terms of milliseconds
    for node in queue:
        start = node.start
        end = node.end
        curr_output = "media/output"+str(outputFilePtr)+".mp3"
        quiet_down = original_sound[start*SECONDS:end*SECONDS+1] - QUIET
        curr_output = AudioSegment.from_file(curr_output,"mp3")
        original_sound = original_sound[0:start*SECONDS] + quiet_down + original_sound[end*SECONDS+1:]
        size_needed = abs(end - start)*SECONDS
        ratio = len(curr_output)*1.0 / size_needed*1.0
        #curr_output = speed_change(curr_output,ratio)
        overlay_sound = overlay_sound[0:start*SECONDS-1]+curr_output+overlay_sound[end*SECONDS+1]
        outputFilePtr+=1
    final_audio = original_sound.overlay(overlay_sound)
    final_audio.export("static/final_audio.mp3",format="mp3")
    video = mpe.VideoFileClip("parksandrec.mp4")
    audio = mpe.AudioFileClip("static/final_audio.mp3")
    final_video = video.set_audio(audio)
    final_video.write_videofile("static/final.mp4")

def speed_change(sound,speed=1.0):
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate*speed)
    })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


