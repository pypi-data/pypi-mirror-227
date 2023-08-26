import cv2,numpy as np
from PIL import Image
import keras_ocr

coords=[]

def cords(input_image_path):
    pipeline = keras_ocr.pipeline.Pipeline()
    image = keras_ocr.tools.read(input_image_path)
    prediction_groups = pipeline.recognize([image])
    # print image with annotation and boxes
    keras_ocr.tools.drawAnnotations(image=image, predictions=prediction_groups[0])
    # Load the existing image
    image=cv2.imread(input_image_path)
    # Get the dimensions of the existing image
    height, width, _ = image.shape
    # Create a black image with the same dimensions as the existing image
    black_image = np.zeros((height, width, 3), dtype=np.uint8)
    img = cv2.imread(input_image_path)

    for predictions in prediction_groups:
        for word, boundary_coords in predictions:
            # Check if all boundary coordinates are same colored pixels
            image=Image.open(input_image_path)
            first_color = image.getpixel((int(boundary_coords[0][0]), int(boundary_coords[0][1])))
            are_all_same_color = all(image.getpixel((int(x), int(y))) == first_color for x, y in boundary_coords)
            if are_all_same_color:
                start_point = (int(boundary_coords[0][0]), int(boundary_coords[0][1]))
                end_point = (int(boundary_coords[2][0]), int(boundary_coords[2][1]))
                thickness = -1
                img = cv2.rectangle(img, start_point, end_point, first_color, thickness)
                black_image = cv2.rectangle(black_image, start_point, end_point, first_color, thickness)
            
            else:
                x1, y1 = boundary_coords[0]
                x2, y2 = boundary_coords[1]
                x3, y3 = boundary_coords[2]
                x4, y4 = boundary_coords[3]
                # Find the minimum and maximum x and y values
                min_x = int(min(x1, x2, x3, x4))
                max_x = int(max(x1, x2, x3, x4))
                min_y = int(min(y1, y2, y3, y4))
                max_y = int(max(y1, y2, y3, y4))

                for x in range(min_x, max_x + 1):
                    for y in range(min_y, max_y + 1):
                        coords.append((x, y))
    return img,black_image

def draw(input_image_path,p,threshold,img,black_image):
    image= cv2.imread(input_image_path)
    for coord in coords:
        x, y = coord
        try : 
            pixel_intensity = np.mean(image[y, x])
            if all(image[y, x] == [0,0,0]) or pixel_intensity < threshold:
                img[y, x] = [255, 255, 255]
                black_image[y, x] = [255, 255, 255]
                for dx in range(-p,p):
                    for dy in range(-p, p):
                        if dx == 0 and dy == 0:
                            continue  # Skip the current pixel
                        new_x, new_y = x + dx, y + dy
                        img[new_y, new_x] = [255, 255, 255]
                        black_image[new_y, new_x] = [255, 255, 255]
        except IndexError: pass
    return img,black_image

def txt(input_image_path,pixels,threshold):
    
    img,black_image=cords(input_image_path)
    img,black_image=draw(input_image_path,pixels,threshold,img,black_image)
    mask_image = cv2.cvtColor(black_image, cv2.COLOR_BGR2GRAY)
    return img,mask_image