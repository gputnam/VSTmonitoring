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

    real = fft_data.channel_data[args.channel].fft_real
    imag = fft_data.channel_data[args.channel].fft_imag

    graph_title = "Event %i Channel %i FFT" % (args.event, args.channel)
    plot(real, imag, args.output, graph_title, args)

def plot(fft_real, fft_imag, output_name, graph_title, args):
    skip = int(not args.keep_baseline)
    n_data = len(fft_real) - skip

    fft_data_array = array('d')
    freq_array = array('d')
    for i,(re,im) in enumerate(zip(fft_real, fft_imag)):
        if i < skip:
            continue
        d = math.sqrt((re*re + im*im))
        fft_data_array.append(d)
        freq_array.append(float(i+skip))

    canvas = ROOT.TCanvas("canvas", "Waveform Canvas", 250,100,700,500)

    graph = ROOT.TGraph(n_data, freq_array, fft_data_array)
    graph.SetTitle(graph_title)
    graph.GetXaxis().SetTitle("fft number")
    graph.GetYaxis().SetTitle("fft value")
    graph.Draw()
    canvas.Update()

    if args.wait:
        raw_input("Press Enter to continue...")

    if args.save:
        canvas.SaveAs(output_name + ".pdf")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = with_location_args(parser)
    parser = with_io_args(parser)

    parser.add_argument("-c", "--channel", type=int, default=0)
    parser.add_argument("-b", "--keep_baseline", action="store_true")
    
    main(parser.parse_args())
