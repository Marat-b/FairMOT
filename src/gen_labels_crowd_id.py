import os.path as osp
import os
import cv2
import json
import numpy as np


def mkdirs(d):
    if not osp.exists(d):
        os.makedirs(d)


def load_func(fpath):
    print('fpath', fpath)
    assert os.path.exists(fpath)
    with open(fpath, 'r') as fid:
        lines = fid.readlines()
    records =[json.loads(line.strip('\n')) for line in lines]
    return records


def gen_labels_crowd(data_root, label_root, ann_root):
    mkdirs(label_root)
    anns_data = load_func(ann_root)

    tid_curr = 0
    for i, ann_data in enumerate(anns_data):
        print(i)
        image_name = '{}.jpg'.format(ann_data['ID'])
        img_path = os.path.join(data_root, image_name)
        anns = ann_data['gtboxes']
        if os.path.exists(img_path):
            img = cv2.imread(
                img_path,
                cv2.IMREAD_COLOR | cv2.IMREAD_IGNORE_ORIENTATION
            )
            img_height, img_width = img.shape[0:2]
            for i in range(len(anns)):
                if 'extra' in anns[i] and 'ignore' in anns[i]['extra'] and anns[i]['extra']['ignore'] == 1:
                    continue
                x, y, w, h = anns[i]['fbox']
                x += w / 2
                y += h / 2
                label_fpath = img_path.replace('images', 'labels_with_ids').replace('.png', '.txt').replace('.jpg', '.txt')
                label_str = '0 {:d} {:.6f} {:.6f} {:.6f} {:.6f}\n'.format(
                    tid_curr, x / img_width, y / img_height, w / img_width, h / img_height)
                with open(label_fpath, 'a') as f:
                    f.write(label_str)
        else:
            print(f'{img_path} does not exists!')
            tid_curr += 1


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Generate png files")
    parser.add_argument(
         "--root_path", dest="root_path",
        help="Root path"
    )
    args = parser.parse_args()
    root_path = args.root_path
    data_val = f'{root_path}/images/val'
    label_val = f'{root_path}/labels_with_ids/val'
    ann_val = f'{root_path}/annotation_val.odgt'
    data_train = f'{root_path}/images/train'
    label_train = f'{root_path}/labels_with_ids/train'
    ann_train = f'{root_path}/annotation_train.odgt'
    gen_labels_crowd(data_train, label_train, ann_train)
    gen_labels_crowd(data_val, label_val, ann_val)


