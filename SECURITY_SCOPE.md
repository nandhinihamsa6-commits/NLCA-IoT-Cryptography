# Security Scope and Limitations

NLCA is an experimental cipher design.

The repository provides deterministic implementation, inverse verification, DDT, LAT, nonlinearity, fixed-point checks, avalanche analysis, reduced-round evaluation, statistical measurements and Python/C equivalence testing.

These results do not constitute a proof of resistance to differential, linear, algebraic, related-key, integral, impossible-differential, side-channel or implementation attacks. Five rounds are retained as the manuscript profile and must be justified with the generated round-convergence evidence. External cryptanalysis remains necessary.

The package does not claim integrity or authenticity. A block cipher mode without authentication must not be presented as authenticated encryption.
