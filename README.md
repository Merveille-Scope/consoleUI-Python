# ConsoleUI-Python

Using this module to print a good looking character-based UI on your console.

Initialize an `Interface` division and register child divs into it. Call .refresh() to print.

## Quick start

There are two basic types of `Division`, `ContainerDivision` and `ContentDivision`. `ContainerDivision` can have other `Division` in it; `ContentDivision` can have string.

```python
interface = Interface(height=24, width=80)  # you want all division to show in this Division

container = ContainerDivision(height=24, width=80)
content_1 = ContentDivision(height=24, width=30)
content_2 = ContentDivision(24, 47)  # height in line, width in mono-spaced half-character

content_1.register('This module will help printing information in blocks on console. Invoked by HTML5, thus these blocks are called `Division`.')
content_2.register('There are two basic types of `Division`, `ContainerDivision` and `ContentDivision`. `ContainerDivision` can have other `Division` in it; `ContentDivision` can have string.')

container.register(content_1)
container.register(content_2)

interface.register(container)

interface.refresh()
```

## Divisions

This module is invoked by HTML. By registering divisions to separate your console into several blocks and print information on them respectively.

There are two kinds of Divisions, `ContentDivision` and `ContainerDivision`. `ContentDivision` accepts any string by `ContentDivision_instance.register(YOUR_STRING)`. `ContainerDivision` accepts divisions by `.register(YOUR_DIVISION)` and can be called multiple times to register several divisions.





## Scratches

要融合一系列的div到一个div中，我需要做的事情：

1. 解决将两个 div 融合的问题。在融合过程中，有如下几个情况
   1. 将另一个div直接拼接在当前div的正下方
      1. 如果没有导致高度超限，直接拼接就完事了
      2. 如果出现高度超限，应当进行无情裁剪
         1. 裁剪风格
            1. 砍头
            2. 砍腿
            3. 砍中间
   2. 将另一个div拼接在当前div的右侧
      1. 当前div到底能不能拼接在右侧——即拼接在右侧后会不会导致超宽
         1. 没有超宽的情况下，直接拼接
         2. 超宽的情况下，有两种处理方式
            1. 对div进行裁剪，使其可以被拼接在右侧
               1. 裁剪风格
                  1. 纵向一刀
                  2. 重新指定宽度，然后重算内容布局，若超高，交给超高裁剪。
            2. ~~拒绝裁剪，将div置于下一行~~
               1. ~~若拼接在下方时导致高度超过预期的处理方式~~
                  1. ~~直接砍掉超高的行~~
                  2. ~~尝试重算div的宽高，期望其可以通过增加宽度使其能够尽可能减少高度避免裁剪。~~
                     1. ~~重算后的新div内容会发生改变，导致下一个被添加的div的位置难以预测，因此应该严格控制这个div的显示范围，不应换行，更不应该尝试重算div的显示方式。~~