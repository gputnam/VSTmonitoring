import ROOT
import os
import sys
from array import array
import argparse
import math
from util import *

def main(args):
	fft_data_file = ROOT.TFile(args.input_file)
	t_directory_file = fft_data_file.Get("VSTAnalysis")

	fft_data = t_directory_file.Get("event") 

	fft_data = get_event(fft_data, args.event, args.absolute)

	graph_title = "Event %i FFT" % (args.event)

	channel_arr = array('d')
	fft1_data = array('d')
	freq_data = array('d')

	temp_channel = array('d')
	temp_fft = array('d')
	temp_freq = array('d')
	for w in range(0,480):
		real = fft_data.channel_data[w].fft_real
		imag = fft_data.channel_data[w].fft_imag

		temp_fft,temp_freq,temp_channel = plot(real, imag, args, w)

		channel_arr = channel_arr + temp_channel
		fft1_data = fft1_data + temp_fft
		freq_data = freq_data + temp_freq
		del temp_fft[:],temp_freq[:],temp_channel[:]

	n = len(channel_arr)

	canvas = ROOT.TCanvas("canvas", "Waveform Canvas", 250,100,700,500)
	graph = ROOT.TGraph2D(n,channel_arr,freq_data,fft1_data)
	graph.SetTitle(graph_title+"; Channel; Frequency(Hz); FFT Value")
	graph.Draw("COLZ")
        #canvas.SetLogz()
	canvas.Update()
	if args.wait:
		raw_input("Press Enter to continue...")
	output_name = args.output
	if args.save:
		canvas.SaveAs(output_name + ".pdf")
		#canvas.SaveAs(output_name + ".jpg")
def plot(fft_real, fft_imag, args, w_int):
	temp = array('d')
	skip = int(not args.keep_baseline)
	n_data = len(fft_real) - skip

        max_freq = 1000.
        freq_bin = max_freq / len(fft_real)

	fft_data_array = array('d')
	freq_array = array('d')
	for i,(re,im) in enumerate(zip(fft_real, fft_imag)):
                if i < 300 or i >  900:
                    continue
                
		if i < skip:
		    continue
		d = math.sqrt((re*re + im*im))
		fft_data_array.append(d)
		freq_array.append(float(i+skip) * freq_bin)
		temp.append(w_int)

	return fft_data_array, freq_array, temp

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = with_location_args(parser)
    parser = with_io_args(parser)

    #parser.add_argument("-c", "--channel", type=int, default=0)
    parser.add_argument("-b", "--keep_baseline", action="store_true")
    
    main(parser.parse_args())
