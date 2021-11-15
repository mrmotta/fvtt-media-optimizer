# Foundry Virtual Tabletop Media Optimizer

An automated media optimizer for [Foundry Virtual Tabletop](https://foundryvtt.com/).

Optimizing media is a good strategy when you self-host your server. Reducing the size of the assets, trying to keep the same quality of the originals, brings to a lower load time when playing, especially if you want to serve them to multiple players and you are not a CDN. This also improves the game experience.

Sometimes, usually when the original files don't have a good quality, the optimization process fails, generating bigger files than the originals. It's normal. In these cases, just discard the converted ones and keep using the old ones.

**Note**: this is not an official tool. For more information about the Foundry VTT guidelines, please take a look at the official [Media Optimization Guide](https://foundryvtt.com/article/media/).

## Table of Contents

- [Usage](#usage)
- [Software dependencies](#software-dependencies)
- [Configuration file](#configuration-file)
  - [Audio settings (`audio`)](#audio-settings-audio)
  - [Folders (`folders`)](#folders-folders)
  - [Image settings (`image`)](#image-settings-image)
  - [Programs (`programs`)](#programs-programs)
  - [Video settings (`video`)](#video-settings-video)
- [File types and encoders](#file-types-and-encoders)
  - [Input](#input)
  - [Output](#output)

## Usage

**Steps**:

1. Edit the [configuration file](config.json) with all the required fields as explained in the [configuration section](#configuration-file).
2. Put all the files you want to be converted into the input folder specified in the [configuration file](config.json). If the folder isn't present in the [script](optimizer.py) folder, simply create it or run the program (the folder will be automatically created).
3. Run the program and wait for it to finish.

**Run the program**:

- Launch it from terminal: `python3 /path/to/optimizer.py`

- Double click on the [script](optimizer.py) itself.

## Software dependencies

Software | Description | Link
---------|-------------|-----
[Python](https://www.python.org/) | An interpreted high-level general-purpose programming language. (Wikipedia page) | [Download page](https://www.python.org/downloads/)
[FFmpeg](https://ffmpeg.org/) | A complete, cross-platform solution to record, convert and stream audio and video. (FFmpeg main page) | [Download page](https://ffmpeg.org/download.html)
[ffmpeg-normalize](https://github.com/slhck/ffmpeg-normalize) | A utility for batch-normalizing audio using ffmpeg. (Github project page) | [PyPI page](https://pypi.org/project/ffmpeg-normalize/)

## Configuration file

The configuration is stored into [`config.json`](config.json). Make sure every key is present and filled with the right value, otherwise the program will stop when it checks for their presence and correctness.

The only exception to this is when some features are disabled (like when the audio normalization key is set to `false`). In this case, the depending keys aren't checked.

### Audio settings (`audio`)

Key | Description | Type | Values
----|-------------|------|-------
`lossless` | Encodes the audio without quality loss. | `boolean` | `false`, `true`
`normalization` | [Normalizes](https://en.wikipedia.org/wiki/Audio_normalization) the audio file according the specified mode. | `boolean` | `false`, `true`
`normalization_mode` | Selects the parameters to use for the normalization process. This key is directly sent to `ffmpeg-normalize`. | `string` | `ebu` ([EBU R 128](https://en.wikipedia.org/wiki/EBU_R_128)), `peak`, `rms`

### Folders (`folders`)

Key | Description | Type
----|-------------|------
`input` | Input folder relative to the [script](optimizer.py) position where to put all the files that need to be processed. It can contain subfolders, and all of their content will be processed. | `string`
`output` | Output folder relative to the [script](optimizer.py) position where to store all the converted files. It keeps the original folder structure. | `string`
`temporary` | A temporary folder used for temporary processes. It's automatically created within the root of the output folder and is automatically deleted (with all its content) at the end of the process, therefore, the input folder shouldn't contain a folder with this name (if found, the program doesn't even start). | `string`

### Image settings (`image`)

Key | Description | Type | Values
----|-------------|------|-------
`compression_level` | For lossy, this is a quality/speed tradeoff. Higher values give better quality for a given size at the cost of increased encoding time. For lossless, this is a size/speed tradeoff. Higher values give smaller size at the cost of increased encoding time. More specifically, it controls the number of extra algorithms and compression tools used, and varies the combination of these tools. This maps to the method option in libwebp. (FFmpeg documentation) | `integer` | [0; 6]
`lossless` | Encodes the image without quality loss. | `boolean` | `false`, `true`
`preset` | Configuration preset. This does some automatic settings based on the general type of the image. (FFmpeg documentation) | `string` | `none`, `default`, `picture`, `photo`, `drawing`, `icon`, `text`
`qscale` | For lossy encoding, this controls image quality, 0 to 100. For lossless encoding, this controls the effort and time spent at compressing more. (FFmpeg documentation) | `integer` | [0; 100]

### Programs (`programs`)

Key | Description | Type
----|-------------|------
`ffmpeg` | The full path to the executable or the short name used to run the program from terminal (usually `ffmpeg`). | `string`
`ffmpeg-normalize` | The full path to the executable or the short name used to run the program from terminal (usually `ffmpeg-normalize`). | `string`

### Video settings (`video`)

Key | Description | Type | Values
----|-------------|------|-------
`keep_audio` | If `true`, keeps the original audio, otherwise the video will be muted. | `boolean` | `false`, `true`
`normalize_audio` | Decides whether to normalize the audio track (according to the audio settings) or not. | `boolean` | `false`, `true`
`output_video_codec` | Sets the video encoder used while generating the output file. | `string` | `vp9` ([VP9](https://en.wikipedia.org/wiki/VP9)), `av1` ([AOMedia Video 1](https://en.wikipedia.org/wiki/AV1))

## File types and encoders

### Input

**Audio file types**: `aac`, `ac3`, `aiff`, `alac`, `f4a`, `flac`, `gsm`, `m4a`, `mp3`, `oga`, `ogg`, `opus`, `raw`, `wav`, `wma`.

**Image file types**: `bmp`, `gif`, `heic`, `heif`, `jp2`, `jpe`, `jpeg`, `jpg`, `jpg2`, `mj2`, `png`, `tif`, `tiff`, `webp`.

**Video file types**: `avi`, `f4v`, `flv`, `m4v`, `mkv`, `mov`, `mp4`, `mpg`, `mpeg`, `mxf`, `qt`, `ts`, `vob`, `webm`.

**Note**: these are not all the possible file types for each category. These should be only the most common ones. If you think there is a common file type that can be decoded (inner tracks' codecs, too) by FFmpeg that I should add to these lists, please let me know opening an issue.

### Output

**Audio**: `flac` (for lossless encoding) and `ogg` (for lossy encoding, with audio track encoded with `libopus`).

**Image**: `webp` (for both lossy and lossless encoding).

**Video**: `webm` (for both VP9 and AV1 video; audio is always encoded with `libopus`).