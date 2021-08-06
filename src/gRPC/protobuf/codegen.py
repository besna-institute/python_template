import grpc_tools.protoc

grpc_tools.protoc.main(
    (
        '',
        '-I.',
        '--python_out=.',
        '--grpc_python_out=.',
        './solver.proto',
    )
)
