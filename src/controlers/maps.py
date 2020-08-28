import pandas as pd
from iieg import db
import math

from models.accident import Accident, Hour

def get_xy():
	points = []
	accidents = Accident.query.all()
	for accident in accidents:
		if not math.isnan(accident.x) and not math.isnan(accident.y):
			points.append((accident.x, accident.y))
	return points