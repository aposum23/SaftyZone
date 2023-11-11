import cv2
import numpy as np
from db_functions import read_db, write_db
from shapely.geometry import Polygon
import os

yolo_net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
# ssd_net = cv2.dnn.readNetFromCaffe('ssd.prototxt', 'ssd.caffemodel')
with open('ssd_classes.txt', 'r') as f:
    classes = f.read().splitlines()


def get_mask_by_filename(file_name: str):
    data = read_db()
    frame_data = data.get(file_name)
    if frame_data is not None:
        mask = np.array(frame_data.get('mask'))
        return mask


def add_mask(frame: np.ndarray, file_name: str):
    data = read_db()
    frame_data = data.get(file_name)
    if frame_data is not None:
        color = frame_data.get('color')
        mask = np.array(frame_data.get('mask'))
        if color is not None:
            cv2.polylines(frame, [mask], isClosed=True, color=color, thickness=2)


def calculate_intersection_percent(rectangle_points, polygon_points):
    rectangle = Polygon(rectangle_points)
    polygon = Polygon(polygon_points)
    # Найдите пересечение между прямоугольником и многогранником
    intersection = rectangle.intersection(polygon)
    # Проверьте, является ли пересечение пустым
    if intersection.is_empty:
        return 0.0

    # Верните площадь пересечения
    return intersection.area / rectangle.area * 100


def crutch_function(frame_number, file_name):
    frame_number -= 1
    folder_name = file_name.split('.')[0]
    image_folder = f'D:/dataset/cameras/{folder_name}'
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")] + \
             [img for img in os.listdir(image_folder) if img.endswith(".Png")]
    peoples = [people for people in os.listdir(image_folder) if people.endswith(".txt")]
    cur_frame_markup = peoples[frame_number]
    img = cv2.imread(os.path.join(image_folder, f"{images[frame_number]}"))
    img_height, img_width = img.shape[:2]

    with open(os.path.join(image_folder, cur_frame_markup)) as f:
        temp = f.readlines()
        marking = []
        if len(temp) > 0:
            for line in temp:
                marking.append(list(map(float, line.split())))
    intersections = []
    for i in range(len(marking)):
        x = marking[i][1]
        y = marking[i][2]
        width = marking[i][3]
        height = marking[i][4]
        center_x = int(x * img_width)
        center_y = int(y * img_height)
        rectangle_width = int(width * img_width)
        rectangle_height = int(height * img_height)
        top_left_x = center_x - int(rectangle_width / 2)
        top_left_y = center_y - int(rectangle_height / 2)
        bottom_right_x = center_x + int(rectangle_width / 2)
        bottom_right_y = center_y + int(rectangle_height / 2)
        rectangle_points = [
            (top_left_x, bottom_right_y),
            (top_left_x, top_left_y),
            (bottom_right_x, top_left_y),
            (bottom_right_x, bottom_right_y)
        ]  # Координаты вершин прямоугольника
        polygon_points = get_mask_by_filename(file_name)  # Координаты вершин многогранника
        data = read_db()
        frame_data = data.get(file_name)
        if frame_data is not None:
            intersection_percent = calculate_intersection_percent(rectangle_points, polygon_points)
            intersections.append(intersection_percent)
    if len(intersections) > 0:
        return max(intersections)
    else:
        return 0


def find_person(image: np.ndarray):

    result = []
    (height, width) = image.shape[:2]
    ln = yolo_net.getLayerNames()
    ln = [ln[i - 1] for i in yolo_net.getUnconnectedOutLayers()]
    blob = cv2.dnn.blobFromImage(image, 1 / 255, (416, 416),
                                 swapRB=True, crop=False)
    yolo_net.setInput(blob)
    # Выполните прямой проход через модель YOLO
    outputs = yolo_net.forward(ln)

    # Инициализируйте списки для обнаруженных объектов
    boxes = []
    confidences = []
    class_ids = []
    # Проанализируйте выходные данные модели YOLO
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            # Отфильтруйте обнаруженные объекты, оставив только людей
            if classes[class_id] == 'person' and confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Вычислите координаты верхнего левого угла прямоугольника
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Добавьте координаты, уверенность и идентификатор класса в соответствующие списки
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            # draw a bounding box rectangle and label on the image
            color = [0, 255, 0]
            result.append(((x, y), (x + w, y + h)))
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
    return result
