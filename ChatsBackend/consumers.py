from channels.consumer import AsyncConsumer, StopConsumer
from json import dumps, loads
from .models import ChatsModel
from ChatAuth.models import CustomAbstractUser
from channels.db import database_sync_to_async

# dumps-> converts Python object into string
# loads-> convert string into object


class ChatHandlerConsumer(AsyncConsumer):
    GROUP_NAME = None
    # gets ran when the connection is established
    async def websocket_connect(self, e):
        print("----------------- Conn has been established.......")
        self.receiver_name = self.scope["url_route"]["kwargs"]["receiver_name"]
        self.group_name = self.NameGenerator(
            self.scope["user"].username, self.receiver_name
        )
        self.GROUP_NAME = self.group_name
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.send({"type": "websocket.accept"})

    # Generates group_name based on sender and receiver name
    def NameGenerator(self, str1, str2):
        if str1 < str2:
            return f"{str1}_{str2}_chats"
        elif str1 > str2:
            return f"{str2}_{str1}_chats"
        else:
            return f"{str1}_{str2}_chats"

    # Gets executed when data is received from user
    async def websocket_receive(self, e):
        self.incoming_data = loads(e["text"])  # getting from the client side
        # getting receiver name from scope (passed via websocket URL)
        self.receiver_name = self.scope["url_route"]["kwargs"]["receiver_name"]
        # getting users object from DB
        self.Receiver_object = await database_sync_to_async(
            CustomAbstractUser.objects.get
        )(username=self.receiver_name)
        self.Curr_User = await database_sync_to_async(CustomAbstractUser.objects.get)(
            username=self.scope["user"].username
        )
        # Group_Name from NameGenerator() Not sure whether usable or not
        # self.GROUP_NAME = self.group_name
        if "Message" in self.incoming_data:
            New_Msg_object = await database_sync_to_async(ChatsModel.objects.create)(
                sender=self.Curr_User,
                receiver=self.Receiver_object,
                message=self.incoming_data["Message"],
                GroupName=self.GROUP_NAME,
            )
            await database_sync_to_async(New_Msg_object.save)()
            # await self.send({
            #     'type':'websocket.send'
            # })
            await self.channel_layer.group_send(
                self.group_name,
                {"type": "websocket.GroupSend", "text": self.incoming_data["Message"]},
            )

        # Handler for sending messages in Group
    async def websocket_GroupSend(self, data_dict):
        print("Messages has been sent to Group.")
        await self.send({"type": "websocket.send", "text": data_dict["text"]})


    async def websocket_disconnect(self, e):
        print("-----------Connnection is Closed------------------------")
        await self.channel_layer.group_discard(
            group=self.GROUP_NAME,
            channel=self.channel_name,
        )
        raise StopConsumer

    def get_group_name(self):
        return self.GROUP_NAME
