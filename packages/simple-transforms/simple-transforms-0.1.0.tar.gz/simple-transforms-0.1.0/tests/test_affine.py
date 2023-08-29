import numpy as np
from flint import flint

import simple_transforms as transform

import pytest

class TestCreation:

    def test_from_mat_exc(self):
        with pytest.raises(TypeError):
            a = transform.from_mat()
        with pytest.raises(TypeError):
            a = transform.from_mat(1, 1)
        with pytest.raises(ValueError):
            a = transform.from_mat([1,2,3])
        with pytest.raises(ValueError):
            a = transform.from_mat([[1,2,3],[1,2,3]])
        with pytest.raises(ValueError):
            a = transform.from_mat([[[1,2,3],[1,2,3]]])

    def test_from_mat_4x4(self):
        a = transform.from_mat([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])
        assert isinstance(a, np.ndarray)
        assert a.shape == (4,4)
        assert np.all( a == np.arange(16).reshape((4,4)))

    def test_from_mat_4x3(self):
        a = transform.from_mat([[0,1,2,3],[4,5,6,7],[8,9,10,11]])
        b = np.array([[0,1,2,3],[4,5,6,7],[8,9,10,11],[0,0,0,1]])
        assert isinstance(a, np.ndarray)
        assert a.shape == (4,4)
        assert np.all( a == b)

    def test_from_mat_3x3(self):
        a = transform.from_mat([[0,1,2],[3,4,5],[6,7,8]])
        b = np.array([[0,1,2,0],[3,4,5,0],[6,7,8,0],[0,0,0,1]])
        assert isinstance(a, np.ndarray)
        assert a.shape == (4,4)
        assert np.all( a == b)


class TestTranslation:

    def test_translation_exc(self):
        with pytest.raises(TypeError):
            a = transform.trans()
        with pytest.raises(ValueError):
            a = transform.trans(1,2)
        with pytest.raises(ValueError):
            a = transform.trans([1,2])
        with pytest.raises(ValueError):
            a = transform.trans([[1,2,3]])
        with pytest.raises(TypeError):
            a = transform.trans([1,2,3], foo=[4,5,6])

    def test_translation(self):
        a = transform.trans([1,2,3])
        b = np.array([[1,0,0,1],[0,1,0,2],[0,0,1,3],[0,0,0,1]])
        assert isinstance(a, np.ndarray)
        assert a.shape == (4,4)
        assert np.all( a == b)

    def test_translation_with_center(self):
        a = transform.trans([5,6,7], center=[0,1,3])
        b = np.array([[1,0,0,5],[0,1,0,6],[0,0,1,7],[0,0,0,1]])
        assert isinstance(a, np.ndarray)
        assert a.shape == (4,4)
        assert np.all( a == b)


class TestScale:

    def test_scale_exc(self):
        with pytest.raises(TypeError):
            a = transform.scale()
        with pytest.raises(ValueError):
            a = transform.scale(1,2)
        with pytest.raises(ValueError):
            a = transform.scale([1])
        with pytest.raises(ValueError):
            a = transform.scale([[1,2,3]])
        with pytest.raises(TypeError):
            a = transform.scale([1,2,3], foo=[4,5,6])

    def test_scale_scalar(self):
        comp = np.eye(4, dtype=np.float64)
        a = transform.scale(2)
        for i in range(3):
            comp[i,i] = 2
        assert a.shape == (4,4)
        assert np.all( a == comp )
        a = transform.scale(0.5)
        for i in range(3):
            comp[i,i] = 0.5
        assert a.shape == (4,4)
        assert np.all( a == comp )
        a = transform.scale(flint(1.0)/3)
        for i in range(3):
            comp[i,i] = 1/3
        assert a.shape == (4,4)
        assert np.all( a == comp )

    def test_scale_vec(self):
        comp = np.eye(4, dtype=np.float64)
        a = transform.scale([2,3,4])
        comp[0,0] = 2
        comp[1,1] = 3
        comp[2,2] = 4
        assert a.shape == (4,4)
        assert np.all( a == comp )

    def test_scale_with_center(self):
        comp = np.eye(4, dtype=np.float64)
        a = transform.scale(2, center=[1,2,3])
        for i in range(3):
            comp[i,i] = 2
        comp[0,3] = -1
        comp[1,3] = -2
        comp[2,3] = -3
        assert a.shape == (4,4)
        assert np.all( a == comp )


class TestRotation:

    def test_rotation_exc(self):
        with pytest.raises(TypeError):
            a = transform.rot()
        with pytest.raises(TypeError):
            a = transform.rot(1)
        with pytest.raises(ValueError):
            a = transform.rot(1,2,3)
        with pytest.raises(ValueError):
            a = transform.rot(1,1)
        with pytest.raises(ValueError):
            a = transform.rot('xoo',1)
        with pytest.raises(ValueError):
            a = transform.rot([1],1)
        with pytest.raises(TypeError):
            a = transform.rot([1,2,3],1, foo=[0,0,0])

    def test_rot_x(self):
        a = transform.rot('x', np.pi/2)
        b = np.array([[1,0,0,0],[0,0,-1,0],[0,1,0,0],[0,0,0,1]])
        assert isinstance(a, np.ndarray)
        assert a.shape == (4,4)
        assert np.all( a == b )

    def test_rot_y(self):
        a = transform.rot('Y', np.pi/2)
        b = np.array([[0,0,1,0],[0,1,0,0],[-1,0,0,0],[0,0,0,1]])
        assert isinstance(a, np.ndarray)
        assert a.shape == (4,4)
        assert np.all( a == b )

    def test_rot_z(self):
        a = transform.rot('z', np.pi/2)
        b = np.array([[0,-1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]])
        assert isinstance(a, np.ndarray)
        assert a.shape == (4,4)
        assert np.all( a == b )

    def test_rot_aa(self):
        a = transform.rot('x', 1)
        b = transform.rot([1,0,0], 1)
        assert np.all( a == b )
        a = transform.rot('y', 1.5)
        b = transform.rot([0,2,0], 1.5)
        assert np.all( a == b )
        a = transform.rot('z', 0.5)
        b = transform.rot([0,0,0.5], 0.5)
        assert np.all( a == b )

    def test_rot_with_center(self):
        a = transform.rot('z',np.pi/2, center=[1,0,0])
        b = np.array([[0,-1,0,1],[1,0,0,-1],[0,0,1,0],[0,0,0,1]], dtype=np.float64)
        assert np.all( a == b )


