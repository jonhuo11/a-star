# Running this project

Do a `pip install` on the `requirements.txt` and run `python main.py`.

I might add some more stuff to this repo in the future but for now its just a basic A\* demo.

In `notes.pdf` are my notes on A\* from Prof. Deng's course ([his website here](https://yuntiandeng.com/)) updated as of August 2025.

# TL;DR

For A*:
- the heuristic $h(n)$ is an estimate of the cost from $n$ to the goal node
- any heuristic must at least be **admissible** -> it must never overestimate the true cost
- if a heuristic is **consistent**, then $h(a) - h(b) \leq \text{edge}(a,b)$ for all $a$, $b$
	- this is the monotone condition
	- consistency -> admissibility
	- A\* no longer revisits nodes
- the algorithm itself is just Dijkstra's with a heuristic
