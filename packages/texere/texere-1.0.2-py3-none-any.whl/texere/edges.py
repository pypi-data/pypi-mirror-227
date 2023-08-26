import numpy as np
from math import sqrt
from PIL import Image,ImageDraw

def mark(input_image_path,threshold):
    input_image= Image.open(input_image_path)
    input_pixels = input_image.load()
    width,height= input_image.width,input_image.height

    output_image = Image.new("RGB",input_image.size)
    draw= ImageDraw.Draw(output_image)

    #converting to gray_scale
    intensity= np.zeros((width,height))
    for x in range (width):
        for y in range(height):
            intensity[x,y]= sum(input_pixels[x,y])/3

    #computing convolution between intensity and kernels
    for x in range (1,input_image.width-1):
        for y in range(1,input_image.height-1):
            magx= intensity[x+1,y]- intensity[x-1,y]
            magy= intensity[x,y+1]- intensity[x,y-1]

            #drwing in black amd white the magnitude
            color= int(sqrt(magx**2+ magy**2))
            #let mess with it
            if threshold!=None and color > threshold : color = 255
            elif threshold!=None : color = 0 #perfect for this, lets try another image 
            draw.point((x,y),(color,color,color))
    return output_image