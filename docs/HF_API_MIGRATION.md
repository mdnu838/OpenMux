# HuggingFace Inference API Migration Notes

## Problem Summary

**Date:** November 10, 2025

HuggingFace has deprecated their free Inference API endpoint and moved to a new paid/dedicated service model.

##  Findings

### 1. Old API Deprecated (HTTP 410 Gone)
- **Old Endpoint:** `https://api-inference.huggingface.co/models/{model_id}`
- **Status:** Returns HTTP 410 Gone with message:
  ```
  {"error":"https://api-inference.huggingface.co is no longer supported. 
   Please use https://router.huggingface.co/hf-inference instead."}
  ```

### 2. New Router Endpoint Not Working
- **Suggested Endpoint:** `https://router.huggingface.co/hf-inference`
- **Status:** Returns HTTP 404 Not Found
- **Tried Formats:**
  - `/hf-inference`
  - `/hf-inference/models/{model_id}`
  - `/hf-inference/{model_id}`
  - With model in payload
- **Result:** All return 404

### 3. Official Library Also Failing
- **Library:** `huggingface-hub` (v0.36.0)
- **Client:** `InferenceClient`
- **Error:** `StopIteration interacts badly with generators and cannot be raised into a Future`
- **Methods Tested:**
  - `text_generation()` - Fails
  - `feature_extraction()` - Not tested yet
- **Root Cause:** API backend changes broke the client library

## Impact on OpenMux

### Current Status
- ✅ HuggingFace unit tests: PASSING (26 tests, mocked)
- ❌ HuggingFace live API tests: SKIPPED (12 tests, API deprecated)
- 🔄 HuggingFace provider: PARTIALLY WORKING (initialization OK, API calls fail)

### Affected Features
1. **HuggingFace Provider** (`openmux/providers/huggingface.py`)
   - Cannot make real API calls
   - Unit tests work (mocked responses)
   - Live integration fails

2. **Orchestrator** (when selecting HuggingFace)
   - Will fail at generation step
   - Fallback to Ollama should work

3. **Task Type Support**
   - CHAT: ❌ Broken
   - CODE: ❌ Broken
   - EMBEDDINGS: ❌ Broken

## Alternatives & Solutions

### Option 1: HuggingFace Serverless Inference (Paid)
- **Endpoint:** `https://api-inference.huggingface.co/models/{model}`
- **Pricing:** Pay-per-use
- **Pros:** Official, reliable, fast
- **Cons:** Requires payment, breaks "free" promise

###  Option 2: HuggingFace Dedicated Endpoints (Paid)
- **Type:** Dedicated GPU instances
- **Pricing:** Hourly billing
- **Pros:** High performance, customizable
- **Cons:** Expensive, overkill for our use case

### Option 3: Remove HuggingFace Provider ⚠️
- **Action:** Deprecate HuggingFace provider
- **Impact:** 
  - Remove 26 unit tests
  - Update documentation
  - Focus on OpenRouter (works) and Ollama (local)
- **Pros:** Clean break, no broken code
- **Cons:** Reduces provider diversity

### Option 4: Wait for API Stabilization
- **Action:** Keep provider code, skip tests until HuggingFace clarifies new API
- **Timeline:** Unknown (could be days/weeks/months)
- **Pros:** Preserves work done
- **Cons:** Broken feature in codebase

### ✅ Option 5: Switch to Transformers Pipeline (LOCAL)
- **Library:** `transformers` (already a dependency)
- **Approach:** Run models locally instead of API
- **Pros:** 
  - Free forever
  - No API rate limits
  - Already have the library
  - Aligns with "local-first" philosophy
- **Cons:**
  - Requires downloading models
  - Higher memory usage
  - Slower than dedicated API

## Recommended Action

**Hybrid Approach:**

1. **Short Term** (v0.2.4):
   - ✅ Keep HuggingFace provider code
   - ✅ Mark live tests as skipped with clear reason
   - ✅ Document API migration in CHANGELOG
   - ✅ Focus on OpenRouter and Ollama providers

2. **Medium Term** (v0.3.0):
   - Implement local Transformers pipeline support
   - Create new `HuggingFaceLocalProvider` using `transformers`
   - Keep remote API code for when it's fixed

3. **Long Term** (v0.4.0):
   - Monitor HuggingFace API updates
   - Re-enable remote provider when API stabilizes
   - Offer both local and remote options

## Files Affected

### Created/Modified for Investigation
1. `serper/hf_api_discovery.py` - API endpoint discovery script
2. `serper/find_hf_models.py` - Model discovery script
3. `serper/test_hf_v2.py` - Test script for new provider
4. `openmux/providers/huggingface_v2.py` - Updated provider (non-working)
5. `tests/integration/test_huggingface_live.py` - Live tests (skipped)

### Documentation
6. `docs/HF_API_MIGRATION.md` - This file

## Next Steps

1. ✅ Document findings (this file)
2. ⏳ Update CHANGELOG.md for v0.2.4
3. ⏳ Update TASK_LIST.md to reflect API situation
4. ⏳ Focus on Ollama provider improvements instead
5. ⏳ Build v0.2.4 with skipped HF tests
6. ⏳ Monitor HuggingFace blog/docs for announcements

## References

- HuggingFace Inference API Docs: https://huggingface.co/docs/api-inference/index
- Inference Endpoints: https://huggingface.co/inference-endpoints
- Serverless Inference: https://huggingface.co/docs/api-inference/quicktour
- huggingface_hub Library: https://huggingface.co/docs/huggingface_hub/guides/inference

---

**Last Updated:** November 10, 2025  
**Status:** Investigation Complete, Workaround Implemented (skip tests)  
**Owner:** OpenMux Development Team
