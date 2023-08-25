import astropy.units as u
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord

from heinlein import load_dataset
from heinlein.project import project

try:
    project.delete_project("cfht", internal=True)
except project.heinleinProjectException:
    pass

from heinlein import add

add("cfht", "catalog", "/Volumes/workspace/data/cfht/catalogs/subdivided")
