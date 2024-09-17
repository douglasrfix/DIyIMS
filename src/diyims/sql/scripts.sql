
-- name: create_schema#
CREATE TABLE "header_table" (
	"version" TEXT,
	"object_CID"	TEXT,
	"object_type"	TEXT,
	"insert_DTS"	TEXT,
	"prior_header_CID"	TEXT,
	'header_CID' TEXT
);

CREATE TABLE "peer_table" (
	"version" TEXT,
	"peer_ID"	TEXT UNIQUE,
	"IPNS_name"	TEXT
);

CREATE TABLE "network_table" (
	"version" TEXT,
	"network_name"	TEXT
);

-- name: insert_peer_row!
insert into peer_table (version, peer_ID, IPNS_name)
values (:version, :peer_ID, :IPNS_name);

-- name: insert_header_row!
insert into header_table (version, object_CID, object_type, insert_DTS,
	 prior_header_CID, header_CID)
values (:version, :object_CID, :object_type, :insert_DTS,
	 :prior_header_CID, :header_CID);

-- name: insert_network_row!
insert into network_table (version, network_name)
values (:version, :network_name);

-- name: select_last_header^
SELECT
 	version,
   	object_CID,
   	object_type,
   	insert_DTS,
   	prior_header_CID,
   	header_CID

FROM
   header_table

ORDER BY

	insert_DTS DESC
;

-- name: select_network_name^
SELECT
 	version,
   	network_name

FROM
   network_table

;


-- name: commit!
commit;
