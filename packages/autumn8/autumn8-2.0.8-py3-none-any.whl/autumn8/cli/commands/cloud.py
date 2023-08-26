import asyncio
import base64
import json
import os
import posixpath
import uuid
from typing import Dict, List, Optional, Union

import click
import httpx
import questionary
from questionary import Choice

import autumn8.lib.api.cloud as cloud_api
from autumn8.cli import options
from autumn8.cli.cli_environment import CliEnvironment
from autumn8.cli.interactive import (
    coro_click_command,
    get_deployment,
    normalize_args,
    validate_and_ask_about_docker_image_name,
    validate_and_ask_about_schedule,
)
from autumn8.common.config.settings import CloudServiceProvider
from autumn8.lib import api, logging

logger = logging.getLogger(__name__)


@click.group(context_settings={"token_normalize_func": normalize_args})
def cloud_commands_group():
    pass


@cloud_commands_group.command()
@options.use_environment
@options.use_organization_id
@options.use_quiet_mode
@options.use_cloud_provider_picker(optional=True)
@click.option(
    "-m",
    "--model_id",
    help="Model ID to get the deployments for",
    prompt_required=False,
    default=None,
)
def list_deployments(
    organization_id: int,
    model_id: int,
    environment: CliEnvironment,
    cloud_provider: CloudServiceProvider,
    quiet,
):
    """List running deployments."""
    logger.info("Fetching the list of deployments...")
    deployments = cloud_api.get_running_deployments(
        organization_id,
        environment,
        model_id=model_id,
        service_provider=cloud_provider,
    )

    click.echo(json.dumps([depl.dict() for depl in deployments], indent=4))
    return


@cloud_commands_group.command()
@click.option(
    "-hw",
    "-t",
    "--machine_type",
    type=str,
    help="Server type to use for the deployment",
    # TODO: add a better interactive prompt listing all available servers
)
@options.use_environment
@options.use_organization_id
@options.use_quiet_mode
@click.option(
    "-m",
    "--model_id",
    prompt=True,
    type=int,
    help="Model ID to deploy",
    # TODO: add a better interactive prompt listing all available models
)
@click.option(
    "-s/-i",
    "should_schedule",
    "--schedule/--immediate",
    is_flag=True,
    default=False,
    help="Schedule the deployment to run in the future",
)
@click.option(
    "--schedule_on",
    type=str,
    help="Schedule the deployment on given date",
)
@click.option(
    "--deployment_id",
    type=str,
    help="Update an existing deployment, retaining its URL",
)
@options.use_cloud_provider_picker(
    # prompt disabled, as only A8F works atm
    optional=True,
    default_value=CloudServiceProvider.AUTUMN8,
)
def deploy(
    organization_id: int,
    model_id: int,
    should_schedule: bool,
    schedule_on: Optional[str],
    deployment_id: Optional[str],
    machine_type: Optional[str],
    environment: CliEnvironment,
    cloud_provider: CloudServiceProvider,
    quiet,
):
    """Deploy a model from AutoDL onto cloud."""

    if machine_type is None:
        machine_type = questionary.text(
            message="Machine type (ie. c5.2xlarge)"
        ).unsafe_ask()
    if machine_type is None:
        raise RuntimeError("Machine type was not picked, aborting...")

    schedule_on = validate_and_ask_about_schedule(should_schedule, schedule_on)

    logger.info(
        "Launching a new deployment with %s...",
        machine_type,
    )
    deployments = cloud_api.deploy(
        organization_id,
        environment,
        machine_type=machine_type,
        service_provider=cloud_provider,
        schedule_on=schedule_on,
        deployment_id=deployment_id,
        model_id=model_id,
    )

    click.echo(json.dumps(deployments, indent=4))


