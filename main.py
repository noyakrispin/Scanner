from datetime import datetime
import os
import re
import gui_analyze


def black_scanner():
    # The occupy percentage reference
    ref_level = gui_analyze.input_occupy()
    # prepare list for the new files
    files = []
    # scan the folder files
    for name in os.listdir("."):
        if name.endswith(".txt"):
            files.append(name)
            print(name)
    # load the files from previous run
    scanned_files = open('file.list', 'r+')
    # list of files from previous run
    scanned_list = scanned_files.read().splitlines()
    # check for new files
    for file in files:
        if file not in scanned_list:
            # New csv file that will contains the parsed data
            data_file = open('data.csv', 'w')
            #
            interval_time = []
            # list of all channels in the scan
            channels_list = []
            # number of channels un the scan
            num_of_channels = 0
            # parse the data
            file_content = open(file, 'r')
            for line in file_content:
                if line.__contains__('0'):
                    if line.__contains__('|') and line.__contains__('-'):
                        line = re.sub('\|', ',', line)
                        line = re.sub('-', '', line)
                        line = re.sub('\.', '/', line)
                        line = re.sub('(\:)(\d{3})','.\g<2>', line)
                        data_file.write(line)
                    elif not line.__contains__('}'):
                        line = line.strip()
                        line = re.sub('(.*)(\d{9})(.*)','\g<2>', line)
                        channels_list.append(line)
                        num_of_channels += 1
                    elif line.__contains__('}'):
                        line = line.strip('}{\n')
                        line = re.sub('-', '', line)
                        line = re.sub('\.', '/', line)
                        line = re.sub('(\:)(\d{3})', '.\g<2>', line)
                        interval_time.append(datetime.strptime(line, '%d/%m/%Y%H:%M:%S.%f'))
            roundup = 0.044263 + (0.057208*num_of_channels) - (0.00019294*(num_of_channels**2)) + (0.0000021959*(num_of_channels**3)) - (0.0000000062509*(num_of_channels**4))
            # calculate the total seconds of the scan
            total_interval_seconds = interval_time[1].__sub__(interval_time[0]).total_seconds()
            data_file.close()
            file_content.close()
            appearance_time = open('appearance_time.csv', 'w')
            for channel in channels_list:
                row0 = ''
                csv_file = open('data.csv', 'r')
                for row1 in csv_file:
                    if not row1.__contains__(channel):
                        continue
                    row1 = row1.strip()
                    row1 = row1.split(',')
                    if row0 != '':
                        date_time1 = row0[1]
                        date_time1 = datetime.strptime(date_time1, '%d/%m/%Y%H:%M:%S.%f')
                        date_time2 = row1[1]
                        date_time2 = datetime.strptime(date_time2, '%d/%m/%Y%H:%M:%S.%f')
                        delta_times = date_time2.__sub__(date_time1)
                        if delta_times.total_seconds() >= 10:
                            appearance_time.write(f'{row0[0]},{str(10+roundup)}\n')
                        else:
                            appearance_time.write(f'{row0[0]},{str(delta_times.total_seconds())}\n')
                    row0 = row1
                csv_file.close()
            appearance_time.close()
            ##############################################################################################
            ##############################################################################################
            excel_file = open('black_scanner.csv', 'a')
            # A Excel file that contains the appearance percent per week
            time = 0.0
            excel_file.write(f'{interval_time[0].date()},{interval_time[1].date()}\n')
            excel_file.write('Frequency[MHz],Occupy[%],Above Threshold\n')
            for channel in channels_list:
                csv_file = open('appearance_time.csv', 'r')
                for line in csv_file:
                    line = line.strip()
                    line.split(',')
                    if channel.__contains__(line[0]):
                        time += float(line[1])
                occupy = time * 100 / total_interval_seconds
                excel_file.write(f'{channel},{occupy}%')
                if occupy >= float(ref_level):
                    excel_file.write(',V\n')
                else:
                    excel_file.write('\n')
                time = 0.0
                csv_file.close()
            scanned_files.write(file+'\n')
            excel_file.close()


if __name__ == '__main__':
    black_scanner()

