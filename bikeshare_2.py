import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter the city to be explored:\n chicago, new york, or washington\n').lower()
        if city in cities:
            break
        else:
            print('Invalid entry. Please enter a valid city.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Enter the month to be explored:\n january, february, march, april, may, june, all\n').lower()
        if month in months:
            break
        else:
            print('Invalid entry. Please enter a valid month.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Enter the day of the week to be explored:\n sunday, monday, tuesday, wednesday, thursday, friday, saturday, all\n').lower()
        if day in days:
            break
        else:
            print('Invalid entry. Please enter a valid day.')

    print('-'*40)
    return city, month, day

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
     # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

# Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    most_common_month = df['month'].mode()[0]
    print('The most common month is:\n', most_common_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day
    most_common_day = df['day_of_week'].mode()[0]
    print('The most Common Day of the Week is:\n', most_common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('The most Common Start Hour is:\n', common_start_hour)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used Start Station is:\n', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("Most commonly used End Station is: \n", common_end_station)

    # display most frequent combination of start station and end station trip
    frequent_station_combination = (df['Start Station'] + "||" + df['End Station']).mode()[0]
    print('The most frequent start statio and end station combination is:\n {}'.format(frequent_station_combination))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    minute, second = divmod(total_travel_time, 60)
    hour, minute = divmod(minute, 60)
    print('The total travel time is:\n, {} hours, {} minutes, and {} seconds.'.format(hour, minute, second))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is:\n, mean_travel_time')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print('The counts of User types are:\n', user_types_counts)

    # Display counts of gender
    try:
        counts_of_gender = df['Gender'].value_counts()
        print('\nGender Types:\n', counts_of_gender)
    except KeyError:
        print('The counts of gender are:\n Sorry, no data available for {} City'.format(city.title()))

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()
        print('The earliest year of birth is:\n', int(earliest_birth))
        print('The most recent year of birth is:\n', int(most_recent_birth))
        print('The most common year of birth is:\n', int(most_common_year))
    except:
        print('Years of Birth:\nSorry, no data available for {} City'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Prompts the user and displays 5 lines of raw data until the user says 'no'. """

    start_data = 0
    end_data = 5
    df_length = len(df.index)

    while start_data < df_length:
        raw_data = input("\nWould you like to see five lines of raw data? Enter 'yes' or 'no'.\n")
        if raw_data.lower() == 'yes':
            print('\nDisplaying 5 lines of data.\n')
            if end_data > df_length:
                end_data = df_length
            print(df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        print("You selected {}, {}, and {}.".format(city.title(), month.title(), day.title()))
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
