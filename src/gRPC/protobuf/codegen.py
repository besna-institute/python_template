import grpc_tools.protoc

grpc_tools.protoc.main(
    (
        "",
        "-I./src/gRPC/protobuf/",
        "--python_out=src/gRPC/generated",
        "--grpc_python_out=src/gRPC/generated",
        "./src/gRPC/protobuf/solver.proto"
    )
)
