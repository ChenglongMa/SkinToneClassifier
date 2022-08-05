# <u>S</u>kin <u>Tone</u> Classifier (stone)

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

An easy-to-use library for skin tone classification.

This can be used to detect face or skin area in the specified images.
The detected skin tones are then classified into the specified color categories.
The library finally generates results to report the detected faces (if any),
dominant skin tones and color category.

---

# Installation

To install SkinToneClassifier:

```shell
pip install skin-tone-classifier
```

# HOW TO USE

## Quick Start

Given the famous photo of [Lenna](http://www.lenna.org/), to detect her skin tone,

<div align="center">
   <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/lena_std.jpg"  alt="Lenna picture" style="display: block; margin: auto"/>
</div>
just run:

```shell
stone -i /path/to/lenna.jpg --debug
```

Then, you can find the processed image in `./debug` folder, e.g.,

<div align="center">
   <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/lena_std-1.jpg"  alt="processed Lenna picture" style="display: block; margin: auto"/>
</div>

In this image, from left to right you can find the following information:

1. detected face enclosed by a rectangle.
2. dominant colors.
    1. _The number of colors depends on settings (default is 2) and their sizes depend on their proportion._
3. specified color categories and the target label is enclosed by a rectangle.
4. you can find a summary text at the bottom.

Furthermore, there will be a report file named `result.csv` which contains more detailed information, e.g.,

|file|face_location|dominant_1|props_1|dominant_2|props_2|category| distance(0-100)|
|-----|-----|-----|-----|-----|-----|-----|-----|
|lena_std|84:153|#CB6268|0.51|#E1A299|0.49|#e7c1b8|17.37|

## Detailed Usage

To see the usage and parameters, run:

```shell
stone -h
```

Output in console:

```text
usage: stone [-h] [-i IMAGE FILENAME [IMAGE FILENAME ...]]
               [-c COLOR [COLOR ...]] [-d] [-o DIRECTORY] [--n_colors N]
               [--new_width WIDTH] [--scale SCALE] [--min_nbrs NEIGHBORS]
               [--min_size WIDTH [HEIGHT ...]]

Skin Tone Classifier

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE FILENAME [IMAGE FILENAME ...], --images IMAGE FILENAME [IMAGE FILENAME ...]
                        Image filename(s) to process;
                        supports multiple values separated by space, e.g., "a.jpg b.png";
                        supports directory or file name(s), e.g., "./path/to/images/ a.jpg";
                        The app will search all images in the directory of this script in default.
  -c COLOR [COLOR ...], --categories COLOR [COLOR ...]
                        Skin tone categories; supports RGB hex value leading by # or RGB values separated by comma(,).
  -d, --debug           Whether to output processed images, used for debugging and verification.
  -o DIRECTORY, --output DIRECTORY
                        The path of output file, defaults to the directory of this script.
  --n_colors N          CONFIG: the number of dominant colors to be extracted, defaults to 2.
  --new_width WIDTH     CONFIG: resize the images with the specified width, defaults to 200.
  --scale SCALE         CONFIG: how much the image size is reduced at each image scale, defaults to 1.1
  --min_nbrs NEIGHBORS  CONFIG: how many neighbors each candidate rectangle should have to retain it.
                                Higher value results in less detections but with higher quality.
  --min_size WIDTH [HEIGHT ...]
                        CONFIG: minimum possible face size. Faces smaller than that are ignored, defaults to "30 30".
```

### Use Cases

#### 1. To process multiple images

1.1 Multiple filenames

```shell
stone -i (or --images) a.jpg b.png
```

1.2 Images in some folder(s)

```shell
stone -i ./path/to/images/
```

NB: Supported image formats: `.jpg, .gif, .png, .jpeg, .webp, .tif`.

In default (i.e., `stone` without `-i` option), the app will search images in current folder.

#### 2. To specify color categories

2.1 Use hex values

```shell
stone -c (or --categories) #373028 #422811 #fbf2f3
```

NB: Values start with '#'.

[//]: # (<div style="display:flex;">)

[//]: # (   <p style="background-color:#373028; color: aliceblue; text-align:center; vertical-align: middle; width: 80px;float: start;">)

[//]: # (      #373028)

[//]: # (   </p>)

[//]: # (   <p style="background-color:#422811; color: aliceblue; text-align:center; vertical-align: middle; width: 80px">)

[//]: # (      #422811)

[//]: # (   </p>)

[//]: # (   <p style="background-color:#513b2e; color: aliceblue; text-align:center; vertical-align: middle; width: 80px">)

[//]: # (      #513b2e)

[//]: # (   </p>  )

[//]: # (   <p style="background-color:#6f503c; color: aliceblue; text-align:center; vertical-align: middle; width: 80px">)

[//]: # (      #6f503c)

[//]: # (   </p>)

[//]: # (   <p style="background-color:#81654f; color: aliceblue; text-align:center; vertical-align: middle; width: 80px">)

[//]: # (      #81654f)

[//]: # (   </p>)

[//]: # (   <p style="background-color:#9d7a54; color: aliceblue; text-align:center; vertical-align: middle; width: 80px">)

[//]: # (      #9d7a54)

[//]: # (   </p>)

[//]: # (   <p style="background-color:#bea07e; color: aliceblue; text-align:center; vertical-align: middle; width: 80px">)

[//]: # (      #bea07e)

[//]: # (   </p>)

[//]: # (   <p style="background-color:#e5c8a6; color: black; text-align:center; vertical-align: middle; width: 80px">)

[//]: # (      #e5c8a6)

[//]: # (   </p>)

[//]: # (   <p style="background-color:#e7c1b8; color: black; text-align:center; vertical-align: middle; width: 80px">)

[//]: # (      #e7c1b8)

[//]: # (   </p>)

[//]: # (   <p style="background-color:#f3dad6; color: black; text-align:center; vertical-align: middle; width: 80px">)

[//]: # (      #f3dad6)

[//]: # (   </p>)

[//]: # (   <p style="background-color:#fbf2f3; color: black; text-align:center; vertical-align: middle; width: 80px">)

[//]: # (      #fbf2f3)

[//]: # (   </p>)

[//]: # (</div>)

2.2 Use RGB tuple values

```shell
stone -c 55,48,40 66,40,17 251,242,243
```

NB: Values split by comma ',', multiple values are still separated by space.

#### 3. Specify output folder

The app puts the final report (`result.csv`) in current folder in default.

To change the output folder:

```shell
stone -o (or --output) ./path/to/output/
```

The output folder will be created if it does not exist.

In `result.csv`, each row is showing the color information of each detected face.
If more than one faces are detected, there will be multiple rows for that image.

#### 4. Store processed image for debugging

```shell
stone -d (or --debug)
```

This option will store the processed image (like the Lenna example above) in `./path/to/output/debug` folder.

By default, to save space, the app does not store processed images.

Like in the `result.csv` file, there will be more than one processed images if 2 or more faces were detected.

#### 5. Tune parameters of face detection

The rest parameters of `CONFIG` are used to detect face.
Please refer to https://stackoverflow.com/a/20805153/8860079 for detailed information. 