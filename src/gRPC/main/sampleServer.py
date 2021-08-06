# gRPCのサーバー実装ではThreadPoolを利用するので、そのためのモジュールをimportしておく
from concurrent.futures import ThreadPoolExecutor
import json

# 「grpc」パッケージと、grpc_tools.protocによって生成したパッケージをimportする
import grpc
import solver_pb2
import solver_pb2_grpc

# サービス定義から生成されたクラスを継承して、定義したリモートプロシージャに対応するメソッドを実装する
class SolverService(solver_pb2_grpc.SolverServiceServicer):
    def AnalyzeOnUnaryRPC(self, request, context):
        # requestで受け取るのはこの形式
        # message SolverRequest {
        #     string apiName = 1;
        #     string name = 2;
        # }

        # エラー対応をするんだったらここでやる。
        # apiNameとnameがないときはerror=Trueにする
        apiName = request.apiName
        name = request.name
        text = "hello {}".format(name)

        # 正しいものじゃなかったら
        if apiName==None or name==None:
            return solver_pb2.SolverError(
                    apiName = apiName,
                    apiVersion = "apiVersion",
                    errorId = 200,
                    errorMessage = "error"
            )

        # 戻り値として返すSolverReplyオブジェクトを作成する
        reply = solver_pb2.SolverReply()
        reply.apiName = apiName
        reply.name = name
        reply.text = text

        # SolverResponseオブジェクトを返す
        return solver_pb2.SolverResponse(reply)

    def AnalyzeOnServerStreamingRPC(self, request, context):
        apiName = request.apiName
        name = request.name
        text = "hello {}".format(name)

        # 戻り値として返すSolverReplyオブジェクトを作成する
        reply = solver_pb2.SolverReply()
        reply.apiName = apiName
        reply.name = name
        reply.text = text

        # UserResponseオブジェクトを返す
        return solver_pb2.SolverResponse(reply=reply,error=False)

    def AnalyzeOnClientStreamingRPC(self, request_iterator, context):
        for request in request_iterator:
            apiName = request.apiName
            name = request.name
            text = "hello {}".format(name)

            # 戻り値として返すSolverReplyオブジェクトを作成する
            reply = solver_pb2.SolverReply()
            reply.apiName = apiName
            reply.name = name
            reply.text = text

        # UserResponseオブジェクトを返す
        return solver_pb2.SolverResponse(reply=reply,error=False)

    def AnalyzeOnBidirectionalStreamingRPC(self, request_iterator, context):
        for request in request_iterator:
            apiName = request.apiName
            name = request.name
            text = "hello {}".format(name)

            # 戻り値として返すSolverReplyオブジェクトを作成する
            reply = solver_pb2.SolverReply()
            reply.apiName = apiName
            reply.name = name
            reply.text = text

        # UserResponseオブジェクトを返す
        return solver_pb2.SolverResponse(reply=reply,error=False)

def main():
    # Serverオブジェクトを作成する
    server = grpc.server(ThreadPoolExecutor(max_workers=2))

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
