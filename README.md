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

