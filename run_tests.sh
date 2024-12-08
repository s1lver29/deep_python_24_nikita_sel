#!/bin/bash

folders=("01" "02" "03" "04" "05" "06" "07")

for folder in "${folders[@]}"; do
  echo "Running tests for $folder/test_*.py"
  coverage run -m unittest discover -s "$folder" -p "test_*.py" -t "."
  coverage report -m
done
