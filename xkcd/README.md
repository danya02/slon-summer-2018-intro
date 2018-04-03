# TL;DR: [this script](random_display.py)
AKA "CLI users are *so screwed*".

The program uses the official [xkcd JSON API](https://xkcd.com/json.html) to get the name, title text and image URL of a comic.
Then it downloads said comic into its own directory, and displays it in a pygame window.
To show the next random comic, click anywhere inside the window.
If the system cannot have the pygame window opened (possible cases include: broken installation, crashed or absent X11 server, ssh connection failure, malicious interference from other network machines, or a mouse chewing on the monitor cable), then instead of showing the comic in a window, it will print the name, title text and transcript to stdout.
(This is pretty pointless, as only a select few comics have transcripts.)
To move to another random comic in this mode, press [ENTER].

The program caches downloaded comics to the current working directory.
If you wish to pre-cache them, perhaps because you anticipate a network outage, you may use [this](cache.py) supplementary script.