@cloud_commands_group.command()
@options.use_environment
@options.use_organization_id
@options.use_quiet_mode
@options.use_cloud_provider_picker(
    # prompt disabled, as only A8F works atm
    optional=True,
    default_value=CloudServiceProvider.AUTUMN8,
)
@click.option(
    "-d",
    "--deployment_id",
    prompt=True,
    help="ID of the deployment to terminate",
)
def terminate_deployment(
    organization_id: int,
    deployment_id: str,
    environment: CliEnvironment,
    cloud_provider: CloudServiceProvider,
    quiet,
):
    """Terminate a running deployment."""
    response = cloud_api.terminate_deployment(
        organization_id, environment, deployment_id, cloud_provider
    )
    click.echo(json.dumps(response, indent=4))


DEFAULT_DOCKER_CONTAINER_REGISTRY = "docker.io"


def build_docker_processing_query_string(
    organization_id: int, machine_type: str
) -> str:
    # TODO: drop obsolete, unused query string?
    container_id = str(uuid.uuid4())

    container_image_name = ""
    deployment_id = 0
    memory = 0

    return "+".join(
        [
            container_id,
            str(organization_id),
            container_image_name,
            str(memory),
            str(deployment_id),
            machine_type,
        ]
    )


@cloud_commands_group.command()
@coro_click_command
@options.use_organization_id
@click.option(
    "-hw",
    "-t",
    "machine_type_param",
    "--machine_type",
    type=str,
    help="Server type to use for the deployment",
    # TODO: add a better interactive prompt listing all available servers
)
@options.use_environment
@options.use_quiet_mode
@click.option(
    "-i",
    "--docker_image_name",
    default="",
    help="Docker image to be used for inference",
)
@click.option(
    "-p",
    "--docker_port",
    type=int,
    default=80,
    prompt=True,
    help="Docker container port that handles HTTP requests",
)
@click.option(
    "-r",
    "--docker_container_registry",
    type=str,
    default=DEFAULT_DOCKER_CONTAINER_REGISTRY,
    help="Docker registry to use the docker image from",
)
@click.option(
    "-h",
    "--container_http_request_path",
    type=str,
    default="",
    prompt=True,
    help="HTTP path on the Docker container to query against",
)
@click.option(
    "-H",
    "--custom_headers",
    type=str,
    multiple=True,
    default=[],
    help="Custom HTTP headers to pass",
)
@click.option(
    "-I",
    "--input",
    type=str,
    help="JSON / Raw Text HTTP Body input to pass within the HTTP request",
)
async def run_docker(
    organization_id: int,
    machine_type_param: Optional[str],
    environment: CliEnvironment,
    quiet: bool,
    docker_image_name: str = "",
    docker_port: Optional[int] = None,
    docker_container_registry: Optional[
        str
    ] = DEFAULT_DOCKER_CONTAINER_REGISTRY,
    container_http_request_path: str = "",
    custom_headers: List[str] = [],
    # disabled, cause these are not working properly right now on a8f
    # docker_environment: Optional[Dict[str, str]] = None,
    # docker_entrypoint: Optional[str] = None,
    input: Optional[str] = None,
):
    """
    Run an inference on a given Docker image by creating
    a temporary container and calling an HTTP request against it
    """
    machine_type: str = (
        questionary.text(message="Machine type (ie. c5.2xlarge)").unsafe_ask()
        if machine_type_param is None
        else machine_type_param
    )
    # AWS-only, quick hack
    machine_type = machine_type.replace(".", "-")

    (
        docker_container_registry_from_image_name,
        docker_image_name,
    ) = await validate_and_ask_about_docker_image_name(docker_image_name)

    if docker_container_registry_from_image_name:
        docker_container_registry = docker_container_registry_from_image_name

    if container_http_request_path.startswith("/"):
        container_http_request_path = container_http_request_path[1:]

    api_keys = api.user.fetch_org_api_keys(environment, organization_id)
    inference_api_key = api_keys[0]["api_key"]

    custom_headers_parsed = {}
    for entry in custom_headers:
        split = entry.split(":")
        if len(split) != 2:
            print(f'"{entry}" is not a valid header entry, skipping...')

        [header, value] = split
        custom_headers_parsed[header.strip()] = value.strip()

    async with httpx.AsyncClient(
        auth=(str(organization_id), inference_api_key)
    ) as httpClient:
        query: str = build_docker_processing_query_string(
            organization_id, machine_type
        )
        url = posixpath.join(
            environment.value.a8f_host,
            "docker-processing",
            query,
            container_http_request_path,
        )
        response: httpx.Response = await httpClient.post(
            url=url,
            json={
                "container_image_name": docker_image_name,
                "container_registry": docker_container_registry,
                "container_port": docker_port,
                "http_request_input": input,
                "http_request_path": container_http_request_path,
                "http_request_headers": custom_headers_parsed,
            },
            timeout=None,
        )

        logger.info("Container responded with:")
        click.echo(response.text)
        response.raise_for_status()


