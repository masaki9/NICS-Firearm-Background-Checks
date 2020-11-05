import matplotlib.pyplot as plt
import pandas as pd

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

data_path = "data/nics-firearm-background-checks.csv"
df = pd.read_csv(data_path, sep=',', header=0)


def clean_data():
    df_dates = df["month"].str.split(
        "-", expand=True).rename(columns={0: 'year', 1: 'month'})

    df.drop(columns=["month"], inplace=True)

    df.insert(0, "year", df_dates['year'].astype(int))
    df.insert(1, "month", df_dates['month'].astype(int))


def add_thousands_separator_yaxis():
    ax = plt.gca()
    ax.get_yaxis().set_major_formatter(
        plt.FuncFormatter(lambda y, loc: "{:,}".format(int(y))))


def add_value_labels(ax, spacing=5, decimal=0):
    # For each bar, place a label
    for rect in ax.patches:
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        space = spacing  # Space between bar and label
        va = 'bottom'  # Vertical alignment

        # If value of bar is negative, place label below bar
        if y_value < 0:
            space *= -1
            va = 'top'

        # Use y as label and format number with decimal
        label = "{1:,.{0}f}".format(decimal, y_value)

        ax.annotate(label, (x_value, y_value), xytext=(0, space),
                    textcoords="offset points", ha='center', va=va)


def plot_num_checks_recent_years():
    # Create groups for years 2015 - 2019
    df_y2019 = df.groupby('year').get_group(2019)\
        .groupby('month')['totals'].sum().reset_index()
    df_y2018 = df.groupby('year').get_group(2018)\
        .groupby('month')['totals'].sum().reset_index()
    df_y2017 = df.groupby('year').get_group(2017)\
        .groupby('month')['totals'].sum().reset_index()
    df_y2016 = df.groupby('year').get_group(2016)\
        .groupby('month')['totals'].sum().reset_index()
    df_y2015 = df.groupby('year').get_group(2015)\
        .groupby('month')['totals'].sum().reset_index()

    plt.figure(figsize=(16, 12))

    # Plot lines for years 2015 - 2019
    plt.plot(df_y2019['month'], df_y2019['totals'],
             "--p", color='indianred', label="2019")
    plt.plot(df_y2018['month'], df_y2018['totals'],
             ":.", color='magenta', label="2018")
    plt.plot(df_y2017['month'], df_y2017['totals'],
             "--.", color='limegreen', label="2017")
    plt.plot(df_y2016['month'], df_y2016['totals'],
             "-.*", markersize=4, color='lightblue', label="2016")
    plt.plot(df_y2015['month'], df_y2015['totals'],
             "-*", markersize=4, color='bisque', label="2015")

    plt.ylim(ymin=0)  # Set y axis to start from 0
    plt.xticks(df_y2019['month'], months)
    plt.ylabel('Number of Checks')
    plt.title('Number of Firearm Background Checks by Month (2015 - 2019)')
    plt.legend(loc='best')
    add_thousands_separator_yaxis()

    plt.show()


