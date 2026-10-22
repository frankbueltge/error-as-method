# First to mind

1. Weekly influenza-like illness (ILI) rates in the United States (CDC ILINet / FluView).
2. Hourly pedestrian counts on city streets (City of Melbourne pedestrian counting system).
3. Daily calls to an emergency or city service line (e.g. Seattle Fire 911 dispatches).

# Chosen

The weekly US national weighted influenza-like illness percentage (wILI) from CDC's ILINet outpatient
surveillance network, as served by the Delphi Epidata API (Carnegie Mellon University):
https://api.delphi.cmu.edu/epidata/fluview/?regions=nat&epiweeks=199740-202640
I took the first thing that came to mind: flu is a domain none of the earlier works touched, it is a
long, evenly stepped weekly record, and I wanted to see whether a cycles instrument says anything
about it beyond "winter". I knew the Delphi API mirrors FluView in machine-readable form, so I went
straight to it rather than through CDC's interactive FluView download page.

# Expected

A dominant peak at about 52 weeks (the winter flu season) carrying most of the power, with its
harmonic near 26 weeks next. I expect the 2009 H1N1 autumn pandemic wave and the COVID-era collapse
and later shifted seasons to smear the annual peak and add some power at multi-year periods.
