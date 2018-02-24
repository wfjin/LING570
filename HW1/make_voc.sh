#!/bin/sh
cat > tmpfile
python3 make_voc.py tmpfile $@