def plot_num_checks_by_type_recent_years():
    # Total number of checks by month between 2015 and 2019 (inclusive)
    df_recent_years = df[(df['year'].between(2015, 2019, inclusive=True))]\
        .groupby('month').sum().reset_index()

    plt.subplots(nrows=5, ncols=1, figsize=(16, 16))

    plt.subplot(5, 1, 1)
    t = "Number of Firearm Background Checks by Month by Type (2015 - 2019)"
    plt.title(t)
    plt.bar(df_recent_years['month'], df_recent_years['handgun'],
            color="lightpink", label='Handgun')
    plt.xticks(df_recent_years['month'], months)
    plt.legend(loc='best')
    add_thousands_separator_yaxis()
    ax = plt.gca()
    add_value_labels(ax, spacing=-15)

    plt.subplot(5, 1, 2)
    plt.bar(df_recent_years['month'], df_recent_years['long_gun'],
            color="lightgreen", label='Long Gun')
    plt.xticks(df_recent_years['month'], months)
    plt.legend(loc='best')
    add_thousands_separator_yaxis()
    ax = plt.gca()
    add_value_labels(ax, spacing=-15)

    plt.subplot(5, 1, 3)
    plt.bar(df_recent_years['month'], df_recent_years['other'],
            color="lightblue", label='Other Gun Type')
    plt.xticks(df_recent_years['month'], months)
    plt.ylabel("Number of Checks")
    plt.legend(loc='best')
    add_thousands_separator_yaxis()
    ax = plt.gca()
    add_value_labels(ax, spacing=-15)

    plt.subplot(5, 1, 4)
    plt.bar(df_recent_years['month'], df_recent_years['multiple'],
            color="lavender", label='Multiple Gun Types Selected')
    plt.xticks(df_recent_years['month'], months)
    plt.legend(loc='best')
    add_thousands_separator_yaxis()
    ax = plt.gca()
    add_value_labels(ax, spacing=-15)

    df_other_types = df_recent_years.copy()
    df_other_types.drop(columns=["year", "month", "permit", "permit_recheck",
                                 "handgun", "long_gun", "other", "multiple",
                                 "totals"], inplace=True)

    df_recent_years['other_types'] = df_other_types.sum(axis=1)

    plt.subplot(5, 1, 5)
    plt.bar(df_recent_years['month'], df_recent_years['other_types'],
            color="beige", label='Other Types of Transactions')
    plt.xticks(df_recent_years['month'], months)
    plt.legend(loc='best')
    add_thousands_separator_yaxis()
    ax = plt.gca()
    add_value_labels(ax, spacing=-15)

    plt.show()


def plot_top10_states_by_num_checks():
    df_top10_states = df.groupby('state')['totals'].sum()\
        .reset_index().sort_values(by='totals', ascending=False)[:10]

    plt.subplots(nrows=2, ncols=1, figsize=(15, 15))

    plt.subplot(2, 1, 1)
    plt.title("Top 10 States/Territories by Number of "
              "Firearm Background Checks (Nov 1998 - Oct 2020)")
    plt.ylabel("Number of Checks")
    plt.bar(df_top10_states['state'], df_top10_states['totals'],
            color="lightcoral")

    ax = plt.gca()
    add_value_labels(ax)
    add_thousands_separator_yaxis()

    df_bottom10_states = df.groupby('state')['totals'].sum()\
        .reset_index().sort_values(by='totals', ascending=False)[-10:]

    plt.subplot(2, 1, 2)
    plt.title("Bottom 10 States/Territories by Number of "
              "Firearm Background Checks (Nov 1998 - Oct 2020)")
    plt.ylabel("Number of Checks")
    plt.bar(df_bottom10_states['state'], df_bottom10_states['totals'],
            color="paleturquoise")

    ax = plt.gca()
    add_value_labels(ax)
    add_thousands_separator_yaxis()

    plt.show()


def plot_num_checks_by_year():
    df_total = df[(df['year'].between(1999, 2019, inclusive=True))]\
        .groupby('year').sum().reset_index()

    plt.figure(figsize=(20, 12))
    plt.margins(x=0.01)
    plt.title("Number of Firearm Background Checks by Year (1999 - 2019)")
    plt.ylabel("Number of Checks")
    plt.xticks(df_total['year'])
    plt.plot(df_total['year'], df_total['totals'], color="goldenrod")
    plt.bar(df_total['year'], df_total['totals'], color="wheat")

    ax = plt.gca()
    add_value_labels(ax)

    add_thousands_separator_yaxis()
    plt.show()


if __name__ == "__main__":
    clean_data()
    plot_num_checks_by_year()
    plot_num_checks_recent_years()
    plot_num_checks_by_type_recent_years()
    plot_top10_states_by_num_checks()
