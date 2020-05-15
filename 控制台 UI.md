# 控制台 UI

这个文件记录控制台 UI 的制作思路。

目前的 UI 按照其对用户操作的反馈方式可以分为被动型 UI 和监听型 UI (名字我自己起的)。

- 被动型 UI：指的是用户如果不进行任何**输入操作**[^1]，则 UI 不会有任何反馈。

  被动型 UI 也可以做得非常有表现力，比如 msfconsole 就是其中之一。

- 监听型 UI：指的是这种 UI 保持实时监听用户的操作，对一切它能够理解的操作进行反馈。

  即使在控制台上，也有很多表现力很高的监听型 UI，比如 top 就是个不错的例子，它保持周期性地刷新，同时当用户执行按下如 q 键等操作时它立即进行了相应反馈，停止刷新，退出程序。

事实上这两种 UI 除了在处理用户的操作时有所不同以外，在 UI 的显示上是没什么差异的。顶多就是一个周期性刷新，一个在用户的一次输入后刷新。

因此为了方便起见，在这里仅仅讨论被动型 UI。

## UI 的两大模块

UI 主要的两个模块是处理输入的模块和处理输出的模块。

### 输入模块

输入模块的主要功能是对用户的输入操作进行处理，在被动型 UI 中这个模块就是对用户输入的单句命令进行解析，然后根据具体命令，将内容转交给相应的模块进行进一步处理。

事实上从这个模块的设计思路上，已经可以看到<u>消息机制</u>的雏形，这个模块正在做的事情就是监听消息和派发消息。

在处理用户的输入时，输入模块将会轮询注册在它下面的各模块以判断哪些模块需要对用户的这个命令进行处理，如果要进行处理，则会将这条命令交给该模块。

> 需要注意的是，如果轮询时没有断路机制的话，则任何命令的输入都会让输入模块遍历所有注册的模块，如果注册的模块数量太多，会产生效率问题。

> 但如果有某种方案可以将轮询操作简化为访问操作自然更好。
>
> 比如注册时将某种条件置入一个字典。

### 输出模块

输出模块的主要功能是向用户反馈上一次的输入操作的结果，或者在监听型 UI 中，反映当时程序运行的状态。该模块是这个文件主要讨论的部分。

本输出模块的设计灵感源自于 HTML 中的 div 标签，为了向其致敬，输出模块的基类起名为 `Division`。

#### 重要前提

在开始之前，必须达成共识，那就是除了该模块以外，任何其他模块都不应该对标准输出通道进行任何写入。所有其他模块的任何非错误输出都需要将自己注册在这个模块中。

#### 分区块输出

这个输出模块的核心思想是将最终输出结果划分为若干个`Division`，然后再分别将这些`Division`输出到控制台窗口。

一个`Division`类应该是这样：

```python
class Division:
    def __init__(self, parent_div=None, **dimensions):
        self.parent_div = parent_div

        self._item_to_print = ''

        # if any of these two were set 0, means it or both are not limited
        # the max lines THIS div should occupy, in lines
        self._div_height = 0 if 'height' not in dimensions else dimensions['height']
        # the max width THIS div should occupy, in characters
        self._div_width = 0 if 'width' not in dimensions else dimensions['width']

        self._container = []  # child divisions will be print

    def set_parent_div(self, parent_div):
        ...

    def set_size(self, **height_or_width_in_int: int):
        ...

    def get_size(self, dimension: str = None):
        ...

    def clear_content(self):
        ...

    def registry(self, obj, callback=None, *args):
        ...

    def _registry_content(self, content, callback=None, *args):
        ...

    def _registry_div(self, div, callback=None, *args):
        ...

    def __repr__(self):
        ...

    def print_div(self):
        ...

    def _container_rendering(self):
        ...

    def _div_rendering(self):
        ...
```

该类中规定了`Division`的基本属性：

- 宽度(`width`)：表示窗口横向能容纳的半角字符数量，当设置为零时表示不限制。

- 高度(`height`)：表示窗口纵向能容纳的行数，当设置为零时表示不限制。

- `Division`中的文字内容(`self._item_to_print`)。

  今后将会统一将文字内容按行分隔，实现横向的 `Division` 渲染。目前仅支持将所有的 `Division` 从上到下输出，所有的 `Division` 都将在自己的行内排斥其他的 `Division`。
  
- `selectable`，这个属性会让该 `Division` 在显示时附带一个数字，**它应该是所有 `Division` 都有的属性**。这个数字在一个窗口与 `Division` 一一对应，不过目前还没有实现。

- `display`，这个属性可以改变一个 `Division` 的显示方式。如果设置为 `'display': float` 则尝试将这个 `Division` 与前一个放在同一行显示，除非这两个 `Division` 的宽度超过容器宽度。

对外提供的方法有：

- 获取和设定宽高。
- 清除内容和容器中的其他div对象。
- 注册对象，若对象不是 `Division` 则将其注册为当前 `Division` 的内容，若是 `Division` 则将其加入当前 `Division` 容器中的子 `Division`。
- 显示区块，将这个区块按照设定好的格式生成字符串并返回。
  - 目前这个方法还没有针对区块的宽高作处理。
  - 容器型区块也不能处理子区块宽高的显示。

##### 关于子区块宽高的处理

这里主要指两种特殊情况，以及它们之间的组合。

- 子区块的宽高超过母区块的情况。
- 多个子区块在组合显示时，总宽高超过母区块的情况。

当子区块为字符串时，宽度超过时尝试换行，高度超过时将最后一行打印为*特殊的提示符号*。

当子区块为区块时，宽度或高度超过时直接显示子区块超宽或超高提示。

存在多个子区块时，且多个区块需要水平排列，且总宽度超限时，尝试对区块进行换行。若换行后高度超限，则显示高度超限提示。

##### 尺寸超限提示

如果将所有的尺寸超限提示都可以无视高度限制，强制显示。

##### 尚未实现的功能

- 设定 ID，通常由它直接隶属的 `Division` 为其设定。

- 获取自己的 ID，在获取自己 ID 的同时将调用自己所有子 `Division` 的获取 ID 方法。

  事实上至少提供三个姿势：

  - 仅返回自己的 ID。
  - 返回自己，和自己所有子模块的 ID。
  - 使用递归方式返回自己，自己的所有子模块和它们的子模块...

- 

#### 默认输出方式

接下来便是争议较大的一点，关于其他模块输出时应该向输出模块传递什么对象的问题。

我个人的意见是，如果传入了字符串，则将它直接输出，如果传递了其他对象且没有指定输出方式，则默认调用该对象的`__str__()`方法。

因此建议为需要输出的模块写一个专用的 `Division`，然后将该 `Division` 注册给窗口中的 `Division`。

















[^1]: 指的是用户在输入任意字符串后敲下回车的操作。如果用户不敲回车，则认为没有输入。