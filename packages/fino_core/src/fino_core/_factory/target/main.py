from fino_core._model.target import TargetConfig, TargetPort, TargetType

from .edinet.main import Edinet


def create_target(target: TargetConfig) -> TargetPort:
    target_type = target.type
    if target_type == TargetType.EDINET:
        return Edinet(target)
