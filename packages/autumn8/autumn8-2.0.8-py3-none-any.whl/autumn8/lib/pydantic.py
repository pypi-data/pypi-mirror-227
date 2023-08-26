from pydantic import BaseModel, ConfigDict


class PydanticModel(BaseModel):
    # "model_" is a protected namespace for Pydantic
    # disabling namespace protection to prevent warnings spam
    # ((the aliases support doesn't let you get attributes by alias,))
    # ((i.e. item.model_id doesn't work))
    # https://github.com/pydantic/pydantic/issues/6041#issuecomment-1582077748
    model_config = ConfigDict(protected_namespaces=())
