import os
import nibabel as nib
import numpy as np

def calculate(inputs, targets):
    """
    return:
    TP, FP, FN, TN
    """
    TP = (inputs * targets)
    FP = ((1 - targets) * inputs)
    FN = (targets * (1 - inputs))
    TN = (inputs * (1 - inputs))
    return TP, FP, FN, TN

def dice_equation(mask1, mask2):
    inter = float(np.sum((mask1 > 0) * (mask2 > 0)))
    summ = float(np.sum(mask1 > 0) + np.sum(mask2 > 0))
    if summ == 0:
        return 0.0
    dice = 2 * inter / summ
    return dice

def iou_equation(mask1, mask2):
    inter = float(np.sum((mask1 > 0) * (mask2 > 0)))
    summ = float(np.sum(mask1 > 0) + np.sum(mask2 > 0))
    if (summ - inter) == 0:
        return 0.0
    iou = inter / (summ - inter)
    return iou

pred_dir = '/home/x/gt'
mask_dir = '/home/x/pred'
dice_list = []
for file in os.listdir(pred_dir):
    if file in os.listdir(mask_dir):
        pred_nii = nib.load(os.path.join(pred_dir, file))
        pred_data = pred_nii.get_fdata().astype('int64')
        mask_nii = nib.load(os.path.join(mask_dir, file))
        mask_data = mask_nii.get_fdata().astype('int64')
        dice = dice_equation(mask_data, pred_data)
        print(dice)
        dice_list.append(dice)
        # iou = iou_equation(mask_data, pred_data)
        # print(iou)
dice_array = np.array(dice_list)
average_dice = np.sum(dice_array) / len(dice_list)
print('average_dice', average_dice)