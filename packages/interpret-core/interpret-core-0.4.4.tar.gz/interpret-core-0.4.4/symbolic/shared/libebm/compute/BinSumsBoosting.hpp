// Copyright (c) 2023 The InterpretML Contributors
// Licensed under the MIT license.
// Author: Paul Koch <code@koch.ninja>

#ifndef BIN_SUMS_BOOSTING_HPP
#define BIN_SUMS_BOOSTING_HPP

#include <stddef.h> // size_t, ptrdiff_t

#include "logging.h" // EBM_ASSERT
#include "zones.h"

#include "common_cpp.hpp" // Multiply
#include "bridge_cpp.hpp" // BinSumsBoostingBridge
#include "GradientPair.hpp"
#include "Bin.hpp"

namespace DEFINED_ZONE_NAME {
#ifndef DEFINED_ZONE_NAME
#error DEFINED_ZONE_NAME must be defined
#endif // DEFINED_ZONE_NAME

template<typename TFloat, bool bHessian, size_t cCompilerScores, bool bWeight, bool bReplication, int cCompilerPack>
GPU_DEVICE NEVER_INLINE static void BinSumsBoostingInternal(BinSumsBoostingBridge * const pParams) {
   static_assert(bWeight || !bReplication, "bReplication cannot be true if bWeight is false");

   // TODO: we can improve the zero dimensional scenario quite a bit because we know that all the scores added will
   // eventually be added into the same bin.  Instead of adding the gradients & hessians & weights & counts from
   // each sample to the bin in order, we can just add those values together for all samples in SIMD variables
   // and then add the totals into the bins. We probably want to write a completely separate function for handling
   // it this way though.
   static constexpr bool bCompilerZeroDimensional = k_cItemsPerBitPackNone == cCompilerPack;
   static constexpr size_t cArrayScores = GetArrayScores(cCompilerScores);

#ifndef GPU_COMPILE
   EBM_ASSERT(nullptr != pParams);
   EBM_ASSERT(1 <= pParams->m_cSamples);
   EBM_ASSERT(0 == pParams->m_cSamples % size_t { TFloat::k_cSIMDPack });
   EBM_ASSERT(nullptr != pParams->m_aGradientsAndHessians);
   EBM_ASSERT(nullptr != pParams->m_aFastBins);
   EBM_ASSERT(k_dynamicScores == cCompilerScores || cCompilerScores == pParams->m_cScores);
#endif // GPU_COMPILE

   const size_t cScores = GET_COUNT_SCORES(cCompilerScores, pParams->m_cScores);

   auto * const aBins = reinterpret_cast<BinBase *>(pParams->m_aFastBins)->Specialize<typename TFloat::T, typename TFloat::TInt::T, bHessian, cArrayScores>();

   const size_t cSamples = pParams->m_cSamples;

   const typename TFloat::T * pGradientAndHessian = reinterpret_cast<const typename TFloat::T *>(pParams->m_aGradientsAndHessians);
   const typename TFloat::T * const pGradientsAndHessiansEnd = pGradientAndHessian + (bHessian ? size_t { 2 } : size_t { 1 }) * cScores * cSamples;

   typename TFloat::TInt::T cBytesPerBin;
   int cBitsPerItemMax;
   int cShift;
   int cShiftReset;
   typename TFloat::TInt maskBits;
   const typename TFloat::TInt::T * pInputData;

   if(!bCompilerZeroDimensional) {
      cBytesPerBin = static_cast<typename TFloat::TInt::T>(GetBinSize<typename TFloat::T, typename TFloat::TInt::T>(bHessian, cScores));

      const int cItemsPerBitPack = GET_ITEMS_PER_BIT_PACK(cCompilerPack, pParams->m_cPack);
#ifndef GPU_COMPILE
      EBM_ASSERT(k_cItemsPerBitPackNone != cItemsPerBitPack); // we require this condition to be templated
      EBM_ASSERT(1 <= cItemsPerBitPack);
      EBM_ASSERT(cItemsPerBitPack <= COUNT_BITS(typename TFloat::TInt::T));
#endif // GPU_COMPILE

      cBitsPerItemMax = GetCountBits<typename TFloat::TInt::T>(cItemsPerBitPack);
#ifndef GPU_COMPILE
      EBM_ASSERT(1 <= cBitsPerItemMax);
      EBM_ASSERT(cBitsPerItemMax <= COUNT_BITS(typename TFloat::TInt::T));
#endif // GPU_COMPILE

      cShift = static_cast<int>(((cSamples >> TFloat::k_cSIMDShift) - size_t { 1 }) % static_cast<size_t>(cItemsPerBitPack)) * cBitsPerItemMax;
      cShiftReset = (cItemsPerBitPack - 1) * cBitsPerItemMax;

      maskBits = MakeLowMask<typename TFloat::TInt::T>(cBitsPerItemMax);

      pInputData = reinterpret_cast<const typename TFloat::TInt::T *>(pParams->m_aPacked);
#ifndef GPU_COMPILE
      EBM_ASSERT(nullptr != pInputData);
#endif // GPU_COMPILE
   }

   const typename TFloat::T * pWeight;
   const uint8_t * pCountOccurrences;
   if(bWeight) {
      pWeight = reinterpret_cast<const typename TFloat::T *>(pParams->m_aWeights);
#ifndef GPU_COMPILE
      EBM_ASSERT(nullptr != pWeight);
#endif // GPU_COMPILE
      if(bReplication) {
         pCountOccurrences = pParams->m_pCountOccurrences;
#ifndef GPU_COMPILE
         EBM_ASSERT(nullptr != pCountOccurrences);
#endif // GPU_COMPILE
      }
   }

   do {
      // this loop gets about twice as slow if you add a single unpredictable branching if statement based on count, even if you still access all the memory
      // in complete sequential order, so we'll probably want to use non-branching instructions for any solution like conditional selection or multiplication
      // this loop gets about 3 times slower if you use a bad pseudo random number generator like rand(), although it might be better if you inlined rand().
      // this loop gets about 10 times slower if you use a proper pseudo random number generator like std::default_random_engine
      // taking all the above together, it seems unlikley we'll use a method of separating sets via single pass randomized set splitting.  Even if count is 
      // stored in memory if shouldn't increase the time spent fetching it by 2 times, unless our bottleneck when threading is overwhelmingly memory pressure
      // related, and even then we could store the count for a single bit aleviating the memory pressure greatly, if we use the right sampling method 

      // TODO : try using a sampling method with non-repeating samples, and put the count into a bit.  Then unwind that loop either at the byte level 
      //   (8 times) or the uint64_t level.  This can be done without branching and doesn't require random number generators

      // we store the already multiplied dimensional value in *pInputData
      typename TFloat::TInt iTensorBinCombined;
      if(!bCompilerZeroDimensional) {
         iTensorBinCombined = TFloat::TInt::Load(pInputData);
         pInputData += TFloat::TInt::k_cSIMDPack;
      }
      while(true) {
         Bin<typename TFloat::T, typename TFloat::TInt::T, bHessian, cArrayScores> * apBins[TFloat::k_cSIMDPack];
         if(!bCompilerZeroDimensional) {
            typename TFloat::TInt iTensorBin = (iTensorBinCombined >> cShift) & maskBits;
            
            // normally the compiler is better at optimimizing multiplications into shifs, but it isn't better
            // if TFloat is a SIMD type. For SIMD shifts & adds will almost always be better than multiplication if
            // there are low numbers of shifts, which should be the case for anything with a compile time constant here
            iTensorBin = Multiply<typename TFloat::TInt, typename TFloat::TInt::T, 
               k_dynamicScores != cCompilerScores && 1 != TFloat::k_cSIMDPack, 
               static_cast<typename TFloat::TInt::T>(GetBinSize<typename TFloat::T, typename TFloat::TInt::T>(bHessian, cCompilerScores))>(
                  iTensorBin, cBytesPerBin);
            
            TFloat::TInt::Execute([aBins, &apBins](const int i, const typename TFloat::TInt::T x) {
               apBins[i] = IndexBin(aBins, static_cast<size_t>(x));
            }, iTensorBin);
#ifndef NDEBUG
#ifndef GPU_COMPILE
            TFloat::Execute([cBytesPerBin, apBins, pParams](const int i) {
               ASSERT_BIN_OK(cBytesPerBin, apBins[i], pParams->m_pDebugFastBinsEnd);
            });
#endif // GPU_COMPILE
#endif // NDEBUG
         }

         // TODO: the ultimate version of this algorithm would:
         //   1) Write to k_cSIMDPack histograms simutaneously to avoid collisions of indexes
         //   2) Sum up the final histograms using SIMD operations in parallel.  If we hvae k_cSIMDPack
         //      histograms, then we're prefectly suited to sum them, and integers and float32 values shouldn't
         //      have issues since we stay well away from 2^32 integers, and the float values don't have addition
         //      issues anymore (where you can't add a 1 to more than 16 million floats)
         //   3) Only do the above if there aren't too many bins. If we put each sample into it's own bin
         //      for a feature, then we should prefer using this version that keeps only 1 histogram

         if(bReplication) {
            const typename TFloat::TInt cOccurences = TFloat::TInt::LoadBytes(pCountOccurrences);
            pCountOccurrences += TFloat::k_cSIMDPack;

            if(!bCompilerZeroDimensional) {
               TFloat::TInt::Execute([apBins](const int i, const typename TFloat::TInt::T x) {
                  auto * const pBin = apBins[i];
                  // TODO: In the future we'd like to eliminate this but we need the ability to change the Bin class
                  //       such that we can remove that field optionally
                  pBin->SetCountSamples(pBin->GetCountSamples() + x);
               }, cOccurences);
            } else {
               TFloat::TInt::Execute([aBins](int, const typename TFloat::TInt::T x) {
                  auto * const pBin = aBins;
                  // TODO: In the future we'd like to eliminate this but we need the ability to change the Bin class
                  //       such that we can remove that field optionally
                  pBin->SetCountSamples(pBin->GetCountSamples() + x);
               }, cOccurences);
            }
         } else {
            if(!bCompilerZeroDimensional) {
               TFloat::Execute([apBins](const int i) {
                  auto * const pBin = apBins[i];
                  // TODO: In the future we'd like to eliminate this but we need the ability to change the Bin class
                  //       such that we can remove that field optionally
                  pBin->SetCountSamples(pBin->GetCountSamples() + typename TFloat::TInt::T { 1 });
               });
            } else {
               TFloat::Execute([aBins](int) {
                  auto * const pBin = aBins;
                  // TODO: In the future we'd like to eliminate this but we need the ability to change the Bin class
                  //       such that we can remove that field optionally
                  pBin->SetCountSamples(pBin->GetCountSamples() + typename TFloat::TInt::T { 1 });
               });
            }
         }

         TFloat weight;
         if(bWeight) {
            weight = TFloat::Load(pWeight);
            pWeight += TFloat::k_cSIMDPack;

            if(!bCompilerZeroDimensional) {
               TFloat::Execute([apBins](const int i, const typename TFloat::T x) {
                  auto * const pBin = apBins[i];
                  // TODO: In the future we'd like to eliminate this but we need the ability to change the Bin class
                  //       such that we can remove that field optionally
                  pBin->SetWeight(pBin->GetWeight() + x);
               }, weight);
            } else {
               TFloat::Execute([aBins](int, const typename TFloat::T x) {
                  auto * const pBin = aBins;
                  // TODO: In the future we'd like to eliminate this but we need the ability to change the Bin class
                  //       such that we can remove that field optionally
                  pBin->SetWeight(pBin->GetWeight() + x);
               }, weight);
            }
         } else {
            if(!bCompilerZeroDimensional) {
               TFloat::Execute([apBins](const int i) {
                  auto * const pBin = apBins[i];
                  // TODO: In the future we'd like to eliminate this but we need the ability to change the Bin class
                  //       such that we can remove that field optionally
                  pBin->SetWeight(pBin->GetWeight() + typename TFloat::T { 1.0 });
               });
            } else {
               TFloat::Execute([aBins](int) {
                  auto * const pBin = aBins;
                  // TODO: In the future we'd like to eliminate this but we need the ability to change the Bin class
                  //       such that we can remove that field optionally
                  pBin->SetWeight(pBin->GetWeight() + typename TFloat::T { 1.0 });
               });
            }
         }

         // TODO: we probably want a templated version of this function for Bins with only 1 cScore so that
         //       we don't have a loop here, which will mean that the cCompilerPack will be the only loop which
         //       will allow the compiler to unroll that loop (since it only unrolls one level of loops)

         size_t iScore = 0;
         do {
            if(!bCompilerZeroDimensional) {
               if(bHessian) {
                  TFloat gradient = TFloat::Load(&pGradientAndHessian[iScore << (TFloat::k_cSIMDShift + 1)]);
                  TFloat hessian = TFloat::Load(&pGradientAndHessian[(iScore << (TFloat::k_cSIMDShift + 1)) + TFloat::k_cSIMDPack]);
                  if(bWeight) {
                     gradient *= weight;
                     hessian *= weight;
                  }
                  TFloat::Execute([apBins, iScore](const int i, const typename TFloat::T grad, const typename TFloat::T hess) {
                     // BEWARE: unless we generate a separate histogram for each SIMD stream and later merge them, pBin can 
                     // point to the same bin in multiple samples within the SIMD pack, so we need to serialize fetching sums
                     auto * const pBin = apBins[i];
                     auto * const aGradientPair = pBin->GetGradientPairs();
                     auto * const pGradientPair = &aGradientPair[iScore];
                     typename TFloat::T binGrad = pGradientPair->m_sumGradients;
                     typename TFloat::T binHess = pGradientPair->GetHess();
                     binGrad += grad;
                     binHess += hess;
                     pGradientPair->m_sumGradients = binGrad;
                     pGradientPair->SetHess(binHess);
                  }, gradient, hessian);
               } else {
                  TFloat gradient = TFloat::Load(&pGradientAndHessian[iScore << TFloat::k_cSIMDShift]);
                  if(bWeight) {
                     gradient *= weight;
                  }
                  TFloat::Execute([apBins, iScore](const int i, const typename TFloat::T grad) {
                     // TODO: for this special case of having just 1 bin, we could sum all the gradients and hessians
                     // before then adding them to the only bin
                     auto * const pBin = apBins[i];
                     auto * const aGradientPair = pBin->GetGradientPairs();
                     auto * const pGradientPair = &aGradientPair[iScore];
                     pGradientPair->m_sumGradients += grad;
                  }, gradient);
               }
            } else {
               if(bHessian) {
                  TFloat gradient = TFloat::Load(&pGradientAndHessian[iScore << (TFloat::k_cSIMDShift + 1)]);
                  TFloat hessian = TFloat::Load(&pGradientAndHessian[(iScore << (TFloat::k_cSIMDShift + 1)) + TFloat::k_cSIMDPack]);
                  if(bWeight) {
                     gradient *= weight;
                     hessian *= weight;
                  }
                  TFloat::Execute([aBins, iScore](int, const typename TFloat::T grad, const typename TFloat::T hess) {
                     // BEWARE: unless we generate a separate histogram for each SIMD stream and later merge them, pBin can 
                     // point to the same bin in multiple samples within the SIMD pack, so we need to serialize fetching sums
                     auto * const pBin = aBins;
                     auto * const aGradientPair = pBin->GetGradientPairs();
                     auto * const pGradientPair = &aGradientPair[iScore];
                     typename TFloat::T binGrad = pGradientPair->m_sumGradients;
                     typename TFloat::T binHess = pGradientPair->GetHess();
                     binGrad += grad;
                     binHess += hess;
                     pGradientPair->m_sumGradients = binGrad;
                     pGradientPair->SetHess(binHess);
                  }, gradient, hessian);
               } else {
                  TFloat gradient = TFloat::Load(&pGradientAndHessian[iScore << TFloat::k_cSIMDShift]);
                  if(bWeight) {
                     gradient *= weight;
                  }
                  TFloat::Execute([aBins, iScore](int, const typename TFloat::T grad) {
                     // TODO: for this special case of having just 1 bin, we could sum all the gradients and hessians
                     // before then adding them to the only bin
                     auto * const pBin = aBins;
                     auto * const aGradientPair = pBin->GetGradientPairs();
                     auto * const pGradientPair = &aGradientPair[iScore];
                     pGradientPair->m_sumGradients += grad;
                  }, gradient);
               }
            }
            ++iScore;
         } while(cScores != iScore);

         pGradientAndHessian += cScores << (bHessian ? (TFloat::k_cSIMDShift + 1) : TFloat::k_cSIMDShift);

         if(bCompilerZeroDimensional) {
            if(pGradientsAndHessiansEnd == pGradientAndHessian) {
               break;
            }
         } else {
            cShift -= cBitsPerItemMax;
            if(cShift < 0) {
               break;
            }
         }
      }
      if(bCompilerZeroDimensional) {
         break;
      }
      cShift = cShiftReset;
   } while(pGradientsAndHessiansEnd != pGradientAndHessian);
}

template<typename TFloat, bool bHessian, size_t cCompilerScores, bool bWeight, bool bReplication, int cCompilerPack>
GPU_GLOBAL static void RemoteBinSumsBoosting(BinSumsBoostingBridge * const pParams) {
   BinSumsBoostingInternal<TFloat, bHessian, cCompilerScores, bWeight, bReplication, cCompilerPack>(pParams);
}

template<typename TFloat, bool bHessian, size_t cCompilerScores, bool bWeight, bool bReplication, int cCompilerPack>
INLINE_RELEASE_TEMPLATED ErrorEbm OperatorBinSumsBoosting(BinSumsBoostingBridge * const pParams) {
   return TFloat::template OperatorBinSumsBoosting<bHessian, cCompilerScores, bWeight, bReplication, cCompilerPack>(pParams);
}

template<typename TFloat, bool bHessian, size_t cCompilerScores, bool bWeight, bool bReplication>
INLINE_RELEASE_TEMPLATED static ErrorEbm BitPackBoosting(BinSumsBoostingBridge * const pParams) {
   if(k_cItemsPerBitPackNone != pParams->m_cPack) {
      return OperatorBinSumsBoosting<TFloat, bHessian, cCompilerScores, bWeight, bReplication, k_cItemsPerBitPackDynamic>(pParams);
   } else {
      // this needs to be special cased because otherwise we would inject comparisons into the dynamic version
      return OperatorBinSumsBoosting<TFloat, bHessian, cCompilerScores, bWeight, bReplication, k_cItemsPerBitPackNone>(pParams);
   }
}


template<typename TFloat, bool bHessian, size_t cCompilerScores>
INLINE_RELEASE_TEMPLATED static ErrorEbm FinalOptionsBoosting(BinSumsBoostingBridge * const pParams) {
   if(nullptr != pParams->m_aWeights) {
      static constexpr bool bWeight = true;

      if(nullptr != pParams->m_pCountOccurrences) {
         static constexpr bool bReplication = true;
         return BitPackBoosting<TFloat, bHessian, cCompilerScores, bWeight, bReplication>(pParams);
      } else {
         static constexpr bool bReplication = false;
         return BitPackBoosting<TFloat, bHessian, cCompilerScores, bWeight, bReplication>(pParams);
      }
   } else {
      static constexpr bool bWeight = false;

      // we use the weights to hold both the weights and the inner bag counts if there are inner bags
      EBM_ASSERT(nullptr == pParams->m_pCountOccurrences);
      static constexpr bool bReplication = false;

      return BitPackBoosting<TFloat, bHessian, cCompilerScores, bWeight, bReplication>(pParams);
   }
}


template<typename TFloat, bool bHessian, size_t cPossibleScores>
struct CountClassesBoosting final {
   INLINE_RELEASE_UNTEMPLATED static ErrorEbm Func(BinSumsBoostingBridge * const pParams) {
      if(cPossibleScores == pParams->m_cScores) {
         return FinalOptionsBoosting<TFloat, bHessian, cPossibleScores>(pParams);
      } else {
         return CountClassesBoosting<TFloat, bHessian, cPossibleScores + 1>::Func(pParams);
      }
   }
};
template<typename TFloat, bool bHessian>
struct CountClassesBoosting<TFloat, bHessian, k_cCompilerScoresMax + 1> final {
   INLINE_RELEASE_UNTEMPLATED static ErrorEbm Func(BinSumsBoostingBridge * const pParams) {
      return FinalOptionsBoosting<TFloat, bHessian, k_dynamicScores>(pParams);
   }
};

template<typename TFloat>
INLINE_RELEASE_TEMPLATED static ErrorEbm BinSumsBoosting(BinSumsBoostingBridge * const pParams) {
   LOG_0(Trace_Verbose, "Entered BinSumsBoosting");

   // all our memory should be aligned. It is required by SIMD for correctness or performance
   EBM_ASSERT(IsAligned(pParams->m_aGradientsAndHessians));
   EBM_ASSERT(IsAligned(pParams->m_aWeights));
   EBM_ASSERT(IsAligned(pParams->m_pCountOccurrences));
   EBM_ASSERT(IsAligned(pParams->m_aPacked));
   EBM_ASSERT(IsAligned(pParams->m_aFastBins));

   ErrorEbm error;

   EBM_ASSERT(1 <= pParams->m_cScores);
   if(EBM_FALSE != pParams->m_bHessian) {
      if(size_t { 1 } != pParams->m_cScores) {
         // muticlass
         error = CountClassesBoosting<TFloat, true, k_cCompilerScoresStart>::Func(pParams);
      } else {
         error = FinalOptionsBoosting<TFloat, true, k_oneScore>(pParams);
      }
   } else {
      if(size_t { 1 } != pParams->m_cScores) {
         // Odd: gradient multiclass. Allow it, but do not optimize for it
         error = FinalOptionsBoosting<TFloat, false, k_dynamicScores>(pParams);
      } else {
         error = FinalOptionsBoosting<TFloat, false, k_oneScore>(pParams);
      }
   }

   LOG_0(Trace_Verbose, "Exited BinSumsBoosting");

   return error;
}

} // DEFINED_ZONE_NAME

#endif // BIN_SUMS_BOOSTING_HPP