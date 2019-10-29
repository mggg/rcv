DESCRIPTION:

Lowell_rcv_citywide.py and Lowell_rcv_3district.py run Ranked Choice Voting (RCV) on a suite of predefined scenarios.
Lowell_rcv_citywide.py runs RCV for one jurisdiction-wide vote. Lowll_rcv_3district.py runs RCV for three districts.

The election winners are determined by a Single Transferable Vote algorithm:
votes that exceed the required threshold are transferred to the ballots' next choice preference and so on. 
We use the Cincinnati method to transfer votes.  

The scenarios (described below) represent a range of potential voter behavior in
communities with two sizeable racial minority populations that together form a Coalition.

The scenarios vary the following parameters:
    - level of racial polarization
    - aggreement among voters on how candidates of certain racial groups are ranked


USER GUIDE:

The most basic (and intended) use of this simulation requires only changing the 
following inputs (located at the very bottom of the Lowell_rcv_citywide.py and 
Lowell_rcv_citywide.py scripts):

    - num_votes = number of total votes cast in each simulation run
        (e.g. num_votes = 3000)
    - num_runs = number of times each election is simulated (note that
        to avoid redundancy, each deterministic scenario is only run once)
        (e.g. num_runs = 100)
    - num_seats = number of seats being filled by the algorithm 
	(e.g. num_seats = 3)

A user may also generate new scenarios to add to the sweep (or contact us with
ideas for new scenarios).

It is not intended for the user to change any of the code that actually simulates
the election. In order to replicate the results in the Lowell report (found at
https://mggg.org/uploads/Lowell-Detailed-Report.pdf) we have also left the relevant
input data (for CVAP) in the code.


SCENARIOS:

There are eight different scenarios in the simulation. The scenarios vary over 
two different levels of voting polarization and four different ways of ordering 
('permuting') the candidates, giving a total of eight possible combinations.


Voting Polarization:
	- In 'Polarized' voting, voters prefer candidates of their racial group to 
	candidates of other racial groups.  That is, White voters prefer White candidates 
	to Coalition candidates and rank all White candidates before ranking any Coalition 
	candidates. Conversely, Coalition voters rank all Coalition candidates before 
	ranking any White candidates.
	- In 'Crossover' voting, some percent of voters from a given racial group
	will prefer a candidate of a different racial group, and
	the remaining voters vote 'Polarized', as above. We use a simple model of 
	crossover voting in which a White 'Crossover' voter ranks a Coalition candidate 
	first and then alternates (i.e. CWCWCW...) between White and Coalition candidates.
	Conversely, a Coalition 'Crossover' voter ranks a White candidate first and then
	alternates between Coalition and White candidates.

Candidate Permutations:
	- In 'Unanimous' voting, all voters agree on the same ranking of White candidates
	and the same ranking of minority candidates.  (How those candidates from 
	different racial groups are ranked compared to each other is determined by
	the voting polarization level described above).
	- In 'Non-White voters permute Coalition candidates' voting,  Coalition voters 
	don't agree on the ranking of Coalition candidates (the simulation chooses each Coalition
	voter's ranking of Coalition candidates at random)
	- In 'White voters permute all candidates' voting, White voters don't agree on the the
	ranking of White candidates OR on the ranking of Coalition candidates
	- In 'White and Coalition voters permute all candidates' voting, there is not agreement
	on the ranking of White or Coalition candidates among voters of any racial group. 


OUTPUTS:

Each Python script generates one output CSV file in the same directory the scripts are stored in. 
It includes the results of a sensitivity analysis that varies crossover voting rates (i.e. the portion of
each racial group that are crossover voters) and relative turnout rates (i.e. the relative 
rate of voter turnout for each racial group, where rates are relative to White and Other voters 
who are assumed to have the highest turnout rates). Each row is defined by a different combination
of crossover and turnout assumptions. Results in each row are the average number of elected
Coalition candidates (averaged over the num_rums) out of the total num_seats.

SIMPLIFYING ASSUMPTIONS:

There are arbitrarily many options and scenarios that can be simulated.  This code makes some
simplifying assumptions that can easily be modified by the user.
	- We assume that if there are n seats, then there are n White candidates and
	n Coalition candidates in the race.  This assumption allows for all possible
	numbers of Coalition (and White) winners between 0 and n.
	- We assume that every voter ranks every candidate.
	- We assume that a Coalition 'crossover' voter is one who prefers a White candidate and
	vice versa for a White 'crossover' voter.
	- We assume that voters do not distinguish between candidates of different races within 
	the Coalition racial groups.