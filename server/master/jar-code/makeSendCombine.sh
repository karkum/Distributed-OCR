#!/bin/bash
javac SendAll.java
jar cvfm SendCombine.jar manifest1.txt SendAll.class TesseractInfo.class ImageConstructor.class ImageConstructor\$Pair.class ImageConstructor\$1.class

sudo cp SendCombine.jar /var/www/cgi-bin
cd /var/www/cgi-bin
