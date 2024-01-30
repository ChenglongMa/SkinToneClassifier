<div style="text-align:center;">
    <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/stone-logo.png" alt="stone logo">
</div>

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/skin-tone-classifier)
[![PyPI](https://img.shields.io/pypi/v/skin-tone-classifier)](https://pypi.org/project/skin-tone-classifier/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/skin-tone-classifier)](https://pypi.org/project/skin-tone-classifier/)
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/ChenglongMa/SkinToneClassifier?include_prereleases)](https://github.com/ChenglongMa/SkinToneClassifier/releases/latest)
[![GitHub License](https://img.shields.io/github/license/ChenglongMa/SkinToneClassifier)](https://github.com/ChenglongMa/SkinToneClassifier/blob/main/LICENSE)
[![GitHub Repo stars](https://img.shields.io/github/stars/ChenglongMa/SkinToneClassifier)](https://github.com/ChenglongMa/SkinToneClassifier)

An easy-to-use library for skin tone classification.

This can be used to detect **face** or **skin area** in the specified images.
The detected skin tones are then classified into the specified color categories.
The library finally generates results to report the detected faces (if any),
dominant skin tones and color categories.

*If you find this project helpful, please
consider [giving it a star](https://github.com/ChenglongMa/SkinToneClassifier)* ⭐. *It would be a great encouragement
for me!*

---

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Installation](#installation)
  - [Install from pip](#install-from-pip)
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
- [Changelogs](#changelogs)
  - [v1.2.0](#v120)
  - [v1.1.3](#v113)
  - [v1.1.2](#v112)
  - [v1.1.1](#v111)
  - [v1.1.0](#v110)
  - [v1.0.1](#v101)
  - [v1.0.0](#v100)
  - [v0.2.0](#v020)
- [Citation](#citation)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Installation

## Install from pip

```shell
pip install skin-tone-classifier --upgrade
```

## Install from source

```shell
git clone git@github.com:ChenglongMa/SkinToneClassifier.git
cd SkinToneClassifier
pip install -e . --verbose
```

# HOW TO USE

> [!TIP]
>
> You can combine the following documents
> and [running examples](https://colab.research.google.com/drive/1k-cryEZ9PInJRXWIi17ib66ufYV2Ikwe?usp=sharing) in
> Google
> Colab to understand the usage of this library more intuitively.
>
> See the running
> examples [here](https://colab.research.google.com/drive/1k-cryEZ9PInJRXWIi17ib66ufYV2Ikwe?usp=sharing).

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
> It is recommended to install v1.2.1, which supports Python 3.9+.
> 
> If you have installed v1.2.0, please upgrade to v1.2.1 by running 
> 
> `pip install skin-tone-classifier --upgrade`
> 

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

# Changelogs

## v1.2.0

<details markdown="1" open>
  <summary><i>Click here to show more.</i></summary>

In this version, we have made the following changes:

1. ✨ **NEW!**: We add a GUI version of `stone` for users who are not familiar with the command line interface.
    * You can use the config GUI of `stone` to process the images.
    * See more information at [here](#use-stone-in-a-gui).

</details>

## v1.1.3

<details markdown="1" open>
  <summary><i>Click here to show more.</i></summary>

In this version, we have made the following changes:

1. ✨ **NEW!**: We add new **patterns** in the `-l` (or `--labels`) option to set the skin tone labels.
    * Now, you can use the following patterns to set the skin tone labels:
        * **Default value**: the uppercase alphabet list leading by the image type (`C` for `color`; `B`
          for `Black&White`).
        * Specify the labels directly using _a space_ as delimiters, e.g., `-l A B C D E` or `-l 1 2 3 4 5`.
        * Specify the range of labels using _a hyphen_ as delimiters, e.g.,
            * `-l A-E` (equivalent to `-l A B C D E`);
            * `-l A-E-2` (equivalent to `-l A C E`);
            * `-l 1-5` (equivalent to `-l 1 2 3 4 5`);
            * `-l 1-10-3` (equivalent to `-l 1 4 7 10`);
    * **NB**: The number of skin tone labels should be equal to the number of colors in the palette.

</details>

## v1.1.2

<details markdown="1">
  <summary><i>Click here to show more.</i></summary>

In this version, we have made the following changes:

1. 🐛 **FIX!**: We fixed a bug where the app will crash when using the `-bw` option.
   Error message: `cannot reshape array of size 62500 into shape (3)`.
2. 🐛 **FIX!**: We fixed a bug where the app may identify the image type as `color` when using the `-bw` option.

</details>

## v1.1.1

<details markdown="1">
  <summary><i>Click here to show more.</i></summary>

In this version, we have made the following changes:

1. ✨ **NEW!**: We add the `-v` (or `--version`) option to show the version number.
2. ✨ **NEW!**: We add the `-r` (or `--recursive`) option to **enable** recursive search for images.
    * For example, `stone -i ./path/to/images/ -r` will search all images in the `./path/to/images/` directory **and its
      subdirectories**.
    * `stone -i ./path/to/images/` will only search images in the `./path/to/images/` directory.
3. 🐛 **FIX!**: We fixed a bug where the app cannot correctly identify the current folder if `-i` option is not
   specified.

</details>

## v1.1.0

<details markdown="1">
  <summary><i>Click here to show more.</i></summary>

In this version, we have made the following changes:

1. ✨ **NEW!**: Now, `stone` can not only be run on **the command line**, but can also be **imported** into other
   projects for use. Check [this](#9-used-as-a-library-by-importing-into-other-projects) for more details.
    * We expose the `process` and `show` functions in the `stone` package.
2. ✨ **NEW!**: We add `URL` support for the input images.
    * Now, you can specify the input image as a URL, e.g., `https://example.com/images/pic.jpg`. Of course, you can mix
      the URLs and local filenames.
3. ✨ **NEW!**: We add **recursive search** support for the input images.
    * Now, when you specify the input image as a directory, e.g., `./path/to/images/`.
      The app will search all images in the directory recursively.
4. 🧬 **CHANGE!**: We change the column header in `result.csv`:
    * `prop` => `percent`
    * `PERLA` => `tone label`
5. 🐛 **FIX!**: We fixed a bug where the app would not correctly sort files that did not contain numbers in their
   filenames.

</details>

## v1.0.1

<details markdown="1">
  <summary><i>Click here to show more.</i></summary>

1. 👋 **BYE**: We have removed the function to pop up a resulting window when processing a **single** image.

    * It can raise an error when running the app in a **web browser** environment, e.g., Jupyter Notebook or Google
      Colab.
    * If you want to see the processed image, please use the `-d` option to store the report image in the `./debug`
      folder.

</details>

## v1.0.0

<details markdown="1">
  <summary><i>Click here to show more.</i></summary>

🎉**We have officially released the 1.0.0 version of the library!** In this version, we have made the following changes:

1. ✨ **NEW!**: We add the `threshold` parameter to control the minimum percentage of required face areas (Defaults to
   0.15).
    * In previous versions, the library could incorrectly identify non-face areas as faces, such as shirts, collars,
      necks, etc.
      In order to improve its accuracy, the new version will further calculate the proportion of skin in the recognized
      area
      after recognizing the facial area. If it is less than the `threshold` value, the recognition area will be ignored.
      (While it's still not perfect, it's an improvement over what it was before.)
2. ✨ **NEW!**: Now, we will back up the previous results if it already exists.
   The backup file will be named as `result_bak_<current_timestamp>.csv`.
3. 🐛 **FIX!**: We fix the bug that the `image_type` option does not work in the previous version.
4. 🐛 **FIX!**: We fix the bug that the library will create an empty `log` folder when checking the help information by
   running `stone -h`.

</details>

## v0.2.0

<details markdown="1">
  <summary><i>Click here to show more.</i></summary>

In this version, we have made the following changes:

1. ✨ **NEW!**: Now we support skin tone classification for **black and white** images.
    * In this case, the app will use different skin tone palettes for color images and black/white images.
    * We use a new parameter `-t` or `--image_type` to specify the type of the input image.
      It can be `color`, `bw` or `auto`(default).
      `auto` will let the app automatically detect whether the input is color or black/white image.
    * We use a new parameter `-bw` or `--black_white` to specify whether to convert the input to black/white image.
      If so, the app will convert the input to black/white image and then classify the skin tones based on the
      black/white palette.

      For example:
      <div style="display: flex; align-items: center;">
         <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/demo-1.png" alt="Processing color image" style="display: block; margin: 20px">
         <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/demo_bw-1.png" alt="Processing black/white image" style="display: block; margin: 20px">
      </div>

2. ✨ **NEW!**: Now we support **multiprocessing** for processing the images. It will largely speed up the processing.
    * The number of processes is set to the number of CPU cores by default.
    * You can specify the number of processes by `--n_workers` parameter.
3. 🧬 **CHANGE!**: We add more details in the report image to facilitate the debugging, as shown above.
    * We add the face id in the report image.
    * We add the effective face or skin area in the report image. In this case, the other areas are blurred.
4. 🧬 **CHANGE!**: Now, we save the report images into different folders based on their `image_type` (color or
   black/white) and the number of detected faces.
    * For example, if the input image is **color** and there are **2 faces** detected, the report image will be saved
      in `./debug/color/faces_2/` folder.
    * If the input image is **black/white** and no face has been detected, the report image will be saved
      in `./debug/bw/faces_0/` folder.
    * You can easily to tune the parameters and rerun the app based on the report images in the corresponding folder.
5. 🐛 **FIX!**: We fix the bug that the app will crash when the input image has dimensionality errors.
    * Now, the app won't crash and will report the error message in `./result.csv`.

</details>

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

The images used in this project are from [Flickr-Faces-HQ Dataset (FFHQ)](https://github.com/NVlabs/ffhq-dataset), which
is licensed under
the [Creative Commons BY-NC-SA 4.0 license](https://github.com/NVlabs/ffhq-dataset/blob/master/LICENSE.txt)

Thank you for considering contributing to **SkinToneClassifier**. We value your input and look forward to collaborating
with you!
