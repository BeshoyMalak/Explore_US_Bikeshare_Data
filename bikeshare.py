import time
import pandas as pd
import numpy as np

CITIES = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    city_name = ''
    while city_name.lower() not in CITIES:
        city_name = input("\nWhat is the name of the city to analyze data? (E.g. Input either chicago, new york city, washington)\n")
        if city_name.lower() in CITIES:
            #We were able to get the name of the city to analyze data.
            city = CITIES[city_name.lower()]
        else:
            #We were not able to get the name of the city to analyze data so we continue the loop.
            print("Sorry we were not able to get the name of the city to analyze data, Please input either chicago, new york city or washington.\n")

    month_name = ''
    while month_name.lower() not in MONTHS:
        month_name = input("\nWhat is the name of the month to filter data? (E.g. Input either 'all' to apply no month filter or january, february, ... , june)\n")
        if month_name.lower() in MONTHS:
            #We were able to get the name of the month to analyze data.
            month = month_name.lower()
        else:
            #We were not able to get the name of the month to analyze data so we continue the loop.
            print("Sorry we were not able to get the name of the month to filter data, Please input either 'all' to apply no month filter or january, february, ... , june.\n")

    day_name = ''
    while day_name.lower() not in DAYS:
        day_name = input("\nWhat is the name of the day to filter data? (E.g. Input either 'all' to apply no day filter or monday, tuesday, ... sunday)\n")
        if day_name.lower() in DAYS:
            day = day_name.lower()
        else:
            print("Sorry we were not able to get the name of the day to filter data, Please input either 'all' to apply no day filter or monday, tuesday, ... sunday.\n")

    print('**'*20)
    
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
    # load data file into a dataframe
    df = pd.read_csv(city)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month)

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    #Displays statistics on the most frequent times of travel.


    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print("The most common month from the given fitered data is: " + MONTHS[common_month].title())

    common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of week from the given fitered data is: " + common_day_of_week)

    common_start_hour = df['hour'].mode()[0]
    print("The most common start hour from the given fitered data is: " + str(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('**'*20)

def station_stats(df):
    #Displays statistics on the most popular stations and trip.

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station from the given fitered data is: " + common_start_station)

    common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station from the given fitered data is: " + common_end_station)

    frequent_combination = (df['Start Station'] + "||" + df['End Station']).mode()[0]
    print("The most frequent combination of start station and end station trip is : " + str(frequent_combination.split("||")))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    #Displays statistics on the total and average trip duration.

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time from the given fitered data is: " + str(total_travel_time))

    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time from the given fitered data is: " + str(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    #Displays statistics on bikeshare users.

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print("The count of user types from the given fitered data is: \n" + str(user_types))

    if city == 'chicago.csv' or city == 'new_york_city.csv':
        gender = df['Gender'].value_counts()
        print("The count of user gender from the given fitered data is: \n" + str(gender))

        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()[0]
        print('Earliest birth from the given fitered data is: {}\n'.format(earliest_birth))
        print('Most recent birth from the given fitered data is: {}\n'.format(most_recent_birth))
        print('Most common birth from the given fitered data is: {}\n'.format(most_common_birth) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    #Displays raw data on user request.
    print(df.head())
    next = 0
    while True:
        view_raw_data = input('\nDo you like to view next five row of raw data? Enter yes or no.\n')
        if view_raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()