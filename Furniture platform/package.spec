# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 所有需要打包的.py文件, main.py为执行文件
file = [
        'terminal_management.py',
        ]

a = Analysis(file,
             pathex=['E:\PythonProject\Furniture_quotation'],  # 此列表为项目绝对路径
             binaries=[],
             datas=[],
             hiddenimports=['sqlite3','openpyxl.cell._writer','openpyxl','xlwings', 'os', 'sys', 're', 'time', 'tkinter', 'glob','PIL','itertools',
             'rest_framework.authentication','rest_framework.permissions','rest_framework.parsers','rest_framework.negotiation','rest_framework.metadata','cv2','django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Products',],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Furniture Platform',  # 程序exe的名称
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          icon='E:\\Pictures\\程序图\\merge-pdf.ico',
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,  #此处console=True表示，打包后的可执行文件双击运行时屏幕会出现一个cmd窗口，不影响原程序运行，如不需要执行窗口，改成False即可
)
