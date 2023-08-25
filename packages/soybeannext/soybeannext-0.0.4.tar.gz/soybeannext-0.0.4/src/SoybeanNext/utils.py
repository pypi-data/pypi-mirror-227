import os
import time
import sys
sys.path.append(".")
from reader import Reader
from forward import Forward
from tqdm import tqdm
import requests


def run(df_path, trait_list, batch_size, output=True):
    r = Reader()  # instantiate class Reader
    s = time.time()
    df = r.readVCF(rf"{df_path}")  # get the processed dataframe
    e = time.time()
    print(f"readVCF————{e - s:.2f}s")
    s = time.time()
    df_filter, isMissing = r.SNPfilter(df)  # get the filtered dataframe
    e = time.time()
    print(f"SNPfilter————{e - s:.2f}s")
    s = time.time()
    index_list, sample_resized = r.one_hot(df_filter)  # convert to one-hot matrix and resize every samples
    e = time.time()
    print(f"one_hot————{e - s:.2f}s")
    s = time.time()
    f = Forward(trait_list)  # instantiate class Forward
    df = f.forward(index_list, sample_resized, batch_size)  # predict and get results
    e = time.time()
    print(f"forward————{e - s: .2f}s")
    if output:
        f.output_dataframe(df)
    return isMissing

# in this module, an example file with 10 samples could be downloaded
# more examples would be added in future
def download_example(example_index=0):
    url = "http://xtlab.hzau.edu.cn/"
    # set an example file folder
    path = 'example/'
    os.makedirs(path, exist_ok=True)
    example_list = ['10_test_examples.vcf']
    # name of the example file
    name = example_list[example_index]
    # the total size of this model
    response = requests.get(url + name)
    total_size = int(response.headers.get('content-length', 0))
    # download with progress bar by tqdm and requests
    with open(path + name, 'wb') as file, tqdm(
            desc=name,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

