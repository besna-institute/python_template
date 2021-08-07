import json
import unittest
from pathlib import Path
from src.gRPC.main.sampleclient import SolverClient
from src.gRPC.main import solver_pb2



class MainTest(unittest.TestCase):


    # AnalyzeOnUnaryRPCのテスト
    def test_AnalyzeOnUnaryRPC(self):
        print("これは？")
        client = SolverClient()
        # テストデータのjsonまでのパス
        path_to_dir = Path(__file__).parent
        path_to_data = path_to_dir / "data"

        # 入力データ(input.json)
        with open(path_to_data / "input1.json") as fp:
            json_input1 = json.load(fp)

        request = solver_pb2.SolverRequest(
            apiName = json_input1["apiName"],
            name = json_input1["name"],
        )
        print("ここまではok")

        # レスポンスを取得
        response = client.analyzeOnUnaryRPC(request,3)

        # 想定される結果
        with open(path_to_data / "output1.json") as fp:
            json_output1 = json.load(fp)

        # self.maxDiff = None
        # self.assertEqual(status_code, status.HTTP_200_OK)

        solver_reply = solver_pb2.SolverReply(
            apiName = json_output1["apiName"],
            name = json_output1["name"],
            text = json_output1["text"],
        )

        solver_response = solver_pb2.SolverResponse(
            reply = solver_reply
        )

        self.assertEqual(response, solver_response)

    # AnalyzeOnServerStreamingRPCのテスト
    # def test_AnalyzeOnServerStreamingRPC(self):
    #     with open(path_to_data / "input1.json") as fp:
    #         json_input1 = json.load(fp)

    #     response = client.post("/", json=json_input1)
    #     status_code = response.status_code

    #     with open(path_to_data / "output1.json") as fp:
    #         json_output1 = json.load(fp)

    #     self.maxDiff = None
    #     self.assertEqual(status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.json(), json_output1)
    #     pass

    # AnalyzeOnClientStreamingRPCのテスト
    # def test_AnalyzeOnClientStreamingRPC(self):
    #     pass

    # AnalyzeOnBidirectionalStreamingRPCのテスト
    # def test_AnalyzeOnBidirectionalStreamingRPC(self):
    #     pass
