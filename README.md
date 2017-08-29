Semantic Paint
==============

If somebody has already shaved that yak, you shouldn't have to.

Semantic paint is a toolkit for attaching metadata (think different colored highlighters) without having write access to the original data.  The idea is that there could be a standard way of finding structure within any given data format.  From that structure, we could build a merkle tree (or DAG) and then attach metadata by combining the hash of the target data with some code that calls out the appropriate subset.  

Ultimately, this means that when you run across some data in the wild, you can analyze its structure and query for brushstrokes.  If you find them, then they will contain the necessary code to generate an object model for that data, which might be useful for working with it.  Further, if you apply brush strokes, those get made available for other people working with the same data.



| Term | Meaning | Examples |
|:--|:--|:--|
| Canvas | The raw data, which the painter might not have permission to modify| A draft of an essay |
| Color | A property that subsets of the canvas can have, and that a painter can apply.  Might be as simple as highlighting some text might form links between parts of the canvas or between different canvasses | *recommended edit* |
| Palette | A set of colors that encapsulate a certain way of thinking about a canvas | *writer feedback* |
| Gallery | A server for holding brush strokes | An ipfs node hosting a particular structure |
| Painter | A person who applies brushstrokes and makes them publicly available in a gallery | Me |
| Brush Stroke | A color together with some targeting code that suffices to attach that color to the canvas | *recommended edit* on the line matching the regex `^Sem.*ta$`: omit the substring matching regex `, and.*$`|

Semantic paint isn't done yet.  This repo contains some brush-stroke targeting code for targeting subsets of text within a canvas.
