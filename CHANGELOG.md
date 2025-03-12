# Changelogs

## v1.2.6

<details markdown="1" open>
  <summary><i>Click here to show more.</i></summary>

In this version, we have made the following changes:

1. ✨ **NEW!**: We have added one new built-in skin tone palette: Monk Skin Tone Palette.

</details>

## v1.2.5

<details markdown="1" open>
  <summary><i>Click here to show more.</i></summary>

In this version, we have made the following changes:

1. ✨ **NEW!**: We have added two new built-in skin tone palettes.
    * The all available colored palettes are `perla`, `yadon-ostfeld`, `proder`.
    * You can use the `-p` option to specify the palette for the processed images.
      - For example, `stone -i ./path/to/images/ -p yadon-ostfeld`.
    * The default palette `perla` is used for color images, and the `bw` palette is used for black/white
      images.
2. ✨ **NEW!**: We have added some new use cases like Web API based projects in the documentation.

</details>

## v1.2.4

<details markdown="1">
  <summary><i>Click here to show more.</i></summary>

In this version, we have made the following changes:

1. 🐛 **FIX!**: We fixed a bug where the app will crash when using the `-bw` option.
     
Thanks [ergo70](https://github.com/ergo70)'s feedback in [issue#25](https://github.com/ChenglongMa/SkinToneClassifier/issues/25).

</details>

## v1.2.3

<details markdown="1">
  <summary><i>Click here to show more.</i></summary>

In this version, we have made the following changes:

1. 🧬 **CHANGE!**: We change the GUI mode to **optional**.
    * Now, you can install the GUI mode by running:
      * ```bash
        pip install skin-tone-classifier[all] --upgrade
        ```
      * It will support both the **CLI** mode and the **GUI** mode.
    * If you don't specify the `[all]` option, the app will install the CLI mode only.
2. 🧬 **CHANGE!**: [For developer]. We base the project to `project.toml` instead of `setup.py`.
     

</details>

## v1.2.0

<details markdown="1">
  <summary><i>Click here to show more.</i></summary>

In this version, we have made the following changes:

1. ✨ **NEW!**: We add a GUI version of `stone` for users who are not familiar with the command line interface.
    * You can use the config GUI of `stone` to process the images.
    * See more information at [here](#use-stone-in-a-gui).
2. ✨ **NEW!**: We add new **patterns** in the `-l` (or `--labels`) option to set the skin tone labels.
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