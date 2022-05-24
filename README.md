# Python Scratch Backend
This is a project that consists of a basic clone of the core functionality of the Scratch environment.
What this actually constitutes is a sprite and sound system, alongside a replica of the Scratch API,
meaning any objects can be made to do exactly the same commands as they can in Scratch.
Blocks and so forth are not formally defined, and currently the implementation is hard-coded for
each functionality of each block, so there are as yet no custom blocks; but for now, this project
aims to be a vague clone of Scratch which can be controlled using Python instead of the block-based
environment. There are potential plans to re-introduce said environment through the addition of a
GUI, but this not certain yet. Feel free to fork yourself if you are intersted :)

## Running
You can create a Python project and import this module (only one file) and create a `Project` object
which will contain a default `Sprite` and `Stage`. Then you can create new sprites, give them costumes,
etc., and have them move around according to the logic of the Scratch environment.
You can have a look at autocomplete to see the kinds of methods that `Sprite`s, `Stage`s, `Costume`s,
etc., may exhibit.
