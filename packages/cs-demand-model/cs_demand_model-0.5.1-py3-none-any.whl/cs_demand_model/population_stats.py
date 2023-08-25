from datetime import date
from functools import lru_cache

import numpy as np
import pandas as pd

from cs_demand_model.config import Config


class PopulationStats:
    def __init__(self, df: pd.DataFrame, config: Config):
        self.__df = df
        self.__config = config

    @property
    def df(self):
        return self.__df

    @property
    def config(self) -> Config:
        return self.__config

    @property
    def stock(self):
        """
        Calculates the daily transitions for each age bin and placement type by
        finding all the transitions (start or end of episode), summing to get total populations for each
        day and then resampling to get the daily populations.
        """
        df = self.df.copy()
        df["bin"] = df.apply(lambda c: (c.age_bin.name, c.placement_type.name), axis=1)
        endings = df.groupby(["DEC", "bin"]).size()
        endings.name = "nof_decs"

        beginnings = df.groupby(["DECOM", "bin"]).size()
        beginnings.name = "nof_decoms"

        endings.index.names = ["date", "bin"]
        beginnings.index.names = ["date", "bin"]

        pops = pd.merge(
            left=beginnings,
            right=endings,
            left_index=True,
            right_index=True,
            how="outer",
        )

        pops = pops.fillna(0).sort_values("date")

        pops = (pops["nof_decoms"] - pops["nof_decs"]).groupby(["bin"]).cumsum()

        pops = pops.unstack(level=1)

        # Resample to daily counts and forward-fill in missing days
        pops = pops.resample("D").first().fillna(method="ffill").fillna(0)

        # Add the missing age bins and fill with zeros
        # pops = pops.T.reindex(self.__config.states(as_index=True)).T.fillna(0)

        return pops

    @lru_cache(maxsize=5)
    def stock_at(self, start_date):
        start_date = pd.to_datetime(start_date)

        index = self.stock.index.get_indexer([start_date], method="nearest")

        stock = self.stock.iloc[index[0]].T
        stock.name = start_date
        return stock

    @property
    def transitions(self):
        transitions = self.df.copy()
        transitions["start_bin"] = transitions.apply(
            lambda c: (c.age_bin.name, c.placement_type.name), axis=1
        )
        transitions["end_bin"] = transitions.apply(
            lambda c: (c.age_bin.name, c.placement_type_after.name), axis=1
        )
        transitions = transitions.groupby(["start_bin", "end_bin", "DEC"]).size()
        transitions = (
            transitions.unstack(level=["start_bin", "end_bin"])
            .fillna(0)
            .asfreq("D", fill_value=0)
        )

        return transitions

    @lru_cache(maxsize=5)
    def raw_transition_rates(self, start_date: date, end_date: date):
        # Ensure we can calculate the transition rates by aligning the dataframes
        stock = self.stock.truncate(before=start_date, after=end_date)
        stock.columns.name = "start_bin"
        transitions = self.transitions.truncate(before=start_date, after=end_date)

        # Calculate the transition rates
        stock, transitions = stock.align(transitions)
        transition_rates = transitions / stock.shift(1).fillna(method="bfill")
        transition_rates = transition_rates.fillna(0)

        # Use the mean rates
        transition_rates = transition_rates.mean(axis=0)
        transition_rates.name = "transition_rate"

        return transition_rates

    @lru_cache(maxsize=5)
    def daily_entrants(self, start_date: date, end_date: date) -> pd.Series:
        """
        Returns the number of entrants and the daily_probability of entrants for each age bracket and placement type.
        """
        PlacementCategories = self.__config.PlacementCategories
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        df = self.df

        # Only look at episodes starting in analysis period
        df = df[(df["DECOM"] >= start_date) & (df["DECOM"] <= end_date)].copy()

        df["to"] = df.apply(lambda c: (c.age_bin.name, c.placement_type.name), axis=1)

        # Group by age bin and placement type
        df = (
            df[df["placement_type_before"] == PlacementCategories.NOT_IN_CARE]
            .groupby(["to"])
            .size()
        )
        df.name = "entrants"

        # Reset index
        df = df.reset_index()

        df["period_duration"] = (end_date - start_date).days
        df["daily_entry_probability"] = df["entrants"] / df["period_duration"]
        df["from"] = df.period_duration.apply(lambda x: tuple())

        df = df.set_index(["from", "to"])

        return df.daily_entry_probability

    def to_excel(self, output_file: str, start_date: date, end_date: date):
        with pd.ExcelWriter(output_file) as writer:
            self.stock_at(end_date).to_excel(writer, sheet_name="population")
            self.raw_transition_rates(start_date, end_date).to_excel(
                writer, sheet_name="transition_rates"
            )
            self.daily_entrants(start_date, end_date).to_excel(
                writer, sheet_name="daily_entrants"
            )
