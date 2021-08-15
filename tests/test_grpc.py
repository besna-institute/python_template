# import json
# import unittest
# from concurrent.futures import ThreadPoolExecutor
# from pathlib import Path

# import grpc

# from src.gRPC.solver_client import SolverClient
# from src.gRPC.solver_server import SolverService
# from src.gRPC.generated import solver_pb2, solver_pb2_grpc


# class MainTest(unittest.TestCase):
#     def init(self):
#         self.client = SolverClient()
#         # テストデータのjsonまでのパス
#         path_to_dir = Path(__file__).parent
#         path_to_data = path_to_dir / "data"

#         # 入力データ(input.json)
#         with open(path_to_data / "input1.json") as fp:
#             json_input1 = json.load(fp)
#         self.inputApiName = json_input1["apiName"]
#         self.inputName = json_input1["name"]

#         # 想定される結果
#         with open(path_to_data / "output1.json") as fp:
#             json_output1 = json.load(fp)

#         self.outputApiName = json_output1["apiName"]
#         self.outputApiVersion = json_output1["apiVersion"]
#         self.outputText = json_output1["text"]

#         # 想定されるエラーメッセージ
#         with open(path_to_data / "error1.json") as fp:
#             json_output1 = json.load(fp)

#         self.errorApiName = json_output1["apiName"]
#         self.errorApiVersion = json_output1["apiVersion"]
#         self.errorErrorId = json_output1["errorId"]
#         self.errorErrorMessage = json_output1["errorMessage"]

#         self.server = grpc.server(ThreadPoolExecutor(2))
#         # Serverオブジェクトに定義したServicerクラスを登録する
#         solver_pb2_grpc.add_SolverServiceServicer_to_server(SolverService(), self.server)
#         # 8000番ポートで待ち受けするよう指定する
#         self.server.add_insecure_port("[::]:8000")

#     # AnalyzeOnUnaryRPCのテスト
#     # @ unittest.skip("モジュール修正中のためスキップ")
#     def test_AnalyzeOnUnaryRPC(self):
#         self.init()
#         self.server.start()
#         request = solver_pb2.SolverRequest(apiName=self.inputApiName, name=self.inputName)

#         # レスポンスを取得
#         response = self.client.analyzeOnUnaryRPC(request, 3)

#         solver_reply = solver_pb2.SolverReply(
#             apiName=self.outputApiName, apiVersion=self.outputApiVersion, text=self.outputText
#         )
#         solver_response = solver_pb2.SolverResponse(reply=solver_reply)
#         self.assertEqual(response, solver_response)

#         # graceはサーバを止めるまで何秒 or msec待つか
#         self.server.stop(grace=0)

#         # 待ち受け終了後の後処理を実行する
#         self.server.wait_for_termination()

#     # AnalyzeOnServerStreamingRPCのテスト
#     # @ unittest.skip("モジュール修正中のためスキップ")
#     def test_AnalyzeOnServerStreamingRPC(self):
#         self.init()
#         self.server.start()
#         request = solver_pb2.SolverRequest(apiName=self.inputApiName, name=self.inputName)

#         # レスポンスを取得
#         response_iterator = iter(self.client.analyzeOnServerStreamingRPC(request, 3))

#         solver_reply = []
#         for response, word in zip(response_iterator, list(self.inputName)):
#             solver_reply = solver_pb2.SolverReply(
#                 apiName=self.outputApiName,
#                 apiVersion=self.outputApiVersion,
#                 text=word,
#             )
#             solver_response = solver_pb2.SolverResponse(reply=solver_reply)
#             self.assertEqual(response, solver_response)
#         # 待ち受け終了後の後処理を実行する
#         self.server.stop(0)
#         self.server.wait_for_termination()

#     # AnalyzeOnClientStreamingRPCのテスト
#     # @ unittest.skip("モジュール修正中のためスキップ")
#     def test_AnalyzeOnClientStreamingRPC(self):
#         self.init()
#         self.server.start()
#         request_list = []
#         for i in list(self.inputName):
#             request_s = solver_pb2.SolverRequest(apiName=self.inputApiName, name=i)
#             request_list.append(request_s)
#         request_iterator = iter(request_list)

