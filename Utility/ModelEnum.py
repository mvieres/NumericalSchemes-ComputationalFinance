from enum import Enum


class ModelEnum(Enum):
    BlackScholes = "BlackScholes"
    HestonCir = "HestonCIR"
    HestonCKLS = "HestonCKLS"
    Cir = "CIR"
    CKLS = "CKLS"
    TrolleSchwartz = "TrolleSchwartz"
