Semantic Paint
==============

Semantic paint is a toolkit for attaching metadata (think different colored highlighters) without having write access to the original data, and in a way that attempts to tolerate small changes to that data.

| Term | Meaning | Examples |
|:--|:--|:--|
| Canvas | The raw data, which the painter might not have permission to modify| A draft of an essay |
| Color | A property that subsets of the canvas can have, and that a painter can apply.  Might be as simple as highlighting some text might form links between parts of the canvas or between different canvasses | *recommended edit* |
| Palette | A set of colors that encapsulate a certain way of thinking about a canvas | *writer feedback* |
| Gallery | A server for holding brush strokes | An ipfs node hosting a particular structure |
| Painter | A person who applies brushstrokes and makes them publicly available in a gallery | Me |
| Brush Stroke | A color together with some targeting code that suffices to attach that color to the canvas |

Semantic paint isn't done yet.  This repo contains some brush-stroke targeting code that will ultimately be referenced by several palettes.
