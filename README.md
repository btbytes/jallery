# jallery - the static gallery generator

jallery (pron. gallery) is a static picture gallery generator.

I mostly wrote this as way to convert a couple of scripts I wrote to publish one-page galleries on my site. Eg: [Bangalore Literature Festival 2023](https://files.btbytes.com/albums/blf-2023/gallery.html). I don't expect anyone to find this terribly novel, maybe somewhat useful if you read the code, and find my approach is something that suits you.


What this code does now:

0. for a given directory full of images already at publication resolution. (cameras these days take pictures at very high resolution, which I don't display in that resolution in any of the galleries i've published so far).
1. `prepare` will put empty text files like `title.txt`, `description.txt`, `footnote.txt`, which then you will edit with a text editor. You can use markdown to write in those files.
2. the `prepare` command will also generate a `.txt` file for every "image" (eg: `.png`, `.jpg`) found in the gallery directory. edit these files to add a description for each image.
3. run `generate` command to get a `gallery.html` in the directory 

```
jallery
usage: Jallery - A simple static gallery generator [-h] {prepare,generate} ...

positional arguments:
  {prepare,generate}

options:
  -h, --help          show this help message and exit
```
