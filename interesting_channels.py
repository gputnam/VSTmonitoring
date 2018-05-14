import ROOT
import argparse

def main(args):
    adc_data_file = ROOT.TFile(args.input_file)
    t_directory_file = adc_data_file.Get("SimpleDaqAnalysis")

    adc_data = t_directory_file.Get("event") 

    i = 0
    for event in adc_data:
        for channel in event.channel_data:
            if int(channel.peaks.size()) > 0:
                print "INTERESTING EVENT: %i CHANNEL: %i" % (i, channel.channel_no)
        i += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", default="output.root")
    
    main(parser.parse_args())
