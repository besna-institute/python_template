import grpc_tools.protoc

grpc_tools.protoc.main(
    (
        "",
        "-I.",
        "--python_out=../generated",
        "--grpc_python_out=../generated",
        "solver.proto",
    )
)
