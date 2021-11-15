import os
import re
import subprocess


def process(name, input_file, output_file, temporary_path, audio, programs, put_in_tmp=False):
    execution = subprocess.run(programs["ffmpeg"] + " -i \"" + input_file + "\"",
                               shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    hertz = int(re.search("[0-9]+ Hz", execution.stderr.decode()).group()[:-3])
    if hertz > 48000:
        hertz = 48000

    if audio["normalization"]:
        if os.path.sep in name:
            output = temporary_path + os.path.sep + os.path.sep.join(name.split(os.path.sep)[:-1])
        else:
            output = temporary_path
        subprocess.run(programs["ffmpeg-normalize"] + " \"" + input_file + "\" -of \"" + output
                       + "\" -vn -ar " + str(hertz) + " -nt " + audio["normalization_mode"],
                       shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        input_file = temporary_path + os.path.sep + name + ".mkv"
        delete = True
    else:
        delete = False

    if put_in_tmp:
        output_file = temporary_path + os.path.sep + name + "."

    if audio["lossless"]:
        subprocess.run(programs["ffmpeg"] + " -i \"" + input_file
                       + "\" -map 0:a -c:a flac -compression_level 12 -sample_fmt s16 -map_metadata -1 \""
                       + output_file + "flac\"", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(programs["ffmpeg"] + " -i \"" + input_file
                       + "\" -map 0:a -c:a libopus -map_metadata -1 \""
                       + output_file + "ogg\"", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if delete:
        os.remove(input_file)
