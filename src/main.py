import os
from shutil import rmtree, copy

def copy_process():
    working = os.getcwd()
    public_dir = os.path.join(working, "public")
    static_dir = os.path.join(working, "static")

    if os.path.exists(public_dir):
        rmtree(public_dir)
    os.mkdir(public_dir)

    copy_to_public(static_dir, public_dir, "")

def copy_to_public(static_dir, public_dir, folder_relative):
    cur_dir_s = os.path.join(static_dir, folder_relative)
    cur_dir_p = os.path.join(public_dir, folder_relative)

    for item in os.listdir(cur_dir_s):
        path_in_static = os.path.join(cur_dir_s, item)
        if os.path.isfile(path_in_static):
            copy(path_in_static, cur_dir_p)
        else:
            path_in_public = os.path.join(cur_dir_p, item)
            os.mkdir(path_in_public)
            extended_path = os.path.join(folder_relative, item)
            copy_to_public(static_dir, public_dir, extended_path)

def main():
    copy_process()

if __name__ == "__main__":
    main()