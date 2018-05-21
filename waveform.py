import ROOT
import sys
import os
from array import array
import argparse
import math
from util import *

def main(args):
    adc_data_file = ROOT.TFile(args.input_file)
    t_directory_file = adc_data_file.Get("VSTAnalysis")

    adc_data = t_directory_file.Get("event") 

    adc_data = get_event(adc_data, args.event, args.absolute)

    waveform = adc_data.channel_data[args.channel].waveform
    channel_data = adc_data.channel_data[args.channel]

    if args.dump:
        print channel_data.Print()

    if channel_data.empty:
        print "Empty channel"
        assert(waveform.size() == 0)
        return

    graph_title = "Event %i Channel %i Waveform" % (args.entry, args.channel)
    plot(waveform, args.output, adc_data.channel_data[args.channel], graph_title, args)

def plot(adc_data, output_name, channel_data, graph_title, args):
    peaks = channel_data.peaks
    baseline = channel_data.baseline
    noise_ranges = channel_data.noise_ranges

    n_data = len(adc_data)

    adc_data_array = array('d')
    time_array = array('d')
    for i,d in enumerate(adc_data):
        adc_data_array.append(d)
        time_array.append(float(i))

    canvas = ROOT.TCanvas("canvas", "Waveform Canvas", 250,100,700,500)

    all_graphs = ROOT.TMultiGraph()
    graph = ROOT.TGraph(n_data, time_array, adc_data_array)
    all_graphs.SetTitle(graph_title)
   
    all_graphs.Add(graph)
    if args.draw_baseline:
        line = ROOT.TGraph(2, array('d', [time_array[0], time_array[-1]]), array('d', [baseline, baseline]))
        line.SetLineColor(ROOT.kRed)
        line.SetLineWidth(1)
        all_graphs.Add(line)
    if args.draw_noise_ranges:
        lines = []
        for pair in noise_ranges:
            lines.append( ROOT.TGraph(2, array('d',[pair[0], pair[0]]), array('d', [channel_data.min, channel_data.max]))) 
            lines[-1].SetLineColor(46)
            lines[-1].SetLineWidth(1)
            all_graphs.Add(lines[-1])
            lines.append( ROOT.TGraph(2, array('d',[pair[1], pair[1]]), array('d', [channel_data.min, channel_data.max]))) 
            lines[-1].SetLineColor(46)
            lines[-1].SetLineWidth(1)
            all_graphs.Add(lines[-1])
 

    all_graphs.Draw("a")

    peak_graphs = []
    if args.draw_peaks:
        for peak in peaks:
            # and loose peak
            n_data = peak.end_loose - peak.start_loose + 1
            peak_graphs.append( ROOT.TGraph(n_data*2) )
            for i in range(n_data):
                waveform_ind = peak.start_loose + i
                peak_graphs[-1].SetPoint(i, time_array[waveform_ind], adc_data_array[waveform_ind])
                peak_graphs[-1].SetPoint(n_data+i, time_array[peak.start_loose + n_data-i-1], baseline)
            peak_graphs[-1].SetFillStyle(1001)
            peak_graphs[-1].SetFillColor(9)
            peak_graphs[-1].Draw("f")
            # draw tight peak
            n_data = peak.end_tight - peak.start_tight + 1
            peak_graphs.append( ROOT.TGraph(n_data*2) )
            for i in range(n_data):
                waveform_ind = peak.start_tight + i
                peak_graphs[-1].SetPoint(i, time_array[waveform_ind], adc_data_array[waveform_ind])
                peak_graphs[-1].SetPoint(n_data+i, time_array[peak.start_tight + n_data-i-1], baseline)
            peak_graphs[-1].SetFillStyle(3007)
            peak_graphs[-1].SetFillColor(8)
            peak_graphs[-1].Draw("f")

    all_graphs.GetXaxis().SetTitle("ADC Count")
    all_graphs.GetYaxis().SetTitle("ADC Value")

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
    parser.add_argument("-p", "--draw_peaks", action="store_true")
    parser.add_argument("-b", "--draw_baseline", action="store_true")
    parser.add_argument("-n", "--draw_noise_ranges", action="store_true")
    parser.add_argument("-d", "--dump", action="store_true")
    
    main(parser.parse_args())
