import pprint
import sys

# 「grpc」パッケージと、protocによって生成したパッケージをimportする
import grpc
import solver_pb2
import solver_pb2_grpc

class SolverClient:

    def __init__(self):
        pass

    def connect(self):
        # サーバーに接続する
        with grpc.insecure_channel("localhost:8000") as channel:

            # 送信先の「stub」を作成する
            stub = solver_pb2_grpc.SolverServiceStub(channel)
        return stub

    def analyzeOnUnaryRPC(self,request,context):
        stub = self.connect()
        response = stub.AnalyzeOnUnaryRPC(request,context)
        return response

    # def analyzeOnServerStreamingRPC(self,request,context):
    #     stub = self.connect()
    #     response = stub.AnalyzeOnServerStreamingRPC(request,context)
    #     return response

    # def analyzeOnClientStreamingRPC(self,request,context):
    #     stub = self.connect()
    #     response = stub.AnalyzeOnClientStreamingRPC(request,context)
    #     return response

    # def analyzeOnBidirectionalStreamingRPC(self,request,context):
    #     stub = self.connect()
    #     response = stub.AnalyzeOnBidirectionalStreamingRPC(request,context)
    #     return response

# def sample():

#     # リクエストを作成する
#     req = solver_pb2.SolverRequest(
#         apiName = "apiName",
#         name = "Taro",
#     )

#     # サーバーに接続する
#     with grpc.insecure_channel("localhost:8000") as channel:

#         # 送信先の「stub」を作成する
#         stub = solver_pb2_grpc.SolverServiceStub(channel)

#         # リクエストを送信する
#         response = stub.AnalyzeOnUnaryRPC(req,3)

#     # 取得したレスポンスの表示
#     pprint.pprint(response)

if __name__ == '__main__':
    solverClient = SolverClient()
    request = solver_pb2.SolverRequest(
        apiName = "apiName",
        name = "Taro",
    )
    response = solverClient.analyzeOnUnaryRPC(request,3)
    pprint.pprint(response)
