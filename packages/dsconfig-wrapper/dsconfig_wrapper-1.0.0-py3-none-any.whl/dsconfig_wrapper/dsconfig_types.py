from dataclasses import dataclass
from dataclasses import field
from typing import TypeAlias


@dataclass(frozen=True)
class Identifier:
    domain: str
    family: str
    member: str
    host: None | str = None


PropertyValue: TypeAlias = str | Identifier | float | int

ClassName = str
InstanceName = str
IdentifierString = str
AttributeName = str
PropertyName = str
CommandName = str


@dataclass(frozen=True)
class AttributeProperties:
    archive_period_ms: None | int = None
    archive_abs_change: None | tuple[float, float] = None
    rel_change: None | tuple[float, float] = None


@dataclass(frozen=True)
class Device:
    identifier: Identifier
    properties: dict[PropertyName, PropertyValue | list[PropertyValue]] = field(
        default_factory=lambda: {}
    )
    polled_commands: dict[CommandName, int] = field(default_factory=lambda: {})
    attribute_properties: dict[AttributeName, AttributeProperties] = field(
        default_factory=lambda: {}
    )


@dataclass(frozen=True)
class Class:
    name: str
    devices: list[Device]


@dataclass(frozen=True)
class Instance:
    server_name: str
    instance_name: str
    classes: list[Class]


@dataclass(frozen=True)
class Server:
    instance_name: str
    class_name: str
    devices: list[Device]


@dataclass(frozen=True)
class Config:
    servers: list[Server]
