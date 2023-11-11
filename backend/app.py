import time

import cv2
from flask import Flask, render_template, Response, request, abort
import os
from db_functions import read_db, write_db
from flask_cors import CORS
import json
from video_processing import add_mask, crutch_function, find_person, get_mask_by_filename, calculate_intersection_percent
from random import randint
from threading import Semaphore

app = Flask(__name__)
CORS(app)
"""data = {
    "DpR-Csp-uipv-ShV-V1.avi": {"is_intersection": 0, "percents": 0},
    "Pgp-com2-K-1-0-9-36.avi": {"is_intersection": 0, "percents": 0},
    "Pgp-lpc2-K-0-1-38.avi": {"is_intersection": 0, "percents": 0},
    "Phl-com3-Shv2-9-K34.avi": {"is_intersection": 0, "percents": 0},
    "Php-Angc-K3-1.avi": {"is_intersection": 0, "percents": 0},
    "Php-Angc-K3-8.avi": {"is_intersection": 0, "percents": 0},
    "Php-Ctm-K-1-12-56.avi": {"is_intersection": 0, "percents": 0},
    "Php-Ctm-Shv1-2-K3.avi": {"is_intersection": 0, "percents": 0},
    "Php-nta4-shv016309-k2-1-7.avi": {"is_intersection": 0, "percents": 0},
    "Spp-210-K1-3-3-5.avi": {"is_intersection": 0, "percents": 0},
    "Spp-210-K1-3-3-6.avi": {"is_intersection": 0, "percents": 0},
    "Spp-K1-1-2-6.avi": {"is_intersection": 0, "percents": 0}
}"""
data = {
    "DpR-Csp-uipv-ShV-V1.avi": {"is_intersection": 0, "percents": 0},
    "Php-nta4-shv016309-k2-1-7.avi": {"is_intersection": 0, "percents": 0},
    "Php-Angc-K3-1.avi": {"is_intersection": 0, "percents": 0},
    "Spp-K1-1-2-6.avi": {"is_intersection": 0, "percents": 0}
}

is_data_available = Semaphore(1)
video_folder = "pure_data"


def process_sse():
    is_data_available.acquire()
    yield 'data: %s\n\n' % json.dumps(data)
    is_data_available.release()


def process_video(file_name):
    # Создайте объект VideoCapture для захвата видео с веб-камеры
    if os.path.exists(f"{video_folder}/{file_name}"):
        cap = cv2.VideoCapture(f"{video_folder}/{file_name}")
        frames_count = 0
        while True:
            # Считайте кадр из видеопотока
            ret, frame = cap.read()
            frames_count += 1
            if not ret:
                frames_count = 0
                cap = cv2.VideoCapture(f"{video_folder}/{file_name}")
                ret, frame = cap.read()
            # Обработайте кадр с помощью OpenCV (добавьте ваш код обработки здесь)
            intersection = crutch_function(frames_count, file_name)

            is_data_available.acquire()
            rectangles = find_person(frame)
            is_data_available.release()
            mask = get_mask_by_filename(file_name.split('.')[0])
            intersections = []
            for rectangle in rectangles:
                frame_data = read_db().get(file_name)
                if frame_data is not None:
                    intersection_percent = calculate_intersection_percent(rectangle, mask)
                    intersections.append(intersection_percent)
            if len(intersections) > 0:
                return max(intersections)
            else:
                return 0
            is_data_available.acquire()
            if intersection > 15:
                data[file_name] = {"is_intersection": 1, "percents": intersection}
            else:
                data[file_name] = {"is_intersection": 0, "percents": intersection}
            is_data_available.release()

            add_mask(frame, file_name)
            # cv2.imshow('graycsale image', frame)
            # cv2.waitKey(0)
            # Преобразуйте кадр в формат, подходящий для передачи через HTTP

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # КОСТЫЛЬ!!!!!!!!!
            # time .sleep(0.25)
            # Верните кадр в виде генератора байтов
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # Освободите ресурсы после завершения
        cap.release()


@app.route('/mask/<video>', methods=['POST'])
def put_mask(video):
    args = request.json
    if not args or 'userSelection' not in args:
        abort(400)
    mask = []
    user_selection = args['userSelection']
    color = args['color']
    if color is not None:
        color = tuple(color)
    else:
        color = (255, 0, 0)
    for section in user_selection:
        x = section['x']
        y = section['y']
        mask.append([x, y])

    data = read_db()
    data[video] = {"mask": mask, "color": color}
    status = write_db(data)
    response = app.response_class(
        response=json.dumps({"status": status}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/video_feed/<video>')
def video_feed(video):
    return Response(process_video(video), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/sse", methods=["GET"])
def sse():
    return Response(process_sse(), mimetype="text/event-stream")


if __name__ == '__main__':
    # context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # context.load_cert_chain('cert.pem', 'key.pem')
    app.run(debug=True, port=9090, host='25.47.207.197', threaded=True)
