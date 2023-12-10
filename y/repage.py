#/usr/bin/env python

from pprint import pprint

from csv import reader as  csv_reader

from fitz import Document

infile = "../read/I Ching (Lynn) [4ca0694e].pdf"
outfile = "4ca0694e.pdf"
tocfile = 'index.csv'
startpage = 16

pagelabels = [
  {'startpage': 0, 'prefix': '', 'style': '', 'firstpagenum': 1},
  {'startpage': 6, 'prefix': '', 'style': 'r', 'firstpagenum': 1},
  {'startpage': startpage, 'prefix': '', 'style': 'D', 'firstpagenum': 1}
]

toc = [ (int(x[0]), x[1].strip().strip('"'), int(x[2]) + startpage)  for x in csv_reader(open(tocfile)) ]

with Document(infile) as pdf:
  pdf.set_page_labels( pagelabels )
  pdf.set_toc(toc)
  pdf.save(outfile, garbage=4, clean=True, deflate=True)


