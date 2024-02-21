# mgl-sprites

![screenshot](https://github.com/chriscamacho/mgl-sprites/raw/main/Screenshot.png "Screenshot")

These examples are based on the geometry shader example, this reduces it to
one sprite at a time so that individual properties like texture and tint
can be set per sprite. Also used is the rich lines shader.

* edit spline example demonstrates screen panning (drag middle mouse button) 
and zoom with mouse wheel
* Sprites can be used to drag start, end and control points
* each sprite has its own size, tint and texture
* textures are using a TexutureArray a vertical strip of textures
* sprite example demonstrates mouse dragging, a dragged sprite can be rotated
and sized with mouse wheel and A & Z keys
* script recognises when not run in a virtual environment and self activates


Enjoy!

## Initial set up

(Linux)
```
git clone https://github.com/chriscamacho/mgl-sprites.git

cd mgl-sprites.git

python -m venv venv

. ./venv/bin/activate

pip install -r requirements.txt

./main.py
```
In future you can run the script without activating the virtual 
environment as it will self activate.
(Not tested on systemdOS, but presumably it will work)

(Windows)

as above but venv activation and pip different
```
./venv/Scritps/activate.ps1

python -m pip install -r requirements.txt
```
Depending on terminal used you may need a different script or to change
you execution policy

With the exception of a harmless error message (it doesn't actually
run the correct activate script) on Windows, the self activation is
enough to allow the script to run.

