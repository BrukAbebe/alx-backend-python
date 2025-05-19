# Python Generators Project

This project implements Python generators to process MySQL data efficiently for the ALX Backend specialization.

## Files
- `seed.py`: Sets up the `ALX_prodev` database and `user_data` table, populates with `user_data.csv`.
- `0-stream_users.py`: Generator to stream rows one by one.
- `1-batch_processing.py`: Generators for batch processing, filtering users over 25.
- `2-lazy_paginate.py`: Generator for lazy pagination.
- `4-stream_ages.py`: Generator to compute average age.
- `user_data.csv`: Input data with `name,email,age` columns (excluded from Git, see sample below).
- `0-main.py`, `1-main.py`, `2-main.py`, `3-main.py`: Test scripts for tasks.
- `.gitignore`: Excludes unnecessary files.

## Setup
1. Install MySQL, Python, and `mysql-connector-python`:
   ```bash
   pip install mysql-connector-python