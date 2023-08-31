#  Copyright 2021-present, the Recognai S.L. team.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import typer

from argilla.client.api import init
from argilla.client.login import ArgillaCredentials


def init_callback() -> None:
    if not ArgillaCredentials.exists():
        typer.echo("You are not logged in. Please run `argilla login` to login to an Argilla server.")
        raise typer.Exit(code=1)

    try:
        init()
    except Exception as e:
        typer.echo(
            "The Argilla Server you are logged in is not available or not responding. Please make sure it's running and try again."
        )
        raise typer.Exit(code=1) from e