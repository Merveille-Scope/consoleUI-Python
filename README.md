# consoleUI-Python

Using this module to print a good looking character-based UI on your console.

Initialize an `Interface` division and register child divs into it. Call .refresh() to print.



# Divisions

This module is invoked by HTML. By registering divisions to separate your console into several blocks and print information on them respectively.

There are two kind of Divisions, `ContentDivision` and `ContainerDivision`. `ContentDivision` accepts any string by `ContentDivision_instance.register(YOUR_STRING)`. `ContainerDivision` accepts divisions by `.register(YOUR_DIVISION)` and can be called multiple times to register several divisions.

