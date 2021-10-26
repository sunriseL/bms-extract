# BMS-Extract

本项目用于在 BMS 工程完成后根据工程文件分析所使用到的 Key 音文件，将 Key 音文件和工程文件导出至一个目录方便后期打包。

## Requirement
- tqdm
- pyinstaller # 如果你想要打包成 exe 文件
- oggenc.exe # 如果需要把 wav 转成 ogg

## Usage
```
usage: extract.py [-h] [-d DIRECTORY] [-o OUTPUT_DIRECTORY] [-f FILE] [--oggenc OGGENC]

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        存放BMS工程以及切音的目录
  -o OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        导出目录（相对于工程目录）
  -f FILE, --file FILE  指定的BMS工程（相对于工程目录）
  --oggenc OGGENC       oggenc.exe的位置
```
如果使用的是已打包好的可执行文件则将 extract.py 替换为 extract.exe 即可

如果需要自己手动打包成 exe 文件则
```
pyinstaller extrace.py --onefile
```


## TODO
- [x] 自动寻找BMS工程文件
- [x] 追踪 Key 音文件是否被使用
- [x] 支持是否导出未被使用 Key 音文件选项
- [ ] 支持多BMS工程文件选择
- [x] 支持导出目录自定义
- [x] 支持 wav 转 ogg 以及对应的工程文件修改(需要使用oggenc.exe)
  