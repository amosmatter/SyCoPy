if __name__ == "__main__":
    from pathlib import Path
    import sys

    sys.path.append(Path(__file__).parents[1].as_posix())

from typing import Dict, Tuple, Hashable, List, Self
from core.system import SystemMorphism, GeneralSystem, ComposedMorphism, AtomicMorphism
from sympy import Basic, Expr, Equality


SpSystemObject_t = Tuple[Basic]


class SolvableExpressionMorphism(SystemMorphism[SpSystemObject_t, SpSystemObject_t]):
    pass

class AtomicSolvableExpressionMorphism(
    SolvableExpressionMorphism, AtomicMorphism[SpSystemObject_t, SpSystemObject_t]
):
    pass

class ComposedSolvableExpressionMorphism(
    SolvableExpressionMorphism,
    ComposedMorphism[SpSystemObject_t, SpSystemObject_t, SpSystemObject_t],
):
    pass

class SystemOfEquations(
    GeneralSystem[str, SolvableExpressionMorphism],
):
    pass

class ComposedSystemOfEquations(
    SystemOfEquations
):
    pass

class AtomicSystemOfEquations(
    SystemOfEquations,
):
    def __init__(self) -> None:
        super().__init__()
        self._morphisms = dict()
        self._equations = list()

    def resolve_morphism(self, obj: SolvableExpressionMorphism, *args, **kwargs): ...

    def make_unique_id_for(self, *args): ...

    def register_morphisms(self, *objs: SolvableExpressionMorphism):
        id_obj_pairs = [(self.make_unique_id_for(obj), obj) for obj in objs]
        self._morphisms.update(id_obj_pairs)

    def register_equations(self, *objs: Equality | Expr):
        self._equations.extend(objs)

    def compose_morphisms(
        self, first: SolvableExpressionMorphism, second: SolvableExpressionMorphism
    ) -> SolvableExpressionMorphism:
        return ComposedSolvableExpressionMorphism(first, second)

    @classmethod
    def from_equations(
        cls,
        equations: List[Equality | Expr],
        solvable_configs: Dict[SpSystemObject_t, SpSystemObject_t],
    ) -> Self:
        obj = cls()
        obj.register_equations(*equations)
        obj.register_morphisms(
            *(
                AtomicSolvableExpressionMorphism(src, tgt)
                for src, tgt in solvable_configs.items()
            )
        )
        return obj
