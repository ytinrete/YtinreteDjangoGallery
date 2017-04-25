from subprocess import call
import os
import shutil
import YtinreteDjangoGallery.configs


# call(["ls", "-l"])


def load_from_data_txt():
    # call(['cp', '/Users/lirui/Desktop/testPic/Vocaloid/_world_is_mine__miku_by_celestialvalkyrie-d2ywz5d.jpg'
    #       ,'/Users/lirui/Desktop/testPic/aaa.jpg'])

    # print(os.listdir('/Volumes/data/Collections/videos/movies'))

    # shutil.move('/Users/lirui/Desktop/testPic/Vocaloid/123  4567.jpg', '/Users/lirui/Desktop/testPic/abc.jpg')

    data = []

    with open('have.txt', 'r', encoding='GBK') as f:
        data_list = f.readlines()

        # data_str = f.readline()
        # try:
        #     while ''!=data_str:
        #         data_str = f.readline()
        #         print(data_str)
        # except IOError as e:
        #     print(str(e))

    data_list = data_list[1:]

    index = 0

    while index < len(data_list):
        group = data_list[index][:-1]
        index += 1
        count = int(data_list[index])
        end = index + count
        while index < end:
            index += 1
            block = []
            block.append(group)  # 0 group
            block.append(data_list[index].split(',')[-1][:-1])  # 1 path
            block.append(data_list[index].split(',')[0])  # 2 number name-front
            details_str = data_list[index].split(',')[-1][:-1].split('/')
            block.append(details_str[-1])  # 3 jpg name
            block.append(block[2] + '_' + details_str[-1].replace(' ', '_'))  # 4 new jpg name
            block.append(details_str[1])  # 5 101

            find_name = details_str[-1][0:details_str[-1].rindex('.')]
            if find_name.find('_thumbs_') != -1:
                find_name = find_name[0:find_name.find('_thumbs_')]
            block.append(find_name)  # 6compare name
            block.append(details_str[-1].split('.')[-1])  # 7 jpg
            data.append(block)
        index += 1

    print('ok')

    movie_src = '/Volumes/data/Collections/videos/movie/'
    index_src = '/Volumes/data/Collections/videos/'
    movie_dist = '/Volumes/data/Collections/videos/movies'

    # test
    for block in data:
        src_picture_path = index_src + block[1]
        if os.path.exists(src_picture_path):
            print('a:' + src_picture_path)

            if not os.path.exists(movie_dist + '/' + block[0]):
                os.makedirs(movie_dist + '/' + block[0])

            if not os.path.exists(movie_dist + '/' + block[0] + '/' + block[4]):
                shutil.copy(src_picture_path, movie_dist + '/' + block[0] + '/' + block[4])
                print('copy pic:' + src_picture_path)
            else:
                print('have pic:' + movie_dist + '/' + block[0] + '/' + block[4])

            move_movie_Fail = True
            src_movie_root = movie_src + block[5]
            if os.path.exists(src_movie_root):
                for sub_file in os.listdir(src_movie_root):
                    if len(sub_file) >= len(block[6]) and len(sub_file) >= len(block[7]) and sub_file.find(
                            block[6]) != -1 and not sub_file.endswith(block[7]):
                        src_movie_path = src_movie_root + '/' + sub_file
                        print('b:' + src_movie_path)

                        movie_tail = sub_file.split('.')[-1]
                        if not os.path.exists(movie_dist + '/' + block[0] + '/' + block[4] + '.' + movie_tail):
                            shutil.move(src_movie_path, movie_dist + '/' + block[0] + '/' + block[4] + '.' + movie_tail)
                            print('move movie:' + src_movie_path)
                        else:
                            print('have movie:' + movie_dist + '/' + block[0] + '/' + block[4] + '.' + movie_tail)

                        move_movie_Fail = False
                        break
            else:
                print('error 2')

            if move_movie_Fail:
                print('---fail!:' + src_picture_path)

        else:
            print('error 1')


