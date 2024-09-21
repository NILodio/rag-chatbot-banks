import platform

from prefect import flow, get_run_logger, task


@task
def say_hi(user_name: str):
    logger = get_run_logger()
    logger.info("Hello from AWS Lambda, %s! 🦆", user_name)
    logger.info("Running some ML dataflow on %s ", platform.platform())


@flow
def ml(user: str = "Marvin"):
    say_hi(user)


def handler(event, context):
    ml()
