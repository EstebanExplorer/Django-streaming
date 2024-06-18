from django.contrib.auth.models import User

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from streaming.models import StreamingSetting


@database_sync_to_async
def save_channel(user, channel_name):
    updated = StreamingSetting.objects.filter(user__id=user.id).update(channel_name=channel_name)

    if updated == 0:
        StreamingSetting.objects.create(user=user, channel_name=channel_name)
   

@database_sync_to_async
def update_channel(channel_name, start):
    StreamingSetting.objects.filter(channel_name=channel_name).update(start=start)
    

class ConnectSignal(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        await save_channel(user, self.channel_name)
    
        await self.accept()
      
   
    # Receive message from WebSocket
    async def receive_json(self, content):
        await update_channel(self.channel_name, 'Start')
    

        if content['CMD'] == 'IN':
            
            await self.send_json({
                "CMD": "IN",
                "initiated": content['CMD']
                }),

        if content['CMD'] == 'ORD':
            mando = content['orden']
            if mando =='Start':
                await update_channel(self.channel_name, mando)
                
             
            await self.send_json({
                    "CMD": "ORD"
                    }),

            if mando =='Stop':
                await update_channel(self.channel_name, mando)
                await self.send_json({
                    "CMD": "DT"
                    }),


    async def event_message(self, event):
        await self.send_json(content=event)
  

    async def disconnect(self, close_code):
        await self.close()
       

