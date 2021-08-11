import json
import unittest
from pathlib import Path
from src.gRPC.sampleclient import SolverClient
from src.gRPC.generated import solver_pb2
import subprocess


class MainTest(unittest.TestCase):


    # AnalyzeOnUnaryRPCのテスト
    def test_AnalyzeOnUnaryRPC(self):
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

        # レスポンスを取得
        response = client.analyzeOnUnaryRPC(request,3)

        # 想定される結果
        with open(path_to_data / "output1.json") as fp:
            json_output1 = json.load(fp)

        # self.maxDiff = None
        # self.assertEqual(status_code, status.HTTP_200_OK)

        solver_reply = solver_pb2.SolverReply(
            apiName = json_output1["apiName"],
            apiVersion = json_output1["apiVersion"],
            text = json_output1["text"],
        )
        solver_response = solver_pb2.SolverResponse(
            reply = solver_reply
        )

        self.assertEqual(response, solver_response)

    # AnalyzeOnServerStreamingRPCのテスト
    def test_AnalyzeOnServerStreamingRPC(self):
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

        # レスポンスを取得
        response_iterator = iter(client.analyzeOnServerStreamingRPC(request,3))

        # 想定される結果
        with open(path_to_data / "output1.json") as fp:
            json_output1 = json.load(fp)


        solver_reply = []
        name = list(json_input1["name"])
        for response,word in zip(response_iterator,name):
            solver_reply = solver_pb2.SolverReply(
                apiName = json_output1["apiName"],
                apiVersion = json_output1["apiVersion"],
                text = word,
            )
            solver_response = solver_pb2.SolverResponse(
                reply = solver_reply
            )
            self.assertEqual(response, solver_response)

    # AnalyzeOnClientStreamingRPCのテスト
    def test_AnalyzeOnClientStreamingRPC(self):
        client = SolverClient()
        # テストデータのjsonまでのパス
        path_to_dir = Path(__file__).parent
        path_to_data = path_to_dir / "data"

        # 入力データ(input.json)
        with open(path_to_data / "input1.json") as fp:
            json_input1 = json.load(fp)

        request_list = []
        requestName = "Taro"
        for i in list(requestName):
            request_s = solver_pb2.SolverRequest(
                apiName= json_input1["apiName"],
                name = i
            )
            request_list.append(request_s)
        request_iterator = iter(request_list)

        # レスポンスを取得
        response = client.analyzeOnClientStreamingRPC(request_iterator,3)

        # 想定される結果
        with open(path_to_data / "output1.json") as fp:
            json_output1 = json.load(fp)

        solver_reply = []
        name = list(json_input1["name"])
        solver_reply = solver_pb2.SolverReply(
                apiName = json_output1["apiName"],
                apiVersion = json_output1["apiVersion"],
                text = json_output1["text"],
            )
        solver_response = solver_pb2.SolverResponse(
            reply = solver_reply
        )

        self.assertEqual(response, solver_response)


    # AnalyzeOnBidirectionalStreamingRPCのテスト
    def test_AnalyzeOnBidirectionalStreamingRPC(self):
        client = SolverClient()
        # テストデータのjsonまでのパス
        path_to_dir = Path(__file__).parent
        path_to_data = path_to_dir / "data"

        # 入力データ(input.json)
        with open(path_to_data / "input1.json") as fp:
            json_input1 = json.load(fp)

        request_list = []
        requestName = "Taro"
        for i in list(requestName):
            request_s = solver_pb2.SolverRequest(
                apiName= json_input1["apiName"],
                name = i
            )
            request_list.append(request_s)
        request_iterator = iter(request_list)

        # レスポンスを取得
        response_iterator = iter(client.analyzeOnBidirectionalStreamingRPC(request_iterator,3))

        # 想定される結果
        with open(path_to_data / "output1.json") as fp:
            json_output1 = json.load(fp)

        solver_reply = []
        name = list(json_input1["name"])
        for response,word in zip(response_iterator,name):
            solver_reply = solver_pb2.SolverReply(
                apiName = json_output1["apiName"],
                apiVersion = json_output1["apiVersion"],
                text = word,
            )
            solver_response = solver_pb2.SolverResponse(
                reply = solver_reply
            )
            self.assertEqual(response, solver_response)
