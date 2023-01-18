from __future__ import print_function, division

import torch
import torch.utils as utils
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
from PIL import Image

from torch.optim import lr_scheduler
import torch.backends.cudnn as cudnn
import numpy as np
import pandas as pd
import torchvision
from tqdm import tqdm
from torchvision import datasets, models, transforms
from torchvision.transforms import ToTensor, ToPILImage
import matplotlib.pyplot as plt
import time
import os
import copy

from torchvision.transforms import ToTensor
tf_toTensor = ToTensor() 

class_names = ['기타',
 '레트로',
 '로맨틱',
 '리조트',
 '매니시',
 '모던',
 '밀리터리',
 '섹시',
 '소피스트케이티드',
 '스트리트',
 '스포티',
 '아방가르드',
 '오리엔탈',
 '웨스턴',
 '젠더리스',
 '컨트리',
 '클래식',
 '키치',
 '톰보이',
 '펑크',
 '페미닌',
 '프레피',
 '히피',
 '힙합']


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def predict_style(image_path, MODEL_PATH, device='cpu'):
    """
    
    image_path: image_path image (어떤형식으로 들어오는지 모르겠다...)
    MODEL_PATH: model 경로
    device: cpu
    class_names: 스타일 종류

    """

    img = Image.open(image_path)
    img = img.resize((224, 224))
    tensor_img = tf_toTensor(img)
    tensor_img = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])(tensor_img)
    tensor_img = torch.reshape(tensor_img, [-1, 3, 224, 224])

    model = torch.load(MODEL_PATH, map_location=device)
    model_pr = model.eval()

    pred = model_pr(tensor_img).argmax()
    pred_style = class_names[pred]
    print(pred_style)
    return pred_style
