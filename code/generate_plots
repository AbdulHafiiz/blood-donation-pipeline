import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from dotenv import load_dotenv

load_dotenv()
DATA_PATH = os.environ.get("DATA_PATH")
PLOT_PATH = os.environ.get("PLOT_PATH")


def extract_data() -> dict:
    # Load data
    dono_retention_df = pd.read_parquet(f"{DATA_PATH}/blood_donation_retention.parquet", engine="auto")
    dono_fac_df = pd.read_csv(f"{DATA_PATH}/donations_facility.csv")
    dono_state_df = pd.read_csv(f"{DATA_PATH}/donations_state.csv")
    newdono_fac_df = pd.read_csv(f"{DATA_PATH}/newdonors_facility.csv")
    newdono_state_df = pd.read_csv(f"{DATA_PATH}/newdonors_state.csv")

    # Transform data
    dono_fac_df = dono_fac_df.assign(year=pd.to_datetime(dono_fac_df["date"]).dt.year)
    dono_fac_df = dono_fac_df.assign(month=pd.to_datetime(dono_fac_df["date"]).dt.month)
    dono_fac_df = dono_fac_df.assign(day_of_year=pd.to_datetime(dono_fac_df["date"]).dt.dayofyear)

    dono_state_df = dono_state_df.assign(year=pd.to_datetime(dono_state_df["date"]).dt.year)
    dono_state_df = dono_state_df.assign(month=pd.to_datetime(dono_state_df["date"]).dt.month)
    dono_state_df = dono_state_df.assign(day_of_year=pd.to_datetime(dono_state_df["date"]).dt.dayofyear)

    newdono_fac_df = newdono_fac_df.assign(year=pd.to_datetime(newdono_fac_df["date"]).dt.year)
    newdono_fac_df = newdono_fac_df.assign(month=pd.to_datetime(newdono_fac_df["date"]).dt.month)
    newdono_fac_df = newdono_fac_df.assign(day_of_year=pd.to_datetime(newdono_fac_df["date"]).dt.dayofyear)

    newdono_state_df = newdono_state_df.assign(year=pd.to_datetime(newdono_state_df["date"]).dt.year)
    newdono_state_df = newdono_state_df.assign(month=pd.to_datetime(newdono_state_df["date"]).dt.month)
    newdono_state_df = newdono_state_df.assign(day_of_year=pd.to_datetime(newdono_state_df["date"]).dt.dayofyear)

    dono_retention_df = dono_retention_df.assign(visit_year=pd.to_datetime(dono_retention_df["visit_date"]).dt.year)
    dono_retention_df = dono_retention_df.assign(visit_date=pd.to_datetime(dono_retention_df["visit_date"]))

    # Return data in dictionary
    data_dict = {
        "dono_retention_df": dono_retention_df,
        "dono_fac_df": dono_fac_df,
        "dono_state_df": dono_state_df,
        "newdono_fac_df": newdono_fac_df,
        "newdono_state_df": newdono_state_df
    }
    return data_dict


