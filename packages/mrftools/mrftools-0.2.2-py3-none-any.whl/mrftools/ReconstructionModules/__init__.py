name = 'mrftools.ReconstructionModules'

RegisteredReconstructionModules = {}

def Register(cls):
    RegisteredReconstructionModules[cls.__name__] = cls
    return cls

from .ReconstructionModule import ReconstructionModule


from .CoilCompressionModule import CoilCompressionModule
from .SVDCompressionModule import SVDCompressionModule
from .NUFFTModule import NUFFTModule
from .IFFTModule import IFFTModule
from .CoilCombinationModule import CoilCombinationModule
from .PatternMatchingModule import PatternMatchingModule
from .ScalingModule import ScalingModule
#from .PreparationModule import PreparationModule
#from .RecoveryModule import RecoveryModule

#from .GradientPreparationModule import GradientPreparationModule
#from .RFPreparationModule import RFPreparationModule

#from .FISPAcquisitionModule import FISPAcquisitionModule
#from .TRUEFISPAcquisitionModule import TRUEFISPAcquisitionModule

#from .InversionModule import InversionModule
#from .T2PreparationModule import T2PreparationModule
#from .SpoilerModule import SpoilerModule

#from .DeadtimeRecoveryModule import DeadtimeRecoveryModule
