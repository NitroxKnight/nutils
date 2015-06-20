# -*- coding: utf8 -*-
#
# Module MATRIX
#
# Part of Nutils: open source numerical utilities for Python. Jointly developed
# by HvZ Computational Engineering, TU/e Multiscale Engineering Fluid Dynamics,
# and others. More info at http://nutils.org <info@nutils.org>. (c) 2014

"""
The matrix module defines a number of 2D matrix objects, notably the
:func:`ScipyMatrix` and :func:`NumpyMatrix`. Matrix objects support basic
addition and subtraction operations and provide a consistent insterface for
solving linear systems. Matrices can be converted to numpy arrays via
``toarray`` or scipy matrices via ``toscipy``.
"""

from __future__ import print_function, division
from . import util, numpy, log


class SolverInfo ( object ):

  def __init__ ( self, tol, callback=None ):
    self.niter = 0
    self._res = numpy.empty( 16 )
    self._logtol = numpy.log10(tol)
    self._clock = util.Clock()
    self._callback = callback

  @property
  def res( self ):
    return self._res[:self.niter]

  def __call__ ( self, res ):
    if self.niter == len(self._res):
      self._res.resize( 2*self.niter )
    self._res[self.niter] = res
    self.niter += 1
    if self._callback:
      self._callback( res )
    if self._clock.check():
      log.progress( 'residual %.2e (%.0f%%)' % ( res, 100. * numpy.log10(res) / self._logtol ) )

class Matrix( object ):
  'matrix base class'

  def __init__( self, shape ):
    'constructor'

    assert len(shape) == 2
    self.shape = shape

  @property
  def size( self ):
    return numpy.prod( self.shape )

  def cond( self, constrain=None, lconstrain=None, rconstrain=None ):
    'condition number'

    x, I, J = parsecons( constrain, lconstrain, rconstrain, self.shape )
    matrix = self.toarray()[numpy.ix_(I,J)]
    return numpy.linalg.cond( matrix )

  def res( self, x, b=0, constrain=None, lconstrain=None, rconstrain=None, scaled=True ):
    'residual'

    x0, I, J = parsecons( constrain, lconstrain, rconstrain, self.shape )
    res = numpy.linalg.norm( (self.matvec(x)-b)[I] )
    if scaled:
      res /= numpy.linalg.norm( (self.matvec(x0)-b)[I] )
    return res

  def clone( self ):
    warnings.warn( 'warning: arrays are immutable; clone returns self for backwards compatibility', DeprecationWarning )
    return self

class ScipyMatrix( Matrix ):
  '''matrix based on any of scipy's sparse matrices'''

  def __init__( self, core ):
    self.core = core
    Matrix.__init__( self, core.shape )

  matvec = lambda self, vec: self.core.dot( vec )
  toarray = lambda self: self.core.toarray()
  toscipy = lambda self: self.core
  __add__ = lambda self, other: ScipyMatrix( self.core + other.toscipy() )
  __sub__ = lambda self, other: ScipyMatrix( self.core - other.toscipy() )
  __mul__ = lambda self, other: ScipyMatrix( self.core * other )
  __rmul__ = __mul__
  __div__ = lambda self, other: ScipyMatrix( self.core / other )
  T = property( lambda self: ScipyMatrix( self.core.transpose() ) )

  def rowsupp( self, tol=0 ):
    'return row indices with nonzero/non-small entries'

    supp = numpy.empty( self.shape[0], dtype=bool )
    for irow in range( self.shape[0] ):
      a, b = self.core.indptr[irow:irow+2]
      supp[irow] = a != b and numpy.any( numpy.abs( self.core.data[a:b] ) > tol )
    return supp

  @log.title
  def solve( self, b=None, constrain=None, lconstrain=None, rconstrain=None, tol=0, x0=None, solver=None, symmetric=False, title='solving system', callback=None, precon=None, info=False, **solverargs ):
    'solve'

    solverinfo = SolverInfo( tol, callback=callback )

    x, I, J = parsecons( constrain, lconstrain, rconstrain, self.shape )
    _b = ( ( b if b is not None else 0 ) - self.matvec(x) )[I]
    _x0 = x0[J] if x0 is not None else numpy.zeros( J.sum() )

    if I.all() and J.all():
      matvec = self.core.dot
    else:
      def matvec( v, _tmp=numpy.zeros(self.shape[1]), _dot=self.core.dot, _I=I, _J=J ):
        _tmp[_J] = v
        return _dot(_tmp)[_I]

    res0 = numpy.linalg.norm(_b-matvec(_x0)) / numpy.linalg.norm(_b)
    log.info( 'residual:', res0 )
    if res0 < tol:
      return (x0,solverinfo) if info else x0

    if tol == 0:
      _A = self.toarray()[ numpy.ix_(I,J) ]
      x[J] = numpy.linalg.solve( _A, _b )
      return x

    if isinstance( precon, str ):
      precon = self.getprecon( precon, constrain, lconstrain, rconstrain )

    if symmetric:
      assert solver is None
      solver = 'cg'
    elif solver is None:
      solver = 'gmres'

    import scipy.sparse.linalg
    solverfun = getattr( scipy.sparse.linalg, solver )
    mycallback = solverinfo if solver != 'cg' else lambda x: solverinfo( numpy.linalg.norm(_b-matvec(x)) / numpy.linalg.norm(_b) )

    _A = scipy.sparse.linalg.LinearOperator( _b.shape*2, matvec, dtype=float )
    x[J], status = solverfun( _A, _b, M=precon, tol=tol, x0=_x0, callback=mycallback, **solverargs )
    assert status == 0, '%s solver failed with status %d' % (solver, status)
    log.info( '%s solver converged in %d iterations' % (solver.upper(), solverinfo.niter) )

    return (x,solverinfo) if info else x

  def getprecon( self, name='SPLU', constrain=None, lconstrain=None, rconstrain=None ):

    import scipy.sparse.linalg

    name = name.lower()
    x, I, J = parsecons( constrain, lconstrain, rconstrain, self.shape )
    A = self.core[I,:][:,J]
    assert A.shape[0] == A.shape[1], 'constrained matrix must be square'
    log.info( 'building %s preconditioner' % name )
    if name == 'splu':
      precon = scipy.sparse.linalg.splu( A.tocsc() ).solve
    elif name == 'spilu':
      precon = scipy.sparse.linalg.spilu( A.tocsc(), drop_tol=1e-5, fill_factor=None, drop_rule=None, permc_spec=None, diag_pivot_thresh=None, relax=None, panel_size=None, options=None ).solve
    elif name == 'diag':
      precon = numpy.reciprocal( A.diagonal() ).__mul__
    else:
      raise Exception( 'invalid preconditioner %r' % name )
    return scipy.sparse.linalg.LinearOperator( A.shape, precon, dtype=float )

