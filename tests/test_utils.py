import unittest
from pathlib import Path

from stone.image import default_tone_labels
from stone.utils import build_image_paths, resolve_labels, alphabet_id


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.image_path = str(Path("./mock_data/images").resolve())
        # Sorted image paths
        self.expected_recursive_image_paths = [
            f"{self.image_path}/fake_img_1.gif",  # In default, sorted by the trailing number
            f"{self.image_path}/fake_img_2.jpeg",
            f"{self.image_path}/subfolder/sub_fake_img_3.gif",
            f"{self.image_path}/subfolder/sub_fake_img_4.jpeg",
            f"{self.image_path}/fake_img_10.webp",  # Sorted by length of the filename if the trailing number is the same
            f"{self.image_path}/subfolder/sub_fake_img_10.jpg",
            f"{self.image_path}/subfolder/sub_fake_img_21.png",
            f"{self.image_path}/fake_img_22.png",
            f"{self.image_path}/fake_img_100.jpg",
            f"{self.image_path}/subfolder/sub_fake_img_101.webp",
        ]

        self.expected_non_recursive_image_paths = [
            p for p in self.expected_recursive_image_paths if "subfolder" not in p
        ]

    def should_exclude_folder(self, paths, excluded_folders):
        """
        Check if the paths do not contain any of the excluded folders.
        :param paths:
        :param excluded_folders:
        :return:
        """
        self.assertTrue(
            all(
                [
                    excluded_folder != path.relative_to(self.image_path).parts[0]
                    for path in paths
                    for excluded_folder in excluded_folders
                ]
            )
        )

    def test_single_directory_recursive(self):
        image_paths = build_image_paths(self.image_path, recursive=True)
        self.assertTrue(isinstance(image_paths, list))
        self.assertEqual(len(image_paths), 10)
        self.should_exclude_folder(image_paths, ["debug", "log"])
        for i in range(len(image_paths)):
            actual = image_paths[i]
            expected = Path(self.expected_recursive_image_paths[i])
            self.assertTrue(actual.samefile(expected), msg=f"{i}: {actual} != {expected}")

    def test_single_directory_non_recursive(self):
        image_paths = build_image_paths(self.image_path, recursive=False)
        self.assertTrue(isinstance(image_paths, list))
        self.assertEqual(len(image_paths), 5)
        self.should_exclude_folder(image_paths, ["subfolder", "debug", "log"])
        self.assertListEqual(
            image_paths,
            [Path(p).resolve() for p in self.expected_non_recursive_image_paths],
        )

    def test_multiple_directories_recursive(self):
        paths = build_image_paths([self.image_path, f"{self.image_path}/subfolder"], recursive=True)
        self.assertTrue(isinstance(paths, list))
        self.assertEqual(len(paths), 10)

    def test_single_file(self):
        paths = build_image_paths(self.expected_recursive_image_paths[0])
        self.assertTrue(isinstance(paths, list))
        self.assertEqual(len(paths), 1)

    def test_multiple_files(self):
        paths = build_image_paths(self.expected_recursive_image_paths)
        self.assertTrue(isinstance(paths, list))
        self.assertEqual(len(paths), len(self.expected_recursive_image_paths))

    def test_single_url(self):
        paths = build_image_paths("http://example.com/image.jpg")
        self.assertTrue(isinstance(paths, list))
        self.assertEqual(len(paths), 1)

    def test_no_valid_images(self):
        with self.assertRaises(FileNotFoundError):
            build_image_paths("/path/to/nonexistent")

    def test_resolve_labels_in_digits(self):
        start, end, step = 1, 12, 1
        labels = [f"{start}-{end}"]
        expected = "1 2 3 4 5 6 7 8 9 10 11 12".split()
        actual = resolve_labels(labels)
        self.assertListEqual(actual, expected)

    def test_resolve_labels_in_alphabet(self):
        start, end, step = "a", "z", 2
        labels = [f"{start}-{end}-{step}"]
        expected = list("ACEGIKMOQSUWY")
        actual = resolve_labels(labels)
        self.assertListEqual(actual, expected)

    def test_resolve_labels_step_is_zero(self):
        start, end, step = "a", "z", 0
        labels = [f"{start}-{end}-{step}"]
        expected = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        actual = resolve_labels(labels)
        self.assertListEqual(actual, expected)

    def test_resolve_labels_start_less_than_end(self):
        start, end, step = 12, 1, 1
        labels = [f"{start}-{end}"]
        expected = labels
        actual = resolve_labels(labels)
        self.assertListEqual(actual, expected)

    def test_default_tone_labels(self):
        tone_palette = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        actual_labels = default_tone_labels(tone_palette)
        self.assertListEqual(
            actual_labels,
            list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        )

    def test_alphabet_id(self):
        self.assertEqual(alphabet_id(0), "A")
        self.assertEqual(alphabet_id(25), "Z")
        self.assertEqual(alphabet_id(26), "AA")
        self.assertEqual(alphabet_id(27), "AB")
        self.assertEqual(alphabet_id(51), "AZ")
        self.assertEqual(alphabet_id(52), "BA")
        self.assertEqual(alphabet_id(77), "BZ")
        self.assertEqual(alphabet_id(78), "CA")

    def test_default_tone_labels_with_more_than_26_tones(self):
        tone_palette = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") * 2
        actual_labels = default_tone_labels(tone_palette)
        self.assertListEqual(
            actual_labels,
            list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX", "AY", "AZ"],
        )


if __name__ == "__main__":
    unittest.main()
