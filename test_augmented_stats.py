# Generate a forest info file for Meraxes.
# Copyright © 2019 Simon Mutch
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np


def test_forest_counts(augfile):
    n_halos = augfile["forests/n_halos"][:]
    n_fof_groups = augfile["forests/n_fof_groups"][:]

    assert not np.all(n_halos == n_fof_groups)
    assert np.all(n_halos >= n_fof_groups)


def test_snap_counts(augfile):
    n_halos = augfile["n_halos"][:]
    n_fof_groups = augfile["n_fof_groups"][:]

    assert not np.all(n_halos == n_fof_groups)
    assert np.all(n_halos >= n_fof_groups)


def test_forest_totals(augfile):
    n_halos_snap = augfile["n_halos"][:]
    n_fofs_snap = augfile["n_fof_groups"][:]

    n_halos = augfile["forests/n_halos"][:]
    n_fof_groups = augfile["forests/n_fof_groups"][:]

    assert n_halos.sum() == n_halos_snap.sum()
    assert n_fof_groups.sum() == n_fofs_snap.sum()


def test_forest_contemps(augfile):
    max_contemp_halos = augfile["forests/max_contemporaneous_halos"][:]
    max_contemp_fofs = augfile["forests/max_contemporaneous_fof_groups"][:]

    assert not np.all(max_contemp_halos == max_contemp_fofs)
    assert np.all(max_contemp_halos >= max_contemp_fofs)
