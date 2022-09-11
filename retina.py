#!/usr/bin/env python3

# Requirements:
# sudo apt-get -y install imagemagick

from os import mkdir, rename, walk
from os.path import exists
from subprocess import check_output, STDOUT
from time import gmtime, strftime
from traceback import format_exc


def destination_folder(suffix='.gallery'):
    """
    """

    try:
        clock = strftime('%Y.%m.%d.UTC.%H.%M.%S', gmtime())
        target_dir = clock + suffix

        if not exists(target_dir):
            mkdir(target_dir, mode=0o755)

        return target_dir
    except:
        print(format_exc())


def image_paths(extensions=('gif', 'jpeg', 'jpg', 'png')):
    """
    """

    try:
        targets = []

        for path, _, files in walk('.'):
            tmp = [path + '/' + f for f in files
                   if len({f[-3:].lower(), f[-4:].lower()} & set(extensions)) > 0]
            if len(tmp) > 0:
                targets += tmp

        return sorted(targets)
    except:
        print(format_exc())


def oscar_mike(from_path, to_path, min_pixels=100*100, force_ratio=False, hash_first=True):
    """
    """

    try:
        def to_shell(cmd):
            return check_output(cmd, stderr=STDOUT, shell=True).decode().lower()

        d = '.'
        img_hash = to_shell('md5sum "' + from_path + '" | cut -d\' \' -f1')[:32]
        img_data = to_shell('identify -format "%w'
                            + d + '%h' + d + '%m" "' + from_path + '"')

        img_w, img_h, img_fmt = img_data.split(d)
        assert int(img_w) * int(img_h) >= min_pixels
        if force_ratio:
            assert int(img_w) / int(img_h) <= 2

        img_dim = img_w + 'x' + img_h
        if hash_first:
            mv_params = from_path, to_path + '/' + '.'.join([img_hash, img_dim, img_fmt])
        else:
            mv_params = from_path, to_path + '/' + '.'.join([img_dim, img_hash, img_fmt])

        rename(*mv_params)
        return mv_params

    except AssertionError:
        return from_path, None

    except:
        print(format_exc())


folder = destination_folder()

for img in image_paths():
    print(oscar_mike(img, folder))