class TestRefection:

    def test_refl_exc(self):
        with pytest.raises(TypeError):
            a = transform.refl()
        with pytest.raises(ValueError):
            a = transform.refl('xxo')
        with pytest.raises(ValueError):
            a = transform.refl(1)
        with pytest.raises(ValueError):
            a = transform.refl([1,2])
        with pytest.raises(TypeError):
            a = transform.refl([1,2,3], foo=[0,0,0])
        
    def test_refl_xyz(self):
        a = transform.refl('x')
        b = np.eye(4)
        b[0,0] = -1
        assert np.all( a == b )
        a = transform.refl('Y')
        b = np.eye(4)
        b[1,1] = -1
        assert np.all( a == b )
        a = transform.refl('z')
        b = np.eye(4)
        b[2,2] = -1
        assert np.all( a == b )

    def test_refl_u(self):
        a = transform.refl([1,1,1])
        bb = 1/np.sqrt(3)
        b = np.eye(4)
        for i in range(3):
            for j in range(3):
                b[i,j] -= 2*bb*bb
        assert np.all( a == b )

    def test_refl_with_center(self):
        a = transform.refl('x', center=[1,0,0])
        b = np.eye(4)
        b[0,0] = -1
        b[0,3] = 2
        assert np.all( a == b )


class TestSkew:

    def test_skew_exc(self):
        with pytest.raises(TypeError):
            a = transform.skew()
        with pytest.raises(TypeError):
            a = transform.skew('x')
        with pytest.raises(ValueError):
            a = transform.skew([1], [1,2,3])
        with pytest.raises(ValueError):
            a = transform.skew('z', [1,2])
        with pytest.raises(TypeError):
            a = transform.skew('z', [1,2,3], foo=[0,0,0])

    def test_skew_z(self):
        a = transform.skew('z',[2,3,4])
        b = np.eye(4)
        b[0,2] = 2
        b[1,2] = 3
        assert np.all( a == b )

    def test_skew_n(self):
        a = transform.skew('z',[2,3,4])
        b = transform.skew([0,0,1],[2,3,1])
        c = transform.skew([0,0,3],[2,3,5])
        assert np.all( a == b )
        assert np.all( a == c )

    def test_skew_with_center(self):
        a = transform.skew('z',[1,0,0],center=[0,0,1])
        b = np.eye(4)
        b[0,2] = 1
        b[0,3] = -1
        assert np.all( a == b )


class TestRescale:

    def test_single(self):
        a = np.array([2,2,2,2], dtype=flint)
        b = np.empty((4,), dtype=flint)
        transform.rescale(a,b)
        assert np.all( b == [1,1,1,1] )

    def test_multiple(self):
        a = np.array([[2,2,2,2],[3,3,3,3],[4,4,4,4]], dtype=flint)
        b = np.empty((3,4), dtype=flint)
        transform.rescale(a,b)
        assert np.all( b == np.ones((3,4)) )

class TestCombine:

    def test_eye(self):
        a = transform.eye()
        b = transform.rot('x',np.pi/2)
        c = transform.combine(a,b)
        assert np.all( c == b )
        c = transform.combine(b,a)
        assert np.all( c == b )

    def test_combine(self):
        a = transform.rot('x', np.pi)
        b = transform.combine(a, a)
        assert np.all( b == np.eye(4) )

    def test_reduce(self):
        a = transform.rot('x', 2*np.pi/10)
        b = transform.transform_reduce([a]*10)
        assert np.all( b == np.eye(4) )


class TestApply:

    def test_apply_vertex(self):
        v = [1,0,0]
        r = transform.rot('z',np.pi/2)
        vr = transform.apply(r, v)
        assert np.all( vr == [0,1,0] )

    def test_apply_vertices(self):
        v = [[1,0,0],[2,0,0],[3,0,0]]
        vt = [[0,1,0],[0,2,0],[0,3,0]]
        r = transform.rot('z',np.pi/2)
        vr = transform.apply(r, v)
        assert np.all( vr == vt )

    def test_apply_homo(self):
        h = [1,0,0,1]
        r = transform.rot('z',np.pi/2)
        hr = transform.apply(r, h)
        assert np.all( hr == [0,1,0,1] )

    def test_apply_homos(self):
        h = [[1,0,0,1], [2,0,0,1], [3,0,0,1], [4,0,0,1]]
        ht = [[0,1,0,1], [0,2,0,1], [0,3,0,1], [0,4,0,1]]
        r = transform.rot('z',np.pi/2)
        hr = transform.apply(r, h)
        print(hr)
        assert np.all( hr == ht )
