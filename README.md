# PulseGrid — Probability Lab

**Individual project by Makhmetov Alikhan**

PulseGrid is an interactive Python web app for exploring probability through a server reliability scenario. Instead of a standard lottery calculator, it models a cluster of servers and asks: how likely is an overload, and how closely do repeated simulations follow the mathematical model?

The app follows an investigative cycle: make a prediction, change the model, generate data, compare it with theory, and interpret the result.

## Start the app

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies with pip install -r requirements.txt.
4. Start the site with streamlit run app.py.

Streamlit prints a local address when the app is ready.

## The four sections

- **Combinatorics** counts distinct overload patterns with combinations, calculates exact probabilities, and displays the full outcome distribution.
- **Simulation** runs from 100 to 100,000 simulated minutes, compares observed frequencies with theoretical probabilities, and reports the mean, median, and standard deviation.
- **Events** explores conditional probability and the probability of overloads in two independent minutes.
- **Formula deck** gathers the formulas and symbol definitions used throughout the project.

The sidebar lets a student set the number of server nodes, the overload chance for each node, the exact number of overloaded nodes to study, and the number of simulation rounds.

## Mathematical model

Let X be the number of overloaded server nodes in one minute. If there are n nodes and each node overloads independently with probability p, then X follows a binomial distribution:

- Number of patterns with exactly m overloaded nodes: C(n, m)
- Exact probability: P(X = m) = C(n, m) p^m (1 - p)^(n - m)
- Probability of at least one overload: P(X ≥ 1) = 1 - (1 - p)^n
- Expected overload count: E[X] = np
- Standard deviation: √(np(1 - p))

The model assumes equal overload chances across nodes and independent outcomes between nodes and minutes. Real servers can influence one another, so the independence assumption is a simplification that can be discussed during a presentation.

## Tech stack

Python, Streamlit, NumPy, Pandas, and Plotly. Probability calculations use Python's standard math.comb function and explicit binomial formulas.

