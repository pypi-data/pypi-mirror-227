from typing import List
from typing import Any
from dataclasses import dataclass
import json
import jsonpickle


@dataclass
class TrajectorySettings:
    trajectoryDirectory: str
    trajectoryFile: str
    densityCompensationFile: str
    trajectoryReadoutLength: int 

    @staticmethod
    def from_dict(obj: Any) -> 'TrajectorySettings':
        _trajectoryDirectory = str(obj.get("trajectoryDirectory"))
        _trajectoryFile = str(obj.get("trajectoryFile"))
        _densityCompensationFile = str(obj.get("densityCompensationFile"))
        _trajectoryReadoutLength = str(obj.get("trajectoryReadoutLength"))
        return TrajectorySettings(_trajectoryDirectory, _trajectoryFile, _densityCompensationFile, _trajectoryReadoutLength)
    
@dataclass
class LegacySettings:
    dependencyDirectory: str
    trFile: str
    baseTR: int
    teFile: str
    baseTE: int
    faFile: str
    faScaling: float
    phFile: str
    idFile: str
    usidFile: str
    dictionaryFile: str

    @staticmethod
    def from_dict(obj: Any) -> 'LegacySettings':
        _dependencyDirectory = str(obj.get("dependencyDirectory"))
        _trFile = str(obj.get("trFile"))
        _baseTR = int(obj.get("baseTR"))
        _teFile = str(obj.get("teFile"))
        _baseTE = int(obj.get("baseTE"))
        _faFile = str(obj.get("faFile"))
        _faScaling = float(obj.get("faScaling"))
        _phFile = str(obj.get("phFile"))
        _idFile = str(obj.get("idFile"))
        _usidFile = str(obj.get("usidFile"))
        _dictionaryFile = str(obj.get("dictionaryFile"))
        return LegacySettings(_dependencyDirectory, _trFile, _baseTR, _teFile, _baseTE, _faFile, _faScaling, _phFile, _idFile, _usidFile, _dictionaryFile)
    
@dataclass
class ClassificationMaps:
    enabled: bool
    T1_wm: float
    T2_wm: float
    T1_gm: float
    T2_gm: float
    T1_csf: float
    T2_csf: float
    sigmaT1_wm: float
    sigmaT2_wm: float
    sigmaT1_gm: float
    sigmaT2_gm: float
    sigmaT1_csf: float
    sigmaT2_csf: float

    @staticmethod
    def from_dict(obj: Any) -> 'ClassificationMaps':
        _enabled = bool(obj.get("enabled"))
        _T1_wm = float(obj.get("T1_wm"))
        _T2_wm = float(obj.get("T2_wm"))
        _T1_gm = float(obj.get("T1_gm"))
        _T2_gm = float(obj.get("T2_gm"))
        _T1_csf = float(obj.get("T1_csf"))
        _T2_csf = float(obj.get("T2_csf"))
        _sigmaT1_wm = float(obj.get("sigmaT1_wm"))
        _sigmaT2_wm = float(obj.get("sigmaT2_wm"))
        _sigmaT1_gm = float(obj.get("sigmaT1_gm"))
        _sigmaT2_gm = float(obj.get("sigmaT2_gm"))
        _sigmaT1_csf = float(obj.get("sigmaT1_csf"))
        _sigmaT2_csf = float(obj.get("sigmaT2_csf"))
        return ClassificationMaps(_enabled, _T1_wm, _T2_wm, _T1_gm, _T2_gm, _T1_csf, _T2_csf, _sigmaT1_wm, _sigmaT2_wm, _sigmaT1_gm, _sigmaT2_gm, _sigmaT1_csf, _sigmaT2_csf)

@dataclass
class CoilCompression:
    enabled: bool
    svdPower: float
    truncationNumberOverride: str

    @staticmethod
    def from_dict(obj: Any) -> 'CoilCompression':
        _enabled = bool(obj.get("enabled"))
        _svdPower = float(obj.get("svdPower"))
        _truncationNumberOverride = int(obj.get("truncationNumberOverride"))
        return CoilCompression(_enabled, _svdPower, _truncationNumberOverride)

