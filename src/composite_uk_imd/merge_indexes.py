from xxlimited import Str
import pandas as pd
import numpy as np
import yaml
import json
from sklearn import linear_model
from pathlib import Path
from typing import Literal

package_dir = Path("data", "packages")

_allowed_indexes = Literal["uk", "gb"]
_component_indexes = Literal["E", "S", "W", "N"]

important_columns = ["lsoa", "overall_score", "income_score", "employment_score"]

# can't use both for 2017 NI annoyingly
gb_predictors = ["income_score", "employment_score"]
uk_predictors = ["employment_score"]

nice_nation = {"N": "Northern Ireland", "S": "Scotland", "W": "Wales", "E": "England"}


def get_country_info() -> dict[str, dict[str, str]]:
    with open(Path("data", "join_description.yaml")) as file:
        countries = yaml.load(file, Loader=yaml.FullLoader)
    return countries


def get_dataset(nation: str):
    """
    load source from yaml and process to consistent format
    """
    info = get_country_info()[nation]
    df = pd.read_csv(Path("data", info["source_file"]))
    rename = {info[x]: x for x in important_columns}
    df = df.rename(columns=rename)
    df["nation"] = nation
    df = df[["nation"] + important_columns]

    if info["adjustment"] == "domains_times_100":
        df["income_score"] = df["income_score"] * 100
        df["employment_score"] = df["employment_score"] * 100

    return df


def make_model(df: pd.DataFrame, setting: _allowed_indexes = "uk"):
    """
    create linear regression for nation
    """
    y = df["overall_score"]
    if setting == "uk":
        predictors = uk_predictors
    else:
        predictors = gb_predictors
    x = df[predictors]
    model = linear_model.LinearRegression()
    reg = model.fit(x, y)

    predicted_values = reg.predict(x)
    residuals = y - predicted_values
    return {
        "r2": reg.score(x, y),
        "intercept": reg.intercept_,
        "coefs": reg.coef_,
        "model": reg,
        "residuals": residuals,
    }


def index_to_nation_options(index: _allowed_indexes) -> str:
    """
    return a string of the allowed nation initials (e..g ESWN)
    """
    if index == "uk":
        nations = "ESWN"
    elif index == "gb":
        nations = "ESW"
    return nations


def summary_models(setting: _allowed_indexes = "uk"):
    """
    run and display variables for each model
    """
    print(f"Running nation models: {setting}")

    nations = index_to_nation_options(setting)

    if setting == "uk":
        options = ["Employment score"]
    else:
        options = ["Income score", "Employment score"]

    all_results = []
    for nation in nations:
        df = get_dataset(nation)
        model = make_model(df, setting=setting)
        results = {}
        results["Nation"] = nice_nation[nation]
        results["Intercept"] = model["intercept"]
        for o, c in zip(options, model["coefs"]):
            results[o] = c
        results["r2"] = model["r2"]
        results["residuals SD"] = model["residuals"].std()
        all_results.append(results)

    df = pd.DataFrame(all_results)
    df = df.round(2)
    df.to_csv(Path("data", "analysis", f"{setting}_models.csv"), index=False)


def all_summary_models():
    """
    Produce summaries of the distributions of different models
    """
    summary_models("uk")
    summary_models("gb")


def transform_index(
    source_nation: str,
    dest_nation: str,
    col_name: str,
    setting: _allowed_indexes = "uk",
) -> pd.DataFrame:
    """
    Apply properties of one model to results from the source
    """

    if setting == "uk":
        predictors = uk_predictors
    else:
        predictors = gb_predictors

    source_df = get_dataset(source_nation)
    dest_df = get_dataset(dest_nation)
    source_model = make_model(source_df, setting)
    dest_model = make_model(dest_df, setting)

    resid = source_model["residuals"]
    source_resid_stdev = resid.std()
    dest_resid_stdev = dest_model["residuals"].std()
    adjusted_resid = (resid / source_resid_stdev) * dest_resid_stdev

    model = dest_model["model"]
    x = source_df[predictors]
    predicted = model.predict(x)
    predicted_with_resid = predicted + adjusted_resid

    source_df[col_name + "_score"] = predicted_with_resid

    return source_df


