PI Web API ML (Machine Learning) client for Python
===

## Overview
This repository has the source code package of the PI Web API ML client for Python. 


## Requirements

 - PI Web API 2018+ instance available on your domain or a public network.
 
## Installation
### pip install

If the python package is hosted on Github, you can install directly from Github


```sh
pip install piwebapiml
```


### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```


## Examples

### Create an instance of the PI Web API top level object.

```python
    from piwebapiml.pml_web_api_client import PMLWebApiClient
    client = PMLWebApiClient("https://webserver/piwebapi", verifySsl=True) 
    client.set_basic_auth("username", "password")	
``` 

#### Kerberos Authentication
```python
    from piwebapiml.pml_web_api_client import PMLWebApiClient
    client = PMLWebApiClient("https://webserver/piwebapi", verifySsl=False)  
	client.set_kerberos_auth()	
``` 

### Get recorded, interpolated and plot values from PI Point and AF Attributes

```python
    pi_point = client.get_pi_point("\\\\MARC-PI2018\\cdt158")        
    attr = client.get_af_attribute('\\\\MARC-PI2018\\Weather\\Cities\\Chicago|Pressure')
        
    df1 = pi_point.get_recorded_values(start_time="*-1d", end_time="*")
    df2 = pi_point.get_interpolated_values(None, "*", None, None, "3h", None, "*-20d", None, None, None)
    df3 = pi_point.get_plot_values(end_time="*", intervals=15, start_time= "*-1d")

    df4 = attr.get_recorded_values(start_time="*-1d", end_time="*")
    df5 = attr.get_interpolated_values(None, "*", None, None, "3h", None, "*-20d", None, None, None)
    df6 = attr.get_plot_values(end_time="*", intervals=15, start_time= "*-1d")
```
### Get summary values

```python
    pi_point = client.get_pi_point("\\\\MARC-PI2018\\cdt158")        
    df2 = pi_point.get_summary_values(start_time="*-1d", end_time="*", summary_type=['Average', 'Total'], summary_duration='1h')
```

### Get recorded, interpolated and plot values from PI Point and AF Attributes in bulk

```python
    paths = ["\\\\MARC-PI2018\\sinusoid", "\\\\MARC-PI2018\\sinusoidu", "\\\\MARC-PI2018\\cdt158"]
    pi_points = client.get_pi_points(paths)
    df1 = pi_points.get_recorded_values_in_bulk(start_time="*-1d", end_time= "*")
    df2 = client.data.get_interpolated_values_in_bulk(start_time="*-1d", end_time="*", interval="1h")
    df3 = client.data.get_plot_values_in_bulk(start_time="*-1d", end_time="*", intervals="14")
    df4 = client.data.get_recorded_values_in_bulk(start_time="*-1d", end_time="*", selected_fields="items.items.value;items.items.timestamp")
```


## Licensing
Copyright 2023 PIDevGuru.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
Please see the file named [LICENSE.md](LICENSE.md).