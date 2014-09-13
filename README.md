# The World GDP Globe

This is a little visualization of GDP data throughout the world.
Check out an interactive demo at [Sina App Engine](http://worldgdp.sinaapp.com)

![github users plotted on a globe](http://fmn.rrimg.com/fmn064/20140913/1750/large_1XrG_24aa00005f561190.jpg)

## Creating the Visualization

All data is provided by [THE WORLD BANK](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD).

Location of each country are passed through the [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding/)
and transformed into geographical coordinates.

Finally, data is plotted on the [WebGL Globe](http://code.google.com/p/webgl-globe/).

## Anatomy of the Repo

Code to transform the data is in `master/GDP_DataTransform`.

Original data from [THE WORLD BANK](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD) is in `master/GDP_DataTransform/world_GDP_2004_2013.xlsx`

