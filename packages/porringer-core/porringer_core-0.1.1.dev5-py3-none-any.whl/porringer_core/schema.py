"""Schema for Porringer"""

from typing import NewType

from pydantic import BaseModel

PackageName = NewType("PackageName", str)


class Package(BaseModel):
    """Package definition"""

    name: PackageName
    version: str
