REM @python mpy-miniterm.py /dev/tty.SLAB_USBtoUART --sync-dir src/ --delete
@cd ../code_esp32_huawei/src/
@for /f %%i in ('dir /b /l /s "*__pycache__*"') do rd "%%i" /S /Q 
@cd ../../mpy-miniterm
@pause "�� ctrl-T, ctrl-G ��ʼ��������ctrl-]�˳�..."
@python mpy-miniterm.py COM30 --sync-dir ../code_esp32_huawei/src/ --delete