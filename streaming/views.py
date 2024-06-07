from django.http import StreamingHttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


from channels.layers import get_channel_layer

from asgiref.sync import AsyncToSync, sync_to_async, async_to_sync

import numpy as np
import cv2
import asyncio
from threading import Thread
import os
import base64

from streaming.models import StreamingSetting
from .forms import EditCameraForm


baseDir = os.path.dirname(os.path.realpath(__file__))
fileDir = os.path.join(baseDir, 'source/cars.xml')


car_cascade = cv2.CascadeClassifier(fileDir)
channel_layer = get_channel_layer()


@login_required(login_url='login')
def dsv(request):
    context = {}
    template = 'dsv.html'
    streaming_setting = StreamingSetting.objects.filter(user=request.user).first()
    
    

    if request.method == 'POST':
        streaming_setting.cam1 = request.POST.get('cam1')
        streaming_setting.cam2 = request.POST.get('cam2')
        streaming_setting.cam3 = request.POST.get('cam3')
        streaming_setting.cam4 = request.POST.get('cam3')
        streaming_setting.num_cam = request.POST.get('num_cam')
        
        streaming_setting.save()
        
        messages.success(
            request, 'Informacion actualizada corectamente '
            )

        return redirect('streaming:dsv')

            
    context['streaming_setting'] = streaming_setting


    return render(request, template, context)


#https://channels.readthedocs.io/en/latest/topics/channel_layers.html
def detected(imgRoi, channel_name):

    ret, jpeg = cv2.imencode('.jpg', imgRoi)
    jpeg64 = base64.b64encode(jpeg)
    image = "data:image/jpg;base64," + jpeg64.decode()
   
    async_to_sync(channel_layer.send)(
    channel_name,
    {
        'type': 'event.message',
        'CMD': 'IMG',
        'img': image,
    }
)


async def get_frame(video, channel_name):
    loop = asyncio.get_event_loop()
    success, frame = await loop.run_in_executor(None, video.read)


    frame = cv2.resize(frame,(400, 312))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Detect cars in the frame
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
    #cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, 1)

    margin = 5
    height, width = frame.shape[:2]


    for (x,y,w,h) in cars: 
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

        start_x = max(x - margin, 0)
        start_y = max(y - margin, 0)
        end_x = min(x + w + margin, width)
        end_y = min(y + h + margin, height)

        imgRoi = frame[start_y:end_y, start_x:end_x] #Cut the box with the margin
        Thread(target=detected, args=(imgRoi, channel_name,)).start()

    if not success:
        print("Failed to read frame")
        return None
    ret, jpeg = await loop.run_in_executor(None, cv2.imencode, '.jpg', frame)
    if not ret:
        print("Failed to encode frame")
        return None
    return jpeg.tobytes()

async def video_stream(camera_url, channel_name):
    video = cv2.VideoCapture(camera_url)
    if not video.isOpened():
        raise Exception("Could not open video device")
    print("Camera opened")
    
    try:
        while True:

            frame = await get_frame(video, channel_name)
            if frame is None:
                print("No frame received")
                break
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            
            cmd = await sync_to_async(StreamingSetting.objects.get)(channel_name=channel_name)
            if cmd.start == 'Stop':
                break

    finally:
        if video.isOpened():
            video.release()
        print("Camera released")



async def streaming_camera(request, camera_number):
    try:
        data = await sync_to_async(lambda: request.user.streaming_settings.order_by('-id').first())()
        camera_url = os.path.join(baseDir, 'videos/cam2.mp4')
        camera_dict = {
        1: data.cam1,
        2: data.cam2,
        3: data.cam3,
        4: data.cam4
        }
        camera_url = camera_dict.get(camera_number, camera_url) or camera_url
        channel_name = data.channel_name
    
        return StreamingHttpResponse(video_stream(camera_url, channel_name), content_type='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(f"Error: {e}")
        return HttpResponseServerError(f"Error: {e}")


async def cam1(request):
    return await streaming_camera(request, 1)

async def cam2(request):
    return await streaming_camera(request, 2)

async def cam3(request):
    return await streaming_camera(request, 3)

async def cam4(request):
    return await streaming_camera(request, 4)