
import os
import pandas as pd
import numpy as np
import yaml
import json
from sklearn import linear_model

join = os.path.join

important_columns = ["lsoa", "overall_score",
                     "income_score", "employment_score"]

# can't use both for 2017 NI annoyingly
gb_predictors = ["income_score", "employment_score"]
uk_predictors = ["employment_score"]

nice_nation = {"N": "Northern Ireland",
               "S": "Scotland",
               "W": "Wales",
               "E": "England"}


def get_country_info():
    with open("country_indexes//join_description.yaml") as file:
        countries = yaml.load(file, Loader=yaml.FullLoader)
    return countries


def get_dataset(nation):
    """
    load source from yaml and process to consistent format
    """
    info = get_country_info()[nation]
    df = pd.read_csv(join("country_indexes", info["source_file"]))
    rename = {info[x]: x for x in important_columns}
    df = df.rename(columns=rename)
    df["nation"] = nation
    df = df[["nation"] + important_columns]

    if info["adjustment"] == "domains_times_100":
        df["income_score"] = df["income_score"] * 100
        df["employment_score"] = df["employment_score"] * 100

    return df


def make_model(df, setting="UK"):
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
    return {"r2": reg.score(x, y),
            "intercept": reg.intercept_,
            "coefs": reg.coef_,
            "model": reg,
            "residuals": residuals
            }


def summary_models(setting="UK", nations="NSEW"):
    """
    run and display variables for each model
    """
    print("Running nation models")

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
    df
    df.to_csv(join("analysis", "{0}_models.csv".format(setting)), index=False)


def all_summary_models():
    summary_models("uk", "ESWN")
    summary_models("gb", "ESW")


