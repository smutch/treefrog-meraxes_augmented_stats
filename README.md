# Treefrog augmented stats for Meraxes

**author:** Simon Mutch

## Installation

```sh
pip install --user git+https://github.com/smutch/treefrog-meraxes_augmented_stats
```

This will install 3 command line tools in your current python environment.

## treefrog_gen_alist

Use this to generate an expansion factor list from a Treefrog file.  It accepts one input argument - the path to the Treefrog file.

## treefrog_gen_forestinfo

Use this to generate the forest info files required for Meraxes to do it's domain decomposition.

Usage:

```sh
treefrog_gen_forestinfo [OPTIONS] FNAME_IN FNAME_OUT
```

Note that this script will make use of multiple threads and/or processes.

## treefrog_test_forestinfo

Use this to do some simple sanity checks on the produced forest info file from `treefrog_gen_forestinfo`.

Usage:

```sh
treefrog_test_forestinfo FNAME_IN
```
