import logging

import numpy as np

from scida.interfaces.mixins.base import Mixin
from scida.misc import rectangular_cutout_mask

log = logging.getLogger(__name__)


class SpatialMixin(Mixin):
    pass


class Spatial3DMixin(SpatialMixin):
    pass


class SpatialCartesian3DMixin(Spatial3DMixin):
    def __init__(self, *args, **kwargs):
        self.hints = {}
        super().__init__(*args, **kwargs)
        # TODO: determine whether periodic?
        self.pbc = True
        # TODO: Dynamically determine location of boxsize
        self.boxsize = np.nan * np.ones(3)
        try:
            bs = self.header["BoxSize"]
        except KeyError:
            bs = None
            print("Info: Cannot determine boxsize.")
        is_cubical = isinstance(bs, np.ndarray) and np.all(bs == bs[0])
        if isinstance(bs, float) or is_cubical:
            self.boxsize[:] = bs
        elif bs is not None:
            # Have not thought about non-cubic cases yet.
            print("Boxsize:", bs)
            raise NotImplementedError
        common_coord_names = ["Coordinates", "Position", "GroupPos", "SubhaloPos"]
        self.hints["CoordinatesName"] = dict()
        for k, cntr in self.data.items():
            found = False
            for ccn in common_coord_names:
                if ccn in cntr.keys(withrecipes=True):
                    found = True
                    log.debug("Found CoordinatesName '%s' for species '%s'" % (ccn, k))
                    self.hints["CoordinatesName"][k] = ccn

                    dfltname = "Coordinates"
                    if ccn == dfltname:
                        break  # nothing to do

                    self.data[k].add_alias("Coordinates", ccn)
            if not found:
                log.debug("Did not find CoordinatesName for species '%s'" % k)

    def get_coords(self, parttype="PartType0"):
        k = self.hints["CoordinatesName"].get(parttype, "")
        if k in self.data[parttype]:
            return self.data[parttype][k]
        return None

    def rectangular_cutout_mask(self, center, width, parttype="PartType0"):
        coords = self.get_coords(parttype=parttype)
        return rectangular_cutout_mask(
            center, width, coords, pbc=self.pbc, boxsize=self.boxsize
        )

    def rectangular_cutout(self, center, width, parttype="PartType0"):
        pass
