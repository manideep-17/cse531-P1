from concurrent import futures
import sys
import json

import grpc
import bank_pb2
import bank_pb2_grpc


class Branch(bank_pb2_grpc.BankServicer):
    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # iterate the processID of the branches
        # TODO: students are expected to store the processID of the branches
        pass

    # TODO: students are expected to process requests from both Client and Branch
    def MsgDelivery(self, request, context):
        pass


def start_grpc_servers(branches):
    servers = []

    for i in range(len(branches)):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        branch = Branch(id=branches[i]["id"],
                        balance=branches[i]["balance"], branches=[])
        bank_pb2_grpc.add_BankServicer_to_server(branch, server)
        port = 50051 + branches[i]["id"]
        server.add_insecure_port(f'[::]:{port}')
        server.start()
        print(f"Branch {branches[i]['id']} started on port: {port}")
        servers.append(server)

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