def transform_all_to(
    destination_index: _component_indexes | str = "E", setting: _allowed_indexes = "uk"
):
    """
    remap all nations to target nation
    """
    nations = index_to_nation_options(setting)

    collection = []
    col_name = "{s}_IMD_{n}".format(n=destination_index, s=setting).upper()
    for nation in nations:
        if nation != destination_index:
            df = transform_index(nation, destination_index, col_name, setting)
        else:
            df = get_dataset(nation)

            df[col_name + "_score"] = df["overall_score"]
        collection.append(df)

    df = pd.concat(collection)
    pop = pd.read_csv(
        Path("data", "analysis", "population", "2019_population.csv"), thousands=","
    )
    df = pd.merge(df, pop, on="lsoa")

    national_index = national_decile_lookups()

    df = pd.merge(df, national_index, on="lsoa")

    # expand a national set of deciles to cover equiv scores elsewhere
    just_origin = df.loc[df["nation"] == destination_index]
    just_origin = just_origin.groupby("original_decile")
    limits = just_origin.agg({col_name + "_score": ["min"]})
    limits = limits.reset_index()
    limits.columns = ["decile", "min_score"]
    limits = limits.sort_values("decile", ascending=True)

    decile_col = destination_index + "_expanded_decile"
    df[decile_col] = 1
    for n, r in limits.iterrows():
        if n == 9:
            continue
        df.loc[df[col_name + "_score"] < r["min_score"], decile_col] = r["decile"] + 1

    # create cumulative sum column on rank so we create deciles based on even pop
    # and get around that some small areas are different sizes
    df[col_name + "_rank"] = df[col_name + "_score"].rank(ascending=False)
    df = df.sort_values(col_name + "_rank")
    df["cum_pop"] = df["pop"].astype("int").cumsum()

    df[col_name + "_pop_decile"] = np.ceil(df["cum_pop"] / sum(df["pop"]) * 10).astype(
        int
    )
    df[col_name + "_pop_quintile"] = np.ceil(df["cum_pop"] / sum(df["pop"]) * 5).astype(
        int
    )

    df = df.drop(columns=["pop", "cum_pop"])
    df = df.rename(columns={"overall_score": "overall_local_score"})
    df.to_csv(Path(package_dir, f"{setting}_index", f"{col_name}.csv"), index=False)


def transform_all():
    """
    Create Re-targetted indexes for all items
    """
    UK_NATIONS = "NESW"
    GB_NATIONS = "ESW"
    for nation in UK_NATIONS:
        transform_all_to(nation, setting="uk")
    for nation in GB_NATIONS:
        transform_all_to(nation, setting="gb")


def deprivation_breakdown(nation="E", setting="uk", nations="ENSW"):
    """
    Create breakdown of where the nations sit in different deciles
    of combined models
    """
    df = pd.read_csv(
        Path(package_dir, f"{setting}_index", f"{setting.upper()}_IMD_{nation}.csv")
    )

    pop = pd.read_csv(
        Path("data", "analysis", "population", "2019_population.csv"), thousands=","
    )
    df = pd.merge(df, pop, on="lsoa")

    pt = df.pivot_table(
        "pop",
        columns="nation",
        index=[f"{setting.upper()}_IMD_{nation}_pop_decile"],
        aggfunc="sum",
    ).fillna(0)
    pt.index.name = "IMD Decile distribution"
    pt.columns.name = None
    for n in nations:
        pt[n] = round(pt[n] / pt[n].sum(), 4)
    pt.to_csv(
        Path("data", "analysis", setting.upper() + f"_imd_{nation}_breakdown.csv")
    )


def all_deprivation_breakdowns():
    for n in "EWNS":
        deprivation_breakdown(
            n,
        )
    for n in "EWS":
        deprivation_breakdown(n, setting="gb", nations="EWS")


def compare_local_global_ranking(
    nation="E", setting: _allowed_indexes = "uk", nations="ENSW"
):
    """
    Calculate difference in rankings between original and composite index
    """
    filepath = Path(
        package_dir, f"{setting}_index", f"{setting.upper()}_IMD_{nation}.csv"
    )
    df = pd.read_csv(filepath)
    score_col = f"{setting.upper()}_IMD_{nation.upper()}_score"
    print("Calc relative displacement")
    results = {}
    for n in nations:
        if n == nation:
            continue
        ldf = df[df.nation == n].copy()
        ldf["local_ranking"] = ldf["overall_local_score"].rank(ascending=False)
        ldf["reduced_ranking"] = ldf[score_col].rank(ascending=False)
        ldf["ranking_match"] = ldf["local_ranking"] == ldf["reduced_ranking"]
        diff = ldf["local_ranking"] - ldf["reduced_ranking"]
        rank_disagreement = (len(ldf) - ldf["ranking_match"].sum()) / len(ldf)
        rank_disagreement = round(rank_disagreement * 100, 1)
        displacement = diff[diff != 0].abs().describe()
        displacement["% of total"] = rank_disagreement
        print("")
        print(nice_nation[n])
        print(f"Disagreement between rankings - {rank_disagreement}%")
        print(displacement)
        results[nice_nation[n]] = displacement
    results_df = pd.DataFrame(results).round(2)
    results_df.to_csv(
        Path(
            "data", "analysis", setting.upper() + f"_imd_{nation}_rank_displacement.csv"
        )
    )


def compare_both_local_global():
    compare_local_global_ranking()
    compare_local_global_ranking(setting="gb", nations="ESW")


def national_decile_lookups():
    """
    create decile lookup for each individual nation
    """
    dfs = []
    for n in "ENWS":
        df = get_dataset(n)
        df["rank"] = df["overall_score"].rank(ascending=False)
        df["original_decile"] = np.ceil(df["rank"] / len(df) * 10).astype(int)
        dfs.append(df)
    df = pd.concat(dfs)[["lsoa", "original_decile"]]
    return df


def produce_indexes_and_analysis():
    all_summary_models()
    transform_all()
    all_deprivation_breakdowns()
    compare_both_local_global()


if __name__ == "__main__":
    produce_indexes_and_analysis()
