# from typing_extensions import Annotated, Union
# from typing import Any
# from bson import ObjectId
# from pydantic import PlainSerializer, AfterValidator, WithJsonSchema

# def validate_object_id(v: Any) -> ObjectId:
#     if isinstance(v, ObjectId):
#         return v
#     if ObjectId.is_valid(v):
#         return ObjectId(v)
#     raise ValueError("Invalid ObjectId")

# PyObjectId = Annotated[
#     Union[str, ObjectId],
#     AfterValidator(validate_object_id),
#     PlainSerializer(lambda x: str(x), return_type=str),
#     WithJsonSchema({"type": "string"}, mode="serialization"),
# ]



# from typing_extensions import Annotated
# from pydantic import BaseModel
# from pydantic.functional_validators import AfterValidator
# from bson import ObjectId as _ObjectId


# def check_object_id(value: str) -> str:
#     if not _ObjectId.is_valid(value):
#         raise ValueError('Invalid ObjectId')
#     return value


# PyObjectId = Annotated[str, AfterValidator(check_object_id)]

from typing import Annotated, Any

from bson import ObjectId
from pydantic_core import core_schema

from pydantic import BaseModel

from typing import Any
from typing import Annotated, Union
from bson import ObjectId
from pydantic import PlainSerializer, AfterValidator, WithJsonSchema

def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")

PyObjectId = Annotated[
    Union[str, ObjectId],
    AfterValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]