"""Store a function to remove one layer inside a geographic database."""
from osgeo import ogr

ogr.DontUseExceptions()

def remove(gdb_path, layer_name):
    """Remove a layer inside an spatial geodatabase."""
    # The database is opened in update mode to allow edits
    ds = ogr.Open(gdb_path, 1)

    if ds is None:
        msg = (
            f"The databse {gdb_path} could not be opened. "
            "Check the path and that the OpenFileGDB driver supports writing."
        )
        raise RuntimeError(msg)

    # Find the layer's index by name
    for i in range(ds.GetLayerCount()):
        if ds.GetLayerByIndex(i).GetName() == layer_name:
            ds.DeleteLayer(i)
            print(f"Deleted layer: {layer_name}")
            break
    else:
        print(f"Layer '{layer_name}' not found.")

    # Close the file by replacing the variable with no data
    ds = None
