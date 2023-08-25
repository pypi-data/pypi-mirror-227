import os
import sys
import webbrowser
from pathlib import Path
from typing import Optional

import typer

from .config import logger
from .utils import SubprocessError, find_zit_root, run_subprocess

dashboard_app = app = typer.Typer(name="dashboard", help="Dashboard commands")


def is_git_repo(path: Path):
    try:
        run_subprocess(["git", "-C", str(path), "rev-parse"], capture_stdout=False)
        return True
    except SubprocessError:
        return False


def clone_zlens_repo(path: Path):
    if is_git_repo(path):
        try:
            logger.info("Updating zlens repository...")
            run_subprocess(["git", "-C", str(path), "pull"])
        except SubprocessError as e:
            logger.info(f"Error updating zlens repository: {e}")
            sys.exit(1)
    else:
        try:
            logger.info("Cloning zlens repository...")
            run_subprocess(["git", "clone", "https://github.com/ZitySpace/zlens.git", str(path)])
        except SubprocessError as e:
            logger.info(f"Error cloning zlens repository: {e}")
            sys.exit(1)


def has_npm():
    try:
        run_subprocess(["npm", "-v"], capture_stdout=False)
        return True
    except FileNotFoundError:
        return False


def check_and_install_poetry():
    try:
        # Check if poetry is already installed
        run_subprocess(["poetry", "--version"], cwd=None, capture_stdout=False)
        logger.info("Poetry is already installed.")
    except FileNotFoundError:
        # Check the Python version
        major_version = sys.version_info.major
        minor_version = sys.version_info.minor

        yes = typer.prompt("Poetry not found. Do you want to install it?", type=bool)
        if not yes:
            logger.info(
                f'Please install poetry manually by "python{major_version}.{minor_version} -m pip install poetry" and'
                ' re-run "zit dashboard install".'
            )
            sys.exit(1)

        # Installation command for Poetry
        install_command = f"python{major_version}.{minor_version} -m pip install poetry"

        try:
            # Run the installation command
            run_subprocess(install_command, cwd=None, shell=True)
            logger.info("Poetry has been installed successfully.")
        except SubprocessError as e:
            logger.error("Error installing Poetry:")
            logger.error(e.stderr)
            sys.exit(1)


def check_and_install_node_nvm():
    reason = None

    try:
        node_version = run_subprocess(["node", "--version"])
        version_number = node_version.replace("v", "")
        major, minor, _ = map(int, version_number.split("."))

        if major != 18:
            reason = f"Node.js version must be 18. Detected version: {major}.{minor}."

    except FileNotFoundError:
        reason = "Node not found."

    except Exception as e:
        logger.error("Error checking Node.js:")
        logger.error(e.stderr)
        sys.exit(1)

    if reason:
        yes = typer.prompt(f"{reason}. Do you want to install Node.js 18 using nvm?", type=bool)

        if not yes:
            logger.info('Please install Node.js 18 manually and re-run "zit dashboard install".')
            sys.exit(1)

        # check and install nvm

        # Load command for nvm
        load_command = f'. {os.path.expanduser("~/.nvm/nvm.sh")} && nvm --version'

        try:
            run_subprocess(load_command, cwd=None, shell=True)
            logger.info("NVM is already installed.")
        except FileNotFoundError:
            yes = typer.prompt("NVM not found. Do you want to install it?", type=bool)
            if not yes:
                logger.info(
                    'Please install nvm manually by "curl -o-'
                    ' https://zityspace-public.s3.cn-north-1.amazonaws.com.cn/nvm_install.sh | bash" and re-run'
                    ' "zit dashboard install".'
                )
                sys.exit(1)

            # Installation command for nvm
            install_command = (
                'bash -c "set -o pipefail && curl -o-'
                ' https://zityspace-public.s3.cn-north-1.amazonaws.com.cn/nvm_install.sh | bash"'
            )

            try:
                # Run the installation command
                run_subprocess(install_command, cwd=None, shell=True)
                logger.info("NVM has been installed successfully.")

                # Run the load command
                run_subprocess(load_command, cwd=None, shell=True)
                logger.info("NVM has been loaded successfully.")
            except SubprocessError as e:
                logger.error("Error installing and loading NVM:")
                logger.error(e.stderr)
                sys.exit(1)

        # install node 18.4.0
        try:
            # download node-v18.4.0-linux-x64.tar.xz and put it in nvm's cache folder $NVM_DIR/.cache/bin
            run_subprocess(
                [
                    "curl",
                    "-L",
                    "-O",
                    "https://zityspace-public.s3.cn-north-1.amazonaws.com.cn/node-v18.4.0-linux-x64.tar.gz",
                ],
                cwd=os.path.expanduser("~/.nvm/.cache/bin"),
            )

            # then run the following command
            run_subprocess(["nvm", "install", "18.4.0"], capture_stdout=False)

            # then use node 18.4.0
            run_subprocess(["nvm", "use", "18.4.0"], capture_stdout=False)

        except SubprocessError as e:
            logger.error("Error installing Node.js:")
            logger.error(e.stderr)
            sys.exit(1)


