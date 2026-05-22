import subprocess
import threading

from logger import logger


def _stream_pipe(pipe, log_fn):
    for line in iter(pipe.readline, b''):
        decoded = line.decode("utf-8").strip()
        if decoded:
            log_fn(decoded)
    pipe.close()


def run_shell_command(command, check=True):
    logger.info(f"Running: {command}")

    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout_thread = threading.Thread(target=_stream_pipe, args=(process.stdout, logger.info))
    stderr_thread = threading.Thread(target=_stream_pipe, args=(process.stderr, logger.error))

    stdout_thread.start()
    stderr_thread.start()

    stdout_thread.join()
    stderr_thread.join()

    returncode = process.wait()

    if check and returncode != 0:
        logger.error(f"Command failed with exit code {returncode}: {command}")
        raise subprocess.CalledProcessError(returncode, command)
