import json
from os import PathLike
from typing import NamedTuple, Self, List, TYPE_CHECKING

if TYPE_CHECKING:
    from pyarn.lockfile import Lockfile


class Dependency(NamedTuple):
    name: str
    asked_version: str
    used_version: str
    integrity: str


class LockFileContent:

    def __init__(self) -> None:
        super().__init__()
        self._dependencies: List[Dependency] = []

    @classmethod
    def from_yarn_file(
        cls, path: int | str | bytes | PathLike[str] | PathLike[bytes]
    ) -> Self:
        from pyarn.lockfile import Lockfile

        yarn_lock_file = Lockfile.from_file(path)

        return cls.from_lockfile(yarn_lock_file)

    @classmethod
    def from_lockfile(cls, yarn_lockfile: "Lockfile") -> Self:
        instance = cls()

        for dep_key, data in yarn_lockfile.data.items():
            dep_name, version_asked = dep_key.rsplit("@", 1)

            version = data["version"]
            integrity = data["integrity"]

            instance.add_dependency(dep_name, version_asked, version, integrity)

        return instance

    def add_dependency(self, name: str, marked: str, version: str, integrity: str):
        self._dependencies.append(Dependency(name, marked, version, integrity))

    def as_security_audit_payload(self) -> str:

        requires_map = {
            dependency.name: dependency.asked_version
            for dependency in self._dependencies
        }

        dependencies_map = {
            dep.name: {"version": dep.used_version, "integrity": dep.integrity}
            for dep in self._dependencies
        }

        payload = {
            "name": "npm_audit_test",
            "version": "1.0.0",
            "requires": requires_map,
            "dependencies": dependencies_map,
        }

        return json.dumps(payload)
