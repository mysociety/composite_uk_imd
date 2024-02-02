import composite_uk_imd

import pytest

from pathlib import Path
import pandas as pd

packages_path = Path(__file__).parent.parent / "data" / "packages"


def test_all_cons():
    """
    Test we have the right number of LAs
    """
    df = pd.read_csv(packages_path / "uk_index" / "constituency_imd.csv")
    no_dupes = df["gss-code"].drop_duplicates()
    assert len(no_dupes) == 650


def test_all_las():
    """
    Test we have the right number of LAs
    """
    df = pd.read_csv(packages_path / "uk_index" / "la_imd.csv")
    no_dupes = df["local-authority-code"].drop_duplicates()
    assert len(no_dupes) == 394


def test_all_lsoas():
    """
    Test we have the right number of lsoa
    """
    df = pd.read_csv(packages_path / "uk_index" / "UK_IMD_E.csv")
    no_dupes = df["lsoa"].drop_duplicates()
    assert len(no_dupes) == 42619
