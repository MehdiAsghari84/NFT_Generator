import os
import random
import cv2
import moviepy.editor as mp
from console_progressbar import ProgressBar
import uuid
from datetime import date
import json

Total_frame = 300
frame_rate = 30
frame_size = (1600,1600)

#Layers
Layer0 = {"Path":"07 - Area - Motion","Position":[0,0],"trait_type":"Background"}
Layer1 = {"Path":"06 - DNA - PNG","Position":[0,0],"trait_type":"DNA"}
Layer2 = {"Path":"05 - Body - PNG","Position":[0,0],"trait_type":"Body"}
Layer3 = {"Path":"02 - Head - PNG","Position":[0,0],"trait_type":"Head"}
Layer4 = {"Path":"04 - Eyes","Position":[0,0],"trait_type":"Eye"}
Layer5 = {"Path":"03 - Accessories - PNG","Position":[0,0],"trait_type":"Accessory"}
Layer6 = {"Path":"01 - Action - Motion","Position":[0,0],"trait_type":"Action"}

Layer0["Samples"] = len(os.listdir(Layer0["Path"]))
Layer1["Samples"] = len(os.listdir(Layer1["Path"]))
Layer2["Samples"] = len(os.listdir(Layer2["Path"]))
Layer3["Samples"] = len(os.listdir(Layer3["Path"]))
Layer4["Samples"] = len(os.listdir(Layer4["Path"]))
Layer5["Samples"] = len(os.listdir(Layer5["Path"]))
Layer6["Samples"] = len(os.listdir(Layer6["Path"]))

layers = [Layer0,Layer1,Layer2,Layer3,Layer4,Layer5,Layer6]

# calculate total states
selection = []

total_choice = Layer0["Samples"] * Layer1["Samples"] * Layer2["Samples"] * Layer3["Samples"] * Layer4["Samples"] * Layer5["Samples"] * Layer6["Samples"]
print("Total number of states is:",total_choice)
product_count = int(input("Please Enter the number of products:"))


def generate_selection():
    choice = []
    for i in range(len(layers)):
        choice.append(random.randint(1, layers[i]["Samples"])-1)
    
    if choice not in selection:
        return choice
    else: generate_selection()

# make clip by selection
def make_movie(frame,clipNo):
    parent_dir = "output/"
    output_path = os.path.join(parent_dir, str(clipNo))
    os.mkdir(output_path)
    fn = os.path.dirname(output_path) + '/' + str(clipNo) + '/Clip.MP4'
    clip = cv2.VideoWriter(fn,cv2.VideoWriter_fourcc(*'mp4v'), 30, frame_size)
    for m in range(Total_frame):
        
        pb1 = ProgressBar(total=100,prefix='clip', suffix='Now', decimals=3, length=50, fill='X', zfill='-')
        current_frame = m
        percent = (current_frame/Total_frame) * 100
        pb1.print_progress_bar(percent)

        f = loadframe(frame,m)

        #creat picture
        if (m==0):
            crop_img = f[0:1080, 260:1340]
            crop_path = os.path.dirname(output_path) + '/' + str(i) + '/pic.jpg'                        
            cv2.imwrite(crop_path, crop_img)

        clip.write(f)
    return fn

# make frame paste layers
def loadframe(frame,frameNo):
    # paste layers
    for k in range(len(frame)):
        img_select = os.path.join(layers[k]["Path"],os.listdir(layers[k]["Path"])[frame[k]])
        img = loadimage(img_select,frameNo)
        if(k==0):
            frame_img = img
        else:
            frame_img = paste(frame_img,img)
    return frame_img

# load images
def loadimage(path,frameNo):
    if(os.path.isdir(path)):
        img_path = os.path.join(path,os.listdir(path)[frameNo])
        image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    else:
        image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    
    return image

# paste two image
def paste(img1,img2):
    image1 = img1.copy()
    image1 = image1[:,:,:3]
    image2 = img2.copy()
    x1, y1, x2, y2 = 0, 0, image2.shape[1], image2.shape[0]
    image1[y1:y2, x1:x2] = image1[y1:y2, x1:x2] * (1 - image2[:, :, 3:] / 255) + image2[:, :, :3] * (image2[:, :, 3:] / 255)                                   
  
    return image1

# add sound on video
def add_sound(video_no_audio):  
    audio = mp.AudioFileClip("Sound 3D MPCP3.mp3")
    video = mp.VideoFileClip(video_no_audio)
    final = video.set_audio(audio)
    dir_path = os.path.dirname(video_no_audio)
    fn = dir_path + "/final_clip.mp4"
    final.write_videofile(fn)

# generate json file
def generate_json(NFT,video_path):
    dir_path = os.path.dirname(video_path)
    attr =[]
    json_dic = {}
    json_dic["name"] = "NFT"
    json_dic["description"] = "Pingo NFT"
    json_dic["image"] = dir_path + "/pic.jpg"
    json_dic["dna"] = str(uuid.uuid1())
    json_dic["edition"] = "1"
    json_dic["date"] = str(date.today())

    for q in range(len(layers)):
        att ={}
        att["trait_type"] = layers[q]["trait_type"]
        att["value"] = os.listdir(layers[q]["Path"])[NFT[q]]
        attr.append(att.copy())

    json_dic["attributes"] = attr

    jfn = dir_path + "/data.json"
    with open(jfn, 'w') as fp:
        json.dump(json_dic, fp)



# main 
for i in range(product_count):
    choice = generate_selection()
    clip = make_movie(choice,i)
    add_sound(clip)
    generate_json(choice,clip)
    selection.append(choice)



    

