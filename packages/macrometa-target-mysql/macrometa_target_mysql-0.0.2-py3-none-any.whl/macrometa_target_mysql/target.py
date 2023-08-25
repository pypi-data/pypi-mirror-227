"""MySQL target class."""

from __future__ import annotations

import io
import typing as t
from pathlib import PurePath

import simplejson as json
from prometheus_client import start_http_server
from singer_sdk import typing as th
from singer_sdk.target_base import SQLTarget

from macrometa_target_mysql.constants import (
    export_errors,
    fabric_label,
    region_label,
    registry_package,
    tenant_label,
    workflow_label,
)
from macrometa_target_mysql.sinks import MySQLSink


class MacrometaTargetMySQL(SQLTarget):
    """Sample target for MySQL."""

    name = "macrometa-target-mysql"

    default_sink_class = MySQLSink

    def __init__(
        self,
        *,
        config: dict | PurePath | str | list[PurePath | str] | None = None,
        parse_env_config: bool = False,
        validate_config: bool = True,
    ) -> None:
        super().__init__(
            config=config,
            parse_env_config=parse_env_config,
            validate_config=validate_config,
        )
        self._MAX_RECORD_AGE_IN_MINUTES = self.config.get("batch_flush_interval")

        # Start the Prometheus HTTP server for exposing metrics
        self.logger.info("MySQL target is starting the metrics server.")
        start_http_server(8001, registry=registry_package)

    config_jsonschema = th.PropertiesList(
        th.Property(
            "username",
            th.StringType,
            secret=True,  # Flag config as protected.
            description="MySQL username",
        ),
        th.Property(
            "password",
            th.StringType,
            secret=True,  # Flag config as protected.
            description="MySQL password",
        ),
        th.Property(
            "host",
            th.StringType,
            description="MySQL host",
        ),
        th.Property(
            "port",
            th.StringType,
            description="MySQL port",
        ),
        th.Property(
            "database",
            th.StringType,
            description="MySQL database",
        ),
        th.Property(
            "target_table",
            th.StringType,
            description="MySQL table name",
        ),
        th.Property(
            "lower_case_table_names",
            th.BooleanType,
            description="Lower case table names",
            default=True,
        ),
        th.Property(
            "allow_column_alter",
            th.BooleanType,
            description="Allow column alter",
            default=False,
        ),
        th.Property(
            "replace_null",
            th.BooleanType,
            description="Replace null to blank",
            default=False,
        ),
        th.Property(
            "batch_flush_size", th.IntegerType, description="Batch Size", default=False
        ),
        th.Property(
            "batch_flush_interval",
            th.IntegerType,
            description="Batch Flush Interval (Minutes)",
            default=False,
        ),
        th.Property(
            "batch_flush_size", th.IntegerType, description="Batch Size", default=10000
        ),
        th.Property(
            "batch_flush_interval",
            th.IntegerType,
            description="Batch Flush Interval (Minutes)",
            default=5,
        ),
    ).to_dict()

    schema_properties = {}

    def _process_lines(self, file_input: t.IO[str]) -> t.Counter[str]:
        if self.config.get("replace_null", False):
            processed_input = io.StringIO()
            for line in file_input:
                data = self.deserialize_json(line.strip())

                if data.get("type", "") == "SCHEMA":
                    self.schema_properties = data["schema"]["properties"]
                elif data.get("type", "") == "RECORD":
                    for key, value in data.get("record", {}).items():
                        if value is not None:
                            continue

                        # https://json-schema.org/understanding-json-schema/reference/type.html
                        _type = self.schema_properties[key]["type"]
                        data_types = _type if isinstance(_type, list) else [_type]

                        if "null" in data_types:
                            continue
                        if "string" in data_types:
                            data["record"][key] = ""
                        elif "object" in data_types:
                            data["record"][key] = {}
                        elif "array" in data_types:
                            data["record"][key] = []
                        elif "boolean" in data_types:
                            data["record"][key] = False
                        else:
                            data["record"][key] = 0

                processed_input.write(json.dumps(data) + "\n")
            processed_input.seek(0)
            try:
                return super()._process_lines(processed_input)
            except Exception as e:
                # Increment export_errors metric
                export_errors.labels(
                    region_label, tenant_label, fabric_label, workflow_label
                ).inc()
                raise e
        else:
            try:
                return super()._process_lines(file_input)
            except Exception as e:
                # Increment export_errors metric
                export_errors.labels(
                    region_label, tenant_label, fabric_label, workflow_label
                ).inc()
                raise e


if __name__ == "__main__":
    MacrometaTargetMySQL.cli()
