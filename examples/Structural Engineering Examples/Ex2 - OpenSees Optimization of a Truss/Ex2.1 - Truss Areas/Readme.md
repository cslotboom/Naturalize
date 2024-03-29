Truss Area Optimizations
===================

In the following example, the areas of a truss member are optimzied to mimize displacements under several different conditions.
The truss in the example has a fixed layout, where the nodes locations and element connectivies are pre-defined, as defined in the image below.
Force is defined at the top node of the model. Each member is a 2d truss, with elastic modulus of 200GPa, and area defined by the algorithm, up to a limit of 100mm^2
<p align="center">

<img src="https://github.com/cslotboom/Naturalize/blob/main/examples/Structural%20Engineering%20Examples/Ex2%20-%20OpenSees%20Optimization%20of%20a%20Truss/Ex2.1%20-%20Truss%20Areas/Truss-Diagram.jpeg" alt="alt text" width=168 height=416>

</p>

The genotype for the problem is a single gene of size 7 - one unit for each truss in the model


