import argparse
import base64
from datetime import datetime
import os
import shutil
from src import *

import json
import asyncio
import numpy as np
import websockets
from PIL import Image
from flask import Flask
from io import BytesIO

from tensorflow.keras.models import load_model
from keras.config import enable_unsafe_deserialization
from keras import __version__ as keras_version

ENGINE_PACKET_TYPE_MESSAGE = 4
SOCKET_PACKET_TYPE_EVENT = 2

target_size = (66, 200)
model = None
prev_image_array = None


class SimplePIController:
    def __init__(self, Kp, Ki):
        self.Kp = Kp
        self.Ki = Ki
        self.set_point = 0.
        self.error = 0.
        self.integral = 0.

    def set_desired(self, desired):
        self.set_point = desired

    def update(self, measurement):
        # proportional error
        self.error = self.set_point - measurement

        # integral error
        self.integral += self.error

        return self.Kp * self.error + self.Ki * self.integral


controller = SimplePIController(0.1, 0.002)
set_speed = 9
controller.set_desired(set_speed)


# Hàm xử lý khi nhận kết nối từ client
async def handle_connection(websocket):
    try:
        # Listen for data from the client
        async for message in websocket:
            try:
                data = json.loads(message[2:])  # Parse JSON
                event_name = data[0]
                data =data[1]
                if event_name == "telemetry":
                    # Parse received data
                    steering_angle = data["steering_angle"]
                    throttle = data["throttle"]
                    speed = data["speed"]
                    imgString = data["image"]

                    # Decode image from base64
                    image = Image.open(BytesIO(base64.b64decode(imgString)))
                    image_array = np.asarray(image)

                    # Preprocess image
                    preprocessed_image = preprocess_image(image_array)

                    # Reshape for prediction (model expects batch size of 1)
                    preprocessed_image = np.expand_dims(preprocessed_image, axis=0)

                    # Predict steering angle
                    steering_angle = float(model.predict(preprocessed_image, batch_size=1))

                    # Update throttle using controller
                    throttle = 10

                    # Print and send response back to the client
                    print(steering_angle, throttle)
                    await send_control(websocket, steering_angle, throttle)

                    # Save frame if image_folder is specified
                    if args.image_folder != '':
                        timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
                        image_filename = os.path.join(args.image_folder, timestamp)
                        image.save('{}.jpg'.format(image_filename))
            except json.JSONDecodeError:
                continue
    except websockets.exceptions.ConnectionClosed as e:
        return


async def emit(websocket, event, data=None, packet_id=0, namespace="/"):
    message_type = f"{ENGINE_PACKET_TYPE_MESSAGE}{SOCKET_PACKET_TYPE_EVENT}"
    payload = [event]
    
    if data:
        payload.append(data)

    # Thêm packet_id vào gói tin nếu có
    if packet_id >= 0:
        message_type += str(packet_id)

    # Xây dựng namespace nếu có
    if namespace and namespace != "/":
        message_type += namespace + ","
    
    # Chuyển payload thành JSON string
    message = message_type + json.dumps(payload)

    # Gửi message qua WebSocket
    await websocket.send(message)

async def send_control(websocket, steering_angle, throttle):
    # Định nghĩa dữ liệu điều khiển
    control_data = {
        "steering_angle": str(steering_angle),
        "throttle": str(throttle)
    }
    
    await emit(websocket, "steer", data=control_data)
    print("Control data sent")
    

# Hàm main để chạy WebSocket server
async def main():
    # Chạy server WebSocket tại địa chỉ ws://localhost:4567
    server = await websockets.serve(handle_connection, "localhost", 4567)
    print("WebSocket server started on ws://localhost:4567")
    await server.wait_closed()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remote Driving')
    parser.add_argument(
        'model',
        type=str,
        help='Path to model h5 file. Model should be on the same path.'
    )
    parser.add_argument(
        'image_folder',
        type=str,
        nargs='?',
        default='',
        help='Path to image folder. This is where the images from the run will be saved.'
    )
    args = parser.parse_args()
    
    enable_unsafe_deserialization()
    model = load_model(args.model)

    if args.image_folder != '':
        print("Creating image folder at {}".format(args.image_folder))
        if not os.path.exists(args.image_folder):
            os.makedirs(args.image_folder)
        else:
            shutil.rmtree(args.image_folder)
            os.makedirs(args.image_folder)
        print("RECORDING THIS RUN ...")
    else:
        print("NOT RECORDING THIS RUN ...")
    
    # Chạy server
    asyncio.run(main())
