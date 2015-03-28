CoNXTroll3r
===========

CoNXTroll3r is a self contained python based web server for controlling your EV3 remotely over the internet. It relies on MJPG-streamer for video streaming.


Compiling MJPG-streamer
-----------------------

First you need to download the necessary packages.

```
sudo apt-get install svn make gcc libjpeg-dev
```

Once the packages are done downloading, you'll need to grab MJPG-streamer.

```
svn co https://svn.code.sf.net/p/MJPG-streamer/code/MJPG-streamer/
cd MJPG-streamer
```

When MJPG-streamer is done downloading, you should be able to compile it with make.

```
make
```

And finally, run the compiled binary `mjpg_streamer`. This will put it up on port 8080.

```
./mjpg_streamer -i "./input_uvc.so -y -n" -o "./output_http.so -w ./www"
```

I've used the flags `-y -n` on the input plugin because my camera only supports YUV video, and has no support for pan/tilt/zoom.