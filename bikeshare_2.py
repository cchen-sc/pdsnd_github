#By Chenxi Chen

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    
    city = input('Which city do you want to explore: chicago, new york city or washington? Enter the city name:\n').lower()
    while city not in CITY_DATA:
        city = input('Invalid city name. Please choose one from: chicago, new york city or washington:\n').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('We have data collected from January to June. Please enter the month of interest or enter "all" to explore for all data:\n').title()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'All', 'Jan', 'Feb', 'Mar', 'Apr', 'Jun']
    while month not in months:
        month = input('Invalid month. Please choose one from Janurary to June or "All" for all available months:\n').title()
    

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('Please enter the day of interest or enter "all" to explore for all data:\n').title()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    while day not in days:
        day = input('Invalid day, please re=enter:\n').title()

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
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    #Ask User if want to view 'RAW' data:
    i = 0
    flag = input("Do you want to view 5 rows of raw data?\n\n").lower()
    while flag in ['yes','y'] and i+5 < df.shape[0]:
        pd.set_option('display.max_columns',200)
        print(df.iloc[i:i+5])
        i += 5
        flag = input("Do you want to view 5 more rows of raw data?\n\n").lower()


    df['Start Month'] = pd.to_datetime(df['Start Time']).dt.month_name()
    df['Start Day'] = pd.to_datetime(df['Start Time']).dt.day_name()
    df['Start Hour'] = pd.to_datetime(df['Start Time']).dt.hour

    if month != 'All':
        df = df[df['Start Month'] == month]
    
    if day != 'All':
        df = df[df['Start Day'] == day]

    return df

def display_data(df):
    i = 0
    flag = input("Do you want to view 10 rows of filtered data?\n\n").lower()
    while flag in ['yes','y'] and i+10 < df.shape[0]:
        print(df.iloc[i:i+10])
        i += 10
        flag = input("Do you want to view 10 more rows of filtered data?\n\n").lower()


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Start Month'].mode()[0]
    print("The most commom month is: {}\n".format(most_common_month))

    # display the most common day of week
    most_common_day = df['Start Day'].mode()[0]
    print("The most commom day of week is: {}\n".format(most_common_day))
    
    # display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print("The most commom start hour is: {}\n".format(most_common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station is: {}.\n".format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print("The most commonly used end station is: {}.\n".format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    df['Combined Stations'] = df['Start Station'] + ' to ' + df['End Station']
    print("The  most frequent combination of start station and end station trip is from {}.\n".format(df['Combined Stations'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Travel Time'] = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time']))/np.timedelta64(1,'m')
    total_tavel_time = df['Travel Time'].sum()
    print("The total travel time of {} (days) and {} (months) is: {:.2f} mins.".format(day, month, total_tavel_time))

    # display mean travel time
    mean_tavel_time = df['Travel Time'].mean()
    print("The mean travel time of {} (days) and {} (months) is: {:.2f} mins.".format(day, month, mean_tavel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The counts of user types is:\n")
    print(df['User Type'].value_counts().to_frame())
    print("\n\n")

    # Display counts of gender
    if "Gender" in df.columns:
        df['Gender'] = df['Gender'].fillna("Unknown")
        print("The counts of gender is:\n")
        print(df['Gender'].value_counts().to_frame())
        print("\n\n")
    else:
        print("There is no gender information collected in this city.\n")
    

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        print("The earliest year of birth is: {}.\n".format(int(df['Birth Year'].min())))
        print("The most recent year of birth is: {}.\n".format(int(df['Birth Year'].max())))
        print("The most common year of birth is: {}.\n".format(int(df['Birth Year'].mode())))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print("There is no Birth Year information collected in this city.\n")
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        #display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df, month, day)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['yes', 'y', 'yup', 'yeah']:
            break


if __name__ == "__main__":
	main()
