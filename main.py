import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import geopandas as gpd

df = pd.read_csv("data/nics-firearm-background-checks.csv", sep=',', header=0)
gdf_states = gpd.read_file("data/cb_2018_us_state_500k.geojson")

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def clean_data():
    df_dates = df["month"].str.split(
        "-", expand=True).rename(columns={0: 'year', 1: 'month'})

    df.drop(columns=["month"], inplace=True)

    df.insert(0, "year", df_dates['year'].astype(int))
    df.insert(1, "month", df_dates['month'].astype(int))

    df_other_types = df.copy()
    df_other_types.drop(columns=["year", "month", "permit", "permit_recheck",
                                 "handgun", "long_gun", "other", "multiple",
                                 "totals"], inplace=True)

    # Other types of transactions such as pre-pawn, rentals, private sale etc.
    df['other_types'] = df_other_types.sum(axis=1, numeric_only=True)


def format_yaxis(ax, decimal=0):
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda y,
                                       loc: "{0:.{1}f}M"
                                       .format(int(y) / 1e+6, decimal)))


def add_bar_value_labels(ax, spacing=5, decimal=2, size=10):
    # For each bar, place a label
    for rect in ax.patches:
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        label = "{0:,.{1}f}M".format(y_value / 1e+6, decimal)
        ax.annotate(label, (x_value, y_value), xytext=(0, spacing), size=size,
                    textcoords="offset points", ha='center', va='bottom')


def plot_num_checks_recent_years():
    df_y2022 = df.groupby('year').get_group(2022)\
        .groupby('month')['totals'].sum().reset_index()
    df_y2021 = df.groupby('year').get_group(2021)\
        .groupby('month')['totals'].sum().reset_index()
    df_y2020 = df.groupby('year').get_group(2020)\
        .groupby('month')['totals'].sum().reset_index()
    df_y2019 = df.groupby('year').get_group(2019)\
        .groupby('month')['totals'].sum().reset_index()
    df_y2018 = df.groupby('year').get_group(2018)\
        .groupby('month')['totals'].sum().reset_index()

    plt.figure(figsize=(16, 12))

    plt.plot(df_y2022['month'], df_y2022['totals'],
             "-*", markersize=4, color='gold', label='2022')
    plt.plot(df_y2021['month'], df_y2021['totals'],
             "--p", color='indianred', label="2021")
    plt.plot(df_y2020['month'], df_y2020['totals'],
             ":.", color='magenta', label="2020")
    plt.plot(df_y2019['month'], df_y2019['totals'],
             "--.", color='limegreen', label="2019")
    plt.plot(df_y2018['month'], df_y2018['totals'],
             "-.*", markersize=4, color='lightblue', label="2018")

    plt.ylim(ymin=0)  # Set y axis to start from 0
    plt.xticks(df_y2021['month'], months)
    plt.ylabel('Number of Checks')
    plt.title('Number of Firearm Background Checks by Month (2018 - 2022 YTD)')
    plt.legend(loc='best')
    ax = plt.gca()
    format_yaxis(ax, 1)

    plt.show()


def plot_num_checks_by_month_by_type():
    df_by_month = df[['month', 'handgun', 'long_gun',
                      'other', 'multiple', 'other_types']]\
        .groupby('month').sum().reset_index()

    plt.subplots(nrows=5, ncols=1, figsize=(16, 16))

    plt.subplot(5, 1, 1)
    plt.title("Number of Firearm Background Checks by Month "
              "by Type (Nov 1998 - Apr 2022)")
    plt.bar(df_by_month['month'], df_by_month['handgun'],
            color="lightpink", label='Handgun')
    plt.xticks(df_by_month['month'], months)
    plt.legend(loc='best')
    ax = plt.gca()
    format_yaxis(ax, 1)
    add_bar_value_labels(ax, spacing=-15)

    plt.subplot(5, 1, 2)
    plt.bar(df_by_month['month'], df_by_month['long_gun'],
            color="lightgreen", label='Long Gun')
    plt.xticks(df_by_month['month'], months)
    plt.legend(loc='best')
    ax = plt.gca()
    format_yaxis(ax, 1)
    add_bar_value_labels(ax, spacing=-15)

    plt.subplot(5, 1, 3)
    plt.bar(df_by_month['month'], df_by_month['other'],
            color="lightblue", label='Other Gun Type')
    plt.xticks(df_by_month['month'], months)
    plt.ylabel("Number of Checks")
    plt.legend(loc='best')
    ax = plt.gca()
    format_yaxis(ax, 1)
    add_bar_value_labels(ax, spacing=-15)

    plt.subplot(5, 1, 4)
    plt.bar(df_by_month['month'], df_by_month['multiple'],
            color="lavender", label='Multiple Gun Types Selected')
    plt.xticks(df_by_month['month'], months)
    plt.legend(loc='best')
    ax = plt.gca()
    format_yaxis(ax, 1)
    add_bar_value_labels(ax, spacing=-15)

    plt.subplot(5, 1, 5)
    plt.bar(df_by_month['month'], df_by_month['other_types'],
            color="beige", label='Other Types of Transactions')
    plt.xticks(df_by_month['month'], months)
    plt.legend(loc='best')
    ax = plt.gca()
    format_yaxis(ax, 1)
    add_bar_value_labels(ax, spacing=-15)

    plt.show()


