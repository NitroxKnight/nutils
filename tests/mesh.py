from nutils import *
from . import unittest, register

# gmsh geo 2D:
#
# Point(1) = {0,0,0,.5};
# Point(2) = {1,0,0,.5};
# Point(3) = {1,1,0,.5};
# Point(4) = {0,1,0,.5};
# Line(5) = {1,2};
# Line(6) = {2,3};
# Line(7) = {3,4};
# Line(8) = {4,1};
# Line Loop(9) = {5,6,7,8};
# Plane Surface(10) = {9};
# Physical Point("corner") = {2};
# Physical Line("neumann") = {5};
# Physical Line("dirichlet") = {6,7,8};
# Physical Surface("interior") = {10};

gmshdata2d = '''\
$MeshFormat
2.2 0 8
$EndMeshFormat
$PhysicalNames
4
0 1 "corner"
1 2 "neumann"
1 3 "dirichlet"
2 4 "interior"
$EndPhysicalNames
$Nodes
13
1 0 0 0
2 1 0 0
3 1 1 0
4 0 1 0
5 0.499999999998694 0 0
6 1 0.499999999998694 0
7 0.5000000000020591 1 0
8 0 0.5000000000020591 0
9 0.5 0.5 0
10 0.2500000000010295 0.7500000000010295 0
11 0.7500000000005148 0.7499999999996735 0
12 0.749999999999432 0.249999999999432 0
13 0.2499999999989704 0.2500000000010296 0
$EndNodes
$Elements
25
1 15 2 1 2 2
2 1 2 2 5 1 5
3 1 2 2 5 5 2
4 1 2 3 6 2 6
5 1 2 3 6 6 3
6 1 2 3 7 3 7
7 1 2 3 7 7 4
8 1 2 3 8 4 8
9 1 2 3 8 8 1
10 2 2 4 10 13 10 8
11 2 2 4 10 9 10 13
12 2 2 4 10 4 10 7
13 2 2 4 10 1 13 8
14 2 2 4 10 3 11 6
15 2 2 4 10 2 12 5
16 2 2 4 10 7 10 9
17 2 2 4 10 7 9 11
18 2 2 4 10 6 11 9
19 2 2 4 10 5 9 13
20 2 2 4 10 5 12 9
21 2 2 4 10 6 9 12
22 2 2 4 10 1 5 13
23 2 2 4 10 2 6 12
24 2 2 4 10 4 8 10
25 2 2 4 10 3 7 11
$EndElements
'''

# gmsh geo 3D:
#
# Point(1) = {0,0,0,1.};
# Point(2) = {1,0,0,1.};
# Point(3) = {1,1,0,1.};
# Point(4) = {0,1,0,1.};
# Point(5) = {0,0,1,1.};
# Point(6) = {1,0,1,1.};
# Point(7) = {1,1,1,1.};
# Point(8) = {0,1,1,1.};
# Line(9) = {1,2};
# Line(10) = {2,3};
# Line(11) = {3,4};
# Line(12) = {4,1};
# Line(13) = {5,6};
# Line(14) = {6,7};
# Line(15) = {7,8};
# Line(16) = {8,5};
# Line(17) = {1,5};
# Line(18) = {2,6};
# Line(19) = {3,7};
# Line(20) = {4,8};
# Line Loop(21) = {9, 18, -13, -17};
# Line Loop(22) = {10, 19, -14, -18};
# Line Loop(23) = {11, 12, 9, 10};
# Line Loop(24) = {17, -16, -20, 12};
# Line Loop(25) = {15, 16, 13, 14};
# Line Loop(26) = {20, -15, -19, 11};
# Plane Surface(27) = {21};
# Plane Surface(28) = {22};
# Plane Surface(29) = {23};
# Plane Surface(30) = {24};
# Plane Surface(31) = {25};
# Plane Surface(32) = {26};
# Surface Loop(33) = {32, 30, 27, 29, 28, 31};
# Volume(34) = {33};
# Physical Point("corner") = {2};
# Physical Surface("neumann") = {32};
# Physical Surface("dirichlet") = {27,28,29};
# Physical Volume("interior") = {34};

