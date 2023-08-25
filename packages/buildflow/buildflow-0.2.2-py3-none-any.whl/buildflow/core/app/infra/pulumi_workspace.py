import dataclasses
import datetime
import enum
import logging
import re
from typing import Any, Dict, Iterable, Optional

from pulumi import automation as auto

from buildflow.config.pulumi_config import PulumiConfig
from buildflow.core.options.infra_options import PulumiOptions
from buildflow.core.processor.processor import ProcessorAPI


# TODO: This only works when its the only error in the logs. Need to update the regex
# Pulumi will log this error that we want to catch:
# A new version of Pulumi is available. To upgrade from version '3.68.0' to '3.73.0',
# run $ curl -sSL https://get.pulumi.com | sh
# or visit https://pulumi.com/docs/reference/install/ for manual instructions and
# release notes.
def _remove_pulumi_upgrade_error_from_logs(stderr: str):
    # The regular expression .* does not match newline characters by default.
    # flags=re.DOTALL makes . the re expression match any character including a newline
    pattern = re.compile(
        r"warning: A new version of Pulumi is available.*release notes\.",
        flags=re.DOTALL,
    )
    return pattern.sub("", stderr).strip()


# Each log replacement rule should have its own function
def _clean_stderr(stderr: str):
    stderr = _remove_pulumi_upgrade_error_from_logs(stderr)
    return stderr


# logs look like:
#   +  gcp:pubsub:Subscription buildflow_subscription_43c1269c create
#   +  gcp:bigquery:Table daring-runway-374503.buildflow.table_9312c458 create
#  @ previewing update....
#   +  pulumi:pulumi:Stack buildflow-app-buildflow-stack create
#
#  Outputs:
#      gcp.bigquery.dataset_id     : "daring-runway-374503.buildflow"
#      gcp.biquery.table_id        : "daring-runway-374503.buildflow.table_9312c458"
#      gcp.pubsub.subscription.name: "buildflow_subscription_43c1269c"
#
#  Resources:
#      + 4 to create
def extract_outputs_from_stdout(stdout: str):
    pattern = re.compile(r"Outputs:\n((?:\s{4}.+\n)+)")
    match = pattern.search(stdout)
    if match:
        outputs = match.group(1)
        outputs = outputs.strip()
        outputs = outputs.split("\n")
        outputs = [output.strip() for output in outputs]
        outputs = [output.split(":") for output in outputs]
        outputs = {key.strip(): value.strip() for key, value in outputs}
        return outputs
    else:
        return {}


@dataclasses.dataclass
class WrappedRefreshResult:
    refresh_result: auto.RefreshResult

    def log_summary(self):
        logging.debug(self.refresh_result.stdout)
        if self.refresh_result.stderr:
            logging.error(self.refresh_result.stderr)
        logging.debug(self.refresh_result.summary)


@dataclasses.dataclass
class WrappedPreviewResult:
    preview_result: auto.PreviewResult

    def __post_init__(self):
        self.preview_result.stderr = _clean_stderr(self.preview_result.stderr)

    def log_summary(self):
        logging.debug(self.preview_result.stdout)
        if self.preview_result.stderr:
            logging.error(self.preview_result.stderr)
        logging.debug(self.preview_result.change_summary)

    def print_change_summary(self):
        # num_to_create = self.preview_result.change_summary.get("create", 0)
        # resource_outputs = extract_outputs_from_stdout(self.preview_result.stdout)
        # resource_outputs_str = "\n".join(
        #     [
        #         f"    {output_key}:{output_value}"
        #         for output_key, output_value in resource_outputs.items()
        #     ]
        # )
        # lines = [
        #     "-" * 80,
        #     f"Number of Resources to create: {num_to_create}",
        #     "",
        #     "Resource Outputs:",
        #     resource_outputs_str,
        #     "-" * 80,
        # ]
        # print("\n".join(lines))
        print(self.preview_result.stdout)


@dataclasses.dataclass
class WrappedUpResult:
    up_result: auto.UpResult

    def log_summary(self):
        logging.warning(self.up_result.stdout)
        if self.up_result.stderr:
            logging.error(self.up_result.stderr)
        logging.warning(self.up_result.summary)
        logging.warning(self.up_result.outputs)


@dataclasses.dataclass
class WrappedDestroyResult:
    destroy_result: auto.DestroyResult

    def log_summary(self):
        logging.warning(self.destroy_result.stdout)
        if self.destroy_result.stderr:
            logging.error(self.destroy_result.stderr)
        logging.warning(self.destroy_result.summary)


@dataclasses.dataclass
class WrappedOutputMap:
    output_map: auto.OutputMap

    def log_summary(self):
        logging.warning(self.output_map)

    def print_summary(self):
        print(self.output_map)


class _PulumiResourceType(enum.Enum):
    BIGQUERY_DATASET = "BigQuery.DataSet"
    BIGQUERY_TABLE = "BigQuery.Table"
    UNKNOWN = "Unknown"


@dataclasses.dataclass
class ResourceState:
    resource_urn: str
    resource_type: str
    resource_id: Optional[str]
    resource_outputs: Dict[str, Any]
    cloud_console_url: Optional[str] = None
    parent: Optional[str] = None
    dependencies: Iterable[str] = ()

    def as_json_dict(self) -> Dict[str, Any]:
        return {
            "resource_urn": self.resource_urn,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "resource_outputs": self.resource_outputs,
            "cloud_console_url": self.cloud_console_url,
            "parent": self.parent,
            "dependencies": self.dependencies,
        }


