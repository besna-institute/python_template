import json
import unittest
from pathlib import Path
from src.gRPC.sampleclient import SolverClient
from src.gRPC.generated import solver_pb2
import subprocess


class MainTest(unittest.TestCase):

    def init(self):
        self.client = SolverClient()
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
        self.inputApiName = json_input1["apiName"]
        self.inputName = json_input1["name"]

        # 想定される結果
        with open(path_to_data / "output1.json") as fp:
            json_output1 = json.load(fp)

        self.outputApiName = json_output1["apiName"]
        self.outputApiVersion = json_output1["apiVersion"]
        self.outputText = json_output1["text"]

        # 想定されるエラーメッセージ
        with open(path_to_data / "error1.json") as fp:
            json_output1 = json.load(fp)

        self.errorApiName = json_output1["apiName"]
        self.errorApiVersion = json_output1["apiVersion"]
        self.errorErrorId = json_output1["errorId"]
        self.errorErrorMessage = json_output1["errorMessage"]

    # AnalyzeOnUnaryRPCのテスト
    def test_AnalyzeOnUnaryRPC(self):
        self.init()

        request = solver_pb2.SolverRequest(
            apiName = self.inputApiName,
            name = self.inputName
        )

        # レスポンスを取得
        response = self.client.analyzeOnUnaryRPC(request,3)

        solver_reply = solver_pb2.SolverReply(
            apiName = self.outputApiName,
            apiVersion = self.outputApiVersion,
            text = self.outputText
        )
        solver_response = solver_pb2.SolverResponse(
            reply = solver_reply
        )
        self.assertEqual(response, solver_response)

    # AnalyzeOnServerStreamingRPCのテスト
    def test_AnalyzeOnServerStreamingRPC(self):
        self.init()

        request = solver_pb2.SolverRequest(
            apiName = self.inputApiName,
            name = self.inputName
        )

        # レスポンスを取得
        response_iterator = iter(self.client.analyzeOnServerStreamingRPC(request,3))

        solver_reply = []
        for response,word in zip(response_iterator,list(self.inputName)):
            solver_reply = solver_pb2.SolverReply(
                apiName = self.outputApiName,
                apiVersion = self.outputApiVersion,
                text = word,
            )
            solver_response = solver_pb2.SolverResponse(
                reply = solver_reply
            )
            self.assertEqual(response, solver_response)

    # AnalyzeOnClientStreamingRPCのテスト
    def test_AnalyzeOnClientStreamingRPC(self):
        self.init()

        request_list = []
        for i in list(self.inputName):
            request_s = solver_pb2.SolverRequest(
                apiName= self.inputApiName,
                name = i
            )
            request_list.append(request_s)
        request_iterator = iter(request_list)

        # レスポンスを取得
        response = self.client.analyzeOnClientStreamingRPC(request_iterator,3)

        solver_reply = solver_pb2.SolverReply(
                apiName = self.outputApiName,
                apiVersion = self.outputApiVersion,
                text = self.outputText
            )
        solver_response = solver_pb2.SolverResponse(
            reply = solver_reply
        )

        self.assertEqual(response, solver_response)


    # AnalyzeOnBidirectionalStreamingRPCのテスト
    def test_AnalyzeOnBidirectionalStreamingRPC(self):
        self.init()
        request_list = []
        for i in list(self.inputName):
            request_s = solver_pb2.SolverRequest(
                apiName= self.inputApiName,
                name = i
            )
            request_list.append(request_s)
        request_iterator = iter(request_list)

        # レスポンスを取得
        response_iterator = iter(self.client.analyzeOnBidirectionalStreamingRPC(request_iterator,3))

        solver_reply = []
        for response,word in zip(response_iterator,list(self.inputName)):
            solver_reply = solver_pb2.SolverReply(
                apiName = self.outputApiName,
                apiVersion = self.outputApiVersion,
                text = word
            )
            solver_response = solver_pb2.SolverResponse(
                reply = solver_reply
            )
            self.assertEqual(response, solver_response)


    # AnalyzeOnUnaryRPCが失敗するテスト
    def test_AnalyzeOnUnaryRPC_Error(self):
        self.init()

        request = solver_pb2.SolverRequest(
            # フィールドを持たない/* apiName = self.inputApiName,*/
            name = self.inputName
        )

        # レスポンスを取得
        response = self.client.analyzeOnUnaryRPC(request,3)

        solver_error = solver_pb2.SolverError(
            apiVersion = self.errorApiVersion,
            errorId = self.errorErrorId,
            errorMessage = self.errorErrorMessage
        )
        solver_response = solver_pb2.SolverResponse(
            error = solver_error
        )
        self.assertEqual(response, solver_response)

    # AnalyzeOnServerStreamingRPCが失敗するテスト
    def test_AnalyzeOnServerStreamingRPC_Error(self):
        self.init()

        request = solver_pb2.SolverRequest(
            # フィールドを持たない/* apiName = self.inputApiName,*/
            name = self.inputName
        )

        # レスポンスを取得
        response_iterator = iter(self.client.analyzeOnServerStreamingRPC(request,3))

        solver_reply = []
        for response,word in zip(response_iterator,list(self.inputName)):
            solver_error = solver_pb2.SolverError(
                apiVersion = self.errorApiVersion,
                errorId = self.errorErrorId,
                errorMessage = self.errorErrorMessage
            )
            solver_response = solver_pb2.SolverResponse(
                error = solver_error
            )
            self.assertEqual(response, solver_response)

    # # AnalyzeOnClientStreamingRPCが失敗するテスト
    # def test_AnalyzeOnClientStreamingRPC_Error(self):
    #     self.init()

    #     request_list = []
    #     for i in list(self.inputName):
    #         request_s = solver_pb2.SolverRequest(
    #             apiName= self.inputApiName,
    #             name = i
    #         )
    #         request_list.append(request_s)
    #     request_iterator = iter(request_list)

    #     # レスポンスを取得
    #     response = self.client.analyzeOnClientStreamingRPC(request_iterator,3)

    #     solver_reply = solver_pb2.SolverReply(
    #             apiName = self.outputApiName,
    #             apiVersion = self.outputApiVersion,
    #             text = self.outputText
    #         )
    #     solver_response = solver_pb2.SolverResponse(
    #         reply = solver_reply
    #     )

    #     self.assertEqual(response, solver_response)


    # # AnalyzeOnBidirectionalStreamingRPCが失敗するテスト
    # def test_AnalyzeOnBidirectionalStreamingRPC_Error(self):
    #     self.init()
    #     request_list = []
    #     for i in list(self.inputName):
    #         request_s = solver_pb2.SolverRequest(
    #             apiName= self.inputApiName,
    #             name = i
    #         )
    #         request_list.append(request_s)
    #     request_iterator = iter(request_list)

    #     # レスポンスを取得
    #     response_iterator = iter(self.client.analyzeOnBidirectionalStreamingRPC(request_iterator,3))

    #     solver_reply = []
    #     for response,word in zip(response_iterator,list(self.inputName)):
    #         solver_reply = solver_pb2.SolverReply(
    #             apiName = self.outputApiName,
    #             apiVersion = self.outputApiVersion,
    #             text = word
    #         )
    #         solver_response = solver_pb2.SolverResponse(
    #             reply = solver_reply
    #         )
    #         self.assertEqual(response, solver_response)
