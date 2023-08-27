## 介绍

在控制台中用于彩色打印的包

## 安装

```
pip install --index-url https://pypi.org/simple colorPrintConsole
```

## 使用

```python
from colorPrintConsole import ColorPrint

cp = ColorPrint()
print(cp.red('红色文本'))
print(cp.green('绿色文本'))
print(cp.yellow('黄色文本'))
print(cp.blue('蓝色文本'))
print(cp.magenta('品红色文本'))
print(cp.cyan('青色文本'))

```