def plot_top10_states_by_num_checks():
    df_top10_states = df.groupby('state')['totals'].sum()\
        .reset_index().sort_values(by='totals', ascending=False)[:10]

    plt.subplots(nrows=2, ncols=1, figsize=(15, 15))

    plt.subplot(2, 1, 1)
    plt.title("Top 10 States/Territories by Number of "
              "Firearm Background Checks (Nov 1998 - Apr 2022)")
    plt.ylabel("Number of Checks")
    plt.bar(df_top10_states['state'], df_top10_states['totals'],
            color="lightcoral")

    ax = plt.gca()
    add_bar_value_labels(ax)
    format_yaxis(ax)

    df_bottom10_states = df.groupby('state')['totals'].sum()\
        .reset_index().sort_values(by='totals', ascending=False)[-10:]

    plt.subplot(2, 1, 2)
    plt.title("Bottom 10 States/Territories by Number of "
              "Firearm Background Checks (Nov 1998 - Apr 2022)")
    plt.ylabel("Number of Checks")
    plt.bar(df_bottom10_states['state'], df_bottom10_states['totals'],
            color="paleturquoise")

    ax = plt.gca()
    add_bar_value_labels(ax, decimal=3)
    format_yaxis(ax, 1)

    plt.show()


def plot_num_checks_by_year():
    df_total = df[(df['year'].between(1999, 2021, inclusive='both'))]\
        .groupby('year').sum().reset_index()

    plt.figure(figsize=(20, 12))
    plt.margins(x=0.01)
    plt.title("Number of Firearm Background Checks by Year (1999 - 2021)")
    plt.ylabel("Number of Checks")
    plt.xticks(df_total['year'])
    plt.plot(df_total['year'], df_total['totals'], color="goldenrod")
    plt.bar(df_total['year'], df_total['totals'], color="wheat")

    ax = plt.gca()
    add_bar_value_labels(ax)
    format_yaxis(ax)

    plt.show()


def plot_num_checks_by_type():
    df_total = df[['handgun', 'long_gun',
                   'other', 'multiple', 'other_types']].sum().reset_index()\
        .rename(columns={'index': 'type', 0: 'total'})

    plt.figure(figsize=(15, 12))
    plt.title("Number of Firearm Background Checks by Type "
              "(Nov 1998 - Apr 2022)")
    plt.ylabel("Number of Checks")

    bar_colors = ['lightpink', 'lightgreen', 'lightblue', 'lavender', 'beige']
    plt.bar(df_total['type'], df_total['total'], color=bar_colors)

    x_labels = ['Handgun', 'Long Gun', 'Other Gun Type',
                'Multiple Gun Types Selected', 'Other Types of Transactions']
    plt.xticks(df_total['type'], x_labels)

    ax = plt.gca()
    format_yaxis(ax)
    add_bar_value_labels(ax)

    plt.show()


def add_labels_and_outlines(gdf, ax, offset=0.4):
    gdf.apply(lambda x: ax.annotate(
        text=x.STUSPS, xy=x.geometry.centroid.coords[0],
        ha='center', color='black', fontsize=10), axis=1)

    gdf.apply(lambda x: ax.annotate(
        text="{:2.2f}M".format(x.totals/1000000),
        xy=(x.geometry.centroid.coords[0][0],
            x.geometry.centroid.coords[0][1]-offset),
        ha='center', color='black', fontsize=10), axis=1)

    gdf.boundary.plot(ax=ax, color='black', linewidth=0.75)


def plot_num_checks_map():
    df_total_by_state = df.groupby('state')['totals'].sum()\
        .reset_index().sort_values(by='state', ascending=True)

    states = pd.merge(gdf_states, df_total_by_state,
                      left_on='NAME', right_on='state', how='inner')

    separated = ['Alaska', 'Guam', 'Hawaii', 'Puerto Rico']
    contiguous = states[~states['NAME'].isin(separated)]
    alaska, guam, hawaii, puerto_rico = \
        [states[states['NAME'] == state] for state in separated]

    fig = plt.figure(constrained_layout=True, figsize=(24, 16))
    gs = fig.add_gridspec(nrows=8, ncols=4)

    ax1 = fig.add_subplot(gs[:-1, :])
    plt.title("Number of Firearm Background Checks (Nov 1998 - Apr 2022)",
              size=20)
    add_labels_and_outlines(contiguous, ax1)

    def ticks_in_mil(x, pos):
        return "{:.0f}M".format(x / 1e+6)

    contiguous.plot(ax=ax1, cmap='Reds', column='totals', legend=True,
                    legend_kwds={'label': "Number of Checks",
                                 'orientation': "vertical",
                                 'shrink': 0.69,
                                 'pad': 0,
                                 'format': ticker.FuncFormatter(ticks_in_mil)})

    ax2 = fig.add_subplot(gs[-1, 0])
    add_labels_and_outlines(alaska, ax2, 2)
    alaska.plot(ax=ax2, cmap='Reds', column='totals')
    plt.xlim(xmin=-182, xmax=-128)

    ax3 = fig.add_subplot(gs[-1, 1])
    add_labels_and_outlines(hawaii, ax3, 0.38)
    hawaii.plot(ax=ax3, cmap='Reds', column='totals')
    plt.xlim(xmin=-160.5, xmax=-154.5)
    plt.ylim(ymin=18.5, ymax=22.5)

    ax4 = fig.add_subplot(gs[-1, 2])
    add_labels_and_outlines(guam, ax4, 0.048)
    guam.plot(ax=ax4, cmap='Reds', column='totals')

    ax5 = fig.add_subplot(gs[-1, 3])
    add_labels_and_outlines(puerto_rico, ax5, 0.09)
    puerto_rico.plot(ax=ax5, cmap='Reds', column='totals')

    plt.show()


if __name__ == "__main__":
    clean_data()
    plot_num_checks_by_year()
    plot_num_checks_recent_years()
    plot_num_checks_by_type()
    plot_num_checks_by_month_by_type()
    plot_num_checks_map()
    plot_top10_states_by_num_checks()
