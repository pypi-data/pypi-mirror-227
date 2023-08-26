import pathlib
import unittest

import altcos


class TestStream(unittest.TestCase):
    SR = "<some-path>" # STREAMS_ROOT
    VALID_STREAM = altcos.Stream.from_str(SR, "x86_64/sisyphus/base")
    VALID_SUBSTREAM = altcos.Stream.from_str(SR, "x86_64/sisyphus/k8s")

    def test_like_ostree_ref(self):
        good = "x86_64/sisyphus/base"
        self.assertEqual(good, str(self.VALID_STREAM))

    def test_like_ostree_ref_for_subref(self):
        good = "x86_64/sisyphus/k8s"
        self.assertEqual(good, str(self.VALID_SUBSTREAM))

    def test_valid_stream_init_from_ref(self):
        ref = "x86_64/sisyphus/base"
        try:
            altcos.Stream.from_str(self.SR, ref)
        except ValueError as e:
            self.fail(e)

    def test_valid_stream_init_from_subref(self):
        ref = "x86_64/sisyphus/k8s"
        try:
            altcos.Stream.from_str(self.SR, ref)
        except ValueError as e:
            self.fail(e)

    def test_invalid_stream_init_from_ref(self):
        ref = "x86_4/branch"
        try:
            altcos.Stream.from_str(self.SR, ref)
        except ValueError:
            pass

    def test_invalid_stream_init_from_subref(self):
        ref = "x86_65/Lol/k8s"
        try:
            altcos.Stream.from_str(self.SR, ref)
        except ValueError:
            pass

    def test_stream_dir(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/base")
        self.assertEqual(good, self.VALID_STREAM.stream_dir)

    def test_stream_dir_for_subref(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/k8s")
        self.assertEqual(good, self.VALID_SUBSTREAM.stream_dir)

    def test_rootfs_dir(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/base/rootfs")
        self.assertEqual(good, self.VALID_STREAM.rootfs_dir)

    def test_rootfs_dir_for_subref(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/base/rootfs")
        self.assertEqual(good, self.VALID_SUBSTREAM.rootfs_dir)

    def test_ostree_bare_dir(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/base/ostree/bare")
        self.assertEqual(good, self.VALID_STREAM.ostree_bare_dir)

    def test_ostree_bare_dir_for_subref(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/base/ostree/bare")
        self.assertEqual(good, self.VALID_SUBSTREAM.ostree_bare_dir)

    def test_ostree_archive_dir(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/base/ostree/archive")
        self.assertEqual(good, self.VALID_STREAM.ostree_archive_dir)

    def test_ostree_archive_dir_for_subref(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/base/ostree/archive")
        self.assertEqual(good, self.VALID_SUBSTREAM.ostree_archive_dir)

    def test_vars_dir(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/base/alt/vars")
        self.assertEqual(good, self.VALID_STREAM.vars_dir)

    def test_vars_dir_for_subref(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/k8s/alt/vars")
        self.assertEqual(good, self.VALID_SUBSTREAM.vars_dir)

    def test_work_dir(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/base/alt/work")
        self.assertEqual(good, self.VALID_STREAM.work_dir)

    def test_work_dir_for_subref(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/k8s/alt/work")
        self.assertEqual(good, self.VALID_SUBSTREAM.work_dir)

    def test_merged_dir(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/base/alt/work/merged")
        self.assertEqual(good, self.VALID_STREAM.merged_dir)

    def test_merged_dir_subref(self):
        good = pathlib.Path(f"{self.SR}/sisyphus/x86_64/k8s/alt/work/merged")
        self.assertEqual(good, self.VALID_SUBSTREAM.merged_dir)


class TestVersion(unittest.TestCase):
    def test_valid_version_init_from_str(self):
        try:
            altcos.Version.from_str("sisyphus_base.20230101.1.0")
        except ValueError as e:
            self.fail(e)

    def test_str(self):
        good = "20230101.1.0"
        version = altcos.Version.from_str("sisyphus_base.20230101.1.0")
        self.assertEqual(good, str(version))

    def test_full_version(self):
        good = "sisyphus_base.20230101.1.0"
        version = altcos.Version.from_str("sisyphus_base.20230101.1.0")
        self.assertEqual(good, version.full)

    def test_full_version_for_subref(self):
        good = "sisyphus_k8s.20230101.1.0"
        version = altcos.Version.from_str("sisyphus_k8s.20230101.1.0")
        self.assertEqual(good, version.full)

    def test_like_path(self):
        good = pathlib.Path("20230101/1/0")
        version = altcos.Version.from_str("sisyphus_base.20230101.1.0")
        self.assertEqual(good, version.like_path)


if __name__ == "__main__":
    unittest.main()
