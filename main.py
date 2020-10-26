import matplotlib.pyplot as plt
import pandas as pd

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
months_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
               "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

data_path = "data/nics-firearm-background-checks.csv"

# Common dataframe used by each plot function
df = pd.read_csv(data_path, sep=',', header=0)


def set_pandas_options():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_rows', None)


def clean_data():
    df_dates = df["month"].str.split(
        "-", expand=True).rename(columns={0: 'year', 1: 'month'})

    counter = 0
    # Fix the issue where the df's date format is in both yy-mmm and mmm-yy.
    for year in df_dates['year']:
        # if year is found in months, swap the values of df year and month
        if year in months:
            df_dates['year'][counter], df_dates['month'][counter] = \
                df_dates['month'][counter], df_dates['year'][counter]
        counter += 1

    counter = 0
    # Convert months to numbers so that they can be sorted properly
    for month in df_dates['month']:
        df_dates['month'][counter] = months_dict[month]
        counter += 1

    counter = 0
    # Convert yy format to yyyy
    for year in df_dates['year']:
        if year == '99' or year == '98':
            df_dates['year'][counter] = "19" + year
        else:
            df_dates['year'][counter] = "20" + year
        counter += 1

    df.drop(columns=["month"], inplace=True)

    # Insert into df, year and month values converted to integers
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
    # Create groups for years 2015 - 2018
    df_y2018 = df.groupby('year').get_group(2018)\
        .groupby('month')['checks_combined'].sum().reset_index()
    df_y2017 = df.groupby('year').get_group(2017)\
        .groupby('month')['checks_combined'].sum().reset_index()
    df_y2016 = df.groupby('year').get_group(2016)\
        .groupby('month')['checks_combined'].sum().reset_index()
    df_y2015 = df.groupby('year').get_group(2015)\
        .groupby('month')['checks_combined'].sum().reset_index()

    plt.figure(figsize=(12, 8))

    # Plot lines for years 2015 - 2018
    plt.plot(df_y2018['month'], df_y2018['checks_combined'],
             ":.", color='magenta', label="2018")
    plt.plot(df_y2017['month'], df_y2017['checks_combined'],
             "--.", color='limegreen', label="2017")
    plt.plot(df_y2016['month'], df_y2016['checks_combined'],
             "-.*", markersize=4, color='lightblue', label="2016")
    plt.plot(df_y2015['month'], df_y2015['checks_combined'],
             "-*", markersize=4, color='bisque', label="2015")

    plt.ylim(ymin=0)  # Set y axis to start from 0
    plt.xticks(df_y2018['month'], months)
    plt.ylabel('Number of Checks')
    plt.title('Total Number of Checks by Month (2015 - 2018)')
    plt.legend(loc='best')
    add_thousands_separator_yaxis()

    plt.show()


def plot_num_checks_by_type_recent_years():
    # Total number of checks by month between 2016 and 2018 (inclusive)
    df_recent_years = df[(df['year'].between(2016, 2018, inclusive=True))]\
        .groupby('month').sum().reset_index()

    plt.subplots(nrows=5, ncols=1, figsize=(15, 15))

    plt.subplot(5, 1, 1)
    plt.title("Total Number of Checks by Month by Type (2016 - 2018)")
    plt.bar(df_recent_years['month'], df_recent_years['handgun'],
            color="lightpink", label='Handgun')
    plt.xticks(df_recent_years['month'], months)
    plt.legend(loc='best')
    add_thousands_separator_yaxis()

    plt.subplot(5, 1, 2)
    plt.bar(df_recent_years['month'], df_recent_years['long_gun'],
            color="lightgreen", label='Long Gun')
    plt.xticks(df_recent_years['month'], months)
    plt.legend(loc='best')
    add_thousands_separator_yaxis()

    plt.subplot(5, 1, 3)
    plt.bar(df_recent_years['month'], df_recent_years['other_gun'],
            color="lightblue", label='Other Gun Type')
    plt.xticks(df_recent_years['month'], months)
    plt.ylabel("Number of Checks")
    plt.legend(loc='best')
    add_thousands_separator_yaxis()

    plt.subplot(5, 1, 4)
    plt.bar(df_recent_years['month'], df_recent_years['multiple'],
            color="lavender", label='Multiple')
    plt.xticks(df_recent_years['month'], months)
    plt.legend(loc='best')
    add_thousands_separator_yaxis()

    plt.subplot(5, 1, 5)
    plt.bar(df_recent_years['month'], df_recent_years['other_sale_types'],
            color="beige", label='Other Types')
    plt.xticks(df_recent_years['month'], months)
    plt.legend(loc='best')
    add_thousands_separator_yaxis()

    plt.show()


def plot_top10_states_by_num_checks():
    df_top10_states = df.groupby('state')['checks_combined'].sum()\
        .reset_index().rename(columns={'checks_combined': '# of checks'})\
        .sort_values(by='# of checks', ascending=False)[:10]

    plt.figure(figsize=(16, 12))
    plt.title("Top 10 States by Number of Checks (Nov 1998 - Oct 2019)")
    plt.ylabel("Number of Checks")
    plt.xticks(rotation='vertical')
    plt.bar(df_top10_states['state'], df_top10_states['# of checks'],
            color="lightcoral")

    ax = plt.gca()
    add_value_labels(ax)

    add_thousands_separator_yaxis()
    plt.show()


def plot_num_checks_by_year():
    df_total = df[(df['year'].between(1999, 2018, inclusive=True))]\
        .groupby('year').sum().reset_index()\
        .rename(columns={'checks_combined': '# of checks'})

    plt.figure(figsize=(20, 12))
    plt.margins(x=0.01)
    plt.title("Number of Checks by Year (1999 - 2018)")
    plt.ylabel("Number of Checks")
    plt.xticks(df_total['year'])
    plt.plot(df_total['year'], df_total['# of checks'], color="goldenrod")
    plt.bar(df_total['year'], df_total['# of checks'], color="wheat")

    ax = plt.gca()
    add_value_labels(ax)

    add_thousands_separator_yaxis()
    plt.show()


if __name__ == "__main__":
    set_pandas_options()
    clean_data()
    plot_num_checks_by_year()
    plot_num_checks_recent_years()
    plot_num_checks_by_type_recent_years()
    plot_top10_states_by_num_checks()
