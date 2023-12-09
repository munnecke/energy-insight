
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_prefix = "/Users/munnecke/opt/anaconda3/envs/homeflow/sdge/"
hoeben_sdge_path = file_prefix + 'hoeben_sdge_trimmed.csv' 
hoeben_sdge_data = pd.read_csv(hoeben_sdge_path)
hoeben_sdge_data['Datetime'] = pd.to_datetime(hoeben_sdge_data['Date'] + ' ' + hoeben_sdge_data['Start Time'], format='%m/%d/%Y %I:%M %p')
print (hoeben_sdge_data)
def show_totals():
    print("Yearly Totals:")
    print(monthly_data.sum(numeric_only=True))

    print("\nMonthly Subtotals:")
    print(monthly_data.set_index('Datetime').resample('M').sum())

# Define the get_rate function as provided
def get_rate(timestamp):
    # Convert the strings to 2D lists of integers
    weekday="666666555555555544444555666666555555555544444555666666555566665544444555666666555566665544444555666666555555555544444555333333222222222211111222333333222222222211111222333333222222222211111222333333222222222211111222333333222222222211111222666666555555555544444555666666555555555544444555"
    weekend="666666666666665544444555666666666666665544444555666666666666665544444555666666666666665544444555666666666666665544444555333333333333332211111222333333333333332211111222333333333333332211111222333333333333332211111222333333333333332211111222666666666666665544444555666666666666665544444555"

    weekday_rates = [list(map(int, weekday[i:i+24])) for i in range(0, len(weekday), 24)]
    weekend_rates = [list(map(int, weekend[i:i+24])) for i in range(0, len(weekend), 24)]

    TOU_rates = [0, 0.81629, 0.48129, 0.15351, 0.51149, 0.44775, 0.1452] #per EV-TOU-5 rates

    # Check if the timestamp is on a weekday or weekend
    if timestamp.weekday() < 5:
        rates = weekday_rates
    else:
        rates = weekend_rates

    # Calculate the month and hour from the timestamp
    month = timestamp.month - 1  # Months are 1-based in datetime, but 0-based in our list
    hour = timestamp.hour

    # Return the rate
    return TOU_rates[rates[month][hour]]
# Apply the TOU rate function
hoeben_sdge_data['TOU Rate'] = hoeben_sdge_data['Datetime'].apply(get_rate)

# Calculate the 'value of' columns
hoeben_sdge_data['Value of Consumption'] = hoeben_sdge_data['Consumption'] * hoeben_sdge_data['TOU Rate']
hoeben_sdge_data['Value of Generation'] = hoeben_sdge_data['Generation'] * hoeben_sdge_data['TOU Rate']
hoeben_sdge_data['Value of Net'] = hoeben_sdge_data['Net'] * hoeben_sdge_data['TOU Rate']

# Group by month and summarize the data
monthly_data = hoeben_sdge_data.groupby(hoeben_sdge_data['Datetime'].dt.to_period('M')).agg({
    'Consumption': 'sum',
    'Generation': 'sum',
    'Net': 'sum',
    'Value of Consumption': 'sum',
    'Value of Generation': 'sum',
    'Value of Net': 'sum'
}).reset_index()
monthly_data['Datetime'] = monthly_data['Datetime'].dt.to_timestamp()

# Create the plot
fig, ax1 = plt.subplots(figsize=(12, 7))

# Plot Consumption, Generation, and Net on the left Y axis
ax1.plot(monthly_data['Datetime'], monthly_data['Consumption'], label='Consumption (kWh)', color='red', marker='o')
ax1.plot(monthly_data['Datetime'], monthly_data['Generation'], label='Generation (kWh)', color='green', marker='o')
ax1.plot(monthly_data['Datetime'], monthly_data['Net'], label='Net (kWh)', color='blue', marker='o')

# Label the left Y axis
ax1.set_ylabel('Energy (kWh)', color='black')
ax1.tick_params(axis='y', labelcolor='black')

# Plot the corresponding "value of" columns on the right Y axis
ax2 = ax1.twinx()
ax2.plot(monthly_data['Datetime'], monthly_data['Value of Consumption'], label='Value of Consumption ($)', color='red', marker='o', linestyle='--')
ax2.plot(monthly_data['Datetime'], monthly_data['Value of Generation'], label='Value of Generation ($)', color='green', marker='o', linestyle='--')
ax2.plot(monthly_data['Datetime'], monthly_data['Value of Net'], label='Value of Net ($)', color='blue', marker='o', linestyle='--')

# Label the right Y axis
ax2.set_ylabel('Value ($)', color='black')
ax2.tick_params(axis='y', labelcolor='black')

# Set the x-axis labels to month names
ax1.set_xticks(monthly_data['Datetime'])
ax1.set_xticklabels(monthly_data['Datetime'].dt.strftime('%b'), rotation=45)

# Title and labels
ax1.set_title('Hoeben - Monthly Energy Data and Corresponding Value')

# Adding legends
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Show the plot
plt.show()
show_totals()




