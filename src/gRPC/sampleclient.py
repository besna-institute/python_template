import pprint
import sys
import grpc
from generated import solver_pb2_grpc,solver_pb2

class SolverClient:

    def __init__(self):
        pass

    def analyzeOnUnaryRPC(self,request,context):
        channel = grpc.insecure_channel("localhost:8000")
        stub = solver_pb2_grpc.SolverServiceStub(channel)
        response = stub.AnalyzeOnUnaryRPC(request,context)
        return response

    def analyzeOnServerStreamingRPC(self,request,context):
        channel = grpc.insecure_channel("localhost:8000")
        stub = solver_pb2_grpc.SolverServiceStub(channel)
        response = stub.AnalyzeOnServerStreamingRPC(request,context)
        return response

    def analyzeOnClientStreamingRPC(self,request,context):
        channel = grpc.insecure_channel("localhost:8000")
        stub = solver_pb2_grpc.SolverServiceStub(channel)
        response = stub.AnalyzeOnClientStreamingRPC(request,context)
        return response

    def analyzeOnBidirectionalStreamingRPC(self,request,context):
        channel = grpc.insecure_channel("localhost:8000")
        stub = solver_pb2_grpc.SolverServiceStub(channel)
        response = stub.AnalyzeOnBidirectionalStreamingRPC(request,context)
        return response

def main():
    solverClient = SolverClient()
    # 単一のリクエスト
    request_u = solver_pb2.SolverRequest(
                apiName = "apiName",
                name = "Taro"
            )

    # ストリーミングのリクエスト
    request_list = []
    requestName = "Taro"
    for i in list(requestName):
        request_s = solver_pb2.SolverRequest(
            apiName = "apiName",
            name = i
        )
        request_list.append(request_s)
    request_iterator = iter(request_list)

    # analyzeOnUnaryRPC
    print("-----------analyzeOnUnaryRPC-----------")
    response_UU = solverClient.analyzeOnUnaryRPC(request_u,3)
    pprint.pprint(response_UU)

    # analyzeOnServerStreamingRPC
    print("-----------analyzeOnServerStreamingRPC-----------")
    response_list_SU = solverClient.analyzeOnServerStreamingRPC(request_u,3)
    response_iterator_SU = iter(response_list_SU)
    for response in response_iterator_SU:
        pprint.pprint(response)

    # analyzeOnClientStreamingRPC
    print("-----------analyzeOnClientStreamingRPC-----------")
    response = solverClient.analyzeOnClientStreamingRPC(request_iterator,3)
    pprint.pprint(response)

    # analyzeOnBidirectionalStreamingRPC
    print("-----------analyzeOnBidirectionalStreamingRPC-----------")
    response_list_SS = solverClient.analyzeOnBidirectionalStreamingRPC(request_iterator,3)
    response_iterator_SS = iter(response_list_SS)
    for response in response_iterator_SS:
        pprint.pprint(response)

if __name__ == '__main__':
    main()
