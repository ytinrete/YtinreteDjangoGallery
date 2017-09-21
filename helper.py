import os
import shutil


def construct_photo_structure():
    structure_src = 'I:/Collections/videos'
    structure_dist = 'C:/Users/ytinrete/Desktop/download/test/videos'

    if os.path.exists(structure_dist):
        shutil.rmtree(structure_dist)

    # os.makedirs(structure_dist)
    count = 1

    print('begin')

    def ignore_files(dir, files):
        ignore = []
        for file in files:
            if os.path.isfile(dir + '/' + file) and not str(file).endswith('.jpg'):
                ignore.append(file)
        return ignore

    shutil.copytree(structure_src, structure_dist, ignore=ignore_files)
    print('end')

    return


def check():
    count = 0
    structure_src = 'I:/Collections/videos/movies'
    for root, dirs, files in os.walk(structure_src):
        if root.find("MicroMsg")>0:
            continue
        for name in files:
            #print("name:" + root + '/' + name)

            if(not (name.endswith("jpg")or  name.lower().endswith("avi")or
                   name.lower().endswith("mp4") or name.lower().endswith("rmvb")
                    or name.lower().endswith("wmv")or name.lower().endswith("mkv"))):
                print("name:" + root + '/' + name)
                count +=1

            # if(name == ".DS_Store" or name =="Thumbs.db"):
            #     os.remove(root + '/' + name)
            #     pass
            # if os.path.isfile(root + '/' + name):
            #     if not name.find('%') == -1:
                    # print("find:" + name)
                    # new_name = name.replace('%', '_')
                    # print(new_name)

    print(count)
    pass


if __name__ == '__main__':
    construct_photo_structure()
    # check()