@dataclass
class DatasetSettings:
    trajectory_settings: TrajectorySettings
    fa_mode: str
    allow_legacy: bool
    legacy_settings: LegacySettings

    @staticmethod
    def from_dict(obj: Any) -> 'DatasetSettings':
        _trajectory_settings = TrajectorySettings.from_dict(obj.get("trajectory_settings"))
        _fa_mode = str(obj.get("fa_mode"))
        _allow_legacy = bool(obj.get("allow_legacy"))
        _legacy_settings = LegacySettings.from_dict(obj.get("legacy_settings"))
        return DatasetSettings(_trajectory_settings, _fa_mode, _allow_legacy, _legacy_settings)

@dataclass
class DicomExport:
    enabled: bool

    @staticmethod
    def from_dict(obj: Any) -> 'DicomExport':
        _enabled =bool(obj.get("enabled")) 
        return DicomExport(_enabled)

@dataclass
class ExecutionSettings:
    maxIterations: int
    gradTolerance: float
    maxLinesearchIterations: int
    t0: float
    t0Max: int
    alpha: float
    beta: float
    maxSingleSteps: int
    waveletLambda: int
    waveletType: str
    waveletLevel: int
    exportIterationResults: bool

    @staticmethod
    def from_dict(obj: Any) -> 'ExecutionSettings':
        _maxIterations = int(obj.get("maxIterations"))
        _gradTolerance = float(obj.get("gradTolerance"))
        _maxLinesearchIterations = int(obj.get("maxLinesearchIterations"))
        _t0 = float(obj.get("t0"))
        _t0Max = int(obj.get("t0Max"))
        _alpha = float(obj.get("alpha"))
        _beta = float(obj.get("beta"))
        _maxSingleSteps = int(obj.get("maxSingleSteps"))
        _waveletLambda = int(obj.get("waveletLambda"))
        _waveletType = str(obj.get("waveletType"))
        _waveletLevel = int(obj.get("waveletLevel"))
        _exportIterationResults = bool(obj.get("exportIterationResults"))
        return ExecutionSettings(_maxIterations, _gradTolerance, _maxLinesearchIterations, _t0, _t0Max, _alpha, _beta, _maxSingleSteps, _waveletLambda, _waveletType, _waveletLevel, _exportIterationResults)

@dataclass
class PreparationSettings:
    initializeWithDCF: bool
    useDCFInIterations: bool
    readoutTruncationLimit: int
    numNearestNeighbors: int
    maskingMode: str

    @staticmethod
    def from_dict(obj: Any) -> 'PreparationSettings':
        _initializeWithDCF = bool(obj.get("initializeWithDCF"))
        _useDCFInIterations = bool(obj.get("useDCFInIterations"))
        _readoutTruncationLimit = int(obj.get("readoutTruncationLimit"))
        _numNearestNeighbors = int(obj.get("numNearestNeighbors"))
        _maskingMode = str(obj.get("maskingMode"))
        return PreparationSettings(_initializeWithDCF, _useDCFInIterations, _readoutTruncationLimit, _numNearestNeighbors, _maskingMode)
    
@dataclass
class IterativeNUFFT:
    enabled: bool
    preparation_settings: PreparationSettings
    execution_settings: ExecutionSettings

    @staticmethod
    def from_dict(obj: Any) -> 'IterativeNUFFT':
        _enabled = bool(obj.get("enabled"))
        _preparation_settings = PreparationSettings.from_dict(obj.get("preparation_settings"))
        _execution_settings = ExecutionSettings.from_dict(obj.get("execution_settings"))
        return IterativeNUFFT(_enabled, _preparation_settings, _execution_settings)
    
@dataclass
class Masking:
    enabled: bool
    angularResolution: float
    stepSize: int
    fillSize: int
    maxDecay: int
    featheringKernelSize: int

    @staticmethod
    def from_dict(obj: Any) -> 'Masking':
        _enabled = bool(obj.get("enabled"))
        _angularResolution = float(obj.get("angularResolution"))
        _stepSize = int(obj.get("stepSize"))
        _fillSize = int(obj.get("fillSize"))
        _maxDecay = int(obj.get("maxDecay"))
        _featheringKernelSize = int(obj.get("featheringKernelSize"))
        return Masking(_enabled, _angularResolution, _stepSize, _fillSize, _maxDecay, _featheringKernelSize)

@dataclass
class NiftiExport:
    enabled: bool

    @staticmethod
    def from_dict(obj: Any) -> 'NiftiExport':
        _enabled = bool(obj.get("enabled"))
        return NiftiExport(_enabled)

