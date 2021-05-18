import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['january', 'february', 'march', 'april', 'may', 'june']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    city = input('Would you like to see data for Chicago, New York, or Washington?\n').title().strip().lower()

    while(city not in ("chicago", "new york", "washington")):
        error_city = input("Your input is invalid! Please try again \n")
        city = error_city.title().lower()

    # get user input for filter mode based on month and day of week
    filter = input('Would you like to filter the data by month, day,both or not at all? Type "none" for no time filter\n').title().strip().lower()
    while(filter not in ("month", "day", "both", "none")):
        error_time = input("Your input is invalid! Please try again \n")
        filter = error_time.title().lower()

    if(filter == "both"):
        month = input("Which month - January, February, March, April, May, or June?\n").title().strip().lower()
        while(month not in ("january", "february", "march", "april", "may", "june")):
            error_month = input("Your input is invalid! Please try again \n")
            month = error_month.title().lower()

        day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n").title().strip().lower()
        while(day not in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")):
            error_day = input("Your input is invalid! Please try again \n")
            day = error_day.title().lower()
    elif(filter == "month"):
        month = input("Which month - January, February, March, April, May, or June?\n").title().strip().lower()
        while(month not in ("january", "february", "march", "april", "may", "june")):
            error_month = input("Your input is invalid! Please try again \n")
            month = error_month.title().lower()
        day = "all"
    elif(filter == "day"):
        day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n").title().strip().lower()
        while(day not in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")):
            error_day = input("Your input is invalid! Please try again \n")
            day = error_day.title().lower()
        month = "all"
    else:
        month = "all"
        day = "all"

    print('-'*40)
    print("Debug:---city:{} month:{} day:{}".format(city, month, day))
    return city, month, day, filter


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def get_time_stats(df, month, day, filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month if no filter
    if(month == 'all'):
        most_month = df['month'].mode()[0]
        most_month_count = df['month'].value_counts().max()
        print('most popular month: {}, count: {}, Filtered by: {}'.format(
            months[most_month - 1], most_month_count, filter))

    # display the most common day of week
    if(day == 'all'):
        most_day = df['day_of_week'].mode()[0]
        most_day_count = df['day_of_week'].value_counts().max()

        print('most popular day: {}, count: {}, Filtered by: {}'.format(
            most_day, most_day_count, filter))

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    most_hour = df['start_hour'].mode()[0]
    most_hour_count = df['start_hour'].value_counts().max()

    print('most popular start hour: {}h, count: {}, Filtered by: {}'.format(
        most_hour, most_hour_count, filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, filter):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    most_start_station_count = df['Start Station'].value_counts().max()
    print('most popular start station: {}, count: {}, Filtered by: {}'.format(
        most_start_station, most_start_station_count, filter))

    # display most commonly used end station
    most_end_station = df['End Station'].mode()[0]
    most_end_station_count = df['End Station'].value_counts().max()
    print('most popular end station: {}, count: {}, Filtered by: {}'.format(
        most_end_station, most_end_station_count, filter))

    # display most frequent combination of start station and end station trip
    df['Start-End'] = df['Start Station'] + ' -> ' + df['End Station']
    
    most_combi_station = df['Start-End'].mode()[0]
    most_combi_station_count = df['Start-End'].value_counts().max()
    print('most popular combination stations: {}, count: {}, Filtered by: {}'.format(
        most_combi_station, most_combi_station_count, filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, filter):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    duration = df['Trip Duration'].sum()
    duration_count = len(df['Trip Duration'].index)

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()

    print('Total duration: {}, count: {}, Avg duration: {} Filtered by: {}'.format(
        duration, duration_count, mean_duration, filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, filter):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_stats = df['User Type'].value_counts()
    for i, v in user_stats.items():
        print('{}: {}\n'.format(i, v))

    # Display counts of gender when the data is available
    if 'Gender' in df:
        gender_stats = df['Gender'].value_counts()
        for i, v in gender_stats.items():
            print('{}: {}\n'.format(i, v))
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe')
   

    # Display earliest, most recent, and most common year of birth only when the data is available
    if 'Birth Year' in df:
        min_year = df['Birth Year'].min()
        max_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        common_year_count = df['Birth Year'].value_counts().max()

        print('earliest year of birth: {}\n most recent year of birth: {}\n most common year of birth: {} with {} times\n'.format(
        min_year, max_year, common_year, common_year_count))
    else:
        print('Birth year stats cannot be calculated because Birth year does not appear in the dataframe')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def view_raw_data(df, count):
    data_option = input(
        'Would you like to view individual trip data? Type "yes" or "no" \n').strip().lower()
    while(data_option not in ('yes', 'no')):
        error_data = input("Your input is invalid! Please try again \n")
        data_option = error_data.title().lower()

    if(data_option == 'yes'):
        print(df.head(count+5))
        view_raw_data(df, count+5)

    if(data_option == 'no'):
        return


def main():
    while True:
        city, month, day, filter = get_filters()
        df = load_data(city, month, day)

        get_time_stats(df, month, day, filter)
        station_stats(df, filter)
        trip_duration_stats(df, filter)
        raw_data = load_data(city, month, day)
        user_stats(df, filter)
        view_raw_data(raw_data, 0)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
