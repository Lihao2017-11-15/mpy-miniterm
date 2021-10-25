REM https://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@github.com/Lihao2017-11-15/mpy-miniterm.git
REM @python mpy-miniterm.py /dev/tty.SLAB_USBtoUART --sync-dir src/ --delete
@cd ../code_esp32_huawei/src/
@for /f %%i in ('dir /b /l /s "*__pycache__*"') do rd "%%i" /S /Q 
@cd ../../mpy-miniterm
@pause "按 ctrl-T, ctrl-G 开始，结束后按ctrl-]退出..."
@python mpy-miniterm.py COM30 --sync-dir ../code_esp32_huawei/src/ --delete