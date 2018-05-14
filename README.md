# VSTmonitoring

A few plotting scripts for using the output from the VST Analysis code. 

## Usage

After running, e.g., the VSTAnalysis module, you should have a regular root file with a branch containing ChannelData and (optionally) HeaderData, as defined in the VSTAnalysis code. You can then using the following plotter scripts on the code:

### waveform.py

Makes a plot of the waveform (only possible if fill_waveform was set to true in the VSTAnalysis fcl file). Arguments:

- Specify input file: -i input_file 
- Whether to save the plot: -s
- Specify output file: -o output_file
- Display plot: -w
- Specify channel: -c
- Specify event: -e
- Show pedestal on plot: -b
- Show peaks on plot: -p
- Show noise ranges on plot: -n
- Also print out ChannelData object: -d

### fft.py

Makes a plot of the FFT of the waveform (only possible if calc_fft was set to true in the VSTAnalysis fcl file). Arguments:

- Specify input file: -i input_file 
- Whether to save the plot: -s
- Specify output file: -o output_file
- Display plot: -w


### interesting_channels.py

Prints out every channel in every event that has a hit on it. Arguments:

- Specify input file: -i input_file 

### summed_waveforms.py 

Plots the waveform of every channel summed across a FEM (only possible if sum_waveforms was set to true in the VSTAnalysis fcl file). Arguments:

- Specify input file: -i input_file 
- Whether to save the plot: -s
- Specify output file: -o output_file
- Display plot: -w
- Specify FEM: -f
- Specify event: -e


### distributions.py

Makes a distribution of different types of data for all the channels. Note that this file can be run when reduce_channel_data is set to true in the VSTAnalysis fcl file. Arguments:

- Specify input file: -i input_file 
- Whether to save the plot: -s
- Specify output file: -o output_file
- Display plot: -w
- Whether to bin by channel or by channel per event (default is to bin by channel): -p
- Whether to print data values: -v
- Which data metric to plot: -d data_types
- Possible values for data_types
  - rms: the RMS noise 
  - occupancy: the hit occupancy percentage
  - mean_peak_height: the average peak height of hits
  - baseline: the pedestal value

