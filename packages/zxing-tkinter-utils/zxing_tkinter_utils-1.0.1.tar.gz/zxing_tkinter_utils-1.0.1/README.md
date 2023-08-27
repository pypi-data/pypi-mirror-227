# 目标

用tkinter开发小型桌面应用。

# App类

一个窗口，有一些预设值：

- 大小不可改变。
- 窗口位置居中。

# place方法

推荐使用tkinter的place布局，宽高坐标都是写死的。

我简化了一下调用方式。

```python
# 之前
xxx.place(x=0, y=0, width=100, height=100)

# 之后
place(xxx, 0, 0, 100, 100)
```