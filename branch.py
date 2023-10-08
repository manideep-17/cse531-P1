from concurrent import futures
import sys
import json

import grpc
import bank_pb2
import bank_pb2_grpc


class Branch(bank_pb2_grpc.BankServicer):
    def __init__(self, id, balance, branches):
        self.id = id
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.channelList = list()
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # iterate the processID of the branches
        # TODO: students are expected to store the processID of the branches
        pass

    def Deposit(self, request, context):
        self.balance += request.money
        # propagate deposit
        if len(self.channelList) == 0:
            for id in self.branches:
                port = 50051 + id
                channel = grpc.insecure_channel(
                    f"localhost:{port}")
                self.channelList.append(channel)
                stub = bank_pb2_grpc.BankStub(channel)
                self.stubList.append(stub)
        for stub in self.stubList:
            stub.Propagate_Deposit(
                bank_pb2.PropagateDepositRequest(balance=self.balance))

        return bank_pb2.DepositResponse(id=self.id, event_id=request.event_id, result="success")

    def Query(self, request, context):
        return bank_pb2.QueryResponse(id=self.id, event_id=request.event_id, balance=self.balance)

    def Withdraw(self, request, context):
        status = "fail"
        if self.balance >= request.money:
            self.balance -= request.money
            # propagate withdraw
            if len(self.channelList) == 0:
                for id in self.branches:
                    port = 50051 + id
                    channel = grpc.insecure_channel(
                        f"localhost:{port}")
                    self.channelList.append(channel)
                    stub = bank_pb2_grpc.BankStub(channel)
                    self.stubList.append(stub)
            for stub in self.stubList:
                stub.Propagate_Withdraw(
                    bank_pb2.PropagateWithdrawRequest(balance=self.balance))
        return bank_pb2.WithdrawResponse(id=self.id, event_id=request.event_id, result=status)

    def Propagate_Deposit(self, request, context):
        self.balance = request.balance
        return bank_pb2.PropagateDepositResponse(result="success")

    def Propagate_Withdraw(self, request, context):
        self.balance = request.balance
        return bank_pb2.PropagateWithdrawResponse(result="success")

    # TODO: students are expected to process requests from both Client and Branch

    def MsgDelivery(self, request, context):
        self.recvMsg.append(request)
        pass


def start_grpc_servers(branches):
    servers = []
    branchPrcoessId = []
    for i in range(len(branches)):
        branchPrcoessId.append(branches[i]["id"])

    for i in range(len(branches)):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        branch = Branch(id=branches[i]["id"],
                        balance=branches[i]["balance"], branches=branchPrcoessId)
        bank_pb2_grpc.add_BankServicer_to_server(branch, server)
        port = 50051 + branches[i]["id"]
        server.add_insecure_port(f'[::]:{port}')
        server.start()
        print(f"Branch {branches[i]['id']} started on port: {port}")
        servers.append(server)

    for server in servers:
        server.wait_for_termination()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nStopping all servers.")
        for server in servers:
            server.stop(0)


if __name__ == '__main__':
    # Fetch the json path from the argv and read the JSON input
    file_path = f'{sys.argv[1]}'
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    branches = []

    for i in range(len(data)):
        if (data[i]["type"] == "branch"):
            branches.append(data[i])

    start_grpc_servers(branches)
