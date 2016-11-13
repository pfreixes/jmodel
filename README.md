jmodel is a json decoder plus a model builder designed to run fast. Instead of perform the class instantiation
in the Python layer, Jmodel uses the same decoder loop - written in Cython - to perform the model builder
stages. As a result Jmodel allows to you instantiate your Python models several times faster than with other
strategies.

The following snippet shows how it can be used, first having a explict model declaration and then building
the related instances with the ``loads`` function

 
# Benchmarking

## Time needed to decode and build models

Time decoding and loading models related with the medium file

| Driver              | Time took (s)|
| ------------------- |:-------------:| 
| Marshmallow         |         0.024 |
| Jmodel              |             ? |

## Loads function

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

