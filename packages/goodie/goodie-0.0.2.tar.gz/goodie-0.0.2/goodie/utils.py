import random
import pandas as pd
import re
import os
import os.path as ops
import json
import numpy as np
from tqdm import tqdm
from glob import glob
import collections
import math
from functools import partial
import time
import six

zh_re = re.compile('[\u4e00-\u9fa5]')


def read_json(file):
    with open(file, encoding='rb') as f:
        return json.load(f)


def write_json(file, path):
    with open(path, 'wb') as f:
        json.dump(file, f)


def read_json_lines(file, lazy=False):
    if lazy:
        return (json.loads(line) for line in open(file, 'r', encoding='utf-8'))
    return [json.loads(x) for x in open(file, encoding='utf-8')]


def write_json_line(line, f):
    line = json.dumps(line, ensure_ascii=False) + '\n'
    f.write(line)


def write_json_lines(lines, path, mode='w+'):
    with open(path, mode, encoding='utf-8') as f:
        for line in lines:
            write_json_line(line, f)


def random_split_list(data, frac=0.8, random_state=None):
    if random_state is None:
        random.seed(random_state)
    random.shuffle(data)
    return data[:int(len(data) * frac)], data[int(len(data) * frac):]


def kfold_split_json_lines(lines, folds, output_dir, key=None, use_value=False, pre_key=None, overwrite=True):
    check_dir(output_dir, overwrite)

    new_lines = []
    for line in lines:
        tmp = line if pre_key is None else line[pre_key]
        if key is not None:
            gp_key = tmp[key]
        else:
            gp_key = list(tmp.keys())[0]
        new_lines.append({'gp_key': gp_key, 'data': line})
    df = pd.DataFrame(new_lines)
    for _, df_gp in df.groupby('gp_key'):
        fold_idx = list(range(folds)) * (len(df_gp) // folds + 1)
        df_gp['fold'] = fold_idx[:len(df_gp)]
        for i in range(folds):
            train = df_gp[df_gp.fold != i]
            dev = df_gp[df_gp.fold == i]
            train_lines = train.data
            dev_lines = dev.data
            write_json_lines(train_lines, osp.join(output_dir, 'train{}.json', ).format(i), 'a+')
            write_json_lines(dev_lines, osp.join(output_dir, 'dev{}.json').format(i), 'a+')


def stratified_sampling(df, by, test_frac=None, test_num=None, random_state=None):
    df.index = range(len(df))
    test_idx = []
    if test_num:
        test_frac = test_num / df.shape[0]
    for by, df_gp in df.groupby(by):
        test_idx += list(df_gp.sample(frac=test_frac, random_state=random_state).index)
    test = df[df.index.isin(test_idx)]
    train = df[~df.index.isin(test_idx)]
    return train, test


def sequence_padding(inputs, length=None, value=0, seq_dims=1, mode='post', dtype='int64'):
    if length is None:
        length = np.max([np.shape(x)[:seq_dims] for x in inputs], axis=0)
    elif not hasattr(length, '__getitem__'):
        length = [length]

    slices = [np.s_[:length[i]] for i in range(seq_dims)]
    slices = tuple(slices) if len(slices) > 1 else slices[0]
    pad_width = [(0, 0) for _ in np.shape(inputs[0])]

    outputs = []
    for x in inputs:
        x = x[slices]
        for i in range(seq_dims):
            if mode == 'post':
                pad_width[i] = (0, length[i] - np.shape(x)[i])
            elif mode == 'pre':
                pad_width[i] = (length[i] - np.shape(x)[i], 0)
            else:
                raise ValueError('"mode" argument must be "post" or "pre".')
        x = np.pad(x, pad_width, 'constant', constant_values=value)
        outputs.append(x)
    return np.array(outputs, dtype=dtype)


class AverageMeter:
    def __init__(self):
        self.total = 0
        self.n = 0

    def update(self, item):
        self.total += item
        self.n += 1

    def accumulate(self):
        return self.total / self.n

    def reset(self):
        self.total = 0
        self.n = 0


def print_item(alist):
    for i in alist:
        print(i)


def label2id(alist):
    alist = sorted(set(alist))
    return dict(zip(alist, range(len(alist))))


def has_zh(s):
    return zh_re.search(s)


def check_dir(out_dir, overwrite=False):
    if osp.exists(out_dir) and overwrite:
        import shutil
        shutil.rmtree(out_dir)
    if not osp.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)


