import itertools
from typing import TypedDict

from dsconfig_wrapper.dsconfig_types import AttributeProperties
from dsconfig_wrapper.dsconfig_types import ClassName
from dsconfig_wrapper.dsconfig_types import CommandName
from dsconfig_wrapper.dsconfig_types import Config
from dsconfig_wrapper.dsconfig_types import Identifier
from dsconfig_wrapper.dsconfig_types import IdentifierString
from dsconfig_wrapper.dsconfig_types import InstanceName
from dsconfig_wrapper.dsconfig_types import PropertyName
from dsconfig_wrapper.dsconfig_types import PropertyValue
from dsconfig_wrapper.dsconfig_types import Server

InnerDict = TypedDict(
    "InnerDict",
    {
        "properties": dict[str, list[str]],
        "attribute_properties": dict[str, dict[str, list[str]]],
    },
)

OutputDict = dict[
    str,
    dict[
        ClassName,
        dict[
            InstanceName,
            dict[
                ClassName,
                dict[IdentifierString, InnerDict],
            ],
        ],
    ],
]


def config_to_json(
    c: Config,
) -> OutputDict:
    def identifier_to_string(i: Identifier) -> str:
        return (
            f"tango://{i.host}/" if i.host is not None else ""
        ) + f"{i.domain}/{i.family}/{i.member}"

    by_class: dict[str, list[Server]] = {}
    for s in c.servers:
        if s.class_name not in by_class:
            by_class[s.class_name] = []
        by_class[s.class_name].append(s)

    def property_value_to_string(prop_value: PropertyValue) -> str:
        if isinstance(prop_value, str):
            return prop_value
        if isinstance(prop_value, (int, float)):
            return str(prop_value)
        return identifier_to_string(prop_value)

    def property_values_to_json(
        prop_value: PropertyValue | list[PropertyValue],
    ) -> list[str]:
        if isinstance(prop_value, list):
            return [property_value_to_string(s) for s in prop_value]
        return [property_value_to_string(prop_value)]

    def polled_commands_to_properties(
        p: dict[CommandName, int]
    ) -> dict[PropertyName, list[str]]:
        if not p:
            return {}
        return {
            "polled_cmd": list(
                itertools.chain.from_iterable(
                    (
                        (command_name, str(duration))
                        for command_name, duration in p.items()
                    )
                )
            )
        }

    def attribute_properties_to_json(ap: AttributeProperties) -> dict[str, list[str]]:
        return (
            (
                {"archive_period": [str(ap.archive_period_ms)]}
                if ap.archive_period_ms is not None
                else {}
            )
            | (
                {
                    "archive_abs_change": [
                        str(ap.archive_abs_change[0]),
                        str(ap.archive_abs_change[1]),
                    ]
                }
                if ap.archive_abs_change is not None
                else {}
            )
            | (
                {"rel_change": [str(ap.rel_change[0]), str(ap.rel_change[1])]}
                if ap.rel_change is not None
                else {}
            )
        )

    return {
        "servers": {
            class_name: {
                server.instance_name: {
                    server.class_name: {
                        identifier_to_string(d.identifier): {
                            "properties": {
                                prop_key: property_values_to_json(props)
                                for prop_key, props in d.properties.items()
                            }
                            | polled_commands_to_properties(d.polled_commands),
                            "attribute_properties": {
                                attribute_name: attribute_properties_to_json(ap)
                                for attribute_name, ap in d.attribute_properties.items()
                            },
                        }
                        for d in server.devices
                    }
                }
                for server in servers
            }
            for class_name, servers in by_class.items()
        }
    }
