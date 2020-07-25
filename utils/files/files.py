import os
from datetime import datetime, timedelta
from typing import List, Dict, Union

from sortedcontainers import SortedDict


class File:
    def __init__(self):
        self.path: str = None
        self.creationDatetime: datetime = None
        self.startTimedelta: timedelta = None
        self.endTimedelta: timedelta = None

    @property
    def startDatetime(self) -> datetime:
        return self.creationDatetime + self.startTimedelta
        
    @property
    def endDatetime(self) -> datetime:
        return self.creationDatetime + self.endTimedelta

    def __str__(self):
        return f"self.path creationDatetime {self.creationDatetime.isoformat()}"


class FileTraveler:
    """
    ft = FileTraveler(".", true)
    for path in ft:
        print(path)
    """

    def __init__(self, rootPath: str, ext: str, recurrent: bool):
        assert os.path.isdir(rootPath)
        assert ext[0] == '.'
        self.root = rootPath
        self.ext = ext.lower()
        self.recurrent = recurrent

    def _findFile(self, folder: str):
        for f in os.listdir(folder):
            path = os.path.join(folder, f)
            if not os.path.isdir(path) and os.path.splitext(f)[1].lower() == self.ext:
                yield path

    def _findFileRecurrent(self, folder: str):
        for f in os.listdir(folder):
            path = os.path.join(folder, f)
            if os.path.isdir(path):
                for file in self._findFileRecurrent(path):
                    yield file
            elif os.path.splitext(f)[1].lower() == self.ext:
                yield path

    def __iter__(self):
        if self.recurrent:
            return self._findFileRecurrent(self.root)
        else:
            return self._findFile(self.root)


class FileList:
    '''
    file list
    '''

    def __init__(self):
        # creation datetime -> File
        self.datetimeDict: Dict[datetime, File] = SortedDict()
        self.pathDict: Dict[str, File] = dict()

    def _crossed(self, start: datetime, end: datetime) -> (bool, File):
        datetimeDict = self.datetimeDict
        index = datetimeDict.bisect_left(start)
        if index > 0:
            k, v = datetimeDict.peekitem(index - 1)
            if v.endDatetime > start:
                return (True, v)
        if index < len(datetimeDict):
            k, v = datetimeDict.peekitem(index)
            if k < end:
                return (True, v)
        return (False, None)

    def addFile(self, file: File):
        '''
        if add same file with file in datetimeDict, return false
        if added file have crossed time range with file in datetimeDict, raise ValueError
        else return True
        '''
        crossed, crossedFile = self._crossed(
            file.startDatetime,file.endDatetime)
        if crossed:
            raise ValueError('file "%s" and "%s" have crossed scan time' % (
                file, crossedFile))

        self.datetimeDict[file.creationDatetime] = file
        self.pathDict[file.path] = file

    def rmFile(self, filepath):
        f: File = self.pathDict.pop(filepath, None)
        if f == None:
            return
        self.datetimeDict.pop(f.creationDatetime)

    def subList(self, filepathsOrTime: List[Union[str, datetime]]):
        subList = FileList()
        for pot in filepathsOrTime:
            if isinstance(pot, str):
                if pot in self.pathDict:
                    subList.addFile(self.pathDict[pot])
            elif isinstance(pot, datetime):
                if pot in self.datetimeDict:
                    subList.addFile(self.pathDict[pot])
        return subList

    def clear(self):
        self.pathDict.clear()
        self.datetimeDict.clear()

    def timeRange(self):
        datetimeDict = self.datetimeDict
        if len(self.datetimeDict) > 0:
            l: File = datetimeDict.peekitem(0)[1]
            r: File = datetimeDict.peekitem(-1)[1]
            return (l.startDatetime, r.endDatetime)
        else:
            return None

    def keys(self):
        return self.datetimeDict.keys()

    def values(self):
        return self.datetimeDict.values()

    def items(self):
        return self.datetimeDict.items()

    def __len__(self):
        return len(self.datetimeDict)

    def __iter__(self):
        return iter(self.datetimeDict)

    def __getitem__(self, timeOrPath: Union[datetime, str]):
        if isinstance(timeOrPath, datetime):
            return self.datetimeDict[timeOrPath]
        elif isinstance(timeOrPath, str):
            return self.pathDict[timeOrPath]
        else:
            raise TypeError(timeOrPath)

    def __contains__(self, timeOrPath: Union[datetime, str]):
        if isinstance(timeOrPath, datetime):
            return timeOrPath in self.datetimeDict
        elif isinstance(timeOrPath, str):
            return timeOrPath in self.pathDict
        else:
            raise TypeError(timeOrPath)
