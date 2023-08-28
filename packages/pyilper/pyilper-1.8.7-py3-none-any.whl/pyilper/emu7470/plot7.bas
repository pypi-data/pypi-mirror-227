10 printer is :DEVADDR("HP7470A")
20 print "IN;SP1;IP2650,1325,7650,6325;"
30 print "SC-1000,1000,-1000,1000;"
40 print "PA-800,800;"
50 gosub 130
60 print "PA200,800;"
70 gosub 130
80 print "PA-800,-200;"
90 gosub 130
100 print "PA200,-200;"
110 gosub 130
120 end
130 print "CI50;PR600,0;CI50;PR-300,-300;CI250;"
140 print "PR-300,-300;CI50;PR600,0;CI50;"
150 return

