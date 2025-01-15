# Impact of topology on multipartite entanglement distribution protocols in quantum networks 

This code was written for the paper [Impact of topology on multipartite entanglement distribution protocols in quantum networks (draft)](https://jazzooi21-CV.short.gy/JOCN-draft).


Quantum networks, applicable from distributed quantum computing to cryptography, require entanglement distribution between all users via repeaters before exchanging quantum information. Previous work has shown that performance of multipartite entanglement distribution protocols is dependent on network topology and repeater placement.
In this paper, we study the performance of three routing protocols in establishing GHZ states on 75 real networks — one single-path (SP) and two multi-path (MP) based protocols. Networks are partitioned into four clusters according to protocol performance in Monte Carlo simulations, and network attributes correlated to each cluster are identified. Furthermore, we investigate the repeater use of the two MP protocols, demonstrating that network topology significantly impacts effectiveness of reallocating repeater resources. Reprioritisation of repeaters saves up to 35% in usage ( ×1.92 to ×1.25 of SP protocol) for the best-performing cluster, whilst retaining more than 5 times the distribution rate and lower than 30% of the runtime of SP.




`QuanTech_jazz_main.ipynb` contains the main analysis, including protocol implementation, data extraction, attribute calculation and repeater removal analysis.

`iterations.ipynb` involves comparison and analysis of network topology and its effect on protocol performance, as well as the $k$-means clustering.

`generate_graphs_for_compare.py` generates standard graphs (e.g. complete graph, star graph, complete bipartite graph) for comparison with real networks.

`trimmed_iters_funcs.py` exists for JIT compiler parallelization (`numba`).