@dataclasses.dataclass
class WrappedStackState:
    project_name: str
    stack_name: str
    _deployment: Optional[auto.Deployment]
    _update_summary: Optional[auto.UpdateSummary]
    _output_map: auto.OutputMap

    @property
    def last_updated(self):
        if self._update_summary is not None:
            return self._update_summary.end_time
        else:
            return datetime.datetime.now()

    def resources(self) -> Iterable[ResourceState]:
        if self._deployment is None:
            return []
        else:
            return [
                ResourceState(
                    resource_urn=resource["urn"],
                    resource_type=resource["type"],
                    resource_id=resource.get("id"),
                    resource_outputs=resource.get("outputs", {}),
                    cloud_console_url=resource.get("outputs", {}).get(
                        "buildflow.cloud_console.url"
                    ),
                    parent=resource.get("parent"),
                    dependencies=resource.get("dependencies", []),
                )
                for resource in self._deployment.deployment.get("resources", [])
            ]

    # NOTE: We only wrap this so we can have an interface between the Pulumi type
    # (in case they change their API)
    def outputs(self) -> Dict[str, Any]:
        return self._output_map

    def print_summary(self):
        if self._update_summary is None:
            print("No stack state found")
        else:
            output_map_lines = [
                f"    {output_key}: {output_value}"
                for output_key, output_value in self._output_map.items()
            ]
            all_lines = [
                "-" * 80,
                f"Project Name: {self.project_name}",
                f"Stack Name: {self.stack_name}",
                f"Last Updated: {self.last_updated}",
                "",
                "Resource Outputs:",
                "\n".join(output_map_lines),
                "-" * 80,
            ]
            print("\n".join(all_lines))

    def as_json_dict(self) -> Dict[str, Any]:
        json_resource_outputs = []
        for key, value in self._output_map.items():
            try:
                resource_type = _PulumiResourceType(key)
            except ValueError:
                resource_type = _PulumiResourceType.UNKNOWN
            json_resource_outputs.append({"type": resource_type.value, "value": value})
        return {
            "project_name": self.project_name,
            "stack_name": self.stack_name,
            "last_updated": self.last_updated.timestamp(),
            "resource_outputs": json_resource_outputs,
        }


class PulumiWorkspace:
    def __init__(
        self, pulumi_options: PulumiOptions, pulumi_config: PulumiConfig
    ) -> None:
        # configuration
        self.options = pulumi_options
        self.config = pulumi_config
        # initial state
        self._pulumi_program_cache = {}

    def get_stack_state(self) -> WrappedStackState:
        try:
            stack = auto.select_stack(
                stack_name=self.config.stack_name,
                project_name=self.config.project_name,
                program=None,
                work_dir=self.config.pulumi_home,
                opts=self.config.workspace_options(),
            )
            return WrappedStackState(
                project_name=self.config.project_name,
                stack_name=self.config.stack_name,
                _deployment=stack.export_stack(),
                _update_summary=stack.info(),
                _output_map=stack.outputs(),
            )
        except auto.StackNotFoundError:
            return WrappedStackState(
                project_name=self.config.project_name,
                stack_name=self.config.stack_name,
                _deployment=None,
                _update_summary=None,
                _output_map={},
            )

    async def refresh(
        self, *, processors: Iterable[ProcessorAPI]
    ) -> WrappedRefreshResult:
        logging.debug(f"Pulumi Refresh: {self.config.workspace_id}")
        stack = self._create_or_select_stack(processors)
        return WrappedRefreshResult(refresh_result=stack.refresh())

    async def preview(
        self, *, processors: Iterable[ProcessorAPI]
    ) -> WrappedPreviewResult:
        logging.debug(f"Pulumi Preview: {self.config.workspace_id}")
        stack = self._create_or_select_stack(processors)
        return WrappedPreviewResult(preview_result=stack.preview())

    async def up(self, *, processors: Iterable[ProcessorAPI]) -> WrappedUpResult:
        logging.debug(f"Pulumi Up: {self.config.workspace_id}")
        stack = self._create_or_select_stack(processors)
        return WrappedUpResult(up_result=stack.up())

    async def outputs(self, *, processors: Iterable[ProcessorAPI]) -> WrappedOutputMap:
        logging.debug(f"Pulumi Outputs: {self.config.workspace_id}")
        stack = self._create_or_select_stack(processors)
        return WrappedOutputMap(output_map=stack.outputs())

    async def destroy(
        self, *, processors: Iterable[ProcessorAPI]
    ) -> WrappedDestroyResult:
        logging.debug(f"Pulumi Destroy: {self.config.workspace_id}")  # noqa: E501
        stack = self._create_or_select_stack(processors)
        return WrappedDestroyResult(destroy_result=stack.destroy())

    def _create_pulumi_program(self, processors: Iterable[ProcessorAPI]):
        def pulumi_program():
            for processor in processors:
                # NOTE: All we need to do is run this method because any Pulumi
                # resources will be instantiated when called. Any Pulumi resources
                # created in the scope of the pulumi_program function will be included
                # in the Pulumi program / stack.
                processor.pulumi_program()

        return pulumi_program

    def _create_or_select_stack(self, processors: Iterable[ProcessorAPI]):
        if self.config.workspace_id not in self._pulumi_program_cache:
            pulumi_program = self._create_pulumi_program(processors)
            self._pulumi_program_cache[self.config.workspace_id] = pulumi_program
        else:
            pulumi_program = self._pulumi_program_cache[self.config.workspace_id]

        stack = auto.create_or_select_stack(
            stack_name=self.config.stack_name,
            project_name=self.config.project_name,
            program=pulumi_program,
            opts=self.config.workspace_options(),
        )

        if self.options.refresh_state:
            stack.refresh()

        return stack