def move_from_exist():
    movie_src = '/Volumes/data/Collections/videos/movie'
    index_src = '/Volumes/data/Collections/videos/index/'
    movie_dist = '/Volumes/data/Collections/videos/movies'

    for index in os.listdir(movie_src):
        if index.startswith('.'):
            break
        count = len(os.listdir(movie_src + '/' + index))

        if count > 0:
            for movie_name in os.listdir(movie_src + '/' + index):
                if not movie_name.endswith('jpg') and not movie_name.endswith('png') and not movie_name.startswith(
                        '.') and movie_name.find('480') == -1 and movie_name.find('720') == -1 and movie_name.find(
                    '240') == -1:
                    src_movie_path = movie_src + '/' + index + '/' + movie_name
                    print('b:' + src_movie_path)

                    if os.path.exists(index_src + index) and len(os.listdir(index_src + index)) > 0:
                        for pic_name in os.listdir(index_src + index):
                            if pic_name.find(movie_name) != -1:
                                src_picture_path = index_src + index + '/' + pic_name
                                print('a:' + src_picture_path)
                                print('enter number:')
                                number = input()
                                if '0' != number and '' != number:
                                    print('enter group:')
                                    group = input()
                                    print('_' + group + '-' + number + '_ sure y/n?')
                                    ans = input()
                                    if 'y' == ans:

                                        dist_path = movie_dist + '/' + group
                                        dist_pic_name = number + '_' + pic_name
                                        dist_movie_name = dist_pic_name + '.' + movie_name.split('.')[-1]

                                        if not os.path.exists(dist_path):
                                            os.makedirs(dist_path)

                                        if not os.path.exists(dist_path + '/' + dist_pic_name):
                                            shutil.copy(src_picture_path, dist_path + '/' + dist_pic_name)
                                            print('copy pic:' + src_picture_path)
                                        else:
                                            print('have pic:' + dist_path + '/' + dist_pic_name)

                                        if not os.path.exists(dist_path + '/' + dist_movie_name):
                                            shutil.move(src_movie_path, dist_path + '/' + dist_movie_name)
                                            print('move movie:' + src_picture_path)
                                        else:
                                            print('have movie:' + dist_path + '/' + dist_movie_name)


def copy_structure_with_pics():
    structure_src = '/Volumes/data/Collections/videos/movies'

    structure_dist = '/Users/lirui/Desktop/movies'

    if not os.path.exists(structure_dist):
        os.makedirs(structure_dist)

    file_kind = {}

    for root, dirs, files in os.walk(structure_src):
        for name in files:
            end = name.split('.')[-1]
            if file_kind.get(end):
                file_kind[end] += 1
            else:
                file_kind[end] = 1

    for k in file_kind:
        print('k:' + k + ' v:' + str(file_kind[k]))

    count = 1
    for group in os.listdir(structure_src):
        if group.startswith('.'):
            continue
        if not os.path.exists(structure_dist + '/' + group):
            os.makedirs(structure_dist + '/' + group)

        for pic in os.listdir(structure_src + '/' + group):
            if pic.endswith('jpg'):
                shutil.copy(structure_src + '/' + group + '/' + pic, structure_dist + '/' + group + '/' + pic)
                count += 1
                print("count:" + str(count))

    pass


def construct_photo_structure():
    structure_src = YtinreteDjangoGallery.configs.PHOTO_SRC_PATH
    structure_dist = YtinreteDjangoGallery.configs.PHOTO_Dist_PATH

    if os.path.exists(structure_dist):
        shutil.rmtree(structure_dist)

    os.makedirs(structure_dist)
    count = 1

    for first in os.listdir(structure_src):
        if first.startswith('.'):
            continue
        if not os.path.exists(structure_dist + '/' + first):
            os.makedirs(structure_dist + '/' + first)

        for group in os.listdir(structure_src + '/' + first):
            if group.startswith('.'):
                continue
            if not os.path.exists(structure_dist + '/' + first + '/' + group):
                os.makedirs(structure_dist + '/' + first + '/' + group)

            for pic in os.listdir(structure_src + '/' + first+ '/' + group):
                if pic.endswith('jpg'):
                    shutil.copy(structure_src+ '/' + first + '/' + group + '/'
                                + pic, structure_dist+ '/' + first + '/' + group + '/' + pic)
                    count += 1
                    print("count:" + str(count))


if __name__ == '__main__':
    # load_from_data_txt()

    # move_from_exist()

    # copy_structure_with_pics()

    construct_photo_structure()

    pass
