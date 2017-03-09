#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ChemTools is a collection of interpretive chemical tools for
# analyzing outputs of the quantum chemistry calculations.
#
# Copyright (C) 2014-2015 The ChemTools Development Team
#
# This file is part of ChemTools.
#
# ChemTools is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# ChemTools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --
'''
This script includes swept-under-the-rug utilities needed for sphinx-gallery.
'''


import os
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def plot_existing_image(imagename):
    '''
    Plot the given image using mathplotlib to have it appear in the examples gallery
    generated by sphinx-gallery.

    Parameters
    ----------
    imagename : str
        Name of the image file to plot.
        It is assumsed that the imagefile exists in data/examples directroy.
    '''
    # find full path to the image file
    path = os.path.abspath(os.path.dirname(__file__)).rsplit('/', 1)[0] + '/data/examples/images/'
    imagepath = os.path.join(path, imagename)
    # show the image
    img = mpimg.imread(imagepath)
    imgplot = plt.imshow(img)
    imgplot.axes.get_xaxis().set_visible(False)
    imgplot.axes.get_yaxis().set_visible(False)
    return imgplot



if __name__ == '__main__':
    args = sys.argv[1:]
    task = args.pop(0)

    if task == 'plot':
        plot_existing_image(imagename=args[0])
    # todo: see whether this can be used as a script for plotting images
    # inside examples using some command like:
    # os.system('../../tools/rug.py plot %s' % 'ex003_image.png')
