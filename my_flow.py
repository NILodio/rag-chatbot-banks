from prefect import flow, get_run_logger


@flow
def my_flow():
    logger = get_run_logger()
    logger.info("Hello from ECS!!")


if __name__ == "__main__":
    my_flow()
