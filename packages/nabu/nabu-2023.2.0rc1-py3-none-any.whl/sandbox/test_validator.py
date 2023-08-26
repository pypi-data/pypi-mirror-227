from nabu.io.config import NabuConfigParser, validate_nabu_config
from nabu.resources.dataset_analyzer import EDFDatasetAnalyzer
from nabu.resources.dataset_validator import NabuValidator

nabu_config = validate_nabu_config(NabuConfigParser("/home/pierre/tmp/nabu2.conf").conf_dict)
E = EDFDatasetAnalyzer("/home/pierre/tmp/5.06_crayon_W150_60_Al2_W0.25_xc1000_")
V = NabuValidator(nabu_config, E)
V.perform_all_checks()
