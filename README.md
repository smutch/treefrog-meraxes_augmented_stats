# Treefrog augmented stats for Meraxes

**author:** SImon Mutch

## generate_alist.py

Use this script to generate an expansion factor list from a Treefrog file.  It accepts one input argument - the path to the Treefrog file.

## generate_forest_info.py

Generate the forest info files required for Meraxes to do it's domain decomposition.

### Parameters

**fname_in** : str
    The VELOCIraptor unified tree file with forest IDs.

**fname_out** : str
    The output meraxes augmented stats filename.

### Notes

This function provides a CLI interface via Click.  The output file can be tested for basic validity using pytest:

```sh
pytest --augfile=<FNAME_OUT>
```