def desc_len(data):
    if isinstance(data[0], dict):
        data = [item['text'] for item in data]
    return pd.Series([len(item) for item in data]).describe()


def batch_generator(data, batch_size):
    batch = []
    for item in data:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if len(batch) > 0:
        yield batch


def split_text(text, seps='。\n！'):
    ret = []
    start = 0
    for i, v in enumerate(text):
        if i > start and v in seps:
            ret.append(text[start:i + 1])
            start = i + 1
    if start < len(text):
        ret.append(text[start:])


def merge_segment(texts, max_len=512, stride=0):
    ret = []
    cur = collections.deque()
    cur_len = 0
    for text in texts:
        cur.append(text)
        cur_len += len(text)
        if cur_len >= max_len:
            ret.append(''.join(cur))
            while cur_len > stride:
                cur_len -= len(cur.popleft())
    if cur:
        if ''.join(cur) not in ret:
            ret.append(''.join(cur))
    return ret


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"函数 {func.__name__} 的执行时间为：{execution_time} 秒")
        return result

    return wrapper


def parallel_apply_generator(
        func, iterable, workers, max_queue_size, dummy=False, random_seeds=True
):
    """多进程或多线程地将func应用到iterable的每个元素中。
    注意这个apply是异步且无序的，也就是说依次输入a,b,c，但是
    输出可能是func(c), func(a), func(b)。结果将作为一个
    generator返回，其中每个item是输入的序号以及该输入对应的
    处理结果。
    参数：
        dummy: False是多进程/线性，True则是多线程/线性；
        random_seeds: 每个进程的随机种子。
    """
    if dummy:
        from multiprocessing.dummy import Pool, Queue
    else:
        from multiprocessing import Pool, Queue

    in_queue, out_queue, seed_queue = Queue(max_queue_size), Queue(), Queue()
    if random_seeds is True:
        random_seeds = [None] * workers
    elif random_seeds is None or random_seeds is False:
        random_seeds = []
    for seed in random_seeds:
        seed_queue.put(seed)

    def worker_step(in_queue, out_queue):
        """单步函数包装成循环执行
        """
        if not seed_queue.empty():
            np.random.seed(seed_queue.get())
        while True:
            i, d = in_queue.get()
            r = func(d)
            out_queue.put((i, r))

    # 启动多进程/线程
    pool = Pool(workers, worker_step, (in_queue, out_queue))

    # 存入数据，取出结果
    in_count, out_count = 0, 0
    for i, d in enumerate(iterable):
        in_count += 1
        while True:
            try:
                in_queue.put((i, d), block=False)
                break
            except six.moves.queue.Full:
                while out_queue.qsize() > max_queue_size:
                    yield out_queue.get()
                    out_count += 1
        if out_queue.qsize() > 0:
            yield out_queue.get()
            out_count += 1

    while out_count != in_count:
        yield out_queue.get()
        out_count += 1

    pool.terminate()


def parallel_apply(
        func,
        iterable,
        workers,
        max_queue_size,
        callback=None,
        dummy=False,
        random_seeds=True,
        unordered=True
):
    """多进程或多线程地将func应用到iterable的每个元素中。
    注意这个apply是异步且无序的，也就是说依次输入a,b,c，但是
    输出可能是func(c), func(a), func(b)。
    参数：
        callback: 处理单个输出的回调函数；
        dummy: False是多进程/线性，True则是多线程/线性；
        random_seeds: 每个进程的随机种子；
        unordered: 若为False，则按照输入顺序返回，仅当callback为None时生效。
    """
    generator = parallel_apply_generator(
        func, iterable, workers, max_queue_size, dummy, random_seeds
    )

    if callback is None:
        if unordered:
            return [d for i, d in generator]
        else:
            results = sorted(generator, key=lambda d: d[0])
            return [d for i, d in results]
    else:
        for i, d in generator:
            callback(d)
