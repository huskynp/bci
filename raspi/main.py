from ADCDifferentialPi import ADCDifferentialPi
import time

adc = ADCDifferentialPi(0x68,0x69, 12)
adc.set_conversion_mode(1)
adc.set_pga(8)

print("     2 Channel BCI       ")
print("=========================")
print("Plug into channel 1 and 5\n")
print("KeyboardInterrupt to end")
input("Ready?")

# begin sampling
start_sample_time = time.time()
channel_1 = []
channel_2 = []

timer = 0
ensured_sample_rate = 240 #250 OR BELOW for 12-bit

samples = 0
LOG_RATE = 5 # seconds between logs

try:
    print("\nsampling...")
    while 1:
        channel_1.append(adc.read_voltage(1))
        channel_2.append(adc.read_voltage(5))
        timer += 1/ensured_sample_rate
        samples += 1
        if (samples/ensured_sample_rate) % LOG_RATE == 0: print(round(timer, 2), "seconds")
        early_time = timer - (time.time() - start_sample_time)
        if early_time > 0: time.sleep(early_time)
        
except KeyboardInterrupt:
    sample_time = time.time()-start_sample_time
    hertz = samples/sample_time
    print("Sample Rate:", round(hertz, 3), " samples per second")
    
    ch1len = len(channel_1)
    ch2len = len(channel_2)
    if(ch1len != ch2len):
        print("Warning: Channel Difference!",)
        if ch1len > ch2len: del channel_1[-1]
        else: del channel_2[-1]
        print("Fixed Lengths:", ch1len, ch2len)
        
        
filename = str(int(time.time())) + "-raw.csv"
print("\nSaving values to " + filename + "...")

import pandas as pd

time_list = [i/ensured_sample_rate for i in range(samples)]


data = {"time": time_list, "ch1": channel_1, "ch2": channel_2}
df = pd.DataFrame(data)
df.to_csv(filename)

print("File saved - run pre_process.py")

input("showing graph (Ctrl+C to exit)...")

import matplotlib.pyplot as plt

df.plot(x="time", y=["ch1", "ch2"])

plt.show()