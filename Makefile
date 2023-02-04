BINARY=bin
INCDIRS=-Iinclude
SRCDIR=src
OBJECTDIR=obj
BINDIR= binaries
PYTHONDIR=python
CC=gcc
OPT=-O0

DEPFLAGS=-MP -MD
CFLAGS=-Wall -Wextra -g $(INCDIRS) $(OPT) $(DEPFLAGS)

CFILES=$(wildcard $(SRCDIR)/*.c)

OBJECTS := $(patsubst $(SRCDIR)%, $(OBJECTDIR)%, $(patsubst %.c,%.o,$(wildcard $(SRCDIR)/*.c)))

DEPFILES=$(patsubst %.c, %.d, $(CFILES))

all: $(BINDIR)/$(BINARY)

$(BINDIR)/$(BINARY): $(OBJECTS) | $(BINDIR) $(OBJECTDIR)
	echo $(CFILES)
	$(CC) -o $@ $^
	
$(OBJECTDIR)/%.o:$(SRCDIR)/%.c $(DEPS) | $(OBJECTDIR)
	@echo Building $@
	@$(CC) -c -o $@ $< $(CFLAGS)

$(OBJECTDIR) :
	@mkdir -p $(OBJECTDIR)
	@echo Created ./$(OBJECTDIR) folder

$(BINDIR):
	@mkdir -p $(BINDIR)
	@echo Created ./$(BINDIR) folder

clean:
	@echo Removing compiled files...
	@rm -fr $(OBJECTDIR) $(BINDIR) 
	@rm -f *.d 
	@echo Files were succesfully removed

pythonclient: $(BINDIR)/$(BINARY)
	./$(BINDIR)/$(BINARY) &
	python3 $(PYTHONDIR)/client.py	

.PHONY:pythonclient clean