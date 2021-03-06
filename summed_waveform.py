import ROOT
import sys
import os
from array import array
import argparse
import math
from util import *

# TODO @INSTILLATION: update
def channel_list(fem):
    return range(fem*64, (fem+1)*64)

def main(args):
    adc_data_file = ROOT.TFile(args.input_file)
    t_directory_file = adc_data_file.Get("VSTAnalysis")

    adc_data = t_directory_file.Get("event") 
    adc_data = get_event(adc_data, args.event, args.absolute)

    empty = adc_data.channel_data[0].empty
    if empty:
        print "Empty channel"
        return
    
    waveform = adc_data.summed_waveforms[args.fem]

    graph_title = "Event %i FEM %i Summed Waveform" % (args.event, args.fem)
    plot(waveform, args.output, graph_title, args)

def plot(adc_data, output_name, graph_title, args):
    n_data = len(adc_data)

    adc_data_array = array('d')
    time_array = array('d')
    for i,d in enumerate(adc_data):
        adc_data_array.append(d)
        time_array.append(float(i))

    canvas = ROOT.TCanvas("canvas", "Waveform Canvas", 250,100,700,500)

    graph = ROOT.TGraph(n_data, time_array, adc_data_array)
    graph.SetTitle(graph_title)
    graph.Draw()
    canvas.Update()
    if args.wait:
       raw_input("Press Enter to continue...")
    if args.save:
       canvas.SaveAs(output_name + ".pdf")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = with_io_args(parser)
    parser = with_location_args(parser)

    parser.add_argument("-f", "--fem", type=int, default=0)
    
    main(parser.parse_args())
