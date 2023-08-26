import warnings

from .config import (  # noqa: F401
    ADD_MODIFY_INCAR,
    ADD_NAMEFILE,
    ADD_WF_METADATA,
    CUSTODIAN_MAX_ERRORS,
    DB_FILE,
    DEFUSE_UNSUCCESSFUL,
    GAMMA_VASP_CMD,
    HALF_KPOINTS_FIRST_RELAX,
    LOBSTER_CMD,
    LOBSTERINPUT_FILES,
    LOBSTEROUTPUT_FILES,
    SCRATCH_DIR,
    SMALLGAP_KPOINT_MULTIPLY,
    STABILITY_CHECK,
    STORE_ADDITIONAL_JSON,
    STORE_BADER,
    STORE_VOLUMETRIC_DATA,
    VASP_CMD,
    VASP_OUTPUT_FILES,
    VDW_KERNEL_DIR,
)

warnings.warn("vasp_config renamed to config.")

__author__ = "Anubhav Jain <ajain@lbl.gov>"
