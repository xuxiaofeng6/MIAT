import os
import random
import shutil

def split_segmentation():
    data_dir = "/path/to/data"
    train_dir = "/path/to/train"
    val_dir = "/path/to/val"
    split_ratio = 0.8  # 指定训练集与验证集的划分比例

    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(val_dir):
        os.makedirs(val_dir)

    img_dir = os.path.join(data_dir, "img")
    label_dir = os.path.join(data_dir, "gt")

    img_files = os.listdir(img_dir)
    num_files = len(img_files)
    random.shuffle(img_files)

    # 将数据集分成训练集和验证集
    num_train = int(num_files * split_ratio)
    train_files = img_files[:num_train]
    val_files = img_files[num_train:]

    for filename in train_files:
        src_img_path = os.path.join(img_dir, filename)
        src_label_path = os.path.join(label_dir, filename)
        dst_img_path = os.path.join(train_dir, filename)
        dst_label_path = os.path.join(train_dir, filename)
        shutil.copy(src_img_path, dst_img_path)
        shutil.copy(src_label_path, dst_label_path)

    for filename in val_files:
        src_img_path = os.path.join(img_dir, filename)
        src_label_path = os.path.join(label_dir, filename)
        dst_img_path = os.path.join(val_dir, filename)
        dst_label_path = os.path.join(val_dir, filename)
        shutil.copy(src_img_path, dst_img_path)
        shutil.copy(src_label_path, dst_label_path)

def split_classification():
    # 设置随机种子，确保每次划分的结果相同
    random.seed(42)

    # 原始数据文件夹路径
    data_dir =

    # 训练集和验证集文件夹路径
    train_dir =
    val_dir =

    # 划分比例
    train_ratio = 0.8

    # 遍历每个类别文件夹
    for label in ['label_0', 'label_1']:
        # 获取所有样本文件名列表
        files = os.listdir(os.path.join(data_dir, label))
        # 打乱顺序
        random.shuffle(files)
        # 计算划分点
        split_idx = int(len(files) * train_ratio)
        # 划分为训练集和验证集
        train_files = files[:split_idx]
        val_files = files[split_idx:]
        # 将训练集和验证集文件夹分别创建在对应的文件夹下
        os.makedirs(os.path.join(train_dir, label), exist_ok=True)
        os.makedirs(os.path.join(val_dir, label), exist_ok=True)
        # 复制文件到对应的文件夹下
        for file in train_files:
            src = os.path.join(data_dir, label, file)
            dst = os.path.join(train_dir, label, file)
            shutil.copy(src, dst)
        for file in val_files:
            src = os.path.join(data_dir, label, file)
            dst = os.path.join(val_dir, label, file)
            shutil.copy(src, dst)

split_classification()