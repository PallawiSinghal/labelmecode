import os
import cv2
import json
font = cv2.FONT_HERSHEY_SIMPLEX
labelme_img_json_folder = "/code/data/labelmeimagejson/"
output_folder = "/code/data/output/"
image_extension = ".png"


if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    
list_data = os.listdir(labelme_img_json_folder)

def read_labelmejson(json_filepath):
    json_data = open(json_filepath)
    loaded_data = json.load(json_data)
    lableme_keys= loaded_data.keys()
    return loaded_data["shapes"]
               
def draw_rectangle_box_on_image(bounding_box,image_data): 
    top_left_xy = bounding_box[0]
    bottom_right_xy = bounding_box[1]
    cv2.rectangle(image_data,(top_left_xy[0],top_left_xy[1]),(bottom_right_xy[0],bottom_right_xy[1]),(0,255,0),3)
    cv2.circle(image_data,(top_left_xy[0],top_left_xy[1]), 15, (255,0,0), -1)
    cv2.circle(image_data,(bottom_right_xy[0],bottom_right_xy[1]), 15, (0,0,255), -1)
    cv2.putText(image_data,'topleft',(top_left_xy[0],top_left_xy[1]), font, 2,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(image_data,'bottomright',(bottom_right_xy[0],bottom_right_xy[1]), font, 2,(255,255,255),2,cv2.LINE_AA)
    return image_data

def calculate_rectangle_box_dimension(bounding_box):
    top_left_xy = bounding_box[0]
    bottom_right_xy = bounding_box[1]
    #height and width of box
    width_bounding_box = bottom_right_xy[0] - top_left_xy[0]#x2-x1
    height_bounding_box = bottom_right_xy[1] - top_left_xy[1]#y2-y1
    dimension = [height_bounding_box,width_bounding_box]
    if any(m < 0 for m in dimension):#height<width
        height_bounding_box = top_left_xy[1] - bottom_right_xy[1]#y1-y2
        width_bounding_box = bottom_right_xy[0] - top_left_xy[0]#x2-x1
    return height_bounding_box,width_bounding_box
  
for i in list_data:
    if i.endswith(".json"):
        json_filepath = labelme_img_json_folder + i
        image_filepath = labelme_img_json_folder + i.split(".")[0] + image_extension
        annotations = read_labelmejson(json_filepath)
        image_data = cv2.imread(image_filepath)
        for each_annotation in annotations:
            bounding_box = each_annotation["points"]
            height_bounding_box,width_bounding_box = calculate_rectangle_box_dimension(bounding_box)
            print("height_bounding_box",height_bounding_box,"width_bounding_box",width_bounding_box)
            image_data = draw_rectangle_box_on_image(bounding_box,image_data)
        output_image = output_folder + i.split(".")[0] + image_extension
        print(output_image)
        cv2.imwrite(output_image,image_data)
