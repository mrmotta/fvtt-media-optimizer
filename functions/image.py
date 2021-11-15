import subprocess


def process(input_file, output_file, image, programs):
    if image["lossless"]:
        lossless = "1"
    else:
        lossless = "0"

    subprocess.run(programs["ffmpeg"] + " -i \"" + input_file + "\" -lossless " + lossless
                   + " -compression_level " + str(image["compression_level"]) + " -preset " + image["preset"]
                   + " -qscale " + str(image["qscale"]) + " -map_metadata -1 \"" + output_file + "webp\"",
                   shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
