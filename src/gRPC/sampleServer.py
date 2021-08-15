# gRPCのサーバー実装ではThreadPoolを利用するので、そのためのモジュールをimportしておく
from concurrent.futures import ThreadPoolExecutor
import json

# 「grpc」パッケージと、grpc_tools.protocによって生成したパッケージをimportする

import grpc
from generated import solver_pb2,solver_pb2_grpc

# サービス定義から生成されたクラスを継承して、定義したリモートプロシージャに対応するメソッドを実装する
class SolverService(solver_pb2_grpc.SolverServiceServicer):
    def AnalyzeOnUnaryRPC(self, request, context):
        """override SolverServiceServicer.AnalyzeOnUnaryRPC"""
        if request.apiName=="" or request.name=="":
            error = solver_pb2.SolverError(
                apiName = "Solver",
                apiVersion = "1.0.0",
                errorId = "error:uncaught_syntax_error",
                errorMessage = "Unexpected token :"
            )
            return solver_pb2.SolverResponse(error = error)
        else:
            reply = solver_pb2.SolverReply(
                apiName = request.apiName,
                apiVersion = "1.0.0",
                text = "Hello, {}".format(request.name)
            )
            return solver_pb2.SolverResponse(reply = reply)

    def AnalyzeOnServerStreamingRPC(self, request, context):
        """override SolverServiceServicer.AnalyzeOnServerStreamingRPC"""
        if request.apiName=="" or request.name=="":
            error = solver_pb2.SolverError(
                apiName = "Solver",
                apiVersion = "1.0.0",
                errorId = "error:uncaught_syntax_error",
                errorMessage = "Unexpected token :"
            )
            return solver_pb2.SolverResponse(error = error)

        else:
            returnList = []
            textList = list(request.name)
            for word in textList:
                # 戻り値として返すSolverReplyオブジェクトを作成する
                reply = solver_pb2.SolverReply(
                    apiName = request.apiName,
                    apiVersion = "1.0.0",
                    text = word
                )
                # SolverResponseオブジェクトを返す
                yield solver_pb2.SolverResponse(reply = reply)


    def AnalyzeOnClientStreamingRPC(self, request_iterator, context):
        """override SolverServiceServicer.AnalyzeOnClientStreamingRPC"""
        responseText = "Hello, "
        for request in request_iterator:
            apiName = request.apiName
            responseText += request.name
            if request.apiName=="" or request.name=="":
                error = solver_pb2.SolverError(
                    apiName = "Solver",
                    apiVersion = "1.0.0",
                    errorId = "error:uncaught_syntax_error",
                    errorMessage = "Unexpected token :"
                )
                return solver_pb2.SolverResponse(error = error)

        reply = solver_pb2.SolverReply(
                    apiName = apiName,
                    apiVersion = "1.0.0",
                    text = responseText
                )
        return solver_pb2.SolverResponse(reply = reply)

    def AnalyzeOnBidirectionalStreamingRPC(self, request_iterator, context):
        """override SolverServiceServicer.AnalyzeOnBidirectionalStreamingRPC"""
        for request in request_iterator:
            if request.apiName=="" or request.name=="":
                error = solver_pb2.SolverError(
                    apiName = "Solver",
                    apiVersion = "1.0.0",
                    errorId = "error:uncaught_syntax_error",
                    errorMessage = "Unexpected token :"
                )
                yield solver_pb2.SolverResponse(error = error)
            else:
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


def main_http():
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

def main_ssl():
    # Serverオブジェクトを作成する
    server = grpc.server(ThreadPoolExecutor(2))
    # Serverオブジェクトに定義したServicerクラスを登録する
    solver_pb2_grpc.add_SolverServiceServicer_to_server(SolverService(), server)

    with open('./certs/server1.key', 'rb') as f:
        private_key = f.read()

    with open('./certs/server1.pem', 'rb') as f:
        certificate_chain = f.read()

    # create server credentials
    server_credentials = grpc.ssl_server_credentials(
        ((private_key, certificate_chain,),)
    )

    # 8000番ポートで待ち受けするよう指定する
    server.add_secure_port('[::]:8000', server_credentials)

    # 待ち受けを開始する
    server.start()
    # 待ち受け終了後の後処理を実行する
    server.wait_for_termination()

if __name__ == '__main__':
    # main()
    main_ssl()
    # gRPC -> grpc
    # クライアント名 -> solverClient
    # サーバ名 -> solverServer
