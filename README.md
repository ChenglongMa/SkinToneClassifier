# <u>S</u>kin <u>Tone</u> Classifier (stone)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/skin-tone-classifier)
![PyPI](https://img.shields.io/pypi/v/skin-tone-classifier)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/ChenglongMa/SkinToneClassifier?include_prereleases)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

An easy-to-use library for skin tone classification.

This can be used to detect **face** or **skin area** in the specified images.
The detected skin tones are then classified into the specified color categories.
The library finally generates results to report the detected faces (if any),
dominant skin tones and color category.

---

# Changelogs 

## (v1.0.0)

We officially release the 1.0.0 version of the library. In this version, we have made the following changes: 

1. ✨ **NEW!**: We add the `threshold` parameter to control the proportion of face areas (Defaults to 0.3). 
   * In previous versions, the library could incorrectly identify non-face areas as faces, such as shirts, collars, necks, etc.
   In order to improve its accuracy, the new version will further calculate the proportion of skin in the recognized area 
   after recognizing the facial area. If it is less than the `threshold` value, the recognition area will be ignored.
   (While it's still not perfect, it's an improvement over what it was before.)
2. ✨ **NEW!**: Now, we will back up the previous results if it already exists. 
The backup file will be named as `result_bak_<current_timestamp>.csv`.
3. 🐛 **FIX!**: We fix the bug that the `image_type` option does not work in the previous version.
4. 🐛 **FIX!**: We fix the bug that the library will create an empty `log` folder when checking the help information by running `stone -h`.

## (v0.2.0)

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
         <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/lena_std-1.jpg" alt="Processing color image" style="display: block; margin: 20px">
         <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/lena_std_bw-1.jpg" alt="Processing black/white image" style="display: block; margin: 20px">
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

# Installation

To install SkinToneClassifier:

```shell
pip install skin-tone-classifier --upgrade
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

Then, you can find the processed image in `./debug/color/faces_1` folder, e.g.,

<div align="center">
   <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/lena_std-1.jpg"  alt="processed Lenna picture" style="display: block; margin: auto"/>
</div>

In this image, from left to right you can find the following information:

1. detected face with a label (Face 1) enclosed by a rectangle.
2. dominant colors.
    1. _The number of colors depends on settings (default is 2) and their sizes depend on their proportion._
3. specified color palette and the target label is enclosed by a rectangle.
4. you can find a summary text at the bottom.

Furthermore, there will be a report file named `result.csv` which contains more detailed information, e.g.,

| file       | image type | face id | dominant 1 | props 1 | dominant 2 | props 2 | skin tone | PERLA | accuracy(0-100) |
|------------|------------|---------|------------|---------|------------|---------|-----------|-------|-----------------|
| lena_std-1 | color      | 1       | #CF7371    | 0.52    | #E4A89F    | 0.48    | #E7C1B8   | CI    | 85.39           |

### Interpretation of the table

1. `file`: the filename of the processed image.
2. `image type`: the type of the processed image, i.e., `color` or `bw` (black/white).
3. `face id`: the id of the detected face, which matches the reported image. `NA` means no face has been detected.
4. `dominant n`: the `n`-th dominant color of the detected face.
5. `props n`: the proportion of the `n`-th dominant color, (0~1.0).
6. `skin tone`: the skin tone category of the detected face.
7. `PERLA`: the **label** of skin tone category of the detected face.
8. `accuracy`: the accuracy of the skin tone category of the detected face, (0~100). The larger the better.

## Detailed Usage

To see the usage and parameters, run:

```shell
stone -h
```

Output in console:

```text
usage: stone [-h] [-i IMAGE FILENAME [IMAGE FILENAME ...]] [-p COLOR [COLOR ...]] [-l LABEL [LABEL ...]]
                   [-t IMAGE TYPE] [-d] [-bw] [-o DIRECTORY] [--n_workers N_WORKERS] [--n_colors N]
                   [--new_width WIDTH] [--scale SCALE] [--min_nbrs NEIGHBORS] [--min_size WIDTH [HEIGHT ...]]

Skin Tone Classifier

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE FILENAME [IMAGE FILENAME ...], --images IMAGE FILENAME [IMAGE FILENAME ...]
                        Image filename(s) to process;
                        Supports multiple values separated by space, e.g., "a.jpg b.png";
                        Supports directory or file name(s), e.g., "./path/to/images/ a.jpg";
                        The app will search all images in current directory in default.
  -p COLOR [COLOR ...], --palette COLOR [COLOR ...]
                        Skin tone palette;
                        Supports RGB hex value leading by "#" or RGB values separated by comma(,),
                        E.g., "-p #373028 #422811" or "-p 255,255,255 100,100,100"
  -l LABEL [LABEL ...], --labels LABEL [LABEL ...]
                        Skin tone labels; default values are the uppercase alphabet list.
  -t IMAGE TYPE, --image_type IMAGE TYPE
                        Specify whether the inputs image(s) is/are colored or black/white.
                        Valid choices are: "auto", "color" or "bw",
                        Defaults to "auto", which will be detected automatically.
  -d, --debug           Whether to output processed images, used for debugging and verification.
  -bw, --black_white    Whether to convert the input to black/white image(s).
                        Then the app will use the black/white palette to classify the image.
  -o DIRECTORY, --output DIRECTORY
                        The path of output file, defaults to current directory.
  --n_workers N_WORKERS
                        The number of workers to process the images, defaults to the number of CPUs in the system.
  --n_colors N          CONFIG: the number of dominant colors to be extracted, defaults to 2.
  --new_width WIDTH     CONFIG: resize the images with the specified width. Negative value will be ignored, defaults to 250.
  --scale SCALE         CONFIG: how much the image size is reduced at each image scale, defaults to 1.1
  --min_nbrs NEIGHBORS  CONFIG: how many neighbors each candidate rectangle should have to retain it.
                        Higher value results in less detections but with higher quality, defaults to 5
  --min_size WIDTH [HEIGHT ...]
                        CONFIG: minimum possible face size. Faces smaller than that are ignored, defaults to "90 90".
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
stone -p (or --palette) #373028 #422811 #fbf2f3
```

NB: Values start with '#' and are separated by space.

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

#### 4. Store report images for debugging

```shell
stone -d (or --debug)
```

This option will store the report image (like the Lenna example above) in
`./path/to/output/debug/<image type>/faces_<n>` folder,
where `<image type>` indicates if the image is `color` or `bw` (black/white);
`<n>` is the number of faces detected in the image.

**By default, to save space, the app does not store report images.**

Like in the `result.csv` file, there will be more than one report images if 2 or more faces were detected.

#### 5. Specify the types of the input image(s)

5.1 The input are color images

```shell
stone -t (or --image_type) color
```

5.2 The input are black/white images

```shell
stone -t (or --image_type) bw
```

5.3 **In default**, the app will detect the image type automatically, i.e.,

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

#### 6. Convert the `color` images to `black/white` images and then do the classification using `bw` palette

```shell
stone -bw (or --black_white)
```

For example:

<div style="display: flex; align-items: center; justify-content: center;">
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/lena_std.jpg"  alt="Lenna picture" style="display: block; margin: 20px"/>
        <p>Input</p>
    </div>
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/lena_std_bw.jpg"  alt="Black/white Lenna picture" style="display: block; margin: 20px"/>
        <p>Convert to black/white image</p>
    </div>
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/ChenglongMa/SkinToneClassifier/main/docs/lena_std_bw-1.jpg"  alt="Report image" style="display: block; margin: 20px"/>
        <p>The final report image</p>
    </div>
</div>

NB: we did not do the opposite, i.e., convert `black/white` images to `color` images 
because the current AI models cannot accurately "guess" the color of the skin from a `black/white` image.
It can further bias the analysis results.

#### 7. Tune parameters of face detection

The rest parameters of `CONFIG` are used to detect face.
Please refer to https://stackoverflow.com/a/20805153/8860079 for detailed information.

#### 8. Multiprocessing settings

```shell
stone --n_workers <Any Positive Integer>
```

Use `--n_workers` to specify the number of workers to process images in parallel, defaults to the number of CPUs in your system.