gmshdata3d = '''\
$MeshFormat
2.2 0 8
$EndMeshFormat
$PhysicalNames
4
0 1 "corner"
2 2 "neumann"
2 3 "dirichlet"
3 4 "interior"
$EndPhysicalNames
$Nodes
14
1 0 0 0
2 1 0 0
3 1 1 0
4 0 1 0
5 0 0 1
6 1 0 1
7 1 1 1
8 0 1 1
9 0.5 0 0.5
10 1 0.5 0.5
11 0.5 0.5 0
12 0 0.5 0.5
13 0.5 0.5 1
14 0.5 1 0.5
$EndNodes
$Elements
41
1 15 2 1 2 2
2 2 2 3 27 2 9 1
3 2 2 3 27 9 5 1
4 2 2 3 27 6 9 2
5 2 2 3 27 9 6 5
6 2 2 3 28 3 10 2
7 2 2 3 28 10 6 2
8 2 2 3 28 7 10 3
9 2 2 3 28 10 7 6
10 2 2 3 29 1 2 11
11 2 2 3 29 1 11 4
12 2 2 3 29 2 3 11
13 2 2 3 29 3 4 11
14 2 2 2 32 4 14 3
15 2 2 2 32 14 7 3
16 2 2 2 32 8 14 4
17 2 2 2 32 14 8 7
18 4 2 4 34 12 13 9 10
19 4 2 4 34 13 12 14 10
20 4 2 4 34 14 12 11 10
21 4 2 4 34 11 12 9 10
22 4 2 4 34 3 11 2 10
23 4 2 4 34 12 8 5 13
24 4 2 4 34 6 5 13 9
25 4 2 4 34 7 6 13 10
26 4 2 4 34 14 4 3 11
27 4 2 4 34 8 7 13 14
28 4 2 4 34 4 8 12 14
29 4 2 4 34 11 1 2 9
30 4 2 4 34 1 12 5 9
31 4 2 4 34 1 4 12 11
32 4 2 4 34 7 14 3 10
33 4 2 4 34 6 2 9 10
34 4 2 4 34 3 14 11 10
35 4 2 4 34 12 8 13 14
36 4 2 4 34 7 13 14 10
37 4 2 4 34 12 4 14 11
38 4 2 4 34 5 12 13 9
39 4 2 4 34 12 1 11 9
40 4 2 4 34 13 6 9 10
41 4 2 4 34 2 11 9 10
$EndElements
'''

@register( '2d', gmshdata=gmshdata2d )
@register( '3d', gmshdata=gmshdata3d )
def gmsh( gmshdata ):

  domain, geom = mesh.gmsh( gmshdata.splitlines() )

  @unittest
  def volume():
    volume = domain.integrate( 1, geometry=geom, ischeme='gauss1' )
    numpy.testing.assert_almost_equal( volume, 1, decimal=10 )

  for group, exact_length in ('neumann',1), ('dirichlet',3), ((),2*domain.ndims):
    @unittest( name=group or 'all' )
    def length():
      length = domain.boundary[group].integrate( 1, geometry=geom, ischeme='gauss1' )
      numpy.testing.assert_almost_equal( length, exact_length, decimal=10 )

  @unittest
  def interfaces():
    err = domain.interfaces.elem_eval( geom - function.opposite(geom), ischeme='uniform2', separate=False )
    numpy.testing.assert_almost_equal( err, 0, decimal=15 )

  @unittest
  def divergence():
    volumes = domain.boundary.integrate( geom*geom.normal(), geometry=geom, ischeme='gauss1' )
    numpy.testing.assert_almost_equal( volumes, 1, decimal=10 )

  @unittest
  def pointeval():
    xy = domain.points.elem_eval( geom, ischeme='gauss1' )
    assert xy.shape == ( 2, 2 ) if domain.ndims==2 else ( 4, 3 )
    assert numpy.all( xy == ([1,0] if domain.ndims==2 else [1,0,0]) )

