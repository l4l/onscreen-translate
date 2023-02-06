# onscreen-translate

[demo.webm](https://user-images.githubusercontent.com/5658339/217007738-287bb74b-aa9b-43ff-82f6-82de7607bebc.webm)

Provides a translation for a given box of your screen.

## Linux

Install:

```sh
git clone https://github.com/l4l/onscreen-translate.git && cd onscreen-translate
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

and then run:

```sh
# on Wayland:
python main.py --box `slurp -f '%x %y %w %h'` --src de --dest es

# or on X.org:
python main.py --box `slop -f '%x %y %w %h'` --src de --dest es
```
