#!/usr/bin/env python

"""Generate a forest info file for Meraxes."""

import numpy as np
import h5py as h5
import click
import pandas as pd
import dask.dataframe as df
from dask import delayed

__author__ = "Simon Mutch"
__date__ = "2017-09-12"


@delayed
def calc_snap_counts(fd: h5.File, group_name: str):
    grp = fd[group_name]

    halos = pd.DataFrame(dict(forest_id=grp["ForestID"][:],
                              fof=(grp["hostHaloID"][:] == -1).astype(int)))

    counts = halos.groupby('forest_id').agg(['count', 'sum'])
    counts.reset_index(inplace=True)
    counts.columns = ('forest_id', 'halos', 'fofs')

    return counts, counts.halos.sum(), counts.fofs.sum()


@click.command()
@click.argument("fname_in", type=click.Path(exists=True))
@click.argument("fname_out", type=click.Path())
def generate_forest_info(fname_in, fname_out):
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


if __name__ == '__main__':
    generate_forest_info()
