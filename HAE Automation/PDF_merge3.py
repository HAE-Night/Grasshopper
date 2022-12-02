import multiprocessing

import PyPDF2
import os
import easygui as g
import time
import multiprocessing as mp
from multiprocessing import Pool

PT_Path_list = []

# 合并生成pdf
def PDF_Merger(save_path, pdf_lst):
    file_merger = PyPDF2.PdfFileMerger()
    for pdf in pdf_lst:
        file_merger.append(pdf, import_bookmarks=False)
    file_merger.write(save_path)
    file_merger.close()


# 保存路径和文件名
def save_name(path_name, end_name):
    file_name = r"{}\{}.pdf".format(path_name, end_name)
    return file_name


# 对文件夹进行pdf筛选
def Estimate_PDF(Path):
    pdf_list = [fe for fe in os.listdir(Path) if fe.endswith('.pdf')]
    # dir_list = [fe for fe in os.listdir(Path) if os.path.isdir(Path + "\\" + fe)]
    pdf_lst = [os.path.join(Path, filename) for filename in pdf_list]
    return pdf_lst


# 寻找PDF文件夹
def Pdf_File(paper_file):
    # PT_Path_list = []
    for name in os.listdir(paper_file):
        Pfile_Path = paper_file + "\\" + name
        if os.path.isdir(Pfile_Path):
            for PF in os.listdir(Pfile_Path):
                PF_path = Pfile_Path + "\\" + PF
                if PF.upper() == "PDF":
                    # print(PF_path)
                    PT_Path_list.append(PF_path)
                else:
                    if os.path.isdir(PF_path): Pdf_File(PF_path)


# 进度条
def Runtime(Len, times):
    for i in range(Len):
        time.sleep(times)


# 合并RUN
def Estimate_PDF2(PFpath):
    Pdf_File(PFpath)
    print(len(PT_Path_list))
    po = Pool(mp.cpu_count())
    for PDF in PT_Path_list:
        PDF_Path = "\\".join(PDF.split("\\")[0: -2])
        PDF_Name = PDF.split("\\")[-2]
        PDF_List = Estimate_PDF(PDF)
        PDF_save = save_name(path_name=PDF_Path, end_name=PDF_Name)
        po.apply_async(PDF_Merger, (PDF_save, PDF_List,))
    po.close()
    po.join()


if __name__ == '__main__':
    name = str(g.diropenbox(title="PDF Folder Selection"))
    Estimate_PDF2(name)
    multiprocessing.freeze_support()
    # app = QApplication(sys.argv)
    # window = Ui_MainWindow()
    # window.show()
    # sys.exit(app.exec_())
    # try:
    #     print(222)
        # g.msgbox(msg="The merge is complete", title="HAE-PY-Night", ok_button="ok")
    # except Exception as e:
    #     g.msgbox(msg="程序出错，请复制一下类容发送给Night:\n" + str(e), title="HAE-PY-Night", ok_button="ok")