def create_plot(data_dict:dict) -> None:
    dono_retention_df = data_dict["dono_retention_df"]
    dono_fac_df = data_dict["dono_fac_df"]
    dono_state_df = data_dict["dono_state_df"]
    newdono_fac_df = data_dict["newdono_fac_df"]
    newdono_state_df = data_dict["newdono_state_df"]

    # Total annual donations
    sns.regplot(
        x=dono_fac_df["year"].drop_duplicates(),
        y=dono_fac_df.groupby("year")["daily"].agg("sum"),
        ci=False,
        line_kws={"color": "red"}
    )
    plt.xticks(dono_fac_df["year"].unique(), rotation=45)
    plt.yticks(list(range(0, 600_001, 50_000)))
    plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.grid(True)
    plt.title("Total Annual Blood Donations")
    plt.xlabel("Year")
    plt.ylabel("Total No. of Donations")
    plt.savefig(f"{PLOT_PATH}/Total Annual Blood Donations.png", bbox_inches="tight")

    # Average daily donations
    sns.regplot(
        x=dono_fac_df["year"].drop_duplicates(),
        y=dono_fac_df.groupby("year")["daily"].agg("sum")/dono_fac_df.groupby("year")["day_of_year"].agg("max"),
        ci=False,
        line_kws={"color": "red"}
    )
    plt.xticks(dono_fac_df["year"].unique(), rotation=45)
    plt.yticks(list(range(0, 1700, 125)))
    plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.grid(True)
    plt.title("Average Daily Blood Donations by Year")
    plt.xlabel("Year")
    plt.ylabel("No. of Average Daily Donations")
    plt.savefig(f"{PLOT_PATH}/Average Daily Blood Donations.png", bbox_inches="tight")

    # Total annual donations (state breakdown)
    plt.figure(figsize=(10, 10))

    state_lst = []
    for idx, state in enumerate(dono_state_df["state"].unique()[1:]):
        if idx > 0 and idx % 4 == 0:
            plt.suptitle(f"Total Annual Blood Donations by State{'s'*(len(state_lst)>1)} ({', '.join(state_lst)})")
            plt.tight_layout()
            plt.savefig(f"{PLOT_PATH}/State Donation Breakdown ({', '.join(state_lst)}).png", bbox_inches="tight")
            plt.figure(figsize=(10, 10))
            state_lst = []

        state_lst.append(state)
        plt.subplot2grid((2, 2), (idx//2%2, idx%2))
        state_data = dono_state_df[dono_state_df["state"] == state]

        x = state_data["year"].drop_duplicates()
        y = state_data.groupby("year")["daily"].agg("sum")
        max_val = str(max(y))
        y_tick = int(max_val[0]+"0"*(len(max_val)-2))

        sns.regplot(x=x, y=y, ci=False, line_kws={"color": "red"})
        plt.title(f"Total blood donations in {state} per year")
        plt.xticks(state_data["year"].unique(), rotation=90)
        plt.yticks(list(range(0, int(max_val)+y_tick+1, y_tick)))
        plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        plt.xlabel("Year")
        plt.ylabel("Total No. of Donations")
        plt.grid(True)
    else:
        plt.suptitle(f"Total Annual Blood Donations by State{'s'*(len(state_lst)>1)} ({', '.join(state_lst)})")
        plt.tight_layout()
        plt.savefig(f"{PLOT_PATH}/State Donation Breakdown ({', '.join(state_lst)}).png", bbox_inches="tight")
        plt.figure(figsize=(10, 10))

    # Average daily donations (state breakdown)
    plt.figure(figsize=(10, 10))

    state_lst = []
    for idx, state in enumerate(dono_state_df["state"].unique()[1:]):
        if idx > 0 and idx % 4 == 0:
            plt.suptitle(f"Average Daily Blood Donations for State{'s'*(len(state_lst)>1)} ({', '.join(state_lst)})")
            plt.tight_layout(rect=[0, 0, 1, 0.98])
            plt.savefig(f"{PLOT_PATH}/State Daily Donation Breakdown ({', '.join(state_lst)}).png", bbox_inches="tight")
            plt.figure(figsize=(10, 10))
            state_lst = []

        state_lst.append(state)
        plt.subplot2grid((2, 2), (idx//2%2, idx%2))
        state_data = dono_state_df[dono_state_df["state"] == state]

        x = state_data["year"].drop_duplicates()
        y = state_data.groupby("year")["daily"].agg("sum")/state_data.groupby("year")["day_of_year"].agg("max")
        max_val = str(round(max(y)))
        y_tick = int(max_val[0]+"0"*(len(max_val)-2))

        sns.regplot(x=x, y=y, ci=False, line_kws={"color": "red"})
        plt.title(f"Total blood donations in {state} per year")
        plt.xticks(state_data["year"].unique(), rotation=90)
        plt.yticks(list(range(0, int(max_val)+y_tick+1, y_tick)))
        plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        plt.xlabel("Year")
        plt.ylabel("Average Daily Blood Donations")
        plt.grid(True)
    else:
        plt.suptitle(f"Average Daily Blood Donations for State{'s'*(len(state_lst)>1)} ({', '.join(state_lst)})")
        plt.tight_layout(rect=[0, 0, 1, 0.98])
        plt.savefig(f"{PLOT_PATH}/State Daily Donation Breakdown ({', '.join(state_lst)}).png", bbox_inches="tight")

    # Donation retention
    dono_years = dono_retention_df.groupby("donor_id").agg(first_visit=("visit_date", "min"), last_visit=("visit_date", "max"))
    repeat_donors = dono_years[dono_years["first_visit"] != dono_years["last_visit"]]

    visits_df = pd.concat(
        [
            dono_retention_df.groupby("visit_year").agg(visit_count=("donor_id", "count")),
            dono_retention_df[dono_retention_df["donor_id"].isin(repeat_donors.index)].groupby("visit_year").agg(repeat_visit_counts=("donor_id", "count"))
        ],
        axis=1
    )
    visits_df = visits_df.assign(**{"Repeated Donors Percentage": visits_df["repeat_visit_counts"]/visits_df["visit_count"]})
    visits_df = visits_df.assign(**{"Single Donors Percentage": 1.0-visits_df["Repeated Donors Percentage"]})
    (visits_df.iloc[:, 2:] * 100).plot.area()

    plt.title(f"Percentage of donors retained per year")
    plt.xticks(visits_df.index, rotation=90)
    plt.yticks(list(range(0, 101, 10)))
    plt.gca().get_yaxis().set_major_formatter(ticker.PercentFormatter())
    plt.xlabel("Year")
    plt.ylabel("Average Daily Blood Donations")
    plt.legend(loc=(0.5, 0.5))
    plt.grid(True)
    plt.savefig(f"{PLOT_PATH}/Donation Retention Percentage.png", bbox_inches="tight")

    return

if __name__ == "__main__":
    data_dict = extract_data()
    create_plot(data_dict=data_dict)