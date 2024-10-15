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
