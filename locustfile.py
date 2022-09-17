from locust import FastHttpUser, SequentialTaskSet, task, between

class WebsiteFira(FastHttpUser):

    @task
    class SequenceOfTasks(SequentialTaskSet):
        wait_time = between(0.8, 3.0)

        @task
        def setFiraVariables(self):
            self.managerServer = "https://fira-live-management-api-preprod.azurewebsites.net"
            self.broadcastServer = "https://fira-live-broadcasting-service-api-preprod.azurewebsites.net"
            self.actionServer = "https://fira-live-broadcasting-actions-api-preprod.azurewebsites.net"
            self.storeId = "62ff2a7abbdd6920b934ec77"

        
        @task
        def getLastLiveFromStore(self):
            liveResponse = self.client.get(self.managerServer + "/api/v1/fira-broadcast-event-controller/last-event/" + self.storeId)
            self.liveId = str(liveResponse.json().get("id"))

        @task
        def getRed5Video(self):
            self.client.get(self.managerServer + "/api/v1/fira-broadcast-event-controller/live-data/" + self.liveId)
        
        @task
        def createNewConnection(self):
            connectionResponse = self.client.post(self.actionServer + "/v1/live-broadcasting-actions/connection/new", json={"userName": "", "broadcastingId": self.liveId,"connectionType": "WEB"})
            self.connectionId = str(connectionResponse.json().get("connectionId"))

        @task
        def getProducts(self):
            self.client.get(self.broadcastServer + "/v1/live-broadcast-event/broadcast-product/retrieve-all-activates/" + self.liveId)

        @task
        def getStats(self):  
            self.client.get(self.actionServer + "/v1/live-broadcasting-actions/client/current-summary/" + self.connectionId)

        @task
        def createUserQueues(self):
            self.client.put(self.actionServer + "/v1/live-broadcasting-actions/connection/call-queues-creation/" + self.liveId + "/" + self.connectionId)
