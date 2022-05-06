import logging
import os
import zipfile
from argparse import ArgumentParser
from dataclasses import dataclass
from os import path
from typing import List, Dict

import pandas as pd

log = logging.getLogger(__name__)

CSV_NAME = 'fault_detector_results.csv'
IMG_APPENDIX = '_original.png'


@dataclass
class DetectionBox:
    fault_id: str
    x0: int
    x1: int
    y0: int
    y1: int
    cls: str
    score: float = -1

    def to_coords(self) -> List[List[int]]:
        return [[self.x0, self.y0], [self.x1, self.y0], [self.x1, self.y1],
                [self.x0, self.y1], [self.x0, self.y0]]

    def to_pascal_voc(self):
        return [self.x0, self.x1, self.y0, self.y1]


class Sample:
    timestamp: str
    filepath: str
    platform_id: str
    channel_id: str

    num_detections: int

    bbox = List[DetectionBox]

    @staticmethod
    def from_dataframe(df: pd.DataFrame, file_path: str) -> 'Sample':
        sample = Sample()
        sample.timestamp = df.TIMESTAMP
        sample.platform_id = 'UNKNOWN'
        sample.channel_id = df.CHANNEL_ID
        sample.filepath = file_path
        sample.bbox = [DetectionBox(df.FAULT_UUID,
                                    df.FAULT_X0, df.FAULT_X1,
                                    df.FAULT_Y0, df.FAULT_Y1,
                                    df.CLASS, df.DEFECT_SCORE)]
        sample.num_detections = 1

        return sample

    def append_bbox(self, df: pd.DataFrame):
        self.bbox.append(DetectionBox(df.FAULT_UUID,
                                      df.FAULT_X0, df.FAULT_X1,
                                      df.FAULT_Y0, df.FAULT_Y1,
                                      df.CLASS, df.DEFECT_SCORE))
        self.num_detections += 1


class Reader:
    _csv_files: List[str]
    _dirs_with_csv: List[str]
    _dir_to_file: Dict[str, Dict[str, str]]

    @property
    def samples(self) -> List[Sample]:
        all_samples = list()

        for i, csv_file in enumerate(self._csv_files):
            samples = {}
            dir_ = self._dirs_with_csv[i]
            files = self._dir_to_file[dir_]

            df = pd.read_csv(self.open(csv_file), header=1)
            df = _preprocess_df(df)

            # create samples with multiple bboxes
            for row in df.itertuples():
                if row.TIMESTAMP in samples:
                    samples[row.TIMESTAMP].append_bbox(row)
                else:
                    samples[row.TIMESTAMP] = \
                        Sample.from_dataframe(row, files[row.TIMESTAMP])

            samples_wo_bbox = list(set(files.keys()) - set(samples.keys()))
            log.info(f'Found {len(samples_wo_bbox)} without faults.')

            log.info(f'Processed {len(samples)} samples for '
                     f'{path.split(dir_)[-1]}.')

            all_samples += list(samples.values())

        return all_samples

    def open(self, file_path: str):
        raise NotImplementedError


class ZipReader(Reader):
    def __init__(self, zip_path: str):
        self._zip_path = zip_path
        try:
            self._file = zipfile.ZipFile(zip_path)
        except zipfile.BadZipfile as e:
            raise RuntimeError(e)

        self._dirs_with_csv = list()
        self._csv_files = list()
        self._dir_to_file = dict()

        self._parse_zip()

    def _parse_zip(self):
        self._csv_files = [o.filename for o in self._file.filelist
                           if o.filename.endswith(CSV_NAME)]

        self._dirs_with_csv = [path.split(o)[0] for o in self._csv_files]

        self._dir_to_file = {
            dir_: {
                '_'.join(path.split(o.filename)[-1].split('_')[:2]): o.filename
                for o in self._file.filelist if
                o.filename.startswith(dir_) and o.filename.endswith(
                    IMG_APPENDIX)} for dir_ in self._dirs_with_csv}

    @property
    def dataframe(self) -> pd.DataFrame:
        dfs = []

        for csv_file in self._csv_files:
            dfs.append(pd.read_csv(self._file.open(csv_file),
                                   header=1))

        return pd.concat(dfs)

    def open(self, file_path: str):
        return self._file.open(file_path)


class WorkspaceReader(Reader):
    def __init__(self, workspace_path: str):
        self._workspace_path = workspace_path

        self._parse_workspace()

    def _parse_workspace(self):
        root_path = self._workspace_path
        while not any([o == CSV_NAME for o in os.listdir(root_path)]):
            dir_ = [o for o in os.listdir(root_path)
                    if path.isdir(path.join(root_path, o))][0]
            root_path = path.join(root_path, dir_)

        root_path = path.split(path.abspath(root_path))[0]

        self._csv_files = list()
        self._dirs_with_csv = list()
        self._dir_to_file = dict()

        for dir_ in os.listdir(root_path):
            subdir = path.join(root_path, dir_)
            files = os.listdir(subdir)
            if CSV_NAME not in os.listdir(subdir):
                continue

            self._csv_files.append(path.join(subdir, CSV_NAME))
            self._dirs_with_csv.append(subdir)

            self._dir_to_file[subdir] = {
                '_'.join(path.split(o)[-1].split('_')[:2]): path.join(subdir,
                                                                      o)
                for o in files if o.endswith(IMG_APPENDIX)
            }

    def open(self, file_path: str):
        return open(file_path, 'rb')


def _preprocess_df(df: pd.DataFrame):
    df['FAULT_X0'] *= df['IMG_W']
    df['FAULT_X1'] *= df['IMG_W']
    df['FAULT_Y0'] *= df['IMG_H']
    df['FAULT_Y1'] *= df['IMG_H']

    df['FAULT_Y0'] -= df['RH_Y0']
    df['FAULT_Y1'] -= df['RH_Y0']

    for key in ('FAULT_X0', 'FAULT_X1', 'FAULT_Y0', 'FAULT_Y1',
                'FAULT_X0_RH', 'FAULT_X1_RH', 'FAULT_Y0_RH', 'FAULT_Y1_RH'):
        df[key] = df[key].apply(lambda x: int(float(x)))

    df['TIMESTAMP'] = df['FILENAME'] \
        .apply(lambda x: '_'.join(x.split('_')[:2]))

    return df


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('zip_file', help='Path to .zip file')
    args = parser.parse_args()

    reader = ZipReader(args.zip_file)
    reader.samples
    print()
