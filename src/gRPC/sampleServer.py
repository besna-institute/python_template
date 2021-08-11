# gRPCのサーバー実装ではThreadPoolを利用するので、そのためのモジュールをimportしておく
from concurrent.futures import ThreadPoolExecutor
import json

# 「grpc」パッケージと、grpc_tools.protocによって生成したパッケージをimportする

import grpc
from generated import solver_pb2,solver_pb2_grpc

# サービス定義から生成されたクラスを継承して、定義したリモートプロシージャに対応するメソッドを実装する
class SolverService(solver_pb2_grpc.SolverServiceServicer):
    def AnalyzeOnUnaryRPC(self, request, context):

        apiName = request.apiName
        name = request.name
        if apiName=="" or name=="":
            error = solver_pb2.SolverError(
                apiName = apiName,
                apiVersion = "1.0.0",
                errorId = "200",
                errorMessage = "error"
            )
            return solver_pb2.SolverResponse(error = error)

        else:
            reply = solver_pb2.SolverReply(
                apiName = apiName,
                apiVersion = "1.0.0",
                text = "Hello, {}".format(name)
            )
            return solver_pb2.SolverResponse(reply = reply)

    def AnalyzeOnServerStreamingRPC(self, request, context):

        apiName = request.apiName
        name = request.name

        if apiName=="" or name=="":
            error = solver_pb2.SolverError(
                apiName = apiName,
                apiVersion = "1.0.0",
                errorId = "200",
                errorMessage = "error"
            )
            return solver_pb2.SolverResponse(error = error)

        else:
            returnList = []
            textList = list(name)
            for word in textList:
                # 戻り値として返すSolverReplyオブジェクトを作成する
                reply = solver_pb2.SolverReply(
                    apiName = apiName,
                    apiVersion = "1.0.0",
                    text = word
                )
                # SolverResponseオブジェクトを返す
                yield solver_pb2.SolverResponse(reply = reply)


    def AnalyzeOnClientStreamingRPC(self, request_iterator, context):
        responseText = "Hello, "
        for request in request_iterator:
            apiName = request.apiName
            responseText += request.name
        reply = solver_pb2.SolverReply(
                    apiName = apiName,
                    apiVersion = "1.0.0",
                    text = responseText
                )
        return solver_pb2.SolverResponse(reply = reply)

    def AnalyzeOnBidirectionalStreamingRPC(self, request_iterator, context):
        for request in request_iterator:
            reply = solver_pb2.SolverReply(
                        apiName = request.apiName,
                        apiVersion = "1.0.0",
                        text = request.name
                    )
            yield solver_pb2.SolverResponse(reply = reply)

def main():
    # Serverオブジェクトを作成する
    server = grpc.server(ThreadPoolExecutor(2))
    # Serverオブジェクトに定義したServicerクラスを登録する
    solver_pb2_grpc.add_SolverServiceServicer_to_server(SolverService(), server)
    # 8000番ポートで待ち受けするよう指定する
    server.add_insecure_port('[::]:8000')
    # 待ち受けを開始する
    server.start()
    # 待ち受け終了後の後処理を実行する
    server.wait_for_termination()
if __name__ == '__main__':
    main()
