import cv2
import os

# folder_to_save = "marked_data"
folder_to_save = "pure_data"
FPS = 1

cur_dir = f'D:/dataset/cameras/'
items = ['DpR-Csp-uipv-ShV-V1', 'Pgp-com2-K-1-0-9-36', 'Pgp-lpc2-K-0-1-38', 'Phl-com3-Shv2-9-K34', 'Php-Angc-K3-1', 'Php-Angc-K3-8', 'Php-Ctm-K-1-12-56', 'Php-Ctm-Shv1-2-K3', 'Php-nta4-shv016309-k2-1-7', 'Spp-210-K1-3-3-5', 'Spp-210-K1-3-3-6', 'Spp-K1-1-2-6']
items = ['Spp-K1-1-2-6']

for item in items:
    cur_folder = item
    if os.path.isdir(f'{cur_dir}/{item}'):
        print(cur_folder)
        image_folder = f'D:/dataset/cameras/{cur_folder}'
        video_name = f'{folder_to_save}/{cur_folder}.avi'

        images = [img for img in os.listdir(image_folder) if img.lower().endswith(".jpg")] + \
                 [img for img in os.listdir(image_folder) if img.lower().endswith(".png")]
        peoples = [people for people in os.listdir(image_folder) if people.endswith(".txt")]

        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape

        video = cv2.VideoWriter(video_name, 0, FPS, (width, height))
        os.chdir(image_folder)
        for i in range(len(images)):
            if images[i].lower().endswith('.png'):
                #print(os.chdir(f"{image_folder}/{images[i].split('.')[0]}.Png"))
                img = cv2.imread(f"{images[i]}")
            else:
                img = cv2.imread(f"{images[i]}")
            img_height, img_width = img.shape[:2]
            """with open(os.path.join(image_folder, peoples[i])) as f:
                temp = f.readlines()
                marking = []
                if len(temp) > 0:
                    for line in temp:
                        marking.append(list(map(float, line.split())))

            for i in range(len(marking)):
                object_class = marking[i][0]
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

                cv2.rectangle(img, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 255, 0), 2)

                # cv2.imshow('graycsale image', img)
                # print(images[i])
                # cv2.waitKey(0)"""

            video.write(img)
        print(video_name)
        cv2.destroyAllWindows()
        video.release()
