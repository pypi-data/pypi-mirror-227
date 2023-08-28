1 printer is :DEVADDR("HP7470A")
10 print "IN;PA300,279;SP2:PD:TL100;XT;"
20 for i=1 to 10
30 print "PR1000,0;XT;"
40 next i
50 print "TL;PU;PA300,279;PD"
60 gosub 1000
70 print "TL1,0;PU;PA1300,279;PD;"
80 gosub 1000
90 print "TL0,5;PU;PA2300,279;"
100 gosub 1000
110 print "PA300,7479;TL100;YT;PU;SP0;"
120 stop
1010 for j=1 to 9
1020 print "PR0,720;YT;"
1030 next j
1040 return
1050 end
