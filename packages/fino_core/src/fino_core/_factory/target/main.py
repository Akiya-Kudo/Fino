from fino_core._model.target import Target, TargetRepository, TargetType

from .edinet.main import Edinet


def create_target(target: Target) -> TargetRepository:
    target_type = target.type
    if target_type == TargetType.EDINET:
        return Edinet(target)