class NumpyMatrix( Matrix ):
  '''matrix based on numpy array'''

  def __init__( self, core ):
    assert isinstance( core, numpy.ndarray )
    self.core = core
    Matrix.__init__( self, core.shape )

  matvec = lambda self, vec: numpy.dot( self.core, vec )
  toarray = lambda self: self.core
  __add__ = lambda self, other: NumpyMatrix( self.core + other.toarray() )
  __sub__ = lambda self, other: NumpyMatrix( self.core - other.toarray() )
  __mul__ = lambda self, other: NumpyMatrix( self.core * other )
  __rmul__ = __mul__
  __div__ = lambda self, other: NumpyMatrix( self.core / other )
  T = property( lambda self: NumpyMatrix( self.core.T ) )

  @log.title
  def solve( self, b=None, constrain=None, lconstrain=None, rconstrain=None, tol=0, title='solving system' ):
    'solve'

    if b is None:
      b = numpy.zeros( self.shape[0] )
    else:
      b = numpy.asarray( b, dtype=float )
      assert b.ndim == 1, 'right-hand-side has shape %s, expected a vector' % (b.shape,)
      assert b.shape == self.shape[:1]

    x, I, J = parsecons( constrain, lconstrain, rconstrain, self.shape )
    if I.all() and J.all():
      return numpy.linalg.solve( self.core, b )

    data = self.core[I]
    x[J] = numpy.linalg.solve( data[:,J], b[I] - numpy.dot( data[:,~J], x[~J] ) )
    return x


# UTILITY FUNCTIONS

def assemble( data, index, shape, force_dense=False ):
  'create data from values and indices'

  if len(shape) == 0:
    retval = data.sum()
  elif len(shape) == 2 and not force_dense:
    import scipy.sparse.linalg
    csr = scipy.sparse.csr_matrix( (data,index), shape )
    retval = ScipyMatrix( csr )
  else:
    flatindex = numpy.dot( numpy.cumprod( (1,)+shape[:0:-1] )[::-1], index )
    retval = numpy.bincount( flatindex, data, numpy.prod(shape) ).reshape( shape ).astype( data.dtype, copy=False )
    if retval.ndim == 2:
      retval = NumpyMatrix( retval )
  assert retval.shape == shape
  log.debug( 'assembled', '%s(%s)' % ( retval.__class__.__name__, ','.join( str(n) for n in shape ) ) )
  return retval

def parsecons( constrain, lconstrain, rconstrain, shape ):
  'parse constraints'

  I = numpy.ones( shape[0], dtype=bool )
  x = numpy.empty( shape[1] )
  x[:] = numpy.nan
  if constrain is not None:
    assert lconstrain is None
    assert rconstrain is None
    assert isinstance( constrain, numpy.ndarray )
    I[:] = numpy.isnan( constrain )
    x[:] = constrain
  if lconstrain is not None:
    assert isinstance( lconstrain, numpy.ndarray )
    x[:] = lconstrain
  if rconstrain is not None:
    assert isinstance( rconstrain, numpy.ndarray )
    I[:] = rconstrain
  J = numpy.isnan(x)
  assert numpy.sum(I) == numpy.sum(J), 'constrained matrix is not square: %dx%d' % ( numpy.sum(I), numpy.sum(J) )
  x[J] = 0
  return x, I, J


# vim:shiftwidth=2:softtabstop=2:expandtab:foldmethod=indent:foldnestmax=2
