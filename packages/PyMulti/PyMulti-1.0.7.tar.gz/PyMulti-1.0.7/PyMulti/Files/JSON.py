# PyMulti (Files) - JSON

''' This is the "JSON" module. '''

'''
Copyright 2023 Aniketh Chavare

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Imports
import json

# Function 1 - Convert
def convert(data, indent=4):
    # Checking the Data Type of "data"
    if (isinstance(data, dict)):
        # Checking the Data Type of "indent"
        if (isinstance(indent, int)):
            # Converting Python Dictionary to JSON String
            return json.dumps(data, indent=indent)
        else:
            raise TypeError("The 'indent' argument must be an integer.")
    elif (isinstance(data, str)):
        # Converting JSON String to Python Dictionary
        return json.loads(data)
    else:
        raise TypeError("The 'data' argument must be a Python dictionary or a JSON string.")