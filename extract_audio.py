import subprocess
def extract(input_filename):
    command = "ffmpeg -i " + input_filename + " -ab 160k -ac 1 -ar 16000 -vn input.flac"
    subprocess.call(command, shell=True)
