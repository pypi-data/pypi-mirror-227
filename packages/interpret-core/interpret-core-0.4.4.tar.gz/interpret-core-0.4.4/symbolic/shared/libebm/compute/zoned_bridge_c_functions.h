// Copyright (c) 2023 The InterpretML Contributors
// Licensed under the MIT license.
// Author: Paul Koch <code@koch.ninja>

#ifndef ZONED_BRIDGE_C_FUNCTIONS_H
#define ZONED_BRIDGE_C_FUNCTIONS_H

#include "libebm.h" // ErrorEbm
#include "bridge_c.h" // INTERNAL_IMPORT_EXPORT_INCLUDE
#include "zones.h" // MAKE_ZONED_C_FUNCTION_NAME

#ifdef __cplusplus
extern "C" {
#endif // __cplusplus

INTERNAL_IMPORT_EXPORT_INCLUDE ErrorEbm MAKE_ZONED_C_FUNCTION_NAME(ApplyUpdate)(
   const ObjectiveWrapper * const pObjectiveWrapper,
   ApplyUpdateBridge * const pData
);

INTERNAL_IMPORT_EXPORT_INCLUDE ErrorEbm MAKE_ZONED_C_FUNCTION_NAME(BinSumsBoosting)(
   const ObjectiveWrapper * const pObjectiveWrapper,
   BinSumsBoostingBridge * const pParams
);

INTERNAL_IMPORT_EXPORT_INCLUDE ErrorEbm MAKE_ZONED_C_FUNCTION_NAME(BinSumsInteraction)(
   const ObjectiveWrapper * const pObjectiveWrapper,
   BinSumsInteractionBridge * const pParams
);

#ifdef ZONE_cpu
INTERNAL_IMPORT_EXPORT_INCLUDE double MAKE_ZONED_C_FUNCTION_NAME(FinishMetric) (
   const ObjectiveWrapper * const pObjectiveWrapper,
   const double metricSum
);
INTERNAL_IMPORT_EXPORT_INCLUDE BoolEbm MAKE_ZONED_C_FUNCTION_NAME(CheckTargets) (
   const ObjectiveWrapper * const pObjectiveWrapper,
   const size_t c, 
   const void * const aTargets
);
#endif // ZONE_cpu


#ifdef __cplusplus
}
#endif // __cplusplus

#endif // ZONED_BRIDGE_C_FUNCTIONS_H
