import PyPDF2
import os
import easygui as g


class POF_Merge(object):
    # 合并生成pdf
    def PDF_Merger(self, save_path, pdf_lst):
        file_merger = PyPDF2.PdfFileMerger()
        print(pdf_lst)
        for pdf in pdf_lst:
            file_merger.append(pdf, import_bookmarks=False)
        file_merger.write(save_path)
        file_merger.close()

    # 保存路径和文件名
    def save_name(self, path_name, end_name):
        # path = "\\".join(path_name.split("\\")[:-1])
        all_file = os.listdir(path_name)
        if "APDF Merger" not in all_file:
            os.makedirs(path_name + r"\APDF Merger")
            file_name = r"{}\{}.pdf".format(path_name + r"\APDF Merger", end_name)
        else:
            file_name = r"{}\{}.pdf".format(path_name + r"\APDF Merger", end_name)
        return file_name

    # 对文件夹进行pdf筛选
    def Estimate_PDF(self, Path):
        pdf_list = [fe for fe in os.listdir(Path) if fe.endswith('.pdf')]
        # dir_list = [fe for fe in os.listdir(Path) if os.path.isdir(Path + "\\" + fe)]
        pdf_lst = [os.path.join(Path, filename) for filename in pdf_list]
        return pdf_lst

    # 合并RDF
    def Estimate_PDF2(self, paper_file, path):
        PDFendName = "-".join([paper_file.split("\\")[-2], paper_file.split("\\")[-1]])
        PLT = self.Estimate_PDF(paper_file)
        # 根目录PDF合并
        if len(PLT) >= 1:
            self.PDF_Merger(save_path=self.save_name(path, PDFendName), pdf_lst=PLT)

        for Pfile in os.listdir(paper_file):
            Pfile_Path = paper_file + "\\" + Pfile
            if os.path.isdir(Pfile_Path):
                print(Pfile_Path)
                # self.PDF_Merger(save_path=self.save_name(path, Pfile), pdf_lst=self.Estimate_PDF(Pfile_Path))
                self.Estimate_PDF2(Pfile_Path, path)


if __name__ == '__main__':
    try:
        POF_Merge().Estimate_PDF2(g.diropenbox(title="PDF Folder Selection"), g.diropenbox(title="PDF The location where the merged files are stored"))
        g.msgbox(msg="The merge is complete", title="HAE-PY-Night", ok_button="ok")
    except Exception as e:
        g.msgbox(msg="Merger failure", title="HAE-PY-Night", ok_button="ok")

