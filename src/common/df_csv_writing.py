import datetime
import logging
import os
import re

import pandas as pd

logger = logging.getLogger(__name__)


def write_df_to_csv(df: pd.DataFrame, store_path: str, initial_path: str, file_appendix: str=''):
    # write dataset to file
    file_name = os.path.splitext(os.path.basename(initial_path))[0]

    # prepare dataset store path
    path = store_path
    if not re.match("\d\d\d\d\d\d\d\d\d\d\d\d", file_name):  # try to find a timestamp with 4 digit year and each 2 digits for month, day, hour, minute, second
        path += datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '_'
    path += file_name + file_appendix + '.csv'
    logger.info(str({"message": "Write dataset to file",
                     "path": path})
                )
    df.to_csv(path, index=False)

