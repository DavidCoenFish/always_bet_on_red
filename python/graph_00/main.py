"""
python main.py
//C:\development\always_bet_on_red\python\graph_00\
python main.py BTC-USD.csv

import pygal                                                       # First import pygal
    bar_chart = pygal.Bar()                                            # Then create a bar graph object
    bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values
    bar_chart.render_to_file('bar_chart.svg')                          # Save the svg to a file

import svgwrite

dwg = svgwrite.Drawing('test.svg', profile='tiny')
dwg.add(dwg.line((0, 0), (10, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.text('Test', insert=(0, 0.2), fill='red'))
dwg.save()
    """

import csv
import sys
import svgwrite

#https://stackoverflow.com/questions/736043/checking-if-a-string-can-be-converted-to-float-in-python
def is_float(element: any) -> bool:
    #If you expect None to be passed:
    if element is None: 
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False

def load_csv(file_path):
    result = []
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                if is_float(row[1]) and is_float(row[2]) and is_float(row[3]) and is_float(row[4]):
                    #Date,Open,High,Low,Close,Adj Close,Volume
                    #print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                    data_open = float(row[1]) / 100.0
                    data_high = float(row[2]) / 100.0
                    data_low = float(row[3]) / 100.0
                    data_close = float(row[4]) / 100.0
                    data_adj_close = float(row[5]) / 100.0
                    result.append([data_open, data_high, data_low, data_adj_close])
                    line_count += 1
        print(f'Processed {line_count} lines.')
    return result

def draw_graph(drawing, data, drawing_low, drawing_height):
    trace = 0
    for row in data:
        if len(row) < 4:
            continue
        #Open,High,Low,Close
        data_open = drawing_height - (row[0] - drawing_low)
        data_high = drawing_height - (row[1] - drawing_low)
        data_low = drawing_height - (row[2] - drawing_low)
        data_close = drawing_height - (row[3] - drawing_low)

        drawing.add(drawing.line((trace + 1, data_low), (trace + 1, data_high), stroke_width=1, stroke='black'))
        if data_open == data_close:
            drawing.add(drawing.line((trace -1, data_open), (trace + 6, data_open), stroke_width=1, stroke='black'))
        elif data_close < data_open: # y axis swapped for drawing
            drawing.add(drawing.line((trace + 1, data_open), (trace + 1, data_close), stroke_width=3, stroke='green'))
        else:
            drawing.add(drawing.line((trace + 1, data_open), (trace + 1, data_close), stroke_width=3, stroke='red'))

        trace += 4

def calculate_vertical_range(data):
    first = True
    result = [0,0]
    for row in data:
        if first == True:
            result[0] = min(row)
            result[1] = max(row)
            first = False
        else:
            result[0] = min(result[0], row[0], row[1], row[2], row[3])
            result[1] = max(result[1], row[0], row[1], row[2], row[3])
    return result

def main():
    data = load_csv(sys.argv[1])
    vertical_range = calculate_vertical_range(data)

    drawing_width = 4 * len(data)
    drawing_height = vertical_range[1] - vertical_range[0]
    drawing = svgwrite.Drawing('test.svg', height=drawing_height, width=drawing_width)

    draw_graph(drawing, data, vertical_range[0], drawing_height)

    drawing.save()

if __name__ == "__main__":
    main()