import pprint

import grpc
from generated import solver_pb2, solver_pb2_grpc


class SolverClient:
    def __init__(self):
        pass

    def analyzeOnUnaryRPC(self, request, context):
        channel = grpc.insecure_channel("localhost:8000")
        stub = solver_pb2_grpc.SolverServiceStub(channel)
        response = stub.AnalyzeOnUnaryRPC(request, context)
        return response

    def analyzeOnServerStreamingRPC(self, request, context):
        channel = grpc.insecure_channel("localhost:8000")
        stub = solver_pb2_grpc.SolverServiceStub(channel)
        response = stub.AnalyzeOnServerStreamingRPC(request, context)
        return response

    def analyzeOnClientStreamingRPC(self, request, context):
        channel = grpc.insecure_channel("localhost:8000")
        stub = solver_pb2_grpc.SolverServiceStub(channel)
        response = stub.AnalyzeOnClientStreamingRPC(request, context)
        return response

    def analyzeOnBidirectionalStreamingRPC(self, request, context):
        channel = grpc.insecure_channel("localhost:8000")
        stub = solver_pb2_grpc.SolverServiceStub(channel)
        response = stub.AnalyzeOnBidirectionalStreamingRPC(request, context)
        return response

    # def analyzeOnUnaryRPC_ssl(self,request,context):
    #     f = open('server1.key', 'r')
    #     trusted_certs = f.read()
    #     f.close()
    #     # create credentials
    #     credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    #     channel = grpc.secure_channel("localhost:8000", credentials)
    #     stub = solver_pb2_grpc.SolverServiceStub(channel)
    #     response = stub.AnalyzeOnUnaryRPC(request,context)
    #     return response

    # def analyzeOnServerStreamingRPC_ssl(self,request,context):
    #     with open('./certs/server1.pem', 'rb') as f:
    #         trusted_certs = f.read()
    #     # create credentials
    #     credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    #     channel = grpc.secure_channel("localhost:8000", credentials)
    #     stub = solver_pb2_grpc.SolverServiceStub(channel)
    #     response = stub.AnalyzeOnServerStreamingRPC(request,context)
    #     return response

    # def analyzeOnClientStreamingRPC_ssl(self,request,context):
    #     with open('./certs/server1.pem', 'rb') as f:
    #         trusted_certs = f.read()
    #     # create credentials
    #     credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    #     channel = grpc.secure_channel("localhost:8000", credentials)
    #     stub = solver_pb2_grpc.SolverServiceStub(channel)
    #     response = stub.AnalyzeOnClientStreamingRPC(request,context)
    #     return response

    # def analyzeOnBidirectionalStreamingRPC_ssl(self,request,context):
    #     with open('./certs/server1.pem', 'rb') as f:
    #         trusted_certs = f.read()
    #     # create credentials
    #     credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    #     channel = grpc.secure_channel("localhost:8000", credentials)
    #     stub = solver_pb2_grpc.SolverServiceStub(channel)
    #     response = stub.AnalyzeOnBidirectionalStreamingRPC(request,context)
    #     return response


def main():
    solverClient = SolverClient()
    # 単一のリクエスト
    request_u = solver_pb2.SolverRequest(apiName="apiName", name="Taro")

    # ストリーミングのリクエスト
    request_list = []
    requestName = "Taro"
    for i in list(requestName):
        request_s = solver_pb2.SolverRequest(apiName="apiName", name=i)
        request_list.append(request_s)
    request_iterator = iter(request_list)

    # analyzeOnUnaryRPC
    print("-----------analyzeOnUnaryRPC-----------")
    response_UU = solverClient.analyzeOnUnaryRPC(request_u, 3)
    pprint.pprint(response_UU)

    # analyzeOnServerStreamingRPC
    print("-----------analyzeOnServerStreamingRPC-----------")
    response_list_SU = solverClient.analyzeOnServerStreamingRPC(request_u, 3)
    response_iterator_SU = iter(response_list_SU)
    for response in response_iterator_SU:
        pprint.pprint(response)

    # analyzeOnClientStreamingRPC
    print("-----------analyzeOnClientStreamingRPC-----------")
    response = solverClient.analyzeOnClientStreamingRPC(request_iterator, 3)
    pprint.pprint(response)

    # analyzeOnBidirectionalStreamingRPC
    print("-----------analyzeOnBidirectionalStreamingRPC-----------")
    response_list_SS = solverClient.analyzeOnBidirectionalStreamingRPC(request_iterator, 3)
    response_iterator_SS = iter(response_list_SS)
    for response in response_iterator_SS:
        pprint.pprint(response)


if __name__ == "__main__":
    main()
