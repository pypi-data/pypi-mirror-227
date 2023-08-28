###########################################################################
#    Copyright (c) 1991 - 1994 Heinz W. Werntges.  All rights reserved.
#   Parts Copyright (c) 1999  Martin Kroeker  All rights reserved.
#    Distributed by Free Software Foundation, Inc.
#
# This file is part of HP2xx.
#
# HP2xx is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY.  No author or distributor accepts responsibility
# to anyone for the consequences of using it or for whether it serves any
# particular purpose or works at all, unless he says so in writing.  Refer
# to the GNU General Public License, Version 2 or later, for full details
#
# Everyone is granted permission to copy, modify and redistribute
# HP2xx, but only under the conditions described in the GNU General Public
# License.  A copy of this license is supposed to have been
# given to you along with HP2xx so you can know your rights and
# responsibilities.  It should be in a file named COPYING.  Among other
# things, the copyright notice and this notice must be preserved on all
# copies.
###########################################################################
#
# Generic Makefile for misc. versions of emu7470; strong emphasis on UNIXes
#
# Utilities etc.:
#

RMCMD    = rm -f


# CC and CFLAGS set for gcc, but any ANSI-C compiler should work.
# For non-gcc compilers, simply set CFLAGS = -O (to start with)
#
CFLAGS	=  -O2 -g  $(DEFINES) $(EX_DEFS) -Wall -pedantic -Wuninitialized -Wunused -Wreturn-type -Wmissing-prototypes -Wstrict-prototypes  
LINT	= splint
LINTFLAGS = -weak -initallelements +posixlib  $(DEFINES) $(EX_DEFS)



#############################################################################
# MAIN CONFIGURATION TASK:
# Define the target machine / OS by uncommenting the appropriate lines below.
# Remember to comment-out the defaults (a) if they do not apply!
#
# Generic UNIX + X11 previewer (default)
#
DEFINES   = -DUNIX 
ALL_LIBS  =  -lm     
#
# Standard setting: No extras:

COMMON_INCS	= emu7470.h 
ALL_INCS	= $(COMMON_INCS) chardraw.h charset0.h charset5.h charset7.h 
ALL_CFLAGS	= -c $(CFLAGS)


# $(SRCS) NOT USED YET:
SRCS	= emu7470.c  chardraw.c $(ALL_INCS) lindef.c 

OBJS	= emu7470.o   chardraw.o  lindef.o 

PROGRAM	= emu7470

$(PROGRAM): $(OBJS)
	$(CC) $(OBJS) $(ALL_LIBS) $(EX_LIBS) -o $(PROGRAM)
	$(BINDCMD)


clean:
	-make mostlyclean
	-$(RMCMD) core a.out *~  $(PROGRAM)


mostlyclean:
	-$(RMCMD) *.o

realclean:
	-make clean
	-$(RMCMD) $(PROGRAM)
