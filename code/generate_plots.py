import os
import pandas as pd
import seaborn as sns
from io import BytesIO
from datetime import datetime
from zoneinfo import ZoneInfo
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from .send_messages import send_document

def buffer_image(plot_figure):
    buffer = BytesIO()
    plot_figure.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    return buffer


def extract_data() -> dict:
    # Load data
    dono_retention_df = pd.read_parquet("https://storage.data.gov.my/healthcare/blood_donation_retention_2024.parquet", engine="auto")
    dono_fac_df = pd.read_csv("https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/donations_facility.csv")
    dono_state_df = pd.read_csv("https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/donations_state.csv")
    newdono_fac_df = pd.read_csv("https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/newdonors_facility.csv")
    newdono_state_df = pd.read_csv("https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/newdonors_state.csv")

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
    file = buffer_image(plt.gcf())
    send_document(
        file=file,
        filename="Total Annual Blood Donations.png"
    )

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
    file = buffer_image(plt.gcf())
    send_document(
        file=file,
        filename="Average Daily Blood Donations.png"
    )

    # Total annual donations (state breakdown)
    plt.figure(figsize=(10, 10))

    state_lst = []
    for idx, state in enumerate(dono_state_df["state"].unique()[1:]):
        if idx > 0 and idx % 4 == 0:
            plt.suptitle(f"Total Annual Blood Donations by State{'s'*(len(state_lst)>1)} ({', '.join(state_lst)})")
            plt.tight_layout()
            file = buffer_image(plt.gcf())
            send_document(
                file=file,
                filename=f"State Donation Breakdown ({', '.join(state_lst)}).png"
            )
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
        file = buffer_image(plt.gcf())
        send_document(
            file=file,
            filename=f"State Donation Breakdown ({', '.join(state_lst)}).png"
        )

    # Average daily donations (state breakdown)
    plt.figure(figsize=(10, 10))

    state_lst = []
    for idx, state in enumerate(dono_state_df["state"].unique()[1:]):
        if idx > 0 and idx % 4 == 0:
            plt.suptitle(f"Average Daily Blood Donations for State{'s'*(len(state_lst)>1)} ({', '.join(state_lst)})")
            plt.tight_layout(rect=[0, 0, 1, 0.98])
            file = buffer_image(plt.gcf())
            send_document(
                file=file,
                filename=f"State Daily Donation Breakdown ({', '.join(state_lst)}).png"
            )
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
        file = buffer_image(plt.gcf())
        send_document(
            file=file,
            filename=f"State Daily Donation Breakdown ({', '.join(state_lst)}).png"
        )

    # Donation retention
    retention_crosstab = dono_retention_df.groupby(["donor_id", "visit_year"])["visit_date"].agg("count").unstack().fillna(0)
    retention_df = (retention_crosstab > 0).astype(int).diff(axis=1).lt(0).sum(axis=0).div((retention_crosstab > 0).astype(int).sum(axis=0).shift(), 0).dropna().to_frame()
    retention_df = retention_df.assign(**{"Single Donors Percentage": 1.0-retention_df[0]})
    retention_df = retention_df.rename({0: "Doner Retention Percentage"}, axis=1)
    (retention_df * 100).plot.area()

    plt.title(f"Percentage of donors retained per year")
    plt.xticks(retention_df.index, rotation=90)
    plt.yticks(list(range(0, 101, 10)))
    plt.gca().get_yaxis().set_major_formatter(ticker.PercentFormatter())
    plt.xlabel("Year")
    plt.ylabel("Average Daily Blood Donations")
    plt.legend(loc=(0.5, 0.5))
    plt.grid(True)
    file = buffer_image(plt.gcf())
    send_document(
        file=file,
        filename="Donation Retention Percentage.png"
    )

    return

def generate_plots():
    data_dict = extract_data()
    send_document(message=f"Malaysia's blood donation statistics for {datetime.now(ZoneInfo('Asia/Kuala_Lumpur')).date().strftime('%d-%m-%Y')}")
    create_plot(data_dict=data_dict)

if __name__ == "__main__":
    generate_plots()