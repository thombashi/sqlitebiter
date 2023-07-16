from typing import Any, Dict, Pattern, Type

from typepy.type import AbstractType


ConvertConfig = Dict[str, Any]
TypeHintRules = Dict[Pattern[str], Type[AbstractType]]
