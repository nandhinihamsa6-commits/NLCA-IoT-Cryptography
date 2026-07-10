from nlca.baselines import baseline_manifest

def test_modern_baselines_present():
    names = baseline_manifest()
    for name in ["AES-128","PRESENT","GIFT-128","SKINNY-128","SIMON-128","SPECK-128","ASCON","NLCA"]:
        assert name in names
