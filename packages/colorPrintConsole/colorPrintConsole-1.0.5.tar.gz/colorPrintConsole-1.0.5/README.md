## 简介

- 在控制台中用于彩色打印的包
- 采用的是亮色

## 安装

```
pip install --index-url https://pypi.org/simple colorPrintConsole
```

## 使用

```python
from colorPrintConsole import ColorPrint

cp = ColorPrint()
cp.red('红色文本')
cp.green('绿色文本')
cp.yellow('黄色文本')
cp.blue('蓝色文本')
cp.magenta('品红色文本')
cp.cyan('青色文本')

```
