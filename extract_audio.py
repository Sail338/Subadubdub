import subprocess
command = "ffmpeg -i input.mp4 -ab 160k -ac 2 -ar 44100 -vn output.mp3"
subprocess.call(command, shell=True)
