# pixelserv

A http server that responds to every request with a gif consisting of a single pixel.

## Usage

To run on the default port 8000:

```
docker run -d sealeg/pixelserv
```

To expose as port 80 on the docker host:

```
docker run -d -p 80:8000 sealeg/pixelserv
```

## Acknowledgements

The pixelserv.py script is a reimplementation of 
[this](http://proxytunnel.sourceforge.net/files/pixelserv.pl.txt)
 perl script
