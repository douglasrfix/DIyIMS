# TODO: include any peer entries from known nodes
# TODO: find providers
# TODO: for each provider insert in peer_table with New flag
# TODO: for each new provider
# TODO:     generate cid for ipns name ,dts file
#           get the cid(wait)
#
#           for some period(?) look for high count repeat want list items
#           for each entry in providers want list insert record in want_table
#           select from want_table grouped by want cid, order by count in group desc order by dts ascending
#               capture most recent dts and delete entries that ont have a current time stamp to filter out
#           the satisfied wants of the canceled wants. for each batch compare the last seen timestamp to the current time stamp and delete the
#           no longer seen
#
            if the entry reflects self cid than we have a match or
                if the entry reflects the highest count
                    put that cid in the want list

            add ipns name file with hash only No to satisfy the remote and local get do not pin the local want.locals

add first see to a want_list entry for a peer to allow for calculating residence time. this would allow
the peer to pulse or flash the cid to distinguish it from a cid not being used a beacon. you code send morse code with such a technique. to blink you would have to satisfy the get and therefore use a different cid for each pulse. the puls must last long enough to hang s get and wait for the end of the pulse.  a long short pulse train would for the same peer would be simple to detect.  the response would be a pulse train in response which would allow the two peers to sync up and allow a few pulses for every one to hang a get before you quite the beaconing.
the cid would not be pinned.

could you detect the same behavior in the swarm or bitswap to advantage?

need a function to generate pulses. and detect pulses and one to detect the bit sequence of a network id

this beaconing would be continuous 1 min on 1 off? 2min on 2 off alternating like a light house maybe based on the network name to avoid collisions.

cycle back to the peer table to determine if we need to watch that peer any longer

collect into a buffer and track the current eight bits 0000 1010 0000, 0000 1010 0000
the four bit code in the middle must start with a 1 with three bits for the id maybe the last three bits of the network name? maybe to short causing collisions.

# TODO:
# TODO:     if a remote node want list entry is satisfied, update ent peer_entry table with ipns and cid of peer_table from file
#            add/update entries from the remote table and start over unpin the file cid and the peer table cid


# return the process by extracting the providers again
# TODO:
# TODO:
# TODO:
# TODO:
# TODO:
# TODO:
# TODO:
