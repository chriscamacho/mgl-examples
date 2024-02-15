# H1
mgl-sprites

This example is based on the geometry shader example, this reduces it to
one sprite at a time so that individual properties like texture and tint
can be set per sprite.

* each sprite has its own size, tint and texture
* demonstrates mouse dragging
* script recognises when not run in a virtual environment and self activates


Enjoy!

# H2
Initial set up

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
