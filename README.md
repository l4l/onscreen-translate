# onscreen-translate

[demo.webm](https://user-images.githubusercontent.com/5658339/216840588-74d46217-c19b-4d38-8c5f-86851b12cf59.webm)

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
