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

#사진 기반 스타일 예측
def predict_style(image_path, MODEL_PATH, device='cpu'):
    """
    
    image_path: image_path 
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

#스타일 기반 인플루언서 추천(제조자)
def recomm_inf_sup(CSV_PATH, gender, size, style):
    """
    
    CSV_PATH: 인플루언서 정보 csv 파일 불러오기(제조사추천용)
    gender: 사용자가 원하는 인플루언서의 성별
    size: 사용자가 원하는 인플루언서의 체구
    style: predict_style 함수에서 predict된 input image의 스타일

    """

    # 제조사추천용 인플루언서 csv 파일 불러오기
    inf_post_info = pd.read_csv(CSV_PATH)

    # 사용자가 입력한 정보대로 인플루언서 필터링
    inf_post_info = inf_post_info[inf_post_info['gender'] == gender]
    inf_post_info = inf_post_info[inf_post_info['size'] == size]
    # 사용자가 입력한 이미지의 style(모델로 예측됨)로 인플루언서 필터링
    inf_post_info = inf_post_info[inf_post_info['inf_style'] == style]

    # 좋아요 수로 인플루언서 정렬
    inf_post_info = inf_post_info.sort_values('likes', ascending = False) # 제조사가 원하는 스타일에 대해 영향력이 큰 인플루언서 순서대로 나타남

    recomm_inf_ids = inf_post_info['user_name'][:2]
    recomm_inf_imgs = inf_post_info['post_id'][:2]

    return recomm_inf_ids, recomm_inf_imgs

#스타일 기반 인플루언서 추천(소비자)
def recomm_inf_cust(CSV_PATH, gender, size, style):
    """
    
    CSV_PATH: 인플루언서 정보 csv 파일 불러오기(소비자추천용)
    gender: 사용자가 원하는 인플루언서의 성별
    size: 사용자가 원하는 인플루언서의 체구
    style: predict_style 함수에서 predict된 input image의 스타일

    """

    # 소비자추천용 인플루언서 csv 파일 불러오기
    inf_post_info = pd.read_csv(CSV_PATH)

    # 사용자가 입력한 정보대로 인플루언서 필터링
    inf_post_info = inf_post_info[inf_post_info['gender'] == gender]
    inf_post_info = inf_post_info[inf_post_info['size'] == size]
    # 사용자가 입력한 이미지의 style(모델로 예측됨)로 인플루언서 필터링
    inf_post_info = inf_post_info[inf_post_info['inf_style'] == style]

    # 스타일 등장 피드 개수로 인플루언서 정렬
    inf_post_info = inf_post_info.sort_values('count', ascending = False) # 소비자가 원하는 피드가 많은 인플루언서 순서대로 나타남

    recomm_inf_ids = inf_post_info['user_name'][:2]
    recomm_inf_imgs = inf_post_info['post_id'][:2]

    return recomm_inf_ids, recomm_inf_imgs