# gmshrect geo:
#
# Point(1) = {0,0,0,.5};
# Point(2) = {1,0,0,.5};
# Point(3) = {2,0,0,.5};
# Point(4) = {0,1,0,.5};
# Point(5) = {1,1,0,.5};
# Point(6) = {2,1,0,.5};
# Line(7) = {1,2};
# Line(8) = {2,3};
# Line(9) = {3,6};
# Line(10) = {6,5};
# Line(11) = {5,4};
# Line(12) = {4,1};
# Line(13) = {2,5};
# Line Loop(14) = {7,13,11,12};
# Line Loop(15) = {8,9,10,-13};
# Plane Surface(16) = {14};
# Plane Surface(17) = {15};
# Physical Line("iface") = {13};
# Physical Surface("left") = {16};
# Physical Surface("right") = {17};

gmshrectdata = '''\
$MeshFormat
2.2 0 8
$EndMeshFormat
$PhysicalNames
3
1 1 "iface"
2 2 "left"
2 3 "right"
$EndPhysicalNames
$Nodes
23
1 0 0 0
2 1 0 0
3 2 0 0
4 0 1 0
5 1 1 0
6 2 1 0
7 0.499999999998694 0 0
8 1.5 0 0
9 2 0.499999999998694 0
10 1.5 1 0
11 0.5000000000020591 1 0
12 0 0.5000000000020591 0
13 1 0.499999999998694 0
14 0.5 0.4999999999999999 0
15 0.2500000000010295 0.7500000000010295 0
16 0.7500000000005148 0.7499999999996735 0
17 0.2499999999989704 0.2500000000010296 0
18 0.7499999999996735 0.2499999999996735 0
19 1.5 0.49999999999983 0
20 1.75 0.249999999999347 0
21 1.25 0.249999999999347 0
22 1.25 0.749999999999631 0
23 1.75 0.749999999999631 0
$EndNodes
$Elements
34
1 1 2 1 13 2 13
2 1 2 1 13 13 5
3 2 2 2 16 17 15 12
4 2 2 2 16 14 15 17
5 2 2 2 16 4 15 11
6 2 2 2 16 1 17 12
7 2 2 2 16 5 16 13
8 2 2 2 16 2 18 7
9 2 2 2 16 11 15 14
10 2 2 2 16 11 14 16
11 2 2 2 16 13 16 14
12 2 2 2 16 13 14 18
13 2 2 2 16 7 14 17
14 2 2 2 16 7 18 14
15 2 2 2 16 1 7 17
16 2 2 2 16 2 13 18
17 2 2 2 16 4 12 15
18 2 2 2 16 5 11 16
19 2 2 3 17 22 13 19
20 2 2 3 17 9 19 20
21 2 2 3 17 13 21 19
22 2 2 3 17 23 19 9
23 2 2 3 17 8 20 19
24 2 2 3 17 21 8 19
25 2 2 3 17 5 13 22
26 2 2 3 17 6 23 9
27 2 2 3 17 2 8 21
28 2 2 3 17 3 20 8
29 2 2 3 17 10 22 19
30 2 2 3 17 10 19 23
31 2 2 3 17 5 22 10
32 2 2 3 17 6 10 23
33 2 2 3 17 2 21 13
34 2 2 3 17 3 9 20
$EndElements
'''

