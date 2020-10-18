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


def plot_figure():
    # Create groups for years 2015 - 2018
    df_y2018 = df.groupby('year').get_group(2018)\
        .groupby('month')['checks_combined'].sum().reset_index()
    df_y2017 = df.groupby('year').get_group(2017)\
        .groupby('month')['checks_combined'].sum().reset_index()
    df_y2016 = df.groupby('year').get_group(2016)\
        .groupby('month')['checks_combined'].sum().reset_index()
    df_y2015 = df.groupby('year').get_group(2015)\
        .groupby('month')['checks_combined'].sum().reset_index()

    plt.figure(figsize=(9, 6))

    # Plot lines for years 2015 - 2018
    plt.plot(-1 + df_y2018['month'], df_y2018['checks_combined'],
             ":.", color='magenta', label="2018")
    plt.plot(-1 + df_y2017['month'], df_y2017['checks_combined'],
             "--.", color='green', label="2017")
    plt.plot(-1 + df_y2016['month'], df_y2016['checks_combined'],
             "-.*", markersize=4, color='lightblue', label="2016")
    plt.plot(-1 + df_y2015['month'], df_y2015['checks_combined'],
             "-*", markersize=4, color='beige', label="2015")

    plt.ylim(ymin=0)  # Set y axis to start from 0
    plt.xticks(df_y2018.index, months)
    plt.ylabel('Number of Checks')
    plt.title('Total Number of Checks by Month (2015 - 2018)')
    plt.legend(loc='best')

    # Add thousands separator to y axis
    ax = plt.gca()
    ax.get_yaxis().set_major_formatter(
        plt.FuncFormatter(lambda y, loc: "{:,}".format(int(y))))

    plt.show()


if __name__ == "__main__":
    set_pandas_options()
    clean_data()
    plot_figure()
