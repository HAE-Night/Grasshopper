import PyPDF2
import os
import easygui as g
import time
import multiprocessing as mp
from multiprocessing import Pool


class POF_Merge(object):
    PT_Path_list = []

    # 合并生成pdf
    def PDF_Merger(self, save_path, pdf_lst):
        file_merger = PyPDF2.PdfFileMerger()
        for pdf in pdf_lst:
            file_merger.append(pdf, import_bookmarks=False)
        file_merger.write(save_path)
        file_merger.close()

    # 保存路径和文件名
    def save_name(self, path_name, end_name):
        file_name = r"{}\{}.pdf".format(path_name, end_name)
        return file_name

    # 对文件夹进行pdf筛选
    def Estimate_PDF(self, Path):
        pdf_list = [fe for fe in os.listdir(Path) if fe.endswith('.pdf')]
        # dir_list = [fe for fe in os.listdir(Path) if os.path.isdir(Path + "\\" + fe)]
        pdf_lst = [os.path.join(Path, filename) for filename in pdf_list]
        return pdf_lst

    # 寻找PDF文件夹
    def Pdf_File(self, paper_file):
        # PT_Path_list = []
        for name in os.listdir(paper_file):
            Pfile_Path = paper_file + "\\" + name
            if os.path.isdir(Pfile_Path):
                for PF in os.listdir(Pfile_Path):
                    PF_path = Pfile_Path + "\\" + PF
                    if PF.upper() == "PDF":
                        # print(PF_path)
                        self.PT_Path_list.append(PF_path)
                    else:
                        if os.path.isdir(PF_path): self.Pdf_File(PF_path)

    # 进度条
    def Runtime(self, Len, times):
        for i in trange(Len):
            time.sleep(times)

    # 合并RUN
    def Estimate_PDF2(self, PFpath):
        self.Pdf_File(PFpath)
        po = Pool(mp.cpu_count())
        for PDF in self.PT_Path_list:
            PDF_Path = "\\".join(PDF.split("\\")[0: -2])
            PDF_Name = PDF.split("\\")[-2]
            PDF_List = self.Estimate_PDF(PDF)
            PDF_save = self.save_name(path_name=PDF_Path, end_name=PDF_Name)
            po.apply_async(self.PDF_Merger, (PDF_save, PDF_List,))
        po.close()
        po.join()


if __name__ == '__main__':
    try:
        mp.freeze_support()
        Pname = g.diropenbox(title="PDF Folder Selection")
        g.msgbox(msg="The program is running, please wait for the result pop-up", title="HAE-PY-Night", ok_button="ok")
        POF_Merge().Estimate_PDF2(Pname)
        g.msgbox(msg="The merge is complete", title="HAE-PY-Night", ok_button="ok")
    except Exception as e:
        g.msgbox(msg="程序出错，请复制一下类容发送给Night:\n" + str(e), title="HAE-PY-Night", ok_button="ok")
