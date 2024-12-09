#!/bin/bash

folders=("01" "02" "03" "04" "05" "06" "07" "10")

for folder in "${folders[@]}"; do
  echo "Running tests for $folder/test_*.py"
  coverage run -m unittest discover -s "$folder" -p "test_*.py" -t "."
  if [ $? -ne 0 ]; then
    echo "Tests failed in folder $folder"
    exit 1
  fi
  coverage report -m
done
