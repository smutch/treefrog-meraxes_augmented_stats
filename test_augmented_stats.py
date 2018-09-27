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