def check_and_install_npm():
    try:
        run_subprocess(["npm", "-v"], capture_stdout=False)
        logger.info("NPM is already installed.")
    except FileNotFoundError:
        yes = typer.prompt("NPM not found. Do you want to install it?", type=bool)
        if not yes:
            logger.info(
                'Please install npm manually by "curl -qL https://www.npmjs.com/install.sh | sh" and re-run "zit'
                ' dashboard install".'
            )
            sys.exit(1)

        # Installation command for npm
        install_command = 'bash -c "set -o pipefail && curl -qL https://www.npmjs.com/install.sh | sh"'

        try:
            # Run the installation command
            run_subprocess(install_command, cwd=None, shell=True)
            logger.info("NPM has been installed successfully.")
        except SubprocessError as e:
            logger.error("Error installing NPM:")
            logger.error(e.stderr)
            sys.exit(1)


def check_and_install_pnpm():
    try:
        run_subprocess(["pnpm", "--version"], cwd=None, capture_stdout=False)
        logger.info("pnpm is already installed.")
    except FileNotFoundError:
        logger.info("pnpm not found. Installing pnpm...")
        install_command = "npm install -g pnpm"

        try:
            run_subprocess(install_command, cwd=None, shell=True)
            logger.info("pnpm has been installed successfully.")
        except SubprocessError as e:
            logger.error("Error installing pnpm:")
            logger.error(e.stderr)
            sys.exit(1)


def install_zlens_dependencies(path: Path):
    api_path = path / "api"
    ui_path = path / "ui"

    check_and_install_poetry()
    logger.info("Installing zlens API dependencies...")
    try:
        new_env = os.environ.copy()
        new_env.pop("VIRTUAL_ENV", None)

        run_subprocess(["poetry", "install"], cwd=str(api_path), env=new_env)
    except SubprocessError as e:
        logger.error("Error installing zlens API dependencies:")
        logger.error(e.stderr)
        sys.exit(1)

    check_and_install_node_nvm()
    check_and_install_npm()
    check_and_install_pnpm()
    logger.info("Installing zlens UI dependencies...")
    try:
        run_subprocess(["pnpm", "install"], cwd=str(ui_path))
    except SubprocessError as e:
        logger.error("Error installing zlens UI dependencies:")
        logger.error(e.stderr)
        sys.exit(1)


def create_database_tables(path: Path):
    api_path = path / "api"
    venv_path = api_path / ".venv"
    python_executable = (
        venv_path / "bin" / "python" if sys.platform != "win32" else venv_path / "Scripts" / "python.exe"
    )
    logger.info("Creating database tables...")
    try:
        run_subprocess(
            [str(python_executable), "-m", "alembic", "upgrade", "head"],
            cwd=str(api_path),
        )
    except SubprocessError as e:
        logger.error("Error creating database tables:")
        logger.error(e.stderr)
        sys.exit(1)