@register
def gmshrect():

  domain, geom = mesh.gmsh( gmshrectdata.splitlines() )

  @unittest
  def volume():
    volume = domain.integrate( 1, geometry=geom, ischeme='gauss1' )
    numpy.testing.assert_almost_equal( volume, 2, decimal=10 )

  @unittest
  def length():
    length = domain.boundary.integrate( 1, geometry=geom, ischeme='gauss1' )
    numpy.testing.assert_almost_equal( length, 6, decimal=10 )

  @unittest
  def divergence():
    volumes = domain.boundary.integrate( geom*geom.normal(), geometry=geom, ischeme='gauss1' )
    numpy.testing.assert_almost_equal( volumes, 2, decimal=10 )

  for group in 'left', 'right':
    subdom = domain[group]
    @unittest( name=group )
    def subvolume():
      volume = subdom.integrate( 1, geometry=geom, ischeme='gauss1' )
      numpy.testing.assert_almost_equal( volume, 1, decimal=10 )
    @unittest( name=group )
    def sublength():
      length = subdom.boundary.integrate( 1, geometry=geom, ischeme='gauss1' )
      numpy.testing.assert_almost_equal( length, 4, decimal=10 )
    @unittest( name=group )
    def subdivergence():
      volumes = subdom.boundary.integrate( geom*geom.normal(), geometry=geom, ischeme='gauss1' )
      numpy.testing.assert_almost_equal( volumes, 1, decimal=10 )

  @unittest
  def iface():
    ax, ay = domain.interfaces['iface'].elem_eval( geom, ischeme='uniform1', separate=False ).T
    bx, by = domain['left'].boundary['iface'].elem_eval( geom, ischeme='uniform1', separate=False ).T
    cx, cy = domain['right'].boundary['iface'].elem_eval( geom, ischeme='uniform1', separate=False ).T
    assert all( ax == 1 )
    assert all( bx == 1 )
    assert all( cx == 1 )
    assert min(ay) == min(by) == min(cy)
    assert max(ay) == max(by) == max(cy)

# gmshperiodic geo:
#
# Point(1) = {0,0,0,.4};
# Point(2) = {1,0,0,.4};
# Point(3) = {1,1,0,.4};
# Point(4) = {0,1,0,.4};
# Line(5) = {1,2};
# Line(6) = {2,3};
# Line(7) = {3,4};
# Line(8) = {4,1};
# Line Loop(9) = {5,6,7,8};
# Plane Surface(10) = {9};
# Physical Surface("interior") = {10};
# Physical Line("right") = {6};
# Physical Line("left") = {8};
# Physical Line("periodic") = {5};
# Periodic Line { 5 } = { -7 };

gmshperiodicdata = '''\
$MeshFormat
2.2 0 8
$EndMeshFormat
$PhysicalNames
4
1 2 "right"
1 3 "left"
1 4 "periodic"
2 1 "interior"
$EndPhysicalNames
$Nodes
21
1 0 0 0
2 1 0 0
3 1 1 0
4 0 1 0
5 0.3333333333347203 0 0
6 0.6666666666675911 0 0
7 1 0.3333333333325025 0
8 1 0.6666666666657889 0
9 0.6666666666675911 1 0
10 0.3333333333347203 1 0
11 0 0.6666666666675911 0
12 0 0.3333333333347203 0
13 0.5000000000000648 0.5000000000000175 0
14 0.7083333333332844 0.2916666666667275 0
15 0.2916666666667967 0.7083333333334922 0
16 0.25099206349244 0.2509920634924497 0
17 0.7083333333334444 0.7083333333332192 0
18 0.1726190476198807 0.5000000000000979 0
19 0.5000000000001986 0.8273809523802892 0
20 0.8273809523805672 0.4999999999999279 0
21 0.4999999999999743 0.172619047619863 0
$EndNodes
$Elements
37
1 1 2 4 5 1 5
2 1 2 4 5 5 6
3 1 2 4 5 6 2
4 1 2 2 6 2 7
5 1 2 2 6 7 8
6 1 2 2 6 8 3
7 1 2 3 8 4 11
8 1 2 3 8 11 12
9 1 2 3 8 12 1
10 2 2 1 10 4 15 10
11 2 2 1 10 2 14 6
12 2 2 1 10 2 7 14
13 2 2 1 10 4 11 15
14 2 2 1 10 3 9 17
15 2 2 1 10 3 17 8
16 2 2 1 10 1 16 12
17 2 2 1 10 1 5 16
18 2 2 1 10 13 14 20
19 2 2 1 10 13 20 17
20 2 2 1 10 13 19 15
21 2 2 1 10 13 17 19
22 2 2 1 10 13 21 14
23 2 2 1 10 13 15 18
24 2 2 1 10 13 16 21
25 2 2 1 10 13 18 16
26 2 2 1 10 7 8 20
27 2 2 1 10 5 6 21
28 2 2 1 10 11 12 18
29 2 2 1 10 9 10 19
30 2 2 1 10 11 18 15
31 2 2 1 10 6 14 21
32 2 2 1 10 9 19 17
33 2 2 1 10 7 20 14
34 2 2 1 10 12 16 18
35 2 2 1 10 5 21 16
36 2 2 1 10 10 15 19
37 2 2 1 10 8 17 20
$EndElements
$Periodic
3
0 1 4
1
1 4
0 2 3
1
2 3
1 5 7
4
2 3
1 4
5 10
6 9
$EndPeriodic
'''

