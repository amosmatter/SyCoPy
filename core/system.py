from typing import Protocol, Tuple, Set, Hashable, Optional


class SystemMorphism[Source, Target](Protocol):
    @property
    def source(self) -> Source: ...

    @property
    def target(self) -> Target: ...


class AtomicMorphism[Source, Target](SystemMorphism[Source, Target]):
    def __init__(self, source: Source, target: Target) -> None:
        super().__init__()
        self._source = source
        self._target = target

    @property
    def source(self) -> Source:
        return self._source

    @property
    def target(self) -> Target:
        return self._target


class ComposedMorphism[Source, Middle, Target](SystemMorphism[Source, Target]):
    def __init__(
        self,
        first: SystemMorphism[Source, Middle],
        second: SystemMorphism[Middle, Target],
    ) -> None:
        super().__init__()
        self._first = first
        self._second = second

    @property
    def source(self) -> Source:
        return self._first.source

    @property
    def target(self) -> Target:
        return self._second.target


class GeneralSystem[IdentificationType: Hashable, MorphismType: SystemMorphism](
    Protocol
):
    def compose_morphisms(
        self, first: MorphismType, second: MorphismType
    ) -> MorphismType: ...

    def compose_system(
        self, other: GeneralSystem[IdentificationType, SystemMorphism]
    ) -> GeneralSystem[IdentificationType, SystemMorphism]: ...

    @property
    def morphisms(self) -> dict[IdentificationType, MorphismType]: ...

    @property
    def resolvable_morphisms(self) -> Set[IdentificationType]: ...

    @property
    def unresolvable_morphisms(self) -> Set[IdentificationType]: ...
