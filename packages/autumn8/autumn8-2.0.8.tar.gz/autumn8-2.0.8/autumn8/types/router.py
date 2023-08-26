from typing import Optional

from autumn8.common.config import settings

from autumn8.lib.pydantic import PydanticModel


# "model_" is a protected namespace for Pydantic
# setting an alias to prevent warnings spam
# https://github.com/pydantic/pydantic/issues/6041#issuecomment-1582077748


class NewModelInfo(PydanticModel):
    name: str
    s3_file_url: Optional[str] = None  # initialized later
    s3_input_file_url: Optional[str] = None
    framework: settings.Framework
    quantization: settings.Quantization
    model_file_type: Optional[str] = None
    domain: Optional[str] = None
    task: Optional[str] = None
    inputs: Optional[str] = None
    group_id: Optional[str] = None
