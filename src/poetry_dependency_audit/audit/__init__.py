from typing import List, Dict, Optional

from pydantic import BaseModel, Field


class Downloads(BaseModel):
    last_day: int
    last_month: int
    last_week: int


class Info(BaseModel):
    author: Optional[str]
    author_email: Optional[str] = None
    bugtrack_url: Optional[str] = None
    classifiers: List[str] = []
    description: str
    description_content_type: Optional[str] = None
    docs_url: Optional[str]
    download_url: Optional[str] = None
    downloads: Optional[Downloads] = None
    dynamic: Optional[List[str]] = None
    home_page: Optional[str] = None
    keywords: Optional[str] = None
    license: Optional[str] = None
    license_expression: Optional[str] = None
    license_files: Optional[List[str]] = None
    maintainer: Optional[str] = None
    maintainer_email: Optional[str] = None
    name: str
    package_url: str
    platform: Optional[str] = None
    project_url: str
    project_urls: Dict[str, str]
    provides_extra: Optional[List[str]] = None
    release_url: str
    requires_dist: Optional[List[str]] = None
    requires_python: Optional[str] = None
    summary: str
    version: str
    yanked: bool
    yanked_reason: Optional[str] = None


class Digests(BaseModel):
    blake2b_256: str
    md5: str
    sha256: str


class Url(BaseModel):
    comment_text: Optional[str] = None
    digests: Digests
    downloads: int
    filename: str
    has_sig: bool
    md5_digest: str
    packagetype: str
    python_version: str
    requires_python: str
    size: int
    upload_time: str
    upload_time_iso_8601: str
    url: str
    yanked: bool
    yanked_reason: Optional[str] = None


class Vulnerability(BaseModel):
    aliases: List[str]
    details: str
    fixed_in: List[str]
    id: str
    link: str
    source: str
    summary: Optional[str]
    withdrawn: None


class Package(BaseModel):
    info: Info
    last_serial: int
    urls: List[Url]
    vulnerabilities: List[Vulnerability]


class Audit(BaseModel):
    packages: Dict[str, Package] = Field(default_factory=dict)

    @property
    def dependencies(self) -> int:
        return len(self.packages)

    @property
    def vulnerable_packages(self) -> Dict[str, List[Vulnerability]]:
        return {
            name: package.vulnerabilities
            for name, package in self.packages.items()
            if package.vulnerabilities
        }

    @property
    def vulnerabilities_count(self) -> int:
        return sum(len(v) for v in self.vulnerable_packages.values())
