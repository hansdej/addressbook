#!/bin/sh
python3 check_assignments.py
cd ../
python3 -m pytest
