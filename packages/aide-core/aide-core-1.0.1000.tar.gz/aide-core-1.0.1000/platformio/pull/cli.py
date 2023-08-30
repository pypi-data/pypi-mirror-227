# Copyright (c) 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mimetypes
import socket

import click
import subprocess
from platformio.compat import IS_WINDOWS
from platformio.home.run import run_server
from platformio.package.manager.core import get_core_package_dir


@click.command("hello", short_help="GUI to manage PlatformIO")
@click.option(
    "--docker-name",
    default="test",
    help=(
        "docker pull"
    ),
)
def cli(docker_name):
    try:
        result = subprocess.run(['docker', 'pull', docker_name], text=True)
        if result.stdout:
            click.echo(result.stdout)
        if result.stderr:
            click.echo(f"Docker Pull Error:\n{result.stderr}")
        else:
            click.echo(f"Docker Pull failed with return code: {result.returncode}")
    except Exception as e:
        click.echo(f"Error executing the command: {e}")