#         # レスポンスを取得
#         response = self.client.analyzeOnClientStreamingRPC(request_iterator, 3)

#         solver_reply = solver_pb2.SolverReply(
#             apiName=self.outputApiName, apiVersion=self.outputApiVersion, text=self.outputText
#         )
#         solver_response = solver_pb2.SolverResponse(reply=solver_reply)

#         self.assertEqual(response, solver_response)
#         # 待ち受け終了後の後処理を実行する
#         self.server.stop(0)
#         self.server.wait_for_termination()

#     # AnalyzeOnBidirectionalStreamingRPCのテスト
#     # @ unittest.skip("モジュール修正中のためスキップ")
#     def test_AnalyzeOnBidirectionalStreamingRPC(self):
#         self.init()
#         self.server.start()
#         request_list = []
#         for i in list(self.inputName):
#             request_s = solver_pb2.SolverRequest(apiName=self.inputApiName, name=i)
#             request_list.append(request_s)
#         request_iterator = iter(request_list)

#         # レスポンスを取得
#         response_iterator = iter(self.client.analyzeOnBidirectionalStreamingRPC(request_iterator, 3))

#         solver_reply = []
#         for response, word in zip(response_iterator, list(self.inputName)):
#             solver_reply = solver_pb2.SolverReply(
#                 apiName=self.outputApiName, apiVersion=self.outputApiVersion, text=word
#             )
#             solver_response = solver_pb2.SolverResponse(reply=solver_reply)
#             self.assertEqual(response, solver_response)

#         self.server.stop(0)
#         # 待ち受け終了後の後処理を実行する
#         self.server.wait_for_termination()

#     # AnalyzeOnUnaryRPCが失敗するテスト
#     # @ unittest.skip("モジュール修正中のためスキップ")
#     def test_AnalyzeOnUnaryRPC_Error(self):
#         self.init()
#         self.server.start()

#         request1 = solver_pb2.SolverRequest(
#             # inputApiNameフィールドを持たない/* apiName = self.inputApiName,*/
#             name=self.inputName
#         )

#         request2 = solver_pb2.SolverRequest(
#             apiName=self.inputApiName
#             # nameフィールドを持たない/* name = self.inputName*/
#         )

#         request3 = solver_pb2.SolverRequest(
#             # inputApiNameフィールドを持たない/* apiName = self.inputApiName,*/
#             # nameフィールドを持たない/* name = self.inputName*/
#         )

#         # そもそもSolverRequestに叱られるので不要
#         # request4 = solver_pb2.SolverRequest(
#         #     apiName = self.inputApiName,
#         #     name = self.inputName,
#         #     # 本来持たないはずのメッセージを持つ
#         #     wrongField = "wrongmMessage"
#         # )

#         # レスポンスを取得
#         response1 = self.client.analyzeOnUnaryRPC(request1, 3)
#         response2 = self.client.analyzeOnUnaryRPC(request2, 3)
#         response3 = self.client.analyzeOnUnaryRPC(request3, 3)

#         solver_error = solver_pb2.SolverError(
#             apiName=self.errorApiName,
#             apiVersion=self.errorApiVersion,
#             errorId=self.errorErrorId,
#             errorMessage=self.errorErrorMessage,
#         )
#         solver_response = solver_pb2.SolverResponse(error=solver_error)
#         self.assertEqual(response1, solver_response)
#         self.assertEqual(response2, solver_response)
#         self.assertEqual(response3, solver_response)
#         self.server.stop(0)
#         # 待ち受け終了後の後処理を実行する
#         self.server.wait_for_termination()

#     # @ unittest.skip("モジュール修正中のためスキップ")
#     def test_AnalyzeOnServerStreamingRPC_Error(self):
#         self.init()
#         self.server.start()
#         request = solver_pb2.SolverRequest(
#             # フィールドを持たない/* apiName = self.inputApiName,*/
#             name=self.inputName
#         )

