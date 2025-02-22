

from Market.BlackScholes import BlackScholes

bs = BlackScholes(t_start=0, t_end=1, s0=100, r=0.9, sigma=0.2)
bs.generate_scenarios(3, 10000)
bs.plot_underlying(legend=True)
