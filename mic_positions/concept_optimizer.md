This is a concept for a script that adjust the calculated microphone positiones to an approximation of the real positions.

This will be achieved with an optimizer that minimizes the sum of all quadratic error between measured and calculated microphone positions.

Inputs are:
* calculated microphone positions
* measured microphone distances

Outputs are:
* adjusted microphone positions
* some kind of mean error


Therefore, each microphone is on its corresponding plane:
* A - top
* B - left
* C - back
* D - right

The 3d space is described by an cartesian coordinate system:
* x between left an right plane. 0 on the left
* y betwenn front and back plane. 0 on front
* z between top and bottom plane. 0 on ???bottom???


To simplify the modell we make some assumptions:
* z offset of B, C, D plane is the same
* mic planes are perfectly flat
* B and C planes cannot be tilted on z plane


Paramters that will be optimized are:
* single y offset of B, C, D plane
* x offsets of B, C, D planes
* y offsets of B, C, D, planes
* tilt of C plane in y and z plane
* tilt of B and C plane in y plane

--> 11 parameters to be optimized

steps: 
* import meaasured 3d mic positions and distance measurements
* only use points with measured distance
* calculate sum of squarred errors
* build a mic positions model with parameters (offsets and tilt)
* optimize those paramters for minimal sum of squarred errors
* return optimized paramters and mic positions
