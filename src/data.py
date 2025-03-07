# data.py
#
# Copyright 2025 João Pastorello
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from pathlib import Path

import gi
try:
    from gi.repository import GLib
except ImportError or ValueError as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)

import pandas as pd


def get_platform_display_name(true_name):
    match true_name:
        case "combined":
            return "Windows, Mac and Linux"
        case "pc":
            return "Windows Only"
        case "mac":
            return "Mac Only"
        case "linux":
            return "Linux Only"


def process_category(true_name):
    if (true_name[:3] == "Mac"):
        true_name = true_name.replace("Mac", "OSX")
    return true_name.split('(')[0].strip()


class Data():

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path = Path(GLib.get_system_data_dirs()[0],
                         "surveam", "surveam", "data")

    def _get_name_mapping(self, name):
        name = name.replace('"', '')
        return self.mappings.get(name, name)

    def _load_mappings(self):
        path = Path(self.path, 'mapping.csv')
        self.mappings = pd.read_csv(path, index_col=0, header=None,
                                    sep=";", engine='c').to_dict()[1]

    def _setup_df(self):
        self.name_index = self.df.index.get_level_values("name")
        self.date_index = self.df.index.get_level_values("date")
        self.platform_index = self.df.index.get_level_values("platform")
        self.category_index = self.df.index.get_level_values("category")

    def load_from_parquet(self):
        path = Path(self.path, 'processed.parquet')
        self.df = pd.read_parquet(path)
        self._setup_df()

    def save_to_parquet(self):
        path = Path(self.path, 'processed.parquet')
        self.df.to_parquet(path)

    def _load_combined_csv(self):
        path = Path(self.path, 'shs.csv')

        df = pd.read_csv(path,
                         na_filter=False,
                         engine='c',
                         parse_dates=[0],
                         dtype={},
                         usecols=["category", "name", "date", "percentage"],
                         converters={'name': self._get_name_mapping,
                                     'category': process_category})

        df.insert(0, "platform", "Windows, Mac and Linux")
        df = df.set_index(["platform", "category", "name", "date"])

        return df

    def _load_platforms_csv(self):
        path = Path(self.path, 'shs_platform.csv')

        df = pd.read_csv(path,
                         na_filter=False,
                         engine='c',
                         parse_dates=[0],
                         index_col=["platform", "category", "name", "date"],
                         dtype={},
                         usecols=["platform", "category", "name",
                                  "date", "percentage"],
                         converters={'name': self._get_name_mapping,
                                     'platform': get_platform_display_name,
                                     'category': process_category})

        return df

    def _process_original_data(self, cdf, pdf):
        cdf_dates = cdf.index.get_level_values("date")
        cdf_categories = cdf.index.get_level_values("category")

        old_pdf = cdf[cdf_dates < '2010-05-01'].rename(
            index={"Windows, Mac and Linux": "Windows Only"}, level="platform")

        list = ["AMD CPU Speeds", "NVIDIA Drivers", "Multi-GPU Systems",
                "MSAA Support Level", "Video Card Driver Name",
                "Processor Vendor", "DirectX 10 GPUs", "Audio Devices",
                "DirectX 10 Systems", "ATI Drivers",
                "DirectX 9 Shader Model 2b and 3.0 GPUs",
                "DirectX 9 Shader Model 2.0 GPUs", "DirectX 11 Systems",
                "DirectX 11 GPUs", "Drive Type"]

        cdf = cdf[(~cdf_categories.isin(list))
                  | (cdf_dates > '2010-05-01')].rename(
                    index={"Windows Version": "OS Version"}, level="category")

        df = pd.concat([cdf, old_pdf, pdf])

        df = df.groupby(["platform", "category", "name", "date"]).sum()

        df = df.sort_index()

        return df

    def load_from_original_csvs(self):
        self._load_mappings()

        cdf = self._load_combined_csv()
        pdf = self._load_platforms_csv()

        self.df = self._process_original_data(cdf, pdf)
        self._setup_df()

    def get_platforms(self):
        return self.platform_index.drop_duplicates().sort_values(ascending=False).tolist()

    def get_categories(self, platform):
        return self.category_index[self.platform_index == platform].drop_duplicates().sort_values().tolist()

    def get_dates(self, platform, category):
        return self.date_index[(self.platform_index == platform) &
            (self.category_index == category)].drop_duplicates().sort_values().astype(str).tolist()

    def get_category_data(self, platform, category, start_moment, end_moment):
        return self.df.loc[(self.date_index >= start_moment) &
            (self.date_index <= end_moment)].xs((platform, category))