@app.command(name="install", help="Install dashboard")
def install():
    logger.info("Installing dashboard: ")

    zit_root = find_zit_root(Path.cwd())
    zlens_path = zit_root / ".zit" / "zlens"
    os.makedirs(zlens_path, exist_ok=True)

    # clone_zlens_repo(zlens_path)
    install_zlens_dependencies(zlens_path)
    create_database_tables(zlens_path)


def start_api_service(api_path: Path, port: int):
    venv_path = api_path / ".venv"
    python_executable = (
        venv_path / "bin" / "python" if sys.platform != "win32" else venv_path / "Scripts" / "python.exe"
    )

    env = os.environ.copy()
    env.pop("http_proxy", None)
    env.pop("https_proxy", None)
    env.pop("all_proxy", None)
    env.pop("HTTP_PROXY", None)
    env.pop("HTTPS_PROXY", None)
    env.pop("ALL_PROXY", None)

    command = [
        str(python_executable),
        "-m",
        "uvicorn",
        "app.api.serv:app",
        "--host",
        "0.0.0.0",
        "--port",
        str(port),
        "--reload",
    ]
    return run_subprocess(command, cwd=str(api_path), capture_stdout=True, env=env, wait=False)


def start_ui_service(ui_path: Path, port: int, api_port: Optional[int] = None):
    env = os.environ.copy()
    env["PORT"] = str(port)

    if api_port:
        env["NEXT_PUBLIC_API_PORT"] = str(api_port)

    command = ["pnpm", "run", "dev"]
    return run_subprocess(command, cwd=str(ui_path), capture_stdout=True, env=env, wait=False)


def start_celery_service(api_path: Path, port: int = 5672):
    venv_path = api_path / ".venv"
    python_executable = (
        venv_path / "bin" / "python" if sys.platform != "win32" else venv_path / "Scripts" / "python.exe"
    )

    # ensure that the python executable used in the subprocess is the one from zlens api venv
    # otherwise, it will be the one from the current activated venv
    env = os.environ.copy()
    env.pop("http_proxy", None)
    env.pop("https_proxy", None)
    env.pop("all_proxy", None)
    env.pop("HTTP_PROXY", None)
    env.pop("HTTPS_PROXY", None)
    env.pop("ALL_PROXY", None)
    env["PATH"] = str(venv_path / "bin") + os.pathsep + env["PATH"]

    command = [
        str(python_executable),
        "-m",
        "celery",
        "-A",
        "app.utils.taskqueue.worker.appFormula",
        "worker",
        "--loglevel=INFO",
        "--pool=processes",
        "--hostname=formulaWorker",
        "--queues",
        "formulaQ",
    ]
    return run_subprocess(command, cwd=str(api_path), capture_stdout=True, env=env, wait=False)


@app.command(name="show", help="Open dashboard")
def show(
    api_port: int = typer.Option(60000, help="Port number for the API service"),
    ui_port: int = typer.Option(60001, help="Port number for the UI service"),
):
    zit_root = find_zit_root(Path.cwd())
    zlens_path = zit_root / ".zit" / "zlens"
    api_path = zlens_path / "api"
    ui_path = zlens_path / "ui"

    try:
        api_process = start_api_service(api_path, api_port)
        ui_process = start_ui_service(ui_path, ui_port, api_port)
        celery_process = start_celery_service(api_path)

        webbrowser.open(f"http://localhost:{ui_port}")

        api_process.wait()
        ui_process.wait()
        celery_process.wait()
    except KeyboardInterrupt:
        print("Dashboard stopped.")
    finally:
        api_process.terminate()
        ui_process.terminate()
        celery_process.terminate()
        sys.exit(0)
