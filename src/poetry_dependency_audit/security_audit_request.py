from typing import TYPE_CHECKING

from .audit import Audit

if TYPE_CHECKING:
    from .lock_file_content import LockFileContent


def request_security_audit(lock_file_content: "LockFileContent") -> Audit:
    import requests

    response = requests.post(
        url="https://registry.npmjs.org/-/npm/v1/security/audits",
        headers={"Content-Type": "application/json; charset=utf-8"},
        data=lock_file_content.as_security_audit_payload(),
    )

    if response.status_code != 200:
        raise ValueError(f"Got status code {response.status_code}, expected 200")

    return Audit.model_validate_json(response.content.decode("utf-8"))
