# -*- mode: python -*-

block_cipher = None


a = Analysis(['MAIN.py'],
             pathex=['C:\\Users\\bktor\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'C:\\Users\\bktor\\Desktop\\GUI'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          name='MAIN',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
