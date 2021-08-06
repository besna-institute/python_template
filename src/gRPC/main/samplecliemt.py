import pprint
import sys

# 「grpc」パッケージと、protocによって生成したパッケージをimportする
import grpc
import solver_pb2
import solver_pb2_grpc

# TODO formatterは後からかける
def main():

    # 引数をチェックする
    # 今回の引数って何？
    if (len(sys.argv) < 2):
        print("usage: {} <user_id>".format(sys.argv[0]))
        sys.exit(-1)
    try:
        user_id = int(sys.argv[1])
    except ValueError:
        print("error: invalid user_id `{}'".format(sys.argv[1]))
        print("usage: {} <user_id>".format(sys.argv[0]))
        sys.exit(-1)

    # リクエストを作成する
    req = user_pb2.UserRequest(id=user_id)

    # サーバーに接続する
    with grpcio.insecure_channel("localhost:1234") as channel:

        # 送信先の「stub」を作成する
        stub = user_pb2_grpc.UserManagerStub(channel)

        # リクエストを送信する
        response = stub.get(req)

    # 取得したレスポンスの表示
    pprint.pprint(response)

if __name__ == '__main__':
    main()
