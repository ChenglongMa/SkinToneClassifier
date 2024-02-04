<div style="text-align:center;">
    <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/stone-logo.png" alt="stone logo">
    <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/illustration.svg" alt="model illustration">
</div>

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/skin-tone-classifier)
[![PyPI](https://img.shields.io/pypi/v/skin-tone-classifier)](https://pypi.org/project/skin-tone-classifier/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/skin-tone-classifier)](https://pypi.org/project/skin-tone-classifier/)
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/ChenglongMa/SkinToneClassifier?include_prereleases)](https://github.com/ChenglongMa/SkinToneClassifier/releases/latest)
[![GitHub License](https://img.shields.io/github/license/ChenglongMa/SkinToneClassifier)](https://github.com/ChenglongMa/SkinToneClassifier/blob/main/LICENSE)
[![youtube](https://img.shields.io/badge/YouTube-Skin_Tone_Classifier-FF0000?logo=youtube)](https://youtube.com/playlist?list=PLYRpHlp-9V_E5ZLhW1hbNaVjS5Zg6b6kQ&si=ezxUR7McUbZa4clT)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1k-cryEZ9PInJRXWIi17ib66ufYV2Ikwe?usp=sharing)
[![GitHub Repo stars](https://img.shields.io/github/stars/ChenglongMa/SkinToneClassifier)](https://github.com/ChenglongMa/SkinToneClassifier)

An easy-to-use library for skin tone classification.

This can be used to detect **face** or **skin area** in the specified images.
The detected skin tones are then classified into the specified color categories.
The library finally generates results to report the detected faces (if any),
dominant skin tones and color categories.

Check out the [Changelog](https://github.com/ChenglongMa/SkinToneClassifier/blob/main/CHANGELOG.md) for the latest updates.

*If you find this project helpful, please
consider [giving it a star](https://github.com/ChenglongMa/SkinToneClassifier)* ⭐. *It would be a great encouragement
for me!*

---

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Video tutorials](#video-tutorials)
  - [Playlist](#playlist)
  - [1. How to install Python and `stone`](#1-how-to-install-python-and-stone)
  - [2. Use `stone` in GUI mode](#2-use-stone-in-gui-mode)
  - [3. Use `stone` in CLI mode](#3-use-stone-in-cli-mode)
  - [4. Use `stone` in Python scripts](#4-use-stone-in-python-scripts)
- [Installation](#installation)
  - [Install from pip](#install-from-pip)
    - [Install the CLI mode only](#install-the-cli-mode-only)
    - [Install the CLI mode and the GUI mode](#install-the-cli-mode-and-the-gui-mode)
  - [Install from source](#install-from-source)
- [HOW TO USE](#how-to-use)
  - [Quick Start](#quick-start)
    - [Use `stone` in a GUI](#use-stone-in-a-gui)
    - [Use `stone` in command line interface (CLI)](#use-stone-in-command-line-interface-cli)
    - [Interpretation of the table](#interpretation-of-the-table)
  - [Detailed Usage](#detailed-usage)
    - [Use Cases](#use-cases)
      - [1. Process multiple images](#1-process-multiple-images)
      - [2. Specify color categories](#2-specify-color-categories)
      - [3. Specify category labels](#3-specify-category-labels)
      - [4. Specify output folder](#4-specify-output-folder)
      - [5. Store report images for debugging](#5-store-report-images-for-debugging)
      - [6. Specify the types of the input image(s)](#6-specify-the-types-of-the-input-images)
      - [7. Convert the `color` images to `black/white` images](#7-convert-the-color-images-to-blackwhite-images)
      - [8. Tune parameters of face detection](#8-tune-parameters-of-face-detection)
      - [9. Multiprocessing settings](#9-multiprocessing-settings)
      - [10. Used as a library by importing into other projects](#10-used-as-a-library-by-importing-into-other-projects)
- [Citation](#citation)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Video tutorials

[![youtube](https://img.shields.io/badge/YouTube-Skin_Tone_Classifier-FF0000?logo=youtube)](https://youtube.com/playlist?list=PLYRpHlp-9V_E5ZLhW1hbNaVjS5Zg6b6kQ&si=ezxUR7McUbZa4clT)

Please visit the following video tutorials if you have no programming background or are unfamiliar with how to use Python and this library 💖

## Playlist

[![playlist](https://img.youtube.com/vi/vu6whI0qcmU/0.jpg)](https://youtube.com/playlist?list=PLYRpHlp-9V_E5ZLhW1hbNaVjS5Zg6b6kQ&si=ezxUR7McUbZa4clT)

<details markdown="1">
  <summary><i>Click here to show more.</i></summary>
    
## 1. How to install Python and `stone`

[![YouTube Video Views](https://img.shields.io/youtube/views/vu6whI0qcmU)](https://www.youtube.com/watch?v=vu6whI0qcmU&list=PLYRpHlp-9V_E5ZLhW1hbNaVjS5Zg6b6kQ&index=1)

[![installation](https://img.youtube.com/vi/vu6whI0qcmU/0.jpg)](https://www.youtube.com/watch?v=vu6whI0qcmU&list=PLYRpHlp-9V_E5ZLhW1hbNaVjS5Zg6b6kQ&index=1)

## 2. Use `stone` in GUI mode

[![YouTube Video Views](https://img.shields.io/youtube/views/08apMEogZgs)](https://www.youtube.com/watch?v=08apMEogZgs&list=PLYRpHlp-9V_E5ZLhW1hbNaVjS5Zg6b6kQ&index=2)

[![use gui mode](https://img.youtube.com/vi/08apMEogZgs/0.jpg)](https://www.youtube.com/watch?v=08apMEogZgs&list=PLYRpHlp-9V_E5ZLhW1hbNaVjS5Zg6b6kQ&index=2)

## 3. Use `stone` in CLI mode

[![YouTube Video Views](https://img.shields.io/youtube/views/rqJ62DijQaw)](https://www.youtube.com/watch?v=rqJ62DijQaw&list=PLYRpHlp-9V_E5ZLhW1hbNaVjS5Zg6b6kQ&index=3)

[![use cli mode](https://img.youtube.com/vi/rqJ62DijQaw/0.jpg)](https://www.youtube.com/watch?v=rqJ62DijQaw&list=PLYRpHlp-9V_E5ZLhW1hbNaVjS5Zg6b6kQ&index=3)

## 4. Use `stone` in Python scripts

Please refer to this notebook [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1k-cryEZ9PInJRXWIi17ib66ufYV2Ikwe?usp=sharing) for more information.

_More videos are coming soon..._

</details>

# Installation

> [!TIP]
> 
> Since v1.2.3, we have made the GUI mode **optional**.
> 


## Install from pip

### Install the CLI mode only

```shell
pip install skin-tone-classifier --upgrade
```

It is useful for users who want to use this library in non-GUI environments, e.g., servers or [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1k-cryEZ9PInJRXWIi17ib66ufYV2Ikwe?usp=sharing).

### Install the CLI mode and the GUI mode

```shell
pip install skin-tone-classifier[all] --upgrade
```

It is useful for users who are not familiar with the command line interface and want to use the GUI mode.

## Install from source

```shell
git clone git@github.com:ChenglongMa/SkinToneClassifier.git
cd SkinToneClassifier
pip install -e . --verbose
```

> [!TIP]
>
> If you encounter the following problem:
> 
> [`ImportError: DLL load failed while importing _core: The specified module could not be found`](https://stackoverflow.com/q/52306805/8860079)
> 
> Please download and install **Visual C++ Redistributable** at [here](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#visual-studio-2015-2017-2019-and-2022).
>
> Then this error will be gone.

# HOW TO USE

> [!TIP]
>
> You can combine the following documents, [the video tutorials above](#video-tutorials)
> and the running examples [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1k-cryEZ9PInJRXWIi17ib66ufYV2Ikwe?usp=sharing)
> to understand the usage of this library more intuitively.
> 

## Quick Start

### Use `stone` in a GUI

✨ Since v1.2.0, we have provided a GUI version of `stone` for users who are not familiar with the command line
interface.

![stone GUI](https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/gui.png)

Instead of typing commands in the terminal, you can use the config GUI of `stone` to process the images.

Steps:

1. Open the terminal that can run `stone` (e.g., `PowerShell` in Windows or `Terminal` in macOS).
2. Type `stone` (without any parameters) or `stone --gui` and press <kbd>Enter</kbd> to open the GUI.
3. Specify the parameters in each tab.
4. Click the `Start` button to start processing the images.

Hopefully, this can make it easier for you to use `stone` 🍻!

> [!TIP]
> 
> 1. It is recommended to install v1.2.3+, which supports Python 3.9+.
> 
>    If you have installed v1.2.0, please upgrade to v1.2.3+ by running 
> 
>    `pip install skin-tone-classifier[all] --upgrade`
>
> 2. If you encounter the following problem:
>    > This program needs access to the screen. Please run with a Framework
>    > build of python, and only when you are logged in on the main display
>    > of your Mac.
> 
>    Please launch the GUI by running `pythonw -m stone` in the terminal.
>    References: 
>       * [stackoverflow](https://stackoverflow.com/a/52732858/8860079)
>       * [python-using-mac](https://docs.python.org/3/using/mac.html)

### Use `stone` in command line interface (CLI)

To detect the skin tone in a portrait, e.g.,

<div align="center">
   <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/demo.png"  alt="Demo picture" style="display: block; margin: auto"/>
</div>

Just run:

```shell
stone -i /path/to/demo.png --debug
```

Then, you can find the processed image in `./debug/color/faces_1` folder, e.g.,

<div align="center">
   <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/demo-1.png"  alt="processed demo picture" style="display: block; margin: auto"/>
</div>

In this image, from left to right you can find the following information:

1. detected face with a label (*Face 1*) enclosed by a rectangle.
2. dominant colors.
    1. _The number of colors depends on settings (default is 2), and their sizes depend on their proportion._
3. specified color palette and the target label is enclosed by a rectangle.
4. you can find a summary text at the bottom.

Furthermore, there will be a report file named `result.csv` which contains more detailed information, e.g.,

| file     | image type | face id | dominant 1 | percent 1 | dominant 2 | percent 2 | skin tone | tone label | accuracy(0-100) |
|----------|------------|---------|------------|-----------|------------|-----------|-----------|------------|-----------------|
| demo.png | color      | 1       | #C99676    | 0.67      | #805341    | 0.33      | #9D7A54   | CF         | 86.27           |

### Interpretation of the table

1. `file`: the filename of the processed image.
    * **NB: The filename pattern of report image is `<file>-<face id>.<extension>`**
2. `image type`: the type of the processed image, i.e., `color` or `bw` (black/white).
3. `face id`: the id of the detected face, which matches the reported image. `NA` means no face has been detected.
4. `dominant n`: the `n`-th dominant color of the detected face.
5. `percent n`: the percentage of the `n`-th dominant color, (0~1.0).
6. `skin tone`: the skin tone category of the detected face.
7. `tone label`: the **label** of skin tone category of the detected face.
8. `accuracy`: the accuracy of the skin tone category of the detected face, (0~100). The larger, the better.

## Detailed Usage

To see the usage and parameters, run:

```shell
stone -h (or --help)
```

Output in console:

```text
usage: stone [-h] [-i IMAGE FILENAME [IMAGE FILENAME ...]] [-r] [-t IMAGE TYPE] [-p PALETTE [PALETTE ...]]
             [-l LABELS [LABELS ...]] [-d] [-bw] [-o DIRECTORY] [--n_workers WORKERS] [--n_colors COLORS]
             [--new_width WIDTH] [--scale SCALE] [--min_nbrs NEIGHBORS] [--min_size WIDTH [HEIGHT ...]]
             [--threshold THRESHOLD] [-v]

Skin Tone Classifier

options:
  -h, --help            show this help message and exit
  -i IMAGE FILENAME [IMAGE FILENAME ...], --images IMAGE FILENAME [IMAGE FILENAME ...]
                        Image filename(s) or URLs to process;
                        Supports multiple values separated by space, e.g., "a.jpg b.png";
                        Supports directory or file name(s), e.g., "./path/to/images/ a.jpg";
                        Supports URL(s), e.g., "https://example.com/images/pic.jpg" since v1.1.0+.
                        The app will search all images in current directory in default.
  -r, --recursive       Whether to search images recursively in the specified directory.
  -t IMAGE TYPE, --image_type IMAGE TYPE
                        Specify whether the input image(s) is/are colored or black/white.
                        Valid choices are: "auto", "color" or "bw",
                        Defaults to "auto", which will be detected automatically.
  -p PALETTE [PALETTE ...], --palette PALETTE [PALETTE ...]
                        Skin tone palette;
                        Supports RGB hex value leading by "#" or RGB values separated by comma(,),
                        E.g., "-p #373028 #422811" or "-p 255,255,255 100,100,100"
  -l LABELS [LABELS ...], --labels LABELS [LABELS ...]
                        Skin tone labels; default values are the uppercase alphabet list leading by the image type ('C' for 'color'; 'B' for 'Black&White'), e.g., ['CA', 'CB', ..., 'CZ'] or ['BA', 'BB', ..., 'BZ'].
  -d, --debug           Whether to generate report images, used for debugging and verification.The report images will be saved in the './debug' directory.
  -bw, --black_white    Whether to convert the input to black/white image(s).
                        If true, the app will use the black/white palette to classify the image.
  -o DIRECTORY, --output DIRECTORY
                        The path of output file, defaults to current directory.
  --n_workers WORKERS   The number of workers to process the images, defaults to the number of CPUs in the system.
  --n_colors COLORS     CONFIG: the number of dominant colors to be extracted, defaults to 2.
  --new_width WIDTH     CONFIG: resize the images with the specified width. Negative value will be ignored, defaults to 250.
  --scale SCALE         CONFIG: how much the image size is reduced at each image scale, defaults to 1.1
  --min_nbrs NEIGHBORS  CONFIG: how many neighbors each candidate rectangle should have to retain it.
                        Higher value results in less detections but with higher quality, defaults to 5.
  --min_size WIDTH [HEIGHT ...]
                        CONFIG: minimum possible face size. Faces smaller than that are ignored, defaults to "90 90".
  --threshold THRESHOLD
                        CONFIG: what percentage of the skin area is required to identify the face, defaults to 0.15.
  -v, --version         Show the version number and exit.
```

### Use Cases

#### 1. Process multiple images

1.1 Multiple filenames

```shell
stone -i (or --images) a.jpg b.png https://example.com/images/pic.jpg
```

1.2 Images in some folder(s)

```shell
stone -i ./path/to/images/
```

NB: Supported image formats: `.jpg, .gif, .png, .jpeg, .webp, .tif`.

In default (i.e., `stone` without `-i` option), the app will search images in current folder.

#### 2. Specify color categories

2.1 Use HEX values

```shell
stone -p (or --palette) #373028 #422811 #513B2E
```

NB: Values start with **'#'** and are separated by **space**.

2.2 Use RGB tuple values

```shell
stone -p 55,48,40 66,40,17 251,242,243
```

NB: Values split by **comma ','**, multiple values are still separated by **space**.

#### 3. Specify category labels

You can assign the labels for the skin tone categories, for example:

```text
"CA": "#373028",
"CB": "#422811",
"CC": "#513B2E",
...
```

To achieve this, you can use the `-l` (or `--labels`) option:

3.1 Specify the labels directly using _spaces_ as delimiters, e.g.,

```shell
stone -l A B C D E F G H
```

3.2 Specify the range of labels based on this pattern: `<start><sep><end><sep><step>`.

Specifically,

* `<start>`: the **start** label, can be a letter (e.g., `A`) or a number (e.g., `1`);
* `<end>`: the **end** label, can be a letter (e.g., `H`) or a number (e.g., `8`);
* `<step>`: the **step** to generate the label sequence, can be a number (e.g., `2` or `-1`), **defaults to `1`**.
* `<sep>`: the **separator** between `<start>` and `<end>`, can be one of these symbols: `-`, `,`, `~`, `:`, `;`, `_`.

Examples:

```shell
stone -l A-H-1
```

which is equivalent to `stone -l A-H` and `stone -l A B C D E F G H`.

```shell
stone -l A-H-2
```

which is equivalent to `stone -l A C E G`.

```shell
stone -l 1-8
```

which is equivalent to `stone -l 1 2 3 4 5 6 7 8`.

```shell
stone -l 1-8-3
```

which is equivalent to `stone -l 1 4 7`.


> [!IMPORTANT]
>
> Please make sure the number of labels is equal to the number of colors in the palette.

#### 4. Specify output folder

The app puts the final report (`result.csv`) in current folder in default.

To change the output folder:

```shell
stone -o (or --output) ./path/to/output/
```

The output folder will be created if it does not exist.

In `result.csv`, each row is showing the color information of each detected face.
If more than one faces are detected, there will be multiple rows for that image.

#### 5. Store report images for debugging

```shell
stone -d (or --debug)
```

This option will store the report image (like the demo portrait above) in
`./path/to/output/debug/<image type>/faces_<n>` folder,
where `<image type>` indicates if the image is `color` or `bw` (black/white);
`<n>` is the number of faces detected in the image.

**By default, to save storage space, the app does not store report images.**

Like in the `result.csv` file, there will be more than one report images if 2 or more faces were detected.

#### 6. Specify the types of the input image(s)

6.1 The input are color images

```shell
stone -t (or --image_type) color
```

6.2 The input are black/white images

```shell
stone -t (or --image_type) bw
```

6.3 **In default**, the app will detect the image type automatically, i.e.,

```shell
stone -t (or --image_type) auto
```

For `color` images, we use the `color` palette to detect faces:

```shell
#373028 #422811 #513b2e #6f503c #81654f #9d7a54 #bea07e #e5c8a6 #e7c1b8 #f3dad6 #fbf2f3
```

<div style="display: inline-block; width: 85px; height: 30px; background-color: #373028; color: white">#373028</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #422811; color: white">#422811</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #513b2e; color: white">#513B2E</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #6f503c; color: white">#6F503C</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #81654f; color: white">#81654F</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #9d7a54; color: white">#9D7A54</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #bea07e;">#BEA07E</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #e5c8a6;">#E5C8A6</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #e7c1b8;">#E7C1B8</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #f3dad6;">#F3DAD6</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #fbf2f3;">#FBF2F3</div>


(Please refer to our paper above for more details.)

For `bw` images, we use the `bw` palette to detect faces:

```shell
#FFFFFF #F0F0F0 #E0E0E0 #D0D0D0 #C0C0C0 #B0B0B0 #A0A0A0 #909090 #808080 #707070 #606060 #505050 #404040 #303030 #202020 #101010 #000000
```

<div style="display: inline-block; width: 85px; height: 30px; background-color: #FFFFFF;">#FFFFFF</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #F0F0F0;">#F0F0F0</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #E0E0E0;">#E0E0E0</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #D0D0D0;">#D0D0D0</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #C0C0C0;">#C0C0C0</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #B0B0B0;">#B0B0B0</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #A0A0A0;">#A0A0A0</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #909090;">#909090</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #808080; color: white">#808080</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #707070; color: white">#707070</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #606060; color: white">#606060</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #505050; color: white">#505050</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #404040; color: white">#404040</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #303030; color: white">#303030</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #202020; color: white">#202020</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #101010; color: white">#101010</div>
<div style="display: inline-block; width: 85px; height: 30px; background-color: #000000; color: white">#000000</div>

(Please refer to
**Leigh, A., & Susilo, T. (2009). Is voting skin-deep? Estimating the effect of candidate ballot photographs on election
outcomes. _Journal of Economic Psychology_, 30(1), 61-70.** for more details.)

#### 7. Convert the `color` images to `black/white` images

and then do the classification using `bw` palette

```shell
stone -bw (or --black_white)
```

For example:

<div style="display: flex; justify-content: center;align-items:flex-end;">
    <div style="text-align: center;flex:1; margin:10px;">
        <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/demo.png"  alt="Demo picture" />
        <p>1. Input</p>
    </div>
    <div style="text-align: center;flex:1; margin:10px;">
        <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/demo_bw.png"  alt="Black/white Demo picture" />
        <p>2. Convert to black/white image</p>
    </div>
    <div style="text-align: center;flex:1; margin:10px;">
        <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/demo_bw-1.png"  alt="Report image" />
        <p>3. The final report image</p>
    </div>
</div>

NB: we did not do the opposite, i.e., convert `black/white` images to `color` images
because the current AI models cannot accurately "guess" the color of the skin from a `black/white` image.
It can further bias the analysis results.

#### 8. Tune parameters of face detection

The rest parameters of `CONFIG` are used to detect face.
Please refer to https://stackoverflow.com/a/20805153/8860079 for detailed information.

#### 9. Multiprocessing settings

```shell
stone --n_workers <Any Positive Integer>
```

Use `--n_workers` to specify the number of workers to process images in parallel, defaults to the number of CPUs in your
system.

#### 10. Used as a library by importing into other projects

You can refer to the following code snippet:

```python
import stone
from json import dumps

# process the image
result = stone.process(image_path, image_type, palette, *other_args, return_report_image=True)
# show the report image
report_images = result.pop("report_images")  # obtain and remove the report image from the `result`
face_id = 1
stone.show(report_images[face_id])

# convert the result to json
result_json = dumps(result)
```

`stone.process` is the main function to process the image.
It has the same parameters as the command line version.

It will return a `dict`, which contains the process result and report image(s) (if required,
i.e., `return_report_image=True`).

You can further use `stone.show` to show the report image(s).
And convert the result to `json` format.

The `result_json` will be like:

```json
{
  "basename": "demo",
  "extension": ".png",
  "image_type": "color",
  "faces": [
    {
      "face_id": 1,
      "dominant_colors": [
        {
          "color": "#C99676",
          "percent": "0.67"
        },
        {
          "color": "#805341",
          "percent": "0.33"
        }
      ],
      "skin_tone": "#9D7A54",
      "tone_label": "CF",
      "accuracy": 86.27
    }
  ]
}
```


# Citation

If you are interested in our work, please cite:

```bibtex
@article{https://doi.org/10.1111/ssqu.13242,
    author = {Rej\'{o}n Pi\tilde{n}a, Ren\'{e} Alejandro and Ma, Chenglong},
    title = {Classification Algorithm for Skin Color (CASCo): A new tool to measure skin color in social science research},
    journal = {Social Science Quarterly},
    volume = {n/a},
    number = {n/a},
    pages = {},
    keywords = {colorism, measurement, photo elicitation, racism, skin color, spectrometers},
    doi = {https://doi.org/10.1111/ssqu.13242},
    url = {https://onlinelibrary.wiley.com/doi/abs/10.1111/ssqu.13242},
    eprint = {https://onlinelibrary.wiley.com/doi/pdf/10.1111/ssqu.13242},
    abstract = {Abstract Objective A growing body of literature reveals that skin color has significant effects on people's income, health, education, and employment. However, the ways in which skin color has been measured in empirical research have been criticized for being inaccurate, if not subjective and biased. Objective Introduce an objective, automatic, accessible and customizable Classification Algorithm for Skin Color (CASCo). Methods We review the methods traditionally used to measure skin color (verbal scales, visual aids or color palettes, photo elicitation, spectrometers and image-based algorithms), noting their shortcomings. We highlight the need for a different tool to measure skin color Results We present CASCo, a (social researcher-friendly) Python library that uses face detection, skin segmentation and k-means clustering algorithms to determine the skin tone category of portraits. Conclusion After assessing the merits and shortcomings of all the methods available, we argue CASCo is well equipped to overcome most challenges and objections posed against its alternatives. While acknowledging its limitations, we contend that CASCo should complement researchers. toolkit in this area.}
}
```

# Contributing

👋 Welcome to **SkinToneClassifier**! We're excited to have your contributions. Here's how you can get involved:

1. 💡 **Discuss New Ideas**: Have a creative idea or suggestion? Start a discussion in
   the [Discussions](https://github.com/ChenglongMa/SkinToneClassifier/discussions) tab to share your thoughts and
   gather feedback from the community.

2. ❓ **Ask Questions**: Got questions or need clarification on something in the repository? Feel free to open
   an [Issue](https://github.com/ChenglongMa/SkinToneClassifier/issues) labeled as a "question" or participate
   in [Discussions](https://github.com/ChenglongMa/SkinToneClassifier/discussions).

3. 🐛 **Issue a Bug**: If you've identified a bug or an issue with the code, please open a
   new [Issue](https://github.com/ChenglongMa/SkinToneClassifier/issues) with a clear description of the problem, steps
   to reproduce it, and your environment details.

4. ✨ **Introduce New Features**: Want to add a new feature or enhancement to the project? Fork the repository, create a
   new branch, and submit a [Pull Request](https://github.com/ChenglongMa/SkinToneClassifier/pulls) with your changes.
   Make sure to follow our contribution guidelines.

5. 💖 **Funding**: If you'd like to financially support the project, you can do so
   by [sponsoring the repository on GitHub](https://github.com/sponsors/ChenglongMa). Your contributions help us
   maintain and improve the project.

# Disclaimer

The images used in this project are from [Flickr-Faces-HQ Dataset (FFHQ)](https://github.com/NVlabs/ffhq-dataset), 
which is licensed under the [Creative Commons BY-NC-SA 4.0 license](https://github.com/NVlabs/ffhq-dataset/blob/master/LICENSE.txt).

Thank you for considering contributing to **SkinToneClassifier**. 
We value your input and look forward to collaborating with you!
