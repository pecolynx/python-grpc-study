poetry_requirements(
    name="poetry",
    module_mapping={
        "grpcio-health-checking": ["grpc_health"],
        "grpcio-testing": ["grpc_testing"],
    },
)

python_sources(
    name="src",
    sources=["grpc_server/**/*.py"],
)

pex_binary(
    name="grpc-server",
    entry_point="grpc_server/main.py",
    dependencies=[
        ":src",
    ],
)

docker_image(
    name="docker",
    repository="grpc-server",
)

python_tests(
    name="tests",
    sources=["tests/**/test_*"],
    dependencies=[
        ":src",
    ],
)