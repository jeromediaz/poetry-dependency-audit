"""
JS Dependency Audit
-------
A library to help perform a security audit check using a yarn (v1) lock file.

Not intended to be used as a standalone tool, but as part of a system
periodically checking for vulnerabilities with no need to download all
npm dependencies.
"""

from .lock_file_content import LockFileContent
from .security_audit_request import request_security_audit

__all__ = ["LockFileContent", "request_security_audit"]

__version__ = "0.9.0"
