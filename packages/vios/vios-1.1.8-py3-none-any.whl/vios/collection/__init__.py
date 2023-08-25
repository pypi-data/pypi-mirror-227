"""本模块主要由工具函数构成, 且依赖server
>>> tasks：实验描述
>>> support：兼容层，如与Scanner格式转换
>>> uapi：与前端进行交互，如matplotlib画图、数据库查询、实时画图等，详见各函数说明。
"""
import asyncio
import inspect
import json
import os
import pickle
import time
from collections import OrderedDict
from functools import cached_property
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import colors

_colors = tuple(colors.cnames)

import numpy as np
from kernel.sched import JupyterProgressBar, Progress
from kernel.sched.task import App
from quark import connect
from tqdm import tqdm
from waveforms import Waveform
from waveforms.scan_iter import StepStatus

from .. import startup

try:
    with open(Path(startup.get('site', '')) / 'etc/bootstrap.json', 'r') as f:
        cfg = json.loads(f.read())['executor']
except Exception as e:
    print(e)
    cfg = {"host": "127.0.0.1", "port": 2088}

print(cfg)
_s = connect('QuarkServer', host=cfg.get('host', '0.0.0.0'), port=cfg.get('port',2088))
_cs = connect('QuarkCanvas', port=2089)
vdict = OrderedDict()
LASTID = {'tid': 0, 'index': 0}


class Task(object):
    """适用于大量任务连续提交（如量子云），获取任务状态、结果、进度等。
    Args:
        task (dict): 任务描述
        timeout (float | None, optional):任务最大时长，默认为None，即任务执行完毕结束.

    任务样例见本模块下experiment。使用方法：
    >>> task = Task(s21) # s21 为experiment中字典描述
    >>> task.run()
    >>> task.bar() # 适用于notebook
    """

    handles = {}

    def __init__(self, task: dict, timeout: float | None = None) -> None:
        """_summary_

        Args:
            task (dict): _description_
            timeout (float | None, optional): _description_. Defaults to None.
        """
        self.task = task
        self.timeout = timeout

        self.data = {}
        self.meta = {}
        self.index = 0 # data areadly fetched

        self.progress = Progress()

    @cached_property
    def name(self):
        return self.task['metainfo'].get('name', 'Unknown')

    def run(self):
        self.stime = time.time()  # start time
        try:
            circuit = self.task['taskinfo']['CIRQ']
            if isinstance(circuit, list) and callable(circuit[0]):
                circuit[0] = inspect.getsource(circuit[0])
        except Exception as e:
            print(e)
        self.taskid = _s.submit(self.task)

    def cancel(self):
        _s.cancel(self.taskid)
        # self.clear()

    def save(self):
        _s.save(self.taskid)

    def result(self):
        meta = True if not self.meta else False
        res = _s.fetch(self.taskid, start=self.index, meta=meta)

        if isinstance(res, str):
            return self.data
        elif isinstance(res, tuple):
            if isinstance(res[0], str):
                return self.data
            data, self.meta = res
        else:
            data = res
        self.index += len(data)
        # data.clear()
        self.process(data)

        return self.data

    def status(self, key: str = 'runtime'):
        if key == 'runtime':
            return _s.track(self.taskid)
        elif key == 'compile':
            return _s.apply('status', user='task')
        else:
            return 'supported arguments are: {rumtime, compile}'

    def report(self):
        return _s.report(self.taskid)

    def step(self, index: int, stage: str = 'raw'):
        if stage in ['ini', 'raw']:
            return _s.review(self.taskid, index)[stage]
        elif stage in ['debug', 'trace']:
            return _s.track(self.taskid, index)[stage]

    def process(self, data: list[dict]):
        for dat in data:
            for k, v in dat.items():
                if k in self.data:
                    self.data[k].append(v)
                else:
                    self.data[k] = [v]

    def join(self):
        try:
            self.result()
        except Exception as e:
            print(e)

        try:
            status = self.status()['status']
            if status in ['Pending']:
                time.sleep(2)
                self.join()
            self.progress.max = self.report()['size']
        except Exception as e:
            print(e, status, self.report())
            time.sleep(1)
            self.join()

        if status in ['Failed', 'Canceled']:
            return self.stop(self.taskid, False)
        elif status in ['Running']:
            # if self.index == self.progress.max:
            #     self.save()
            # else:
            self.progress.goto(self.index)
        elif status in ['Finished', 'Archived']:
            self.progress.goto(self.progress.max)
            if hasattr(self, 'app'):
                self.app.save()

        # if self.index and self.index == self.progress.max:
            return self.stop(self.taskid)

        if isinstance(self.timeout, float):
            if self.timeout > 0 and (time.time() - self.stime > self.timeout):
                msg = f'Timeout: {self.timeout}'
                print(msg)
                raise TimeoutError(msg)
            time.sleep(2)
            self.join()
        else:
            self.handles[self.taskid] = asyncio.get_running_loop(
            ).call_later(2, self.join)

    def clear(self):
        for tid, handle in self.handles.items():
            self.stop(tid)

    def stop(self, tid: int, success: bool = True):
        try:
            self.progress.finish(success)
            self.handles[tid].cancel()
        except Exception as e:
            # print(e)
            pass

    def bar(self):
        # self.stop(self.taskid)
        bar = JupyterProgressBar(description=self.name)
        bar.listen(self.progress)
        bar.display()
        self.join()


