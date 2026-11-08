import re
from os import PathLike
from typing import (
    Dict,
    List,
    Mapping,
    NamedTuple,
    Optional,
    Self,
    Tuple,
    TYPE_CHECKING,
    Union,
)

if TYPE_CHECKING:
    from lockfile_parser import PoetryLockParser


def parse_dependency_str(dependency_str: str) -> Tuple[str, str]:
    without_space = dependency_str.replace(" ", "")
    split = re.split("[^a-zA-Z0-9-_.]", without_space, 1)
    if len(split) == 1:
        return split[0], ""
    return split[0], without_space[len(split[0]) :]


def asked_version_map(pyproject_path: Union[str, PathLike]) -> Mapping[str, str]:
    import toml

    with open(pyproject_path) as f:
        pyproject = toml.load(f)

    poetry_tool_dependencies = (
        pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {})
    )
    asked_versions: Dict[str, str] = dict(poetry_tool_dependencies.items())

    project = pyproject.get("project", {})

    for dependency in project.get("dependencies", []):
        package, asked_version = parse_dependency_str(dependency)
        asked_versions[package] = asked_version

    for dependencies in project.get("optional-dependencies", {}).values():
        for dependency in dependencies:
            package, asked_version = parse_dependency_str(dependency)
            asked_versions[package] = asked_version

    return asked_versions


class Dependency(NamedTuple):
    name: str
    asked_version: str
    used_version: str


class LockFileContent:

    def __init__(self) -> None:
        super().__init__()
        self._dependencies: List[Dependency] = []

    @classmethod
    def from_poetry_file(
        cls,
        poetry_lock_path: Union[str, bytes, PathLike[str], PathLike[bytes]],
        pyproject_path: Optional[Union[str, bytes, PathLike[str], PathLike[bytes]]] = None,
    ) -> Self:
        from lockfile_parser import PoetryLockParser

        poetry_lock_file = PoetryLockParser(str(poetry_lock_path))

        asked_versions = (
            asked_version_map(pyproject_path) if pyproject_path is not None else {}
        )

        return cls.from_lockfile(poetry_lock_file, asked_versions)

    @classmethod
    def from_lockfile(
        cls,
        poetry_lockfile: "PoetryLockParser",
        asked_versions: Optional[Mapping[str, str]] = None,
    ) -> Self:
        instance = cls()
        asked_versions = asked_versions or {}

        for dep_name, data in poetry_lockfile.package_map.items():
            source = data.get("source")
            if source is not None and source.get("type") != "pypi":
                continue

            version = data["version"]
            asked_version = asked_versions.get(dep_name, "")

            instance.add_dependency(dep_name, asked_version, version)

        return instance

    def add_dependency(self, name: str, asked_version: str, version: str):
        self._dependencies.append(Dependency(name, asked_version, version))

    @property
    def dependencies(self) -> List[Dependency]:
        return list(self._dependencies)

    @property
    def count(self) -> int:
        return len(self._dependencies)
