from prefect import flow, task


@task
def say_hello():
    print("hi")


@flow(log_prints=True)
def my_flow():
    say_hello()


if __name__ == "__main__":
    my_flow()
