import pandas as pd


# parse_data takes the data.csv and dictionary.txt files and creates a dataframe displaying the counts
# of flap events for each link.

# custom split function for get_dictionary
def split(line, sep, pos):
    line = line.split(sep)
    return sep.join(line[:pos]), sep.join(line[pos:])


def get_dictionary():
    # This function opens dictionary.txt and creates a dictionary of tuples consisting of the format
    # ['Device,Port': 'Label'] to label those links in the dataframe
    with open("dictionary.txt", "r") as f:
        content = f.read().splitlines()
    return dict([tuple(map(str, split(sub, ',', 2))) for sub in content])


def process_data():
    # This function returns a dataframe from the events that are given in data.csv
    # and creates a count of events based on the given timestamps.
    # It also replaces the device names with the labels given in the dictionary

    # pandas options to display the dataframe in console, use print(df) to see the dataframe for testing
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    df = pd.read_csv("data.csv", header=None, names=('Device', 'Port', 'Date', 'Time', 'Event'),
                     parse_dates={'Timestamp': ['Date', 'Time']})

    # merge device and port values together to later rename them according to dictionary.txt labels
    df.Device = df.Device.astype(str) + ',' + df.Port.astype(str)
    df.drop(['Port'], axis=1, inplace=True)

    # look for duplicates of (Timestamp, Device) values and put that summation in a new 'Count' column
    df = df.pivot_table(index=['Timestamp', 'Device'], aggfunc='size').to_frame('Count').reset_index()

    # this turns the 'Device' column values into column headers (and timestamps into the new index)
    df = df.pivot(index='Timestamp', columns='Device', values='Count')
    df.fillna(0, inplace=True)

    # group counts based on day
    df = df.resample('D').sum()

    res = get_dictionary()

    # traverse through columns in dataframe and label them
    for column in df:
        if column in res:
            df.rename(columns={column: res[column]}, inplace=True)
        else:
            df.drop(column, axis=1, inplace=True)

    # removes the column header name when the 'Timestamp' column was assigned as index of the dataframe
    del df.index.name

    return df
