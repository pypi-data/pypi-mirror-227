from nabu.io.config import NabuConfigParser, validate_nabu_config
from nabu.resources.dataset_analyzer import EDFDatasetAnalyzer
from nabu.resources.dataset_validator import NabuValidator
from nabu.preproc.ccd import FlatField
from nabu.utils import partition_dict

nabu_config = validate_nabu_config(NabuConfigParser("/home/pierre/tmp/nabu2.conf").conf_dict)
E = EDFDatasetAnalyzer("/home/pierre/tmp/5.06_crayon_W150_60_Al2_W0.25_xc1000_")
V = NabuValidator(nabu_config, E)
V.perform_all_checks()
V.remove_unused_radios() # modifies "E", so we can use "E"

#F = FlatFieldCorrection(E.radio_dims[::-1], E.projections, E.flats, E.darks)


projs_subsets = partition_dict(E.projections, 30)


import os
def correct_flatfield(shape, projs, flats, darks):
    print("[%d] Processing new subset" % os.getpid())
    F = FlatFieldCorrection(shape, projs, E.flats, E.darks)
    res = F.correct_radios()
    return res


from distributed import Client
cli = Client("tcp://172.24.9.65:8786")

futs = []
for proj_subset in projs_subsets:
    f = cli.submit(
        correct_flatfield,
        E.radio_dims[::-1],
        proj_subset,
        E.flats,
        E.darks
    )
    futs.append(f)




def build_sino(F, corrected_radios):
    res = np.zeros((F.n_angles,) + F.shape, dtype="f")
    for i in range(F.n_angles):
        res[i] = corrected_radios[i]
    return res




