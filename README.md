# observer-design-pattern-python

## The purpose of this repo is the following:
### Have some fun with design patterns + Display to employers my Python Programming capabilities

The idea is to imitate GCP PubSub infrastructure as best as possible using the Observer design pattern with only pure Python 
The `main.yaml` file shows configuration of a persons setup - based on this file, the program will create the necessary observers and notify 
each observer

To run this repo: 
1. CD in to the directory
2. run 
```python3 src/main.py --input_path_to_yaml=src/main.yaml --input_path_to_data=src/data/uk_dummy_addresses.json```
3. To run the tests, run:
```
PYTHONPATH=$(pwd)/src pytest tests/unit_tests/
PYTHONPATH=$(pwd)/src pytest tests/integration_tests/
```
_so we don't have to set PYTHONPATH for this repo permanently_ 

