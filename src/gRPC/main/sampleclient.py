import pprint
import sys

# 「grpc」パッケージと、protocによって生成したパッケージをimportする
import grpc
from src.gRPC.main import solver_pb2
from src.gRPC.main import solver_pb2_grpc
class SolverClient:

    def __init__(self):
        pass

    # def connect(self):
    #     # サーバーに接続する
    #     with grpc.insecure_channel("localhost:8000") as channel:

    #         # 送信先の「stub」を作成する
    #         stub = solver_pb2_grpc.SolverServiceStub(channel)
    #     return stub

    def analyzeOnUnaryRPC(self,request,context):
        with grpc.insecure_channel("localhost:8000") as channel:
            # 送信先の「stub」を作成する
            stub = solver_pb2_grpc.SolverServiceStub(channel)

            response = stub.AnalyzeOnUnaryRPC(request,context)
        return response

    def analyzeOnServerStreamingRPC(self,request,context):
        with grpc.insecure_channel("localhost:8000") as channel:
            # 送信先の「stub」を作成する
            stub = solver_pb2_grpc.SolverServiceStub(channel)
            response = stub.AnalyzeOnServerStreamingRPC(request,context)
        return response

    def analyzeOnClientStreamingRPC(self,request,context):
        with grpc.insecure_channel("localhost:8000") as channel:
            # 送信先の「stub」を作成する
            stub = solver_pb2_grpc.SolverServiceStub(channel)
            response = stub.AnalyzeOnClientStreamingRPC(request,context)
        return response

    def analyzeOnBidirectionalStreamingRPC(self,request,context):
        with grpc.insecure_channel("localhost:8000") as channel:
            # 送信先の「stub」を作成する
            stub = solver_pb2_grpc.SolverServiceStub(channel)
            response = stub.AnalyzeOnBidirectionalStreamingRPC(request,context)
        return response

if __name__ == '__main__':
    # main()
    request = solver_pb2.SolverRequest(
        apiName = "apiName",
        name = "Taro",
    )
    solverClient = SolverClient()
    response = solverClient.analyzeOnUnaryRPC(request,3)
    pprint.pprint(response)