def decode_base64_model_output(model_output_base64: str):
    model_output_base64_bytes = bytes(model_output_base64, encoding="utf-8")

    model_output = base64.decodebytes(model_output_base64_bytes)
    return model_output


@cloud_commands_group.command()
@options.use_organization_id
@options.use_environment
@options.use_quiet_mode
@click.option(
    "--deployment_url", type=str, help="Public dns of your deployment"
)
@click.option("--model_id", type=int, help="Model id of model")
@click.option(
    "-I",
    "model_input",
    "--input",
    type=str,
    help="JSON / Raw Text HTTP Body input to pass within the HTTP request",
)
@click.option(
    "-f",
    "--input_file",
    type=str,
    help="filepath to file with JSON / Raw Text HTTP Body input to pass within the HTTP request",
)
@click.option(
    "-d",
    "--decode64",
    type=bool,
    is_flag=True,
    help="Decode model output from base64 string",
)
@click.option(
    "-O",
    "--output_file",
    type=str,
    help="Output file",
)
def run_inference(
    organization_id: int,
    environment: CliEnvironment,
    quiet: bool,
    deployment_url: Optional[str],
    model_id: Optional[int],
    model_input: Optional[str],
    input_file: Optional[str],
    decode64: bool,
    output_file: Optional[str],
):
    """
    Run an inference on a given deployment
    """

    api_keys = api.user.fetch_org_api_keys(environment, organization_id)
    inference_api_key = api_keys[0]["api_key"]

    if decode64 and output_file is None:
        output_file = questionary.text(
            "Please specify output file to decode base64 to",
            default="",
        ).unsafe_ask()

    if deployment_url is None:
        deployment_url = get_deployment(
            organization_id, environment, model_id=model_id
        )

    if input_file is not None:
        if os.path.exists(input_file):
            with open(input_file, "r", encoding="utf-8") as file:
                model_input = file.read()

    if deployment_url is None:
        click.echo(
            "You need to specify either deployment_url or choose existing deployment"
        )
        return

    final_input: str = (
        model_input
        if model_input is not None
        else questionary.text("JSON model input").unsafe_ask()
    )

    json_input = None
    try:
        json_input = json.loads(final_input)
    except json.JSONDecodeError:
        pass

    with httpx.Client(
        auth=(str(organization_id), inference_api_key)
    ) as httpClient:
        response: httpx.Response = httpClient.post(
            url=deployment_url,
            json=json_input if json_input is not None else None,
            content=final_input if json_input is None else None,
            timeout=None,
        )
        if decode64:
            data = json.loads(response.text)
            if "message" in data and "output" in data["message"]:
                model_output_base64 = data["message"]["output"]
                model_output = decode_base64_model_output(model_output_base64)
                if (
                    output_file is None
                ):  # check for this is above, additional check for pylint
                    return
                with open(output_file, "wb") as f:
                    f.write(model_output)
            else:
                logger.info("Deployment responded with:")
                click.echo(response.text)
                response.raise_for_status()
        else:
            logger.info("Deployment responded with:")
            click.echo(response.text)
            response.raise_for_status()
            if output_file is not None:
                with open(output_file, "w") as f:
                    f.write(response.text)