#         # レスポンスを取得
#         response_iterator = iter(self.client.analyzeOnServerStreamingRPC(request, 3))
#         for response in response_iterator:
#             solver_error = solver_pb2.SolverError(
#                 apiName=self.errorApiName,
#                 apiVersion=self.errorApiVersion,
#                 errorId=self.errorErrorId,
#                 errorMessage=self.errorErrorMessage,
#             )
#             solver_response = solver_pb2.SolverResponse(error=solver_error)
#             self.assertEqual(response, solver_response)

#         self.server.stop(0)
#         # 待ち受け終了後の後処理を実行する
#         self.server.wait_for_termination()

#     # @ unittest.skip("モジュール修正中のためスキップ")
#     def test_AnalyzeOnClientStreamingRPC_Error(self):
#         self.init()
#         self.server.start()
#         request_list = []
#         for index, i in enumerate(list(self.inputName)):
#             if index % 2 == 1:
#                 name = ""
#             else:
#                 name = i
#             request_s = solver_pb2.SolverRequest(apiName=self.inputApiName, name=name)
#             request_list.append(request_s)
#         request_iterator = iter(request_list)

#         # レスポンスを取得
#         response = self.client.analyzeOnClientStreamingRPC(request_iterator, 3)

#         solver_error = solver_pb2.SolverError(
#             apiName=self.errorApiName,
#             apiVersion=self.errorApiVersion,
#             errorId=self.errorErrorId,
#             errorMessage=self.errorErrorMessage,
#         )
#         solver_response = solver_pb2.SolverResponse(error=solver_error)
#         self.assertEqual(response, solver_response)
#         self.server.stop(0)
#         # 待ち受け終了後の後処理を実行する
#         self.server.wait_for_termination()

#     # AnalyzeOnBidirectionalStreamingRPCが失敗するテスト
#     def test_AnalyzeOnBidirectionalStreamingRPC_Error(self):
#         self.init()
#         self.server.start()
#         request_list = []
#         for index, i in enumerate(list(self.inputName)):
#             if index % 2 == 1:
#                 name = ""
#             else:
#                 name = i
#             request_s = solver_pb2.SolverRequest(apiName=self.inputApiName, name=name)
#             request_list.append(request_s)
#         request_iterator = iter(request_list)

#         # レスポンスを取得
#         response_iterator = iter(self.client.analyzeOnBidirectionalStreamingRPC(request_iterator, 3))

#         indexList = [i for i in range(len(self.inputName))]
#         for index, response, word in zip(indexList, response_iterator, list(self.inputName)):
#             if index % 2 == 1:
#                 solver_error = solver_pb2.SolverError(
#                     apiName=self.errorApiName,
#                     apiVersion=self.errorApiVersion,
#                     errorId=self.errorErrorId,
#                     errorMessage=self.errorErrorMessage,
#                 )
#                 solver_response = solver_pb2.SolverResponse(error=solver_error)
#             else:
#                 solver_reply = solver_pb2.SolverReply(
#                     apiName=self.outputApiName, apiVersion=self.outputApiVersion, text=word
#                 )
#                 solver_response = solver_pb2.SolverResponse(reply=solver_reply)
#             self.assertEqual(response, solver_response)
#         self.server.stop(0)
#         # 待ち受け終了後の後処理を実行する
#         self.server.wait_for_termination()

#     @unittest.skip("モジュール修正中のためスキップ")
#     def test_AnalyzeOnUnaryRPC_ssl(self):
#         self.init()
#         self.server.start()
#         request = solver_pb2.SolverRequest(apiName=self.inputApiName, name=self.inputName)

#         # レスポンスを取得
#         response = self.client.analyzeOnUnaryRPC_ssl(request, 3)

#         solver_reply = solver_pb2.SolverReply(
#             apiName=self.outputApiName, apiVersion=self.outputApiVersion, text=self.outputText
#         )
#         solver_response = solver_pb2.SolverResponse(reply=solver_reply)
#         self.assertEqual(response, solver_response)

#         # graceはサーバを止めるまで何秒 or msec待つか
#         self.server.stop(grace=0)

#         # 待ち受け終了後の後処理を実行する
#         self.server.wait_for_termination()
