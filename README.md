IN PROGRESS ....

# Time needed to decode and build models

Time decoding and loading models related with the medium file

| Driver              | Time took (s)|
| ------------------- |:-------------:| 
| Marshmallow         |         0.024 |
| Jmodel              |             ? |

# Bencharks loads function

Parsing many lines (lines 1000) (Repeated 10 times)

| Driver              | Time took (s)|
| ------------------- |:-------------:| 
| Python version      |         0.501 |
| Jmodel              |         0.083 |
| Python C version    |         0.055 |
| ujson               |         0.029 |


Parsing medium file  (size 120257)

| Driver              | Time took (s)|
| ------------------- |:-------------:| 
| Python version      |         0.078 |
| Jmodel              |         0.012 |
| Python C version    |         0.010 |
| ujson               |         0.009 |


Parsing file with a lot of text (size 567916)

| Driver              | Time took (s)|
| ------------------- |:-------------:| 
| Python version      |         0.129 |
| Jmodel              |         0.018 |
| ujson               |         0.012 |
| Python C version    |         0.011 |

