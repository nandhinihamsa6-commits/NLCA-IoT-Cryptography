from nlca.primitives import substitute_nibbles, permute_bits, diffusion_layer, inverse_diffusion_layer, f_function

def test_inverse_layers():
    x = bytes(range(16))
    assert substitute_nibbles(substitute_nibbles(x), inverse=True) == x
    assert permute_bits(permute_bits(x), inverse=True) == x
    for r in range(12):
        assert inverse_diffusion_layer(diffusion_layer(x, r), r) == x

def test_f_function_range():
    assert 0 <= f_function(0x1234) <= 0xFFFF