def transform_index(source_nation, dest_nation, col_name, setting="UK"):
    """
    apply properties of one model to results from the source
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
    adjusted_resid = (resid/source_resid_stdev) * dest_resid_stdev

    model = dest_model["model"]
    x = source_df[predictors]
    predicted = model.predict(x)
    predicted_with_resid = predicted + adjusted_resid

    source_df[col_name + "_score"] = predicted_with_resid

    return source_df


def transform_all_to(destination_index="E", setting="UK", nations="NSEW"):
    """
    remap all nations to target nation
    """
    collection = []
    col_name = "{s}_IMD_{n}".format(n=destination_index, s=setting)
    for nation in nations:
        if nation != destination_index:
            df = transform_index(nation, destination_index, col_name, setting)
        else:
            df = get_dataset(nation)
            df[col_name + "_score"] = df["overall_score"]
        collection.append(df)

    df = pd.concat(collection)
    df[col_name + "_rank"] = df[col_name + "_score"].rank(ascending=False)

    pop = pd.read_csv(join("analysis", "population",
                           "2019_population.csv"), thousands=',')
    df = pd.merge(df, pop, on="lsoa")

    # create cumulative sum column on rank so we create deciles based on even pop
    # and get around that some small areas are different sizes
    df = df.sort_values(col_name + "_rank")
    df["cum_pop"] = df["pop"].astype("int").cumsum()

    df[col_name +
        "_pop_decile"] = np.ceil(df["cum_pop"]/sum(df["pop"]) * 10).astype(int)
    df[col_name +
        "_pop_quintile"] = np.ceil(df["cum_pop"]/sum(df["pop"]) * 5).astype(int)

    df = df.drop(columns=["pop", "cum_pop"])

    df = df.rename(columns={"overall_score": "overall_local_score"})
    df.to_csv(join(setting + "_index", col_name + ".csv"), index=False)


def transform_all():
    """
    create re-targetted indexes for all
    """
    UK_NATIONS = "NESW"
    GB_NATIONS = "ESW"
    for nation in UK_NATIONS:
        transform_all_to(nation, setting="UK", nations=UK_NATIONS)
    for nation in GB_NATIONS:
        transform_all_to(nation, setting="GB", nations=GB_NATIONS)


def deprivation_breakdown(nation="E", setting="UK", nations="ENSW"):
    """
    create breakdown of where the nations sit in different deciles
    of combined models
    """
    df = pd.read_csv(join(setting + "_index", setting +
                          "_IMD_{0}.csv".format(nation)))

    pop = pd.read_csv(join("analysis", "population",
                           "2019_population.csv"), thousands=',')
    df = pd.merge(df, pop, on="lsoa")

    pt = df.pivot_table("pop", columns="nation", index=[
        setting + "_IMD_{0}_pop_decile".format(nation)], aggfunc='sum').fillna(0)
    pt.index.name = "IMD Decile distribution"
    pt.columns.name = None
    for n in nations:
        pt[n] = round(pt[n]/pt[n].sum(), 2)
    print(pt)
    pt.to_csv(join("analysis", setting +
                   "_imd_{0}_breakdown.csv".format(nation)))


def all_deprivation_breakdowns():
    for n in "EWNS":
        deprivation_breakdown(n,)
    for n in "EWS":
        deprivation_breakdown(n, setting="GB", nations="EWS")


def compare_local_global_ranking(nation="E", setting="UK", nations="ENSW"):
    """
    Calculate difference in rankings between original and composite index
    """
    filepath = join(setting + "_index", setting +
                    "_IMD_{0}.csv".format(nation))
    df = pd.read_csv(filepath)
    score_col = "{1}_IMD_{0}_score".format(nation, setting)
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
        rank_disagreement = (len(ldf) - ldf["ranking_match"].sum())/len(ldf)
        rank_disagreement = round(rank_disagreement*100, 1)
        displacement = diff[diff != 0].abs().describe()
        displacement["% of total"] = rank_disagreement
        print("")
        print(nice_nation[n])
        print("Disagreement between rankings - {0}%".format(rank_disagreement))
        print(displacement)
        results[nice_nation[n]] = displacement
    results_df = pd.DataFrame(results).round(2)
    print(results_df)
    results_df.to_csv(join("analysis", setting +
                           "_imd_{0}_rank_displacement.csv".format(nation)))


def compare_both_local_global():
    compare_local_global_ranking()
    compare_local_global_ranking(setting="GB", nations="ESW")


def add_to_lookup(data, nation):
    """
    create json dict for this nation, update if overlapping with others
    """
    info = get_country_info()[nation]
    df = pd.read_csv(join("country_indexes", info["source_file"]))
    rename = {info[x]: x for x in important_columns}
    df = df.rename(columns=rename)
    df = df[important_columns]

    df["local_ranking"] = df["overall_score"].rank(ascending=False)
    df["local_decile"] = np.ceil(df["local_ranking"]/len(df) * 10).astype(int)
    df["local_quintile"] = np.ceil(
        df["local_ranking"]/len(df) * 10).astype(int)

    for x, row in df.iterrows():
        current = data.get(row["lsoa"], {})
        current[nation + "_r"] = row["local_ranking"]
        current[nation + "_d"] = row["local_decile"]
        current[nation + "_q"] = row["local_quintile"]
        data[row["lsoa"]] = current
    return data


def add_composite_to_lookup(data, composite):
    core = "{0}_IMD_E".format(composite)
    loc = join("{0}_index".format(composite),
               core + ".csv")
    df = pd.read_csv(loc)

    for x, row in df.iterrows():
        current = data.get(row["lsoa"], {})
        current[composite + "_r"] = row[core + "_rank"]
        current[composite + "_d"] = row[core + "_pop_decile"]
        current[composite + "_q"] = row[core + "_pop_quintile"]
        data[row["lsoa"]] = current
    return data


def create_master_lookup():
    """
    create single json lookup between LSOA and national deprivation
    """
    data = {}
    for nation in "ESNW":
        print("adding {0}".format(nation))
        data = add_to_lookup(data, nation)
    for composite in ["GB", "UK"]:
        print("adding {0}".format(composite))
        data = add_composite_to_lookup(data, composite)

    with open(join("composite_lookups", "imd_lsoa.json"), 'w') as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":

    all_summary_models()
    transform_all()
    all_deprivation_breakdowns()
    compare_both_local_global()
    create_master_lookup()
