import os
import re
import subprocess

import functions.audio


def process(name, input_file, output_file, temporary_path, video, audio, programs):
    audio_processing = False
    output = output_file

    execution = subprocess.run(programs["ffmpeg"] + " -i \"" + input_file + "\"",
                               shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    fps = float(re.search("[0-9.]+ fps", execution.stderr.decode()).group()[:-3])
    if fps > 30.0:
        fps = 30.0

    if re.search(": Audio: ", execution.stderr.decode()) is not None and video["keep_audio"]:
        audio_processing = True
        output = temporary_path + os.path.sep + name + "."
        audio_config = audio.copy()
        audio_config["normalization"] = video["normalize_audio"]
        audio_config["lossless"] = False
        functions.audio.process(name, input_file, output_file, temporary_path, audio_config, programs, put_in_tmp=True)

    if video["output_video_codec"] == "vp9":
        subprocess.run(programs["ffmpeg"] + " -i \"" + input_file + "\" -map 0:v -c:v libvpx-vp9 -r " + str(fps)
                       + " -b:v 0 -crf 40 -speed 4 -quality good -row-mt 1 -tile-columns 0 -tile-rows 0"
                       + " -frame-parallel 0 -aq-mode 0 -map_metadata -1 \"" + output + "webm\"",
                       shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(programs["ffmpeg"] + " -i \"" + input_file + "\" -map 0:v -c:v libsvtav1 -r " + str(fps)
                       + " -rc cqp -qp 50 -preset 7 -tile_rows 0 -tile_columns 0 -map_metadata -1 \""
                       + output + "webm\"", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if audio_processing:
        video_file = output + "webm"
        audio_file = temporary_path + os.path.sep + name + ".ogg"
        subprocess.run(programs["ffmpeg"] + " -i \"" + video_file + "\" -i \"" + audio_file + "\" -map 0:v -c:v copy"
                       + " -map 1:a -c:a copy -map_metadata -1 \"" + output_file + "webm\"",
                       shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(audio_file)
        os.remove(video_file)
