from prefect import flow
from prefect.deployments import DeploymentImage


@flow(log_prints=True)
def my_flow(name: str = "world"):
    print(f"Hello {name}! I'm a flow running in a ECS task!")


if __name__ == "__main__":
    my_flow.deploy(
        name="my-deployment2",
        work_pool_name="rag-chatbot-queue-poll",
        image=DeploymentImage(
            name="prefect-flows:latest",
            platform="linux/amd64",
        ),
    )
