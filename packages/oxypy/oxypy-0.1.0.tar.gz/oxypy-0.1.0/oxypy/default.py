from typing import Generic, Protocol, Type, TypeVar

T_co = TypeVar("T_co", covariant=True)


class Default(Protocol, Generic[T_co]):
    """
    A protocol that gives a type to ability to have a default value
    """
    @classmethod
    def default(cls: Type[T_co]) -> T_co:
        ...  # noqa
