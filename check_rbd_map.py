#!/usr/bin/python
import os
import re
import sys

PATH_CONFIG_FILE = '/etc/ceph/rbdmap'
PATH_RBD_IMAGES = '/dev/rbd'
EXIT_OK = 0
EXIT_WARN = 1
EXIT_CRITICAL = 2


def create_pools(path):
    pools = []
    with open(path, "r") as file:
        for line in file:
            if "#" in line:
                continue
            else:
                if re.search(r'\w', line):
                    image = re.split(r' ', line, maxsplit=1)
                    pools.append(image[0])
    return pools


def check_files(pools):
    is_ok = True
    not_mapped_images = 'Not mapped: '
    pointer_not_mapped_images = 0
    for image in pools:
        full_path_to_image = PATH_RBD_IMAGES + '/' + image
        if not os.path.exists(full_path_to_image):
            is_ok = False
            pointer_not_mapped_images += 1
            not_mapped_images += (str(pointer_not_mapped_images) + ') ' + image + ' ')
    if is_ok:
        print('OK. All images are mapped.')
        sys.exit(EXIT_OK)
    else:
        print(not_mapped_images)
        sys.exit(EXIT_CRITICAL)


def main():
    try:
        pools = create_pools(PATH_CONFIG_FILE)
    except:
        print("Warning! File cannot be opened or it doesn't exist")
        sys.exit(EXIT_WARN)
    if len(pools) == 0:
        print('Warning! Not images in %s' % PATH_CONFIG_FILE)
        sys.exit(EXIT_WARN)
    else:
        check_files(pools)


if __name__ == '__main__':
    main()