@dataclass
class PatternMatching:
    voxelsPerBatch: int

    @staticmethod
    def from_dict(obj: Any) -> 'PatternMatching':
        _voxelsPerBatch = int(obj.get("voxelsPerBatch"))
        return PatternMatching(_voxelsPerBatch)

@dataclass
class PreparationSettings:
    initializeWithDCF: bool
    useDCFInIterations: bool
    readoutTruncationLimit: int
    maskingMode: str

    @staticmethod
    def from_dict(obj: Any) -> 'PreparationSettings':
        _initializeWithDCF = bool(obj.get("initializeWithDCF"))
        _useDCFInIterations = bool(obj.get("useDCFInIterations"))
        _readoutTruncationLimit = int(obj.get("readoutTruncationLimit"))
        _maskingMode = str(obj.get("maskingMode"))
        return PreparationSettings(_initializeWithDCF, _useDCFInIterations, _readoutTruncationLimit, _maskingMode)
    
@dataclass
class ResampledMatrixSize:
    x: int
    y: int
    z: int

    @staticmethod
    def from_dict(obj: Any) -> 'ResampledMatrixSize':
        _x = int(obj.get("x"))
        _y = int(obj.get("y"))
        _z = int(obj.get("z"))
        return ResampledMatrixSize(_x, _y, _z)

@dataclass
class SyntheticImages:
    enabled: bool
    az_largescale_connection_string: str
    az_model_container: str
    models: List[str]

    @staticmethod
    def from_dict(obj: Any) -> 'SyntheticImages':
        _enabled = bool(obj.get("enabled"))
        _az_largescale_connection_string = str(obj.get("az_largescale_connection_string"))
        _az_model_container = str(obj.get("az_model_container"))
        _models = obj.get("models")
        return SyntheticImages(_enabled, _az_largescale_connection_string, _az_model_container, _models)
    
@dataclass
class ReconstructionSettings:
    resampledMatrixSize: ResampledMatrixSize
    device: str
    coilCompression: CoilCompression
    iterativeNUFFT: IterativeNUFFT
    patternMatching: PatternMatching
    classificationMaps: ClassificationMaps
    masking: Masking
    syntheticImages: SyntheticImages
    niftiExport: NiftiExport
    dicomExport: DicomExport

    @staticmethod
    def from_dict(obj: Any) -> 'ReconstructionSettings':
        _resampledMatrixSize = ResampledMatrixSize.from_dict(obj.get("resampledMatrixSize"))
        _device = str(obj.get("device"))
        _coilCompression = CoilCompression.from_dict(obj.get("coilCompression"))
        _iterativeNUFFT = IterativeNUFFT.from_dict(obj.get("iterativeNUFFT"))
        _patternMatching = PatternMatching.from_dict(obj.get("patternMatching"))
        _classificationMaps = ClassificationMaps.from_dict(obj.get("classificationMaps"))
        _masking = Masking.from_dict(obj.get("masking"))
        _syntheticImages = SyntheticImages.from_dict(obj.get("syntheticImages"))
        _niftiExport = NiftiExport.from_dict(obj.get("niftiExport"))
        _dicomExport = DicomExport.from_dict(obj.get("dicomExport"))
        return ReconstructionSettings(_resampledMatrixSize, _device, _coilCompression, _iterativeNUFFT, _patternMatching, _classificationMaps, _masking, _syntheticImages, _niftiExport, _dicomExport)

@dataclass
class ReconstructionConfiguration:
    mrftools_version: str
    dataset_settings: DatasetSettings
    reconstruction_settings: ReconstructionSettings

    @staticmethod
    def ReadFromFile(filepath: str):
        with open(filepath, 'r') as f:
            return jsonpickle.decode(f.read())

    def SaveToFile(self, filepath: str):
        with open(filepath, 'w') as f:
            frozen = jsonpickle.encode(self, indent=1)
            f.write(frozen)

    @staticmethod
    def from_dict(obj: Any) -> 'ReconstructionConfiguration':
        _mrftools_version = str(obj.get("mrftools_version"))
        _dataset_settings = DatasetSettings.from_dict(obj.get("dataset_settings"))
        _reconstruction_settings = ReconstructionSettings.from_dict(obj.get("reconstruction_settings"))
        return ReconstructionConfiguration(_mrftools_version, _dataset_settings, _reconstruction_settings)
