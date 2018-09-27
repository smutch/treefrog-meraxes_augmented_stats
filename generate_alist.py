#!/usr/bin/env python
# -*- coding: utf-8 -*-

import h5py as h5
import numpy as np
import sys

fname = sys.argv[1]

with h5.File(fname, 'r') as fd:
    n_snaps = fd['Header'].attrs['NSnaps']

    alist = np.zeros(n_snaps)
    for snap in range(n_snaps):
        alist[snap] = fd[f'Snap_{snap:03d}'].attrs['scalefactor']

with open("a_list.txt", "w") as fd:
    for v in alist:
        print(v, file=fd)
