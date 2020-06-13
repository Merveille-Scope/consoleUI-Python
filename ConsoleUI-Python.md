# ConsoleUI-Python

This module will help printing information in blocks on console. Invoked by HTML5, thus these blocks are called `Division`.

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

