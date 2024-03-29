import glob
import os


class Address_Selection:
    def __init__(self, address_path):
        self.address_path = address_path

    def get_file_name(self):
        # 获取文件路径上的文件名
        return os.path.basename(self.address_path)
