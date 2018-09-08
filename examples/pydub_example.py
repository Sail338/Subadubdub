from pydub import AudioSegment



def speed_change(mp3,speed=1.0):
	sound_with_altered_frame_rate = mp3._spawn(mp3.raw_data, overrides={
	"frame_rate": int(mp3.frame_rate * speed)})
	return sound_with_altered_frame_rate.set_frame_rate(mp3.frame_rate)

mp3 = AudioSegment.from_file("../data/cb214.mp3",format="mp3")

ten_seconds_in = mp3[:10000]
beginning = ten_seconds_in - 15
beginning = speed_change(beginning,1.01)
beginning = beginning + mp3[10001:]


middle = mp3[40000:]

final = beginning.overlay(middle)


final.export("quiet.mp3", format="mp3")
middle.export("middle.mp3",format="mp3")
