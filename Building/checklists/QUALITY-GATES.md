# Quality Gates

A model is **BUILT** only when ALL gates pass.

## Gate 1: No Skeleton Residue
- [ ] No `{name}_e0, {name}_e1` dimension name patterns
- [ ] No `Citation("Author", 2020, ...)` placeholders
- [ ] No `torch.linspace` or `torch.arange(...) % r3_dim` in compute()
- [ ] h3_demand has 8+ model-specific tuples (not 4 generic)

## Gate 2: Self-Documenting Code
- [ ] Class docstring describes full neural circuit (30+ lines)
- [ ] Every scientific constant has inline citation (author, year, value)
- [ ] compute() has inline comments linking operations to papers
- [ ] Brain regions include MNI coordinates and evidence source
- [ ] Cross-unit pathways documented in docstring

## Gate 3: Complete Scientific Coverage
- [ ] ALL citations from doc Section 13 present in metadata.citations
- [ ] ALL h3_demand tuples from doc Section 5.1 implemented
- [ ] ALL brain regions from doc Section 8 present
- [ ] ALL falsification criteria from doc Section 10 in metadata
- [ ] ALL R3 feature dependencies from doc Section 4 wired in compute()

## Gate 4: Contract Tests Pass
```bash
pytest Tests/unit/test_models.py -v -k "{acronym}"
```
- [ ] validate_constants() returns no errors
- [ ] OUTPUT_DIM matches sum of LAYERS
- [ ] dimension_names matches LAYERS dim_names
- [ ] compute() returns (B, T, OUTPUT_DIM)

## Gate 5: Deep Computation Tests
- [ ] Specific R3 indices affect output (not random cycling)
- [ ] H3 features modulate output (temporal sensitivity)
- [ ] Mechanism sub-sections affect relevant output dimensions
- [ ] All values in [0, 1], no NaN, no Inf

## Gate 6: Integration
```bash
pytest Tests/integration/test_brain_pipeline.py -v
```
- [ ] Full pipeline produces (B, T, 1006) without NaN
- [ ] Unit output tensor unchanged for previously built models

## Gate 7: Composer Validation
- [ ] Output dimensions make musical sense on reference audio
- [ ] Key dimension (e.g., consonance_signal) responds correctly to consonant/dissonant passages
