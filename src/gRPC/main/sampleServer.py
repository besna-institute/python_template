# gRPCのサーバー実装ではThreadPoolを利用するので、そのためのモジュールをimportしておく
from concurrent.futures import ThreadPoolExecutor
import json

# 「grpc」パッケージと、grpc_tools.protocによって生成したパッケージをimportする
import grpc
import solver_pb2
import solver_pb2_grpc

# ユーザー情報の読み込み
with open("../users.json") as fp:
    users = json.load(fp)

# サービス定義から生成されたクラスを継承して、定義したリモートプロシージャに対応するメソッドを実装する
class SolverService(solver_pb2_grpc.SolverServiceServicer):
    def AnalyzeOnUnaryRPC(self, request, context):
        # クライアントが送信した引数はrequest引数に格納され、
        # このオブジェクトに対しては一般的なPythonオブジェクトと
        # 同様の形でプロパティにアクセスできる
        user_id = request.id

        # ユーザー情報はユーザーIDを文字列に変換したものをキーとする辞書型データ
        # なので、適宜文字列型に変換して使用している
        if str(user_id) not in users:
            # 該当するユーザーが存在しない場合エラーを返す
            return solver_pb2.UserResponse(error=True,
                                         message="not found")
        user = users[str(user_id)]

        # 戻り値として返すUserオブジェクトを作成する
        result = solver_pb2.User()
        result.id = user["id"]
        result.nickname = user["nickname"]
        result.mail_address = user["mail_address"]
        result.user_type = solver_pb2.User.UserType.Value(user["user_type"])

        # UserResponseオブジェクトを返す
        return solver_pb2.UserResponse(error=False,
                                     user=result)

    def AnalyzeOnServerStreamingRPC(self, request, context):
        pass

    def AnalyzeOnClientStreamingRPC(self, request_iterator, context):
        pass

    def AnalyzeOnBidirectionalStreamingRPC(self, request_iterator, context):
        pass

    def get(self, request, context):
        """ユーザー情報を取得する
        """
        # クライアントが送信した引数はrequest引数に格納され、
        # このオブジェクトに対しては一般的なPythonオブジェクトと
        # 同様の形でプロパティにアクセスできる
        user_id = request.id

        # ユーザー情報はユーザーIDを文字列に変換したものをキーとする辞書型データ
        # なので、適宜文字列型に変換して使用している
        if str(user_id) not in users:
            # 該当するユーザーが存在しない場合エラーを返す
            return solver_pb2.UserResponse(error=True,
                                         message="not found")
        user = users[str(user_id)]

        # 戻り値として返すUserオブジェクトを作成する
        result = solver_pb2.User()
        result.id = user["id"]
        result.nickname = user["nickname"]
        result.mail_address = user["mail_address"]
        result.user_type = solver_pb2.User.UserType.Value(user["user_type"])

        # UserResponseオブジェクトを返す
        return solver_pb2.UserResponse(error=False,
                                     user=result)

def main():
    # Serverオブジェクトを作成する
    server = grpc.server(ThreadPoolExecutor(max_workers=2))

    # Serverオブジェクトに定義したServicerクラスを登録する
    solver_pb2_grpc.add_UserManagerServicer_to_server(UserManager(), server)

    # 1234番ポートで待ち受けするよう指定する
    server.add_insecure_port('[::]:1234')

    # 待ち受けを開始する
    server.start()

    # 待ち受け終了後の後処理を実行する
    server.wait_for_termination()

if __name__ == '__main__':
    main()
