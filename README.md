# School Test Database

Test database for Jinja Senior Secondary School used by the OneCard System.

## Overview

Contains 3,600 students with payment transactions. OneCard connects via read-only access.

## Tables

| Table | Records |
|-------|:-------:|
| students | 3,600 |
| payments | ~4,200 |
| classes | 6 |
| terms | 3 |
| staff | 5 |

## Setup

mysql -u root -p < setup.sql
python generate_data.py
python add_payments.py

## Author

Herman Software Solutions
- GitHub: https://github.com/jiangsalim
