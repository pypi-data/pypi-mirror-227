"""
Contains functions for the HIL sub-group commands.
"""

import json
import traceback
import click
from embedops_cli.eo_types import (
    NoRepoIdException,
    NetworkException,
    LoginFailureException,
)
from embedops_cli.api.rest import ApiException
from embedops_cli.hil.hil_types import HILRepoId404Exception
from embedops_cli.sse.sse_api import SSEApi
from embedops_cli.sse import eo_sse
from embedops_cli.utilities import echo_error_and_fix
from embedops_cli import config
from embedops_cli.hil.hil_common import hil_run
from embedops_cli import embedops_authorization


@click.command()
@click.pass_context
def blink(ctx: click.Context):

    """Get a streaming response for the given event feed using urllib3."""

    try:

        repo_id = config.get_repo_id()

        if not repo_id:
            raise NoRepoIdException()

        sse_api = SSEApi()
        for event in sse_api.sse_blink_gateway(repo_id):
            if event.event == eo_sse.SSE_TEXT_EVENT:
                eo_sse.sse_print_command_text(event)
            elif event.event == eo_sse.SSE_RESULT_EVENT:
                result_event_obj = json.loads(event.data)
                ctx.exit(result_event_obj["exitCode"])
            else:
                pass  # Just ignore

        # If the command hasn't returned anything yet, exit here
        ctx.exit(2)

    except NoRepoIdException as exc:
        echo_error_and_fix(exc)
        ctx.exit(2)
    except NetworkException as exc:
        if exc.status_code == 401:
            echo_error_and_fix(LoginFailureException())
        elif exc.status_code == 404:
            echo_error_and_fix(HILRepoId404Exception())
        else:
            echo_error_and_fix(exc)

        ctx.exit(2)


@click.command()
@click.pass_context
def run(ctx: click.Context):

    """Run hil in local mode, using the current repository as a source."""

    ctx.exit(hil_run(local=True))


@click.command()
@click.pass_context
def fleet(ctx: click.Context):

    """Get a list of fleet devices for the current repo."""

    try:

        repo_id = config.get_repo_id()

        if not repo_id:
            raise NoRepoIdException()

        api_client = embedops_authorization.get_user_client()
        fleet_devices = api_client.get_repo_fleet_devices(repo_id)

        max_name_length = max(len(device.device_name) for device in fleet_devices)

        for device in fleet_devices:
            if device.is_online:
                status = click.style("Online", fg="green")
            else:
                status = click.style("Offline", fg="red")

            click.echo(f"{device.device_name.ljust(max_name_length)}\t{status}")

    except NoRepoIdException as exc:
        echo_error_and_fix(exc)
        ctx.exit(2)
    except ApiException as exc:
        if exc.status == 401:
            echo_error_and_fix(LoginFailureException())
        elif exc.status == 404:
            echo_error_and_fix(HILRepoId404Exception())
        else:
            echo_error_and_fix(NetworkException(exc.status))

        ctx.exit(2)
    except Exception as exc:  # pylint: disable=broad-except
        traceback.print_exc()
        ctx.exit(2)
