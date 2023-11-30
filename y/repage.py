#/usr/bin/env python

from pprint import pprint

from csv import reader as  csv_reader

from fitz import Document

infile = "../read/I Ching (Lynn) [4ca0694e].pdf"
outfile = "4ca0694e.pdf"

startpage = 18

with Document(fname) as pdf:

  csvfile = [ (int(x[0]), x[1].strip().strip('"'), int(x[2]) + startpage)  for x in csv_reader(open('siu.csv')) ]

  pdf.set_toc(csvfile)
  pdf.save(fnew, garbage=4, clean=True, deflate=True)

  
