import glob
import time

SAMPLE_RATE = 2

# Function to find the list of temperature probes
def find_temperature_probes():

    # Get and return a list of the temperature probes
    return glob.glob('/sys/bus/w1/devices/28*')

# Function to read the current temperature reported by the requested probe
#
#  Arguments:
#
#   probe: A string containing the path to a DS18B20 probe
#          (call find_temperature_probes to get a list of these).
#
#   returns: A float containing the current temperature
#            or -1 if an error occured
#
def read_temperature(probe):

    # Open the location contining data relating to the chosen probe
    probe_handle = open(probe + "/w1_slave", 'r')

    # Read the first line of data from the probe
    line = probe_handle.readline()

    # Check that the temperatur was measured correctly
    # by checking that there is data and that the data
    # ends with the string 'YES'
    if line != '' and line.endswith('YES\n'):

        # Read the next line and check that it contains the temperature

        temperature_line = probe_handle.readline()
        temperature_index = temperature_line.find('t=')

        if temperature_line != "" and temperature_index != -1:
            return float(temperature_line[temperature_index+2:]) / 1000.0

    return -1

# Function to repeatedly read and print the current temperature reported by a
# requested probe
#
#  Arguments:
#
#   probe: A string containing the path to a DS18B20 probe
#          (call find_temperature_probes to get a list of these).
#
def monitor_temperature(probe):

    # Start reading the temperature repeatedly and keep doing so until
    # the execution of the program is stopped
    while True:

        # Read the current temperature of the requested probe
        temperature = read_temperature(probe)

        # Print the current temperature
        print('The temperature is %f' % temperature)

        # Stop execution until the next sample needs to be taken
        time.sleep(1/SAMPLE_RATE)

#
# Start the execution of the program
#
if __name__ == "__main__":

    print('Starting temperature monitor...')

    # Handle any errors that may occur during the execution of the program
    try:

        # Get the list of currently attached probes
        probes = find_temperature_probes()

        # Check that there are temperature probes attached to the system
        if probes != None and len(probes) >= 1:

            # Monitor the first temperature probe connected
            monitor_temperature(probes[0])
        else:
            print('No temperature probes found!')

    except KeyboardInterrupt:
        pass
    finally:
        # When the user chooses to quit the program, then print an
        # appropriate message
        print("Stopping temperature monitor...")
