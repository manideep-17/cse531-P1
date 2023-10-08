import time
import sys
import json

import grpc
import bank_pb2
import bank_pb2_grpc


class Customer:
    def __init__(self, id, events):
        self.id = id
        self.events = events
        self.recvMsg = list()
        self.channel = None
        self.stub = None
        self.port = 50051 + id
        self.lastProcessedId = -1

    def appendEvents(self, events):
        self.events.extend(events)

    def createStub(self):
        self.channel = grpc.insecure_channel(f"localhost:{self.port}")
        stub = bank_pb2_grpc.BankStub(self.channel)
        return stub

    def executeEvents(self):
        if self.stub is None:
            self.stub = self.createStub()
        result = {
            "id": self.id,
            "events": []
        }
        for i in range(self.lastProcessedId+1, len(self.events)):
            self.lastProcessedId = i
            print(
                f"processing {self.events[i]['interface']} Event with Index: {i}")
            if (self.events[i]["interface"] == "deposit"):
                response = self.stub.Deposit(bank_pb2.DepositRequest(
                    id=self.id, event_id=self.events[i]["id"], money=self.events[i]["money"]))
                result["events"].append({
                    "id": response.event_id,
                    "interface": self.events[i]["interface"],
                    "result": response.result
                })
            if (self.events[i]["interface"] == "query"):
                response = self.stub.Query(bank_pb2.QueryRequest(
                    id=self.id, event_id=self.events[i]["id"]))
                result["events"].append({
                    "id": response.event_id,
                    "interface": self.events[i]["interface"],
                    "balance": response.balance
                })
            if (self.events[i]["interface"] == "withdraw"):
                response = self.stub.Withdraw(bank_pb2.WithdrawRequest(
                    id=self.id, event_id=self.events[i]["id"], money=self.events[i]["money"]))
                result["events"].append({
                    "id": response.event_id,
                    "interface": self.events[i]["interface"],
                    "result": response.result
                })
        return result


if __name__ == '__main__':
    # Fetch the json path from the argv and read the JSON input
    file_path = f'{sys.argv[1]}'
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    customerData = []
    customers = {}
    response = []

    for i in range(len(data)):
        if (data[i]["type"] == "customer"):
            # customerData.append(data[i])
            if data[i]["id"] not in customers:
                customers[data[i]["id"]] = Customer(
                    data[i]["id"], data[i]["events"])
                response.append(customers[data[i]["id"]].executeEvents())

            else:
                customers[data[i]["id"]].appendEvents(data[i]["events"])
                response.append(customers[data[i]["id"]].executeEvents())
    print(response)
