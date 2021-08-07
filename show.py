from tkinter import *
from tkmagicgrid import *
import io
import csv

# Create a root window
root = Tk()
root.title("Attendence Sheet")
# Create a MagicGrid widget
grid = MagicGrid(root)
grid.pack(side="top", expand=1, fill="both")

# Display the contents of some CSV file
with io.open("present.csv", "r", newline="") as csv_file:
    reader = csv.reader(csv_file)
    parsed_rows = 0
    for row in reader:
        if parsed_rows == 0:
    	    # Display the first row as a header
    	    grid.add_header(*row)
        else:
    	    grid.add_row(*row)
        parsed_rows += 1

# Start Tk's event loop
root.mainloop()



