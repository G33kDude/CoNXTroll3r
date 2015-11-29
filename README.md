CoNXTroll3r
===========

CoNXTroll3r is a self contained python based web server for controlling
your EV3 remotely over the internet. It relies on MJPG-streamer for video
streaming.

CoNXTroll3r Setup
-----------------

Other than MJPG-streamer, CoNXTroll3r relies only on `python-ev3dev`.
You can get this package directly from the ev3dev repositories using apt-get.
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-ev3dev
```

Once it is finished installing you can test CoNXTroll3r by running `http.py`
```
python http.py
```

This should start a webserver on port 8081 you can visit using the URL
`http://ev3dev:8081` (substituting `ev3dev` for your EV3's hostname or
IP address as necessary).

After you've confirmed the python server is working correctly, it is time
to set up MJPG-streamer for the live video feed.

Compiling MJPG-streamer
-----------------------

Start by downloading all the prerequisites for download and compilation.
```
sudo apt-get install unzip make gcc libjpeg-dev
```

Next you'll need to grab the source archive from the project's SourceForge.
```
wget http://sourceforge.net/code-snapshots/svn/m/mj/mjpg-streamer/code/mjpg-streamer-code-182.zip
```

Now you can unzip the source and compile it using `make`.
This should only take a minute or two, even on the EV3's slow processor.
```
unzip mjpg-streamer-code-182.zip
cd mjpg-streamer-code-182/mjpg-streamer
make
```

You can test the resulting binaries using the following command. This will
open a server on port 8080 that can be viewed from a web browser.
```
./mjpg_streamer -i "./input_uvc.so -y -n" -o "./output_http.so -w ./www"
```

I've used the flags `-y -n` on the input plugin because my webcam seems to
only support YUV video, and has no support for pan/tilt/zoom.
