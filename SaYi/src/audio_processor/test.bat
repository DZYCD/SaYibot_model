chcp 65001
@echo off
echo 正在以显卡加速模式启动中，请稍后……
set WEBUI_CONFIG_DEVICE=cuda
E:\DZYCDscript\ba_bert\ba_bert\bertvenv\python.exe "E:\DZYCDscript\ba_bert\ba_bert\main.py"
