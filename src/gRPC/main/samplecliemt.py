import pprint
import sys

# 「grpc」パッケージと、protocによって生成したパッケージをimportする
import grpc
import solver_pb2
import solver_pb2_grpc

def main():

    # リクエストを作成する
    req = solver_pb2.SolverRequest(
        apiName = "apiName",
        name = "Taro",
    )

    # サーバーに接続する
    with grpc.insecure_channel("localhost:8000") as channel:

        # 送信先の「stub」を作成する
        stub = solver_pb2_grpc.SolverServerStub(channel)

        # リクエストを送信する
        response = stub.get(req)

    # 取得したレスポンスの表示
    pprint.pprint(response)

if __name__ == '__main__':
    main()
