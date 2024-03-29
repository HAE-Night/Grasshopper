import os

# x = "Fabric"
# print(x.strip())
# print(x.replace(" ", "").replace("\n", "").upper())
#


if __name__ == '__main__':
    save_path = r"phone"
    print(os.path.exists(save_path))
    if not os.path.exists(save_path):
        print("ttt")
        os.mkdir(save_path)  # 创建文件夹
