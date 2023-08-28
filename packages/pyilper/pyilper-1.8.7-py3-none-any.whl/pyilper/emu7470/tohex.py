import sys

for line in sys.stdin:
   print("00 ",end="")
   for c in line:
      if c=="\n":
         continue
      x="%2.2x" % ord(c)
      print(x,end="")
   print("")
