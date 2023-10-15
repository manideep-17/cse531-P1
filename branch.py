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
        self.branches = branches
        self.channelList = list()
        self.stubList = list()
        self.recvMsg = list()

    def Deposit(self, request):
        self.balance += request.money
        if len(self.channelList) == 0:
            for id in self.branches:
                port = 50051 + id
                channel = grpc.insecure_channel(
                    f"localhost:{port}")
                self.channelList.append(channel)
                stub = bank_pb2_grpc.BankStub(channel)
                self.stubList.append(stub)
        for stub in self.stubList:
            stub.MsgDelivery(
                bank_pb2.MsgDeliveryRequest(balance=self.balance, interface="propagatedeposit"))
        return {
            "id": self.id,
            "event_id": request.event_id,
            "result": "success"
        }

    def Query(self, request):
        return {
            "id": self.id,
            "event_id": request.event_id,
            "balance": self.balance
        }

    def Withdraw(self, request):
        status = "fail"
        if self.balance >= request.money:
            status = "success"
            self.balance -= request.money
            if len(self.channelList) == 0:
                for id in self.branches:
                    port = 50051 + id
                    channel = grpc.insecure_channel(
                        f"localhost:{port}")
                    self.channelList.append(channel)
                    stub = bank_pb2_grpc.BankStub(channel)
                    self.stubList.append(stub)
            for stub in self.stubList:
                stub.MsgDelivery(
                    bank_pb2.MsgDeliveryRequest(balance=self.balance, interface="propagatewithdraw"))
        return {
            "id": self.id,
            "event_id": request.event_id,
            "result": status
        }

    def Propagate_Deposit(self, request):
        self.balance = request.balance
        return {
            "result": "success"
        }

    def Propagate_Withdraw(self, request):
        self.balance = request.balance
        return {
            "result": "success"
        }

    def MsgDelivery(self, request, context):
        self.recvMsg.append(request)
        if request.interface == "query":
            response = self.Query(request=request)
        elif request.interface == "deposit":
            response = self.Deposit(request=request)
        elif request.interface == "withdraw":
            response = self.Withdraw(request=request)
        elif request.interface == "propagatewithdraw":
            response = self.Propagate_Withdraw(request=request)
        elif request.interface == "propagatedeposit":
            response = self.Propagate_Deposit(request=request)
        else:
            print("issue")
        id = response.get("id", None)
        event_id = response.get("event_id", None)
        balance = response.get("balance", None)
        result = response.get("result", None)
        return bank_pb2.MsgDeliveryResponse(id=id, event_id=event_id, balance=balance, result=result)


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
    file_path = f'{sys.argv[1]}'
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    branches = []

    for i in range(len(data)):
        if (data[i]["type"] == "branch"):
            branches.append(data[i])

    start_grpc_servers(branches)
