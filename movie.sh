python3 3dmovie.py ./output/
mogrify -format png ./output/*.ppm
convert -delay 8 ./output/*.png movie.gif
