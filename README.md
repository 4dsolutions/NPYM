# NPYM

Experimental schema for recording Quaker doings within a Yearly Meeting region.

modeling_1_v2.py and modeling_2_v2.py are sufficient to create the persistent NPYM.db, a sqlite file,
populated with real world slate data, mostly from Multnomah Monthly Meeting, Portland, Oregon, 2015.
The data was published in world-readable FGC Cloud (MMM not a member of FGC in 2015) in PDF format.
I used it to test my Flask-implemented API.

The schema is designed to allow a complete record of a Friend's service through
time, with "now" but a cross-section through a growing timeline of timelines (scenarios).
Friends take up roles for a duration.  The tables store start and end dates using integers,
numbering from the beginning of the epoch 01/01/0001, with a proleptic Gregorian calendar.

The API runs queries to populate simple Jinja2 templates, standard with Flask.

Example URIs (purely science fictional at this time -- no reason to try visiting, just 
get your own version up and running for continuing development):

List all meetings in NPYM:    
ds.npym.org/meetings

List details for one meeting: 
ds.npym.org/meeting/mm

Currently serving on Committees etc.: 
ds.npym.org/meeting/mm/slate

... at Yearly Meeting level:  
ds.npym.org/meeting/npym/slate

Listing of Friends willing to be listed: 
ds.npym.org/meeting/mm/friends

(ds = directory services) -- in 2015 we were talking about partitioning into subdomains
but had not done so.  I was clerk of IT Committee, brainstorming about the future.

