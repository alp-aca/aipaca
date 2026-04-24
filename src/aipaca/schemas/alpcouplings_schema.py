from pydantic import BaseModel, field_validator, model_validator, Field, RootModel
from typing import Literal, List, Annotated, Union
from enum import Enum
from alpaca import ALPcouplings

class MatrixSymmetry(Enum):
    S = "Symmetric"
    A = "Antisymmetric"
    X = "Asymmetric"

def create_matrix(size: int, symmetry: MatrixSymmetry):
    class MatrixModel(RootModel[List[List[float]]]):
        root: List[List[float]] = Field(..., description=f"{symmetry.value} {size}x{size} matrix", title=f"Matrix{size}{symmetry.name[0]}")

        @field_validator('root')
        def validate_matrix(cls, value):
            if len(value) != size or any(len(row) != size for row in value):
                raise ValueError(f"Matrix must be {size}x{size}.")
            epsilon = 1e-6
            for i in range(size):
                for j in range(i+1, size):
                    if symmetry == MatrixSymmetry.S:
                        if abs(value[i][j] - value[j][i]) > epsilon * max(abs(value[i][j]), abs(value[j][i])):
                            raise ValueError("Matrix must be symmetric.")
                    elif symmetry == MatrixSymmetry.A:
                        if abs(value[i][j] + value[j][i]) > epsilon * max(abs(value[i][j]), abs(value[j][i])):
                            raise ValueError("Matrix must be antisymmetric.")
            return value

        class Config:
            title = f"Matrix{size}{symmetry.name[0]}"
    MatrixModel.__name__ = f"Matrix{size}{symmetry.name[0]}"
    return MatrixModel

Matrix2S = create_matrix(2, symmetry=MatrixSymmetry.S)
Matrix3S = create_matrix(3, symmetry=MatrixSymmetry.S)
Matrix2A = create_matrix(2, symmetry=MatrixSymmetry.A)
Matrix3A = create_matrix(3, symmetry=MatrixSymmetry.A)
Matrix2X = create_matrix(2, symmetry=MatrixSymmetry.X)
Matrix3X = create_matrix(3, symmetry=MatrixSymmetry.X)

class ALPcouplingsBase(BaseModel):
    """Base model for ALP couplings."""
    __class__: Literal['ALPcouplings']
    scale: float = Field(..., description="Energy scale (in GeV) at which the couplings are defined")
    basis: Literal['derivative_above', 'massbasis_ew', 'RL_below', 'VA_below'] = Field(..., description="Basis in which the couplings are defined")
    values: dict = Field(..., description="Values of the ALP couplings")

    def to_ALPcouplings(self) -> ALPcouplings:
        if self.basis == 'derivative_above':
            return ALPcouplingsDerivativeAbove.to_ALPcouplings(self)
        elif self.basis == 'VA_below':
            return ALPcouplingsVABelow.to_ALPcouplings(self)
        elif self.basis == 'RL_below':
            return ALPcouplingsRLBelow.to_ALPcouplings(self)
        raise NotImplementedError("This method should be implemented in subclasses.")

    @classmethod
    def from_ALPcouplings(cls, alp_couplings: ALPcouplings) -> "ALPcouplingsBase":
        raise NotImplementedError("This method should be implemented in subclasses.")

class ValsDerivativeAbove(BaseModel):
    cG_Re: float = Field(..., description="Real part of the coupling to gluons")
    cG_Im: float = Field(..., description="Imaginary part of the coupling to gluons")
    cW_Re: float = Field(..., description="Real part of the coupling to W bosons")
    cW_Im: float = Field(..., description="Imaginary part of the coupling to W bosons")
    cB_Re: float = Field(..., description="Real part of the coupling to B bosons")
    cB_Im: float = Field(..., description="Imaginary part of the coupling to B bosons")
    cqL_Re: Matrix3S = Field(..., description="Real part of the coupling to left-handed quarks")
    cqL_Im: Matrix3A = Field(..., description="Imaginary part of the coupling to left-handed quarks")
    cuR_Re: Matrix3S = Field(..., description="Real part of the coupling to right-handed up-type quarks")
    cuR_Im: Matrix3A = Field(..., description="Imaginary part of the coupling to right-handed up-type quarks")
    cdR_Re: Matrix3S = Field(..., description="Real part of the coupling to right-handed down-type quarks")
    cdR_Im: Matrix3A = Field(..., description="Imaginary part of the coupling to right-handed down-type quarks")
    clL_Re: Matrix3S = Field(..., description="Real part of the coupling to left-handed leptons")
    clL_Im: Matrix3A = Field(..., description="Imaginary part of the coupling to left-handed leptons")
    ceR_Re: Matrix3S = Field(..., description="Real part of the coupling to right-handed charged leptons")
    ceR_Im: Matrix3A = Field(..., description="Imaginary part of the coupling to right-handed charged leptons")

