import json
import os
from datetime import datetime
from threading import Semaphore
from io import BytesIO
import cv2
import matplotlib.pyplot as plt
from flask import Flask, Response, request, abort, send_file
from flask_cors import CORS
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Table

import report_functions
from db_functions import read_db, write_db
from video_processing import add_mask, find_person, get_mask_by_filename, \
    calculate_intersection_percent

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
photo_folder = "photos"


def process_sse():
    is_data_available.acquire()
    yield 'data: %s\n\n' % json.dumps(data)
    is_data_available.release()


def process_data(file_name):
    # Создайте объект VideoCapture для захвата видео с веб-камеры
    if os.path.exists(f"{video_folder}/{file_name}"):
        cap = cv2.VideoCapture(f"{video_folder}/{file_name}")
        frames_count = 0
        while True:
            ret, frame = cap.read()
            frames_count += 1
            if not ret:
                frames_count = 0
                cap = cv2.VideoCapture(f"{video_folder}/{file_name}")
                ret, frame = cap.read()

            is_data_available.acquire()
            rectangles = find_person(frame)
            is_data_available.release()

            masks = get_mask_by_filename(file_name)

            intersections = []
            for mask in masks:
                for rectangle in rectangles:
                    frame_data = read_db().get(file_name)
                    if frame_data is not None:
                        intersection_percent = calculate_intersection_percent(rectangle, mask)
                        intersections.append(intersection_percent)
            final_intersection = 0
            if len(intersections) > 0:
                final_intersection = max(intersections)
            is_data_available.acquire()
            if final_intersection > 15:
                data[file_name] = {"is_intersection": 1, "percents": final_intersection}
                report_data = report_functions.read_db()
                if report_data.get(file_name) is not None:
                    report_data[file_name].append({
                        "date": datetime.now().timestamp(),
                        'place': file_name.split('.')[0],
                        'intersection_percent': final_intersection,
                        "responsible": "Duhno Michail"
                    })
                else:
                    report_data[file_name] = [{
                        "date": datetime.now().timestamp(),
                        'place': file_name.split('.')[0],
                        'intersection_percent': final_intersection,
                        "responsible": "Duhno Michail"
                    }]
                report_functions.write_db(report_data)
            else:
                data[file_name] = {"is_intersection": 0, "percents": final_intersection}
            is_data_available.release()

            add_mask(frame, file_name)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # КОСТЫЛЬ!!!!!!!!!
            # time .sleep(0.25)
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
    color = args.get('color')

    if color is not None:
        color = tuple(color)
    else:
        color = (0, 0, 255)

    if len(user_selection) == 0:
        data = read_db()
        data[video] = {"mask": [], "color": color}
        status = write_db(data)
        response = app.response_class(
            response=json.dumps({"status": status}),
            status=200,
            mimetype='application/json'
        )
        return response

    cap = cv2.VideoCapture(f"{video_folder}/{video}")
    success, image = cap.read()
    img_height, img_width = image.shape[:2]
    for section in user_selection:
        x = float(section['x'])
        y = float(section['y'])
        mask.append([int(x * img_width), int(y * img_height)])

    data = read_db()
    cur_mask = data[video]['mask']
    cur_mask.append(mask)
    data[video] = {"mask": cur_mask, "color": color}
    status = write_db(data)
    response = app.response_class(
        response=json.dumps({"status": status}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/video_feed/<video>')
def video_feed(video):
    return Response(process_data(video), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/sse", methods=["GET"])
def sse():
    return Response(process_sse(), mimetype="text/event-stream")


@app.route("/get_report_data", methods=["GET"])
def gent_report_data():
    report_data = report_functions.read_db()
    data_to_send = []
    for key in report_data:
        for event in report_data[key]:
            data_to_send.append({
                "date": datetime.fromtimestamp(event['date']).strftime('%m.%d.%y %H:%M:%S'),
                "intersection_percent": event['intersection_percent'],
                "place": event['place'],
                "responsible": event['responsible']
            })
    return data_to_send


@app.route("/get_all_cameras_info", methods=["GET"])
def get_report_data():
    report_data = report_functions.read_db().keys()
    result = []
    for key in report_data:
        result.append({
            'name': key,
            'code': key
        })

    return result


@app.route("/report", methods=["POST"])
def generate_report():
    args = request.json
    print(args)

    cameras = args.get('cameras')
    month = datetime.now().month
    year = datetime.now().year
    report_data = report_functions.read_db()
    report_data_to_handle = dict()
    for key in report_data:
        if key in cameras:
            report_data_to_handle[key] = report_data[key]

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    pdf.setFont('FreeSans', 14)

    for key in report_data_to_handle:
        pdf.drawString(80, 800, f"Site Report: {key}")
        data_frame = [['Source name', "Percentage of entry into the danger zone", "Time of entry", "Responsible"]]
        place = report_data_to_handle[key]
        x = []
        y = []
        for event in place:
            x.append(datetime.fromtimestamp(event['date']).strftime('%m-%d-%H:%M:%S'))
            y.append(event['intersection_percent'])
            data_frame.append([
                key,
                event['intersection_percent'],
                datetime.fromtimestamp(event['date']).strftime('%m-%d-%H:%M:%S'),
                event['responsible']
            ])

        plt.plot(x, y, color='green')
        plt.xlabel('Дата')  # Подпись для оси х
        num_ticks = 5
        if len(x) < num_ticks:
            step = 1
        else:
            step = len(x) // num_ticks
        plt.xticks(x[::step])
        plt.ylabel('Процент вхождения')  # Подпись для оси y
        plt.savefig('plot.png')
        pdf.drawInlineImage('plot.png', x=5, y=300)
        table = Table(data_frame)
        table_width, table_height = table.wrap(0, 0)
        pdf.showPage()
        table.drawOn(pdf, 0, 0)

    pdf.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f'report_{datetime.now().strftime("%d-%m-%y")}.pdf')


if __name__ == '__main__':
    # context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # context.load_cert_chain('cert.pem', 'key.pem')
    app.run(debug=True, port=9090, host='25.47.207.197', threaded=True)
