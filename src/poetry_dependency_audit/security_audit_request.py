from typing import TYPE_CHECKING

from .audit import Audit, Package

if TYPE_CHECKING:
    from .lock_file_content import LockFileContent


def request_pypi_info(package_name: str, version: str) -> Package:
    import requests

    response = requests.get(
        url=f"https://pypi.org/pypi/{package_name}/{version}/json",
    )

    if response.status_code != 200:
        raise ValueError(
            f"Got status code {response.status_code}, expected 200 "
            f"for {package_name} {version}"
        )

    return Package.model_validate_json(response.content)


def request_security_audit(lock_file_content: "LockFileContent") -> Audit:
    return Audit(
        packages={
            dependency.name: request_pypi_info(
                dependency.name, dependency.used_version
            )
            for dependency in lock_file_content.dependencies
        }
    )
