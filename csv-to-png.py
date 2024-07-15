import argparse
import pandas as pd
import matplotlib.pyplot as plt

def plot_data(input_csv, output_png):
    """
    Reads the input CSV, processes the data, and plots the CPU, LPM, and DEEP LPM usage for each mote over time.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv)
    
    # Ensure 'mote' is treated as a category for consistent colors across plots
    df['mote'] = df['mote'].astype('category')

    # Setup the plot - 3 subplots vertically
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 15), sharex=True)

    # Plot CPU, LPM, and DEEP LPM in separate subplots
    for name, group in df.groupby('mote'):
        axes[0].plot(group['time'], group['cpu'], label=f'Mote {name}')
        axes[1].plot(group['time'], group['lpm'], label=f'Mote {name}')
        axes[2].plot(group['time'], group['deeplpm'], label=f'Mote {name}')

    # Set titles, labels, and legends
    axes[0].set_title('CPU Usage Over Time')
    axes[1].set_title('LPM Usage Over Time')
    axes[2].set_title('DEEP LPM Usage Over Time')
    for ax in axes:
        ax.set_xlabel('Time (units)')
        ax.set_ylabel('Value')
        ax.legend(loc='best')

    # Improve layout and save the figure
    plt.tight_layout()
    plt.savefig(output_png)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot CPU, LPM, and DEEP LPM usage from CSV data.')
    parser.add_argument('input_csv', type=str, help='Input CSV file path.')
    parser.add_argument('output_png', type=str, help='Output PNG file path.')
    
    args = parser.parse_args()
    
    plot_data(args.input_csv, args.output_png)