def submit(app: App, block: bool = False, path: str | Path = Path.cwd(), encoding: bool = True):
    """转换继承自App的任务为server可执行任务

    Args:
        app (App): 任务基类

    Args:
        app (App): 任务基类
        path (str | Path, optional): 线路读写路径. Defaults to Path.cwd().
        encoding (bool, optional): 是否序列化. Defaults to False.

    Raises:
        TypeError: _description_
    """
    app.toserver = 'ready'
    app.run(dry_run=True, quiet=True)
    time.sleep(3)

    loop, index = [], ()
    filepath = Path(path)/f'{app.name.replace(".","_")}.cirq'
    with open(filepath, 'w', encoding='utf-8') as f:
        for step in tqdm(app.circuits(), desc='CircuitExpansion'):
            if isinstance(step, StepStatus):
                cc = step.kwds['circuit']
                if not encoding:
                    f.writelines(str(cc)+'\n')
                else:
                    f.writelines(str(pickle.dumps(cc))+'\n')
                loop.append(step.iteration)
                index = step.index
            else:
                raise TypeError('Wrong type of step!')
    app.datashape = [i+1 for i in index]
    # return

    deps = []
    for k, v in app.mapping.items():
        deps.append(f'<{k}>={app[v]}')

    sample = _s.query('station.sample')
    trigger = _s.query('station.triggercmds')
    init = [(f'{t.split(".")[0]}.CH1.Shot', app.shots, 'any') for t in trigger]

    toserver = Task(dict(metainfo={'name': f'{sample}:/{app.name.replace(".","_")}', 'tid': app.id,
                                   'priority': app.task_priority, 'user': 'kernel',
                                   'other': {'shots': app.shots, 'signal': app.signal, 'lib': app.lib,
                                             'align_right': app.align_right,
                                             'waveform_length': app.waveform_length}},

                         taskinfo={'STEP': {'main': ['WRITE', ('loop',)],
                                            'trigger': ['WRITE', 'trig'],
                                            'READ': ['READ', 'read'],
                                            },
                                   'INIT': init,
                                   'RULE': deps,
                                   'CIRQ': str(filepath.resolve()),
                                   'LOOP': {'loop': [('index', np.asarray(loop), 'au')],
                                            'trig': [(t, 0, 'au') for t in trigger]
                                            }
                                   }))
    toserver.timeout = 1e9 if block else None
    toserver.app = app
    app.toserver = toserver
    app.run()


def showave(task: Task, step: int = 0,
            start: float = 0, stop: float = 99e-6, sample_rate: float = 6e9,
            keys: tuple = ('Q0',), stage: str = 'ini', backend: str = 'mpl'):
    cmds = task.step(step, stage=stage)['main']

    _stop = round(stop * sample_rate)
    _start = round(start * sample_rate)
    # n = round((stop - start) * sample_rate)
    xt = np.arange(_stop - _start) / sample_rate + start

    wdict = {}
    if stage in ['ini', 'raw']:
        for target, (ctype, value, unit, kwds) in cmds.items():
            if kwds['target'].split('.')[0] not in keys:  # qubit name
                continue
            if isinstance(value, Waveform):
                wdict[target] = value(xt)
    elif stage in ['debug', 'trace']:
        for dev, chqval in cmds.items():
            if dev not in keys:  # device name
                continue
            for chq, value in chqval.items():
                if chq.endswith('Waveform'):
                    wdict[f'{dev}.{chq}'] = value[_start:_stop]

    if backend == 'mpl':
        sdict = {k: wdict[k] for k in sorted(wdict)}
        plt.figure()
        for i, (target, wave) in enumerate(sdict.items()):
            plt.plot(xt, wave+i*0)
        plt.legend(list(sdict))
    else:
        sdict = {k: {'data': (xt, wdict[k]),'color': colors.to_rgb(_colors[i+10])} for i,k in enumerate(sorted(wdict))}
        _cs.plot([[sdict]])