class ValsVABelow(BaseModel):
    cG_Re: float = Field(..., description="Real part of the coupling to gluons")
    cG_Im: float = Field(..., description="Imaginary part of the coupling to gluons")
    cgamma_Re: float = Field(..., description="Real part of the coupling to photons")
    cgamma_Im: float = Field(..., description="Imaginary part of the coupling to photons")
    cuV_Re: Matrix2S = Field(..., description="Real part of the vector coupling to up-type quarks")
    cuV_Im: Matrix2A = Field(..., description="Imaginary part of the vector coupling to up-type quarks")
    cdV_Re: Matrix3S = Field(..., description="Real part of the vector coupling to down-type quarks")
    cdV_Im: Matrix3A = Field(..., description="Imaginary part of the vector coupling to down-type quarks")
    ceV_Re: Matrix3S = Field(..., description="Real part of the vector coupling to charged leptons")
    ceV_Im: Matrix3A = Field(..., description="Imaginary part of the vector coupling to charged leptons")
    cuA_Re: Matrix2S = Field(..., description="Real part of the axial coupling to up-type quarks")
    cuA_Im: Matrix2A = Field(..., description="Imaginary part of the axial coupling to up-type quarks")
    cdA_Re: Matrix3S = Field(..., description="Real part of the axial coupling to down-type quarks")
    cdA_Im: Matrix3A = Field(..., description="Imaginary part of the axial coupling to down-type quarks")
    ceA_Re: Matrix3S = Field(..., description="Real part of the axial coupling to charged leptons")
    ceA_Im: Matrix3A = Field(..., description="Imaginary part of the axial coupling to charged leptons")
    cnu_Re: Matrix3S = Field(..., description="Real part of the coupling to neutrinos")
    cnu_Im: Matrix3A = Field(..., description="Imaginary part of the coupling to neutrinos")

class ValsRLBelow(BaseModel):
    cG_Re: float = Field(..., description="Real part of the coupling to gluons")
    cG_Im: float = Field(..., description="Imaginary part of the coupling to gluons")
    cgamma_Re: float = Field(..., description="Real part of the coupling to photons")
    cgamma_Im: float = Field(..., description="Imaginary part of the coupling to photons")
    cuR_Re: Matrix2S = Field(..., description="Real part of the right-handed coupling to up-type quarks")
    cuR_Im: Matrix2A = Field(..., description="Imaginary part of the right-handed coupling to up-type quarks")
    cdR_Re: Matrix3S = Field(..., description="Real part of the right-handed coupling to down-type quarks")
    cdR_Im: Matrix3A = Field(..., description="Imaginary part of the right-handed coupling to down-type quarks")
    ceR_Re: Matrix3S = Field(..., description="Real part of the right-handed coupling to charged leptons")
    ceR_Im: Matrix3A = Field(..., description="Imaginary part of the right-handed coupling to charged leptons")
    cuL_Re: Matrix2S = Field(..., description="Real part of the left-handed coupling to up-type quarks")
    cuL_Im: Matrix2A = Field(..., description="Imaginary part of the left-handed coupling to up-type quarks")
    cdL_Re: Matrix3S = Field(..., description="Real part of the left-handed coupling to down-type quarks")
    cdL_Im: Matrix3A = Field(..., description="Imaginary part of the left-handed coupling to down-type quarks")
    ceL_Re: Matrix3S = Field(..., description="Real part of the left-handed coupling to charged leptons")
    ceL_Im: Matrix3A = Field(..., description="Imaginary part of the left-handed coupling to charged leptons")
    cnuL_Re: Matrix3S = Field(..., description="Real part of the left-handed coupling to neutrinos")
    cnuL_Im: Matrix3A = Field(..., description="Imaginary part of the left-handed coupling to neutrinos")

