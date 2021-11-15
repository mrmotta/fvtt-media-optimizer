#!/usr/bin/env python3

import json
import os
import shutil

import functions.audio
import functions.configuration
import functions.image
import functions.video


def wait_to_end(exit_code):
    print()
    input("Press any key to end...")
    exit(exit_code)


def normalize_file_name(string):
    items = string.split(os.path.sep)
    string = items[-1]
    keep_characters = ('.', '-', '_')
    string = "".join(char for char in string.replace(" ", "_") if char.isalnum() or char in keep_characters).rstrip()
    items[-1] = string
    return os.path.sep.join(items)


def process():
    audio_input_formats = (
        "aac", "ac3", "aiff", "alac", "f4a", "flac", "gsm", "m4a", "mp3", "oga", "ogg", "opus", "raw", "wav", "wma")
    image_input_formats = (
        "bmp", "gif", "heic", "heif", "jp2", "jpe", "jpeg", "jpg", "jpg2", "mj2", "png", "tif", "tiff", "webp")
    video_input_formats = (
        "avi", "f4v", "flv", "m4v", "mkv", "mov", "mp4", "mpg", "mpeg", "mxf", "qt", "ts", "vob", "webm")

    input_file = config["folders"]["input"] + os.path.sep + name + "." + extension
    output_file = config["folders"]["output"] + os.path.sep + normalize_file_name(name) + "."

    if extension.lower() in audio_input_formats:
        functions.audio.process(name, input_file, output_file, temporary_path, config["audio"], config["programs"])

    elif extension.lower() in image_input_formats:
        functions.image.process(input_file, output_file, config["image"], config["programs"])

    elif extension.lower() in video_input_formats:
        functions.video.process(name, input_file, output_file, temporary_path, config["video"], config["audio"],
                                config["programs"])

    else:
        print("Unrecognized file format in \"" + name + "." + extension + "\". Skipping.")


if __name__ == '__main__':
    print()
    print("+-------------------------------------------------------------------------------------+")
    print("| An automated media optimizer for Foundry Virtual Tabletop (https://foundryvtt.com/) |")
    print("+-------------------------------------------------------------------------------------+")
    print()

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    try:
        with open("config.json", "r") as file:
            config = json.loads(file.read())
    except FileNotFoundError:
        print("Configuration file (\"config.json\") not found!")
        wait_to_end(exit_code=1)

    try:
        functions.configuration.check_config(config)
    except Exception:
        wait_to_end(exit_code=2)
    print()

    try:
        if not os.path.isdir(config["folders"]["input"]):
            os.mkdir(config["folders"]["input"])
    except Exception:
        print("An error occurred while checking or creating the input folder (\"" + config["folders"]["input"] + "\")")
        wait_to_end(exit_code=3)

    try:
        if not os.path.isdir(config["folders"]["output"]):
            os.mkdir(config["folders"]["output"])
    except Exception:
        print("An error occurred while checking or creating the output folder (\""
              + config["folders"]["output"] + "\")")
        wait_to_end(3)

    if config["folders"]["temporary"] in os.listdir(config["folders"]["input"]):
        print("In the input folder (\""
              + config["folders"]["input"] + "\") there is a folder with the same name of the temporary folder (\""
              + config["folders"]["temporary"] + "\") used for processing.")
        wait_to_end(exit_code=4)

    if len(os.listdir(config["folders"]["output"])) > 0:
        print("To avoid possible collisions, please empty the output folder (\"" + config["folders"]["output"] + "\").")
        wait_to_end(exit_code=5)

    temporary_path = config["folders"]["output"] + os.path.sep + config["folders"]["temporary"]
    os.mkdir(temporary_path)

    print("Replicating input directory tree...")
    files_number = 0
    for path, _, files in os.walk(config["folders"]["input"]):
        files_number += len(files)
        if not path == config["folders"]["input"]:
            path = path.split(os.path.sep)
            output_path = path.copy()
            output_path[0] = config["folders"]["output"]
            tmp_path = path.copy()
            tmp_path[0] = temporary_path
            output_path = os.path.sep.join(output_path)
            tmp_path = os.path.sep.join(tmp_path)
            os.mkdir(output_path)
            os.mkdir(tmp_path)
    print("Replication completed.")
    print()

    index = 1
    for path, _, files in os.walk(config["folders"]["input"]):
        for file in files:
            name, extension = os.path.splitext(path + os.path.sep + file)
            items = name.split(os.path.sep)[1:]
            name = os.path.sep.join(items)
            extension = extension[1:]

            print("Processing file " + str(index) + " of " + str(files_number) + ": " + name + "." + extension)
            index += 1

            process()

    shutil.rmtree(temporary_path)

    if index == 1:
        print("Nothing to process.")
    else:
        print("Process completed!")

    wait_to_end(exit_code=0)
