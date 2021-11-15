import subprocess


def check_audio(config):
    if "audio" not in config:
        print("Audio key (audio) not found!")
        raise Exception()
    
    if "lossless" not in config["audio"]:
        print("Audio lossless encoding key (audio / lossless) not found!")
        raise Exception()
    if not type(config["audio"]["lossless"]) == bool:
        print("Audio lossless encoding key (audio / lossless) has to be a boolean value!")
        raise Exception()

    if "normalization" not in config["audio"]:
        print("Audio normalization key (audio / normalization) not found!")
        raise Exception()
    if not type(config["audio"]["normalization"]) == bool:
        print("Audio normalization key (audio / normalization) has to be a boolean value!")
        raise Exception()
    
    if config["audio"]["normalization"]:
        check_audio_normalization(config)


def check_audio_normalization(config):
    normalization_modes = ("ebu", "peak", "rms")

    if "normalization_mode" not in config["audio"]:
        print("Audio normalization mode (audio / normalization_mode) key not found!")
        raise Exception()
    if not type(config["audio"]["normalization_mode"]) == str:
        print("Audio normalization mode key (audio / normalization_mode) has to be a string!")
        raise Exception()
    if config["audio"]["normalization_mode"] not in normalization_modes:
        print("Wrong audio normalization mode (audio / normalization_mode)!")
        print("Please choose one between: " + str(normalization_modes).replace("'", '"')[1:-1] + ".")
        raise Exception()


def check_folders(config):
    if "folders" not in config:
        print("Folders key (folders) not found!")
        raise Exception()

    if "input" not in config["folders"]:
        print("Input folder key (folders / input) not found!")
        raise Exception()
    if not type(config["folders"]["input"]) == str:
        print("Input folder key (folders / input) has to be a string!")
        raise Exception()

    if "output" not in config["folders"]:
        print("Output folder key (folders / output) not found!")
        raise Exception()
    if not type(config["folders"]["output"]) == str:
        print("Output folder key (folders / output) has to be a string!")
        raise Exception()

    if "temporary" not in config["folders"]:
        print("Temporary folder key (folders / temporary) not found!")
        raise Exception()
    if not type(config["folders"]["temporary"]) == str:
        print("Temporary folder key (folders / temporary) has to be a string!")
        raise Exception()


def check_image(config):
    compression_level_range = range(7)
    presets = ("none", "default", "picture", "photo", "drawing", "icon", "text")
    qscale_range = range(101)

    if "image" not in config:
        print("Image key (image) not found!")
        raise Exception()

    if "compression_level" not in config["image"]:
        print("Image compression level key (image / compression_level) not found!")
        raise Exception()
    if not type(config["image"]["compression_level"]) == int:
        print("Image compression level key (image / compression_level) has to be an integer value!")
        raise Exception()
    if config["image"]["compression_level"] not in compression_level_range:
        print("Wrong image compression level (image / compression_level)!")
        print("Please choose one in range: [" + str(compression_level_range.start) + "; "
              + str(compression_level_range.stop - 1) + "].")
        raise Exception()

    if "lossless" not in config["image"]:
        print("Image lossless encoding key (image / lossless) not found!")
        raise Exception()
    if not type(config["image"]["lossless"]) == bool:
        print("Image lossless encoding key (image / lossless) has to be a boolean value!")
        raise Exception()

    if "preset" not in config["image"]:
        print("Image preset (image / preset) not found!")
        raise Exception()
    if not type(config["image"]["preset"]) == str:
        print("Image preset key (image / preset) has to be a string!")
        raise Exception()
    if config["image"]["preset"] not in presets:
        print("Wrong image preset (image / preset)!")
        print("Please choose one between: " + str(presets).replace("'", '"')[1:-1] + ".")
        raise Exception()

    if "qscale" not in config["image"]:
        print("Image quality key (image / qscale) not found!")
        raise Exception()
    if not type(config["image"]["qscale"]) == int:
        print("Image quality key (image / qscale) has to be an integer value!")
        raise Exception()
    if config["image"]["qscale"] not in qscale_range:
        print("Wrong image quality (image / qscale)!")
        print("Please choose one in range: [" + str(qscale_range.start) + "; " + str(qscale_range.stop - 1) + "].")
        raise Exception()


def check_programs(config):
    if "programs" not in config:
        print("Programs key (programs) not found!")
        raise Exception()

    if "ffmpeg" not in config["programs"]:
        print("FFmpeg key (programs / ffmpeg) not found!")
        raise Exception()
    if not type(config["programs"]["ffmpeg"]) == str:
        print("FFmpeg key (programs / ffmpeg) has to be a string!")
        raise Exception()
    process = subprocess.run(config["programs"]["ffmpeg"],
                             shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if "Hyper fast Audio and Video encoder" not in process.stderr.decode():
        print("FFmpeg installation not found!")
        raise Exception()

    if "ffmpeg-normalize" not in config["programs"]:
        print("FFmpeg normalize key (programs / ffmpeg-normalize) not found!")
        raise Exception()
    if not type(config["programs"]["ffmpeg-normalize"]) == str:
        print("FFmpeg normalize key (programs / ffmpeg-normalize) has to be a string!")
        raise Exception()
    process = subprocess.run(config["programs"]["ffmpeg-normalize"] + " -h",
                             shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if "command line tool for normalizing audio files" not in process.stdout.decode():
        print("FFmpeg normalizer installation not found!")
        raise Exception()


def check_video(config):
    video_output_codecs = ("vp9", "av1")

    if "video" not in config:
        print("Video key (video) not found!")
        raise Exception()

    if "keep_audio" not in config["video"]:
        print("Video keep audio key (video / keep_audio) not found!")
        raise Exception()
    if not type(config["video"]["keep_audio"]) == bool:
        print("Video keep audio key (audio / keep_audio) has to be a boolean value!")
        raise Exception()

    if "normalize_audio" not in config["video"]:
        print(" key (video / normalize_audio) not found!")
        raise Exception()
    if not type(config["video"]["normalize_audio"]) == bool:
        print("Video audio normalization key (audio / normalize_audio) has to be a boolean value!")
        raise Exception()
    if config["video"]["normalize_audio"]:
        check_audio_normalization(config)

    if "output_video_codec" not in config["video"]:
        print("Video keep audio key (video / keep_audio) not found!")
        raise Exception()
    if not type(config["video"]["output_video_codec"]) == str:
        print("Video keep audio key (video / keep_audio) has to be a string!")
        raise Exception()
    if config["video"]["output_video_codec"] not in video_output_codecs:
        print("Wrong video codec (video / output_video_codec)!")
        print("Please choose one between: " + str(video_output_codecs).replace("'", '"')[1:-1] + ".")
        raise Exception()


def check_config(config):
    print("Checking configuration file...")

    check_programs(config)
    check_folders(config)
    check_audio(config)
    check_image(config)
    check_video(config)

    print("Check completed!")
