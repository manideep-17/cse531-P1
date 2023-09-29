import time
import sys
import json

import grpc
import bank_pb2
import bank_pb2_grpc


class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = None
        self.port = 50051 + id
        self.lastProcessedId = -1

    def appendEvents(self, events):
        self.events.extend(events)

    # TODO: students are expected to create the Customer stub
    def createStub(self):
        with grpc.insecure_channel(f"localhost:{self.port}") as channel:
            stub = bank_pb2_grpc.BankStub(channel)
        return stub

    # TODO: students are expected to send out the events to the Bank
    def executeEvents(self):
        if self.stub is None:
            self.stub = self.createStub()
        result = []
        for i in range(self.lastProcessedId+1, len(self.events)):
            print("processing event", i)
            print(self.events[i])
            self.lastProcessedId = i
            # if(self.events[i]["interface"] == "deposit"):
            #     response = self.stub.Deposit(id=self.id, event_id=self.events[i]["id"], money=self.events[i]["money"])
        pass


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