@register
def gmshperiodic():

  domain, geom = mesh.gmsh( gmshperiodicdata.splitlines() )

  @unittest
  def volume():
    volume = domain.integrate( 1, geometry=geom, ischeme='gauss1' )
    numpy.testing.assert_almost_equal( volume, 1, decimal=10 )

  for group, exact_length in ('right',1), ('left',1), ((),2):
    @unittest( name=group or 'all' )
    def length():
      length = domain.boundary[group].integrate( 1, geometry=geom, ischeme='gauss1' )
      numpy.testing.assert_almost_equal( length, exact_length, decimal=10 )

  @unittest
  def interface():
    err = domain.interfaces['periodic'].elem_eval( function.opposite(geom) - geom, ischeme='uniform2', separate=False )
    numpy.testing.assert_almost_equal( abs(err)-[0,1], 0, decimal=15 )

  @unittest
  def basis():
    basis = domain.basis( 'std', degree=1 )
    err = domain.interfaces.integrate( basis - function.opposite(basis), geometry=geom, ischeme='gauss1' )
    numpy.testing.assert_almost_equal( err, 0, decimal=15 )

@register( 'new', mesh.newrectilinear )
@register( 'old', mesh.rectilinear )
def rectilinear( rectilinear ):

  domain, geom = rectilinear( [4,5] )

  @unittest
  def volume():
    volume = domain.integrate( 1, geometry=geom, ischeme='gauss1' )
    numpy.testing.assert_almost_equal( volume, 20, decimal=15 )

  @unittest
  def divergence():
    domain.volume_check( geom )

  for group, exact_length in ('right',5), ('left',5), ('top',4), ('bottom',4), ((),18):
    @unittest( name=group or 'all' )
    def length():
      length = domain.boundary[group].integrate( 1, geometry=geom, ischeme='gauss1' )
      numpy.testing.assert_almost_equal( length, exact_length, decimal=10 )

  @unittest
  def interface():
    geomerr = domain.interfaces.elem_eval( geom - function.opposite(geom), ischeme='uniform2', separate=False )
    numpy.testing.assert_almost_equal( geomerr, 0, decimal=15 )
    normalerr = domain.interfaces.elem_eval( geom.normal() + function.opposite(geom.normal()), ischeme='uniform2', separate=False )
    numpy.testing.assert_almost_equal( normalerr, 0, decimal=15 )

  for basistype in 'discont', 'std', 'spline':
    for degree in 1, 2, 3:
      @unittest( name=basistype+str(degree) )
      def pum():
        basis = domain.basis( basistype, degree=degree )
        values = domain.interfaces.elem_eval( basis, geometry=geom, ischeme='uniform2', separate=False )
        numpy.testing.assert_almost_equal( values.sum(1), 1 )
