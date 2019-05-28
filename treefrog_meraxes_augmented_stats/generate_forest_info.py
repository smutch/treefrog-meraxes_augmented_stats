#!/usr/bin/env python
# 
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
import h5py as h5
import click
import pandas as pd
import dask.dataframe as df
from dask import delayed

__author__ = "Simon Mutch"
__date__ = "2017-09-12"


@delayed  # NOQA
def calc_snap_counts(fd: h5.File, group_name: str):
    """Calculate the counts for a single snapshot.

    Parameters
    ----------
    fd : h5py.File
        The input VELOCIraptor HDF5 file.

    group_name : str
        The name of the HDF5 group for the corresponding snapshot.

    Returns
    -------
    counts : pandas.DataFrame
        The forest IDs, along with the total number of halos and fof groups in each
        forest.

    total_halos : int
        The total number of halos at this snapshot.

    total_fofs : int
        The total number of FOF groups in this snapshot.
    """

    grp = fd[group_name]

    halos = pd.DataFrame(dict(forest_id=grp["ForestID"][:],
                              fof=(grp["hostHaloID"][:] == -1).astype(int)))

    counts = halos.groupby('forest_id').agg(['count', 'sum'])
    counts.reset_index(inplace=True)
    counts.columns = ('forest_id', 'halos', 'fofs')

    return counts, counts.halos.sum(), counts.fofs.sum()


def generate_forest_info(fname_in, fname_out):
    """Generate the forest info files required for Meraxes to do it's domain
    decomposition.

    Parameters
    ----------
    fname_in : str
        The VELOCIraptor unified tree file with forest IDs.

    fname_out : str
        The output meraxes augmented stats filename.

    Notes
    -----
    This function is provided through a Click CLI interface.
    """

    with h5.File(fname_in, "r") as fd:
        snap_groups = [k for k in fd.keys() if "Snap" in k]

        res = [calc_snap_counts(fd, group_name) for group_name in snap_groups]

        counts = df.from_delayed([r[0] for r in res]).groupby('forest_id').agg(['sum', 'max']).compute().sort_index()
        counts.columns = 'halos halos_max fofs fofs_max'.split()

        n_halos = np.array([r[1].compute() for r in res])
        n_fofs = np.array([r[2].compute() for r in res])

    with h5.File(fname_out, "w") as fd:
        cds_kwargs = dict(compression=7, shuffle=True, chunks=True)
        fd.create_dataset("n_halos", data=n_halos, **cds_kwargs)
        fd.create_dataset("n_fof_groups", data=n_fofs, **cds_kwargs)

        fd.attrs["n_snaps"] = np.int32(len(snap_groups))
        fd.attrs["n_halos_max"] = np.int32(np.max(n_halos))
        fd.attrs["n_fof_groups_max"] = np.int32(np.max(n_fofs))

        grp = fd.create_group("forests")
        grp.attrs["n_forests"] = np.int32(counts.shape[0])
        grp.create_dataset("forest_ids", data=counts.index.values, **cds_kwargs)
        grp.create_dataset("n_halos", data=counts.halos.values.astype('i4'), **cds_kwargs)
        grp.create_dataset("n_fof_groups", data=counts.fofs.values.astype('i4'), **cds_kwargs)
        grp.create_dataset("max_contemporaneous_halos",
                           data=counts.halos_max.values.astype('i4'), **cds_kwargs)
        grp.create_dataset("max_contemporaneous_fof_groups",
                           data=counts.fofs_max.values.astype('i4'), **cds_kwargs)


@click.command()  # NOQA
@click.argument("fname_in", type=click.Path(exists=True))
@click.argument("fname_out", type=click.Path())
def cli(fname_in, fname_out):
    generate_forest_info(fname_in, fname_out)


if __name__ == '__main__':
    cli()
