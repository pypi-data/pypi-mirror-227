from __future__ import annotations

import dataclasses
import enum
import pathlib
import datetime

import gi

gi.require_version("OSTree", "1.0")

from gi.repository import GLib, Gio, OSTree


class Arch(enum.StrEnum):
    X86_64 = "x86_64"


class Branch(enum.StrEnum):
    SISYPHUS = "sisyphus"
    P10 = "p10"


@dataclasses.dataclass
class Stream:
    repo_root: str
    arch: Arch
    branch: Branch
    name: str = "base"
    osname: str = "altcos"

    def __str__(self) -> str:
        return str(pathlib.Path(self.arch, self.branch, self.name))
    
    def export(self) -> str:
        attrs = [attr for attr in dir(Stream) if isinstance(getattr(Stream, attr), property)]
        exports = [f"export {attr.upper()}={getattr(self, attr)}" for attr in attrs]
        exports.extend([f"export {attr.upper()}={getattr(self, attr)}" for attr in self.__dict__])
        exports.append(f"export STREAM={self}")

        return ";".join(exports)

    @classmethod
    def from_str(cls, repo_root: str, stream: str) -> Stream:
        if len(parts := stream.split("/")) != 3 or any(not part for part in parts):
            raise ValueError(f"invalid stream format :: \"{stream}\"")

        return cls(repo_root, Arch(parts[0]), Branch(parts[1]), parts[2])
    
    @property
    def parent(self) -> Stream:
        """ returns the parent stream, or itself, if itself is the parent """
        return Stream(self.repo_root, self.arch, self.branch, "base")

    @property
    def stream_dir(self) -> pathlib.Path:
        """ current stream directory """
        return pathlib.Path(self.repo_root, self.branch, self.arch, self.name)

    @property
    def alt_dir(self) -> pathlib.Path:
        """ tree of ALT specific directories """
        return self.stream_dir.joinpath("alt")

    @property
    def rootfs_dir(self) -> pathlib.Path:
        return self.parent.stream_dir.joinpath("rootfs")
    
    @property
    def rootfs_archive(self) -> pathlib.Path:
        return self.rootfs_dir.joinpath(f"altcos-latest-{self.arch}.tar")

    @property
    def work_dir(self) -> pathlib.Path:
        return self.alt_dir.joinpath("work")

    @property
    def vars_dir(self) -> pathlib.Path:
        return self.alt_dir.joinpath("vars")

    @property
    def merged_dir(self) -> pathlib.Path:
        return self.work_dir.joinpath("merged")

    @property
    def ostree_dir(self) -> pathlib.Path:
        """ tree of OSTree specific directories """
        return self.parent.stream_dir.joinpath("ostree")

    @property
    def ostree_bare_dir(self) -> pathlib.Path:
        return self.ostree_dir.joinpath("bare")

    @property
    def ostree_archive_dir(self) -> pathlib.Path:
        return self.ostree_dir.joinpath("archive")


class Repository:
    class Mode(enum.StrEnum):
        BARE = "bare"
        ARCHIVE = "archive"
    
    def __init__(self, stream: Stream, mode: Repository.Mode) -> None:
        self.stream = stream
        self.mode = mode

        self.path = stream.ostree_bare_dir \
                if self.mode == Repository.Mode.BARE else stream.ostree_archive_dir

        self.storage: OSTree.Repo = OSTree.Repo.new(Gio.file_new_for_path(str(self.path)))
    
    def open(self) -> Repository:
        self.storage.open(None)
        return self

    def exists(self) -> bool:
        try:
            self.storage.open(None)
        except GLib.Error:
            return False
        return True

    def last_commit(self) -> Commit | None:
        if (hashsum := self.storage.resolve_rev(str(self.stream), True)[1]) is None:
            return None
        return Commit(self, hashsum)

    def commit_by_version(self, version: Version, commit: Commit = None) -> Commit | None:
        if commit is None:
            commit = self.last_commit()

        if commit.version.full == version.full:
            return commit

        if (parent := commit.parent) is None:
            return None

        return self.commit_by_version(version, parent)

    def list_streams(self) -> list[Stream]:
        return [Stream.from_str(self.stream.repo_root, ref)
                for ref in self.storage.list_refs()[1]]


@dataclasses.dataclass
class Version:
    major: int
    minor: int
    branch: Branch
    name: str = "base"
    date: datetime.datetime | None = None

    def __post_init__(self) -> None:
        self.date = self.date or datetime.datetime.now().strftime("%Y%m%d")

    def __str__(self) -> str:
        return f"{self.date}.{self.major}.{self.minor}"

    @classmethod
    def from_str(cls, version: str) -> Version:
        if len(parts := version.split(".")) != 4:
            raise ValueError(f"invalid version format \"{version}\"")
        
        if len(prefix := parts[0].split("_")) != 2:
            raise ValueError(f"invalid version prefix format \"{version}\"")
        
        [branch, name] = Branch(prefix[0]), prefix[1]
        [date, major, minor] = parts[1], *map(int, parts[2:])

        return cls(major, minor, branch, name, date)

    @property
    def full(self) -> str:
        return f"{self.branch}_{self.name}.{self}"
    
    @property
    def like_path(self) -> pathlib.Path:
        return pathlib.Path(self.date, str(self.major), str(self.minor))


@dataclasses.dataclass
class Commit:
    repo: Repository
    hashsum: str

    def __str__(self) -> str:
        return self.hashsum

    def exists(self) -> bool:
        try:
            self.repo.storage.load_commit(self.hashsum)
        except GLib.Error:
            return False
        return True

    @property
    def version(self) -> Version:
        content = self.repo.storage.load_commit(self.hashsum)
        return Version.from_str(content[1][0]["version"])

    @property
    def description(self) -> str:
        return self.repo.storage.load_commit(self.hashsum)[1][4]
    
    @property
    def parent(self) -> Commit | None:
        content = self.repo.storage.load_commit(self.hashsum)
        parent_hashsum = OSTree.commit_get_parent(content[1])

        return Commit(self.repo, parent_hashsum) \
                if parent_hashsum else None


class Platform(enum.StrEnum):
    QEMU = "qemu"
    METAL = "metal"


class Format(enum.StrEnum):
    QCOW2 = "qcow2"
    ISO = "iso"


@dataclasses.dataclass
class Artifact:
    location: str | None = None
    signature: str | None = None
    uncompressed: str | None = None
    uncompressed_signature: str | None = None


@dataclasses.dataclass
class Build:
    platform: Platform
    fmt: Format
    disk: Artifact | None = None
    kernel: Artifact | None = None
    initrd: Artifact | None = None
    rootfs: Artifact | None = None


ALLOWED_BUILDS = {
    Platform.QEMU: {
        Format.QCOW2: None,
    },
    Platform.METAL: {
        Format.ISO: None,
    }
}
