import os
from os import F_OK

from tasks import *
from taskinit import *
import casac

import sys
import numpy as np

# CHUNKS=8
# combine all data
CHUNKS=-1

if len(sys.argv) < 2:
    msg = 'Usage: {} <filename.ms>'.format(sys.argv[0])
    raise SystemExit(msg)

ms_string_array = sys.argv[1:]
# ms_string_array = np.sort(sys.argv[1:])
print(ms_string_array[:5])
# ms_string_array.sort(key= lambda x: float(os.path.splitext(os.path.basename(x))[0][23:]))
print(os.path.splitext(os.path.basename(ms_string_array[0]))[0][22:])
ms_string_array.sort(key= lambda x: float(os.path.splitext(os.path.basename(x))[0][22:]))
print(ms_string_array[:5])
for file_ in ms_string_array: print(file_)

if CHUNKS < 0:
    print('Combining all data into MS')
#     rephased_ms = '1627186156_sdp_l0-67p-rephased.ms'
    rephased_ms = '1627186165_sdp_l0-67P-rephased.ms'
    concat(vis=ms_string_array, concatvis=rephased_ms)
else:
    print('Combining chunks of data')
#     for ittr_ in range(0, len(ms_string_array), CHUNKS):
#         string_array = ms_string_array[ittr_:ittr_+CHUNKS]
#         rephased_ms = '1627186156_sdp_l0-67p-{}-rephased.ms'.format(ittr_)
#         print('Creating concat file {}'.format(rephased_ms))
#         concat(vis=string_array, concatvis=rephased_ms)

# -fin-
