# 编程内容：PDF合并自动化
# 作者：子夜
# 时间：2022年9月27日 下午5:09
import PyPDF2
import os
import easygui as g


class Name(object):
    # 保存路径和文件名
    def save_name(self, path_name, item_name, end_name):
        all_file = os.listdir(path_name)
        if "PDF Merger" not in all_file:
            os.makedirs(path_name + r"\PDF Merger")
            file_name = r"{}\{}-{}.pdf".format(path_name + r"\PDF Merger", item_name, end_name)
        else:
            file_name = r"{}\{}-{}.pdf".format(path_name + r"\PDF Merger", item_name, end_name)
        return file_name

    # 合并生成pdf
    def PDF_Merger(self, save_path, pdf_lst):
        file_merger = PyPDF2.PdfFileMerger()
        for pdf in pdf_lst:
            # print(pdf)
            file_merger.append(pdf, import_bookmarks=False)
        file_merger.write(save_path)
        file_merger.close()

    def select_file(self):
        direction = g.diropenbox(title="PDF文件夹选择")
        msg = "HEA-PDF合并命名"
        title = "HAE-PY-Night"
        name = g.enterbox(msg, title, "ASSEMBLY&CUTTING LIST", True)
        return direction, name

    # Run
    def File_Run(self):
        paper_file = g.diropenbox(title="PDF文件夹选择")
        Valuelist = g.multenterbox(fields=['文件夹', '文件结尾名'], title="HAE-PY-Night", msg="确认填写信息", values=[paper_file, "ASSEMBLY&CUTTING LIST"])
        paper_file, end_name = Valuelist[0], Valuelist[1]

        print(paper_file)
        if paper_file:
            # 对文件夹进行pdf筛选
            pdf_list = [fe for fe in os.listdir(paper_file) if fe.endswith('.pdf')]
            pdf_lst = [os.path.join(paper_file, filename) for filename in pdf_list]
            floor = list(set(["-".join(i.split("-")[0:-1]) for i in pdf_lst]))

            # 相同楼层的pdf提取分类
            for fr in range(len(floor)):
                i = 0
                Pdf_count2 = []
                while i < len(pdf_lst):
                    if floor[fr] == "-".join(pdf_lst[i].split("-")[:-1]):
                        Pdf_count2.append(pdf_lst[i])
                    i += 1
                save_path = self.save_name(paper_file, floor[fr].split("\\")[-1], end_name)
                self.PDF_Merger(save_path, Pdf_count2)
            g.msgbox(msg="合并已完成！\n文件目录：{}\\PDF Merger".format(paper_file), title="HAE-PY-Night", ok_button="完成")
        else:
            g.msgbox(msg=r"合并终止，未成功选择文件夹", title="HAE-PY-Night", ok_button="完成")


if __name__ == '__main__':
    Pdf = Name()
    Pdf.File_Run()
