import os
import argparse
import time


def log_deleted(path, log_filename='clean_trash.log'):
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_file.write(f"{path}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--trash_folder_path', required=True)
    parser.add_argument('--age_thr', type=float, required=True)
    args = parser.parse_args()

    trash_path = os.path.abspath(args.trash_folder_path)
    if os.path.isdir(trash_path):
        try:
            while True:
                current_time = time.time()
                for root, dirs, files in os.walk(trash_path, topdown=False):
                    for filename in files:
                        f_path = os.path.join(root, filename)
                        try:
                            if not os.path.exists(f_path):
                                continue
                            mtime = os.path.getmtime(f_path)
                            if current_time - mtime > args.age_thr:
                                os.remove(f_path)
                                log_deleted(f_path)
                        except Exception:
                            pass
                    if root != trash_path:
                        try:
                            if not os.listdir(root):
                                os.rmdir(root)
                                log_deleted(root)
                        except Exception:
                            pass

                time.sleep(1)
        except Exception:
            pass
