import numpy as np
import json
import sys

out_name = sys.argv[1]
eta      = sys.argv[2]
alpha    = sys.argv[3]
lr       = sys.argv[4]
epoch    = sys.argv[5]

dd = {"eta":eta,
	"alpha":alpha,
	"lr":lr,
	"epoch":epoch}

with open(out_name, 'w') as fp:
	json.dump(dd, fp)
