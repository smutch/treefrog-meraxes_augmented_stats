# Treefrog augmented stats for Meraxes

**author:** Simon Mutch

## generate_alist.py

Use this script to generate an expansion factor list from a Treefrog file.  It accepts one input argument - the path to the Treefrog file.

## generate_forest_info.py

Use this script to generate the forest info files required for Meraxes to do it's domain decomposition.

Usage:

```sh
generate_forest_info.py [OPTIONS] FNAME_IN FNAME_OUT
```

### Notes

This function provides a CLI interface via Click.  The output file can be tested for basic validity using pytest:

```sh
pytest --augfile=<FNAME_OUT>
```