class Yukawas(BaseModel):
    yu_Re: Matrix3X = Field(..., description="Real part of Yukawa couplings for up-type quarks")
    yu_Im: Matrix3X = Field(..., description="Imaginary part of Yukawa couplings for up-type quarks")
    yd_Re: Matrix3X = Field(..., description="Real part of Yukawa couplings for down-type quarks")
    yd_Im: Matrix3X = Field(..., description="Imaginary part of Yukawa couplings for down-type quarks")
    ye_Re: Matrix3X = Field(..., description="Real part of Yukawa couplings for charged leptons")
    ye_Im: Matrix3X = Field(..., description="Imaginary part of Yukawa couplings for charged leptons")

class ALPcouplingsDerivativeAbove(ALPcouplingsBase):
    """ALP couplings in the derivative basis above the electroweak scale."""
    basis: Literal['derivative_above'] = 'derivative_above'
    values: ValsDerivativeAbove = Field(..., description="Values of the ALP couplings in the derivative basis above the electroweak scale")
    yukawas: Yukawas = Field(..., description="Yukawa couplings of the SM fermions")

    def to_ALPcouplings(self) -> ALPcouplings:
        return ALPcouplings.from_dict(self.model_dump())

    @classmethod
    def from_ALPcouplings(cls, alp_couplings: ALPcouplings) -> "ALPcouplingsDerivativeAbove":
        if alp_couplings.basis != 'derivative_above':
            raise ValueError(f"Expected basis 'derivative_above', got '{alp_couplings.basis}'")
        return cls(**alp_couplings.to_dict())

class ALPcouplingsVABelow(ALPcouplingsBase):
    """ALP couplings in the vector-axial basis below the electroweak scale."""
    basis: Literal['VA_below'] = 'VA_below'
    values: ValsVABelow = Field(..., description="Values of the ALP couplings in the vector-axial basis below the electroweak scale")

    def to_ALPcouplings(self) -> ALPcouplings:
        return ALPcouplings.from_dict(self.model_dump())

    @classmethod
    def from_ALPcouplings(cls, alp_couplings: ALPcouplings) -> "ALPcouplingsVABelow":
        if alp_couplings.basis != 'VA_below':
            raise ValueError(f"Expected basis 'VA_below', got '{alp_couplings.basis}'")
        return cls(**alp_couplings.to_dict())


class ALPcouplingsRLBelow(ALPcouplingsBase):
    """ALP couplings in the right-handed basis below the electroweak scale."""
    basis: Literal['RL_below'] = 'RL_below'
    values: ValsRLBelow = Field(..., description="Values of the ALP couplings in the right-left basis below the electroweak scale")

    def to_ALPcouplings(self) -> ALPcouplings:
        return ALPcouplings.from_dict(self.model_dump())

    @classmethod
    def from_ALPcouplings(cls, alp_couplings: ALPcouplings) -> "ALPcouplingsRLBelow":
        if alp_couplings.basis != 'RL_below':
            raise ValueError(f"Expected basis 'RL_below', got '{alp_couplings.basis}'")
        return cls(**alp_couplings.to_dict())

ALPcouplingsSchema = Annotated[Union[ALPcouplingsDerivativeAbove, ALPcouplingsVABelow, ALPcouplingsRLBelow], Field(..., discriminator='basis')]

def parse_ALPcouplings(alp_couplings: ALPcouplings) -> ALPcouplingsBase:
    dispatch = {
        'derivative_above': ALPcouplingsDerivativeAbove,
        'VA_below': ALPcouplingsVABelow,
        'RL_below': ALPcouplingsRLBelow,
    }
    return dispatch[alp_couplings.basis].from_ALPcouplings(alp_couplings)