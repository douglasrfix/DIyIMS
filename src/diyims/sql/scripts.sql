

-- name: insert_header!
insert into Header (ObjectIPFSPath, ObjectSubType, UserHeaderIPFSPath, PeerHeaderIPFSPath, PublishedUTCDTS, PriorIPFSPath, Version)
values (:ObjectIPFSPath, :ObjectSubType, :UserHeaderIPFSPath, :PeerHeaderIPFSPath, :PublishedUTCDTS, :PriorIPFSPath, :Version)

-- name: insert_peer!
insert into Peer (PeerID, IPNSPath, VoluntaryBootStrap, FlagCID, PublishedUTCDTS, PriorIPFSPath, Version)
values (:PeerID, :IPNSPath, :VoluntaryBootStrap, :FlagCID, :PublishedUTCDTS, :PriorIPFSPath, :Version)

-- name: insert_user!
insert into User (FullName, Address, Website, Email, UserName, PublishedUTCDTS, PriorIPFSPath, Version)
values (:FullName, :Address, :Website, :Email, :UserName, :PublishedUTCDTS, :PriorIPFSPath, :Version)

-- name: insert_connected!
insert into connected (Addr, Peer)
values (:Addr, :Peer)

-- name: insert_WantList!
insert into WantList (Peer, CID)
values (:Peer, :CID)

-- name: pragma#
PRAGMA journal_mode = OFF;

-- name: clear_connected#
delete from connected;

-- name: clear_wantlist#
delete from WantList;

-- name: select_all
SELECT
   Addr, 
   Peer,
   CID
FROM
   connected c
INNER JOIN WantList w using(Peer) inner join BootStrap b using(Peer) inner join Peer p where w.CID = p.FlagCID;


-- name: create_schema#
CREATE TABLE "Network_Peers" (
	"PeerID"	TEXT,
	"IPNSPath"	TEXT,
	"AnnouncementIPFSPath"	TEXT,
   "SelfIndicator"  TEXT,
   "TableInsertDTS" TEXT,
   "PriorTableEntryIPFSPath" TEXT
);