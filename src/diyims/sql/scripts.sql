
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
	"peer_ID"	TEXT,
	"IPNS_name"	TEXT,
	"peer_type" TEXT,
	"origin_update_DTS"	TEXT,
	"local_update_DTS" TEXT,
	"execution_platform"	TEXT,
	"python_version"	TEXT,
	"IPFS_agent"	TEXT,
	"processing_status" TEXT,
	"agent" TEXT,
	"version"	TEXT,
	PRIMARY KEY("peer_ID")
);

CREATE TABLE "want_list_table" (
	"peer_ID"	TEXT,
	"object_CID" TEXT,
	"insert_DTS"	TEXT,
	"last_update_DTS" TEXT,
	"insert_update_delta" INTEGER,
	"source_peer_type"	TEXT,
	PRIMARY KEY("peer_ID", "object_CID")
);

CREATE TABLE "network_table" (
	"network_name"	TEXT
);

-- name: set_pragma#
PRAGMA journal_mode = WAL
;
-- name: insert_peer_row!
insert into peer_table (peer_ID, IPNS_name, peer_type, origin_update_DTS, local_update_DTS, execution_platform, python_version,
		IPFS_agent, processing_status, agent, version)
values (:peer_ID, :IPNS_name, :peer_type, :origin_update_DTS, :local_update_DTS, :execution_platform, :python_version,
		:IPFS_agent, :processing_status, :agent, :version);

-- name: update_peer_table_peer_type_status!
update peer_table set peer_type = :peer_type, processing_status = :processing_status, local_update_DTS = :local_update_DTS
where peer_ID = :peer_ID

-- name: update_peer_table_status!
update peer_table set processing_status = :processing_status
where peer_ID = :peer_ID

-- name: reset_peer_table_status#
update peer_table set processing_status = "WLR"
where processing_status  = "WLX" or processing_status = "WLP"

-- name: select_peers_by_peer_type_status
SELECT
	peer_ID,
	IPNS_name,
	peer_type,
   	origin_update_DTS,
	local_update_DTS,
   	execution_platform,
	python_version,
   	IPFS_agent,
	processing_status,
	agent,
 	version

FROM
   peer_table

where peer_type = :peer_type and (processing_status = "WLR" or processing_status = "ADR")

-- name: select_peer_table_entry_by_key^
SELECT
	peer_ID,
	IPNS_name,
	peer_type,
   	origin_update_DTS,
	local_update_DTS,
   	execution_platform,
	python_version,
   	IPFS_agent,
	processing_status,
	agent,
 	version

FROM
   peer_table

where peer_ID = :peer_ID

-- name: insert_header_row!
insert into header_table (version, object_CID, object_type, insert_DTS,
	 prior_header_CID, header_CID)
values (:version, :object_CID, :object_type, :insert_DTS,
	 :prior_header_CID, :header_CID);

-- name: insert_want_list_row!
insert into want_list_table (peer_ID, object_CID, insert_DTS, last_update_DTS, insert_update_delta, source_peer_type)
values (:peer_ID, :object_CID, :insert_DTS, :last_update_DTS,
 :insert_update_delta, :source_peer_type);

-- name: update_last_update_DTS!
update want_list_table set last_update_DTS = :last_update_DTS,
 insert_update_delta = :insert_update_delta
where peer_ID = :peer_ID and object_CID = :object_CID



-- name: insert_network_row!
insert into network_table (network_name)
values (:network_name);

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

-- name: select_last_peer_table_entry_pointer^
SELECT
 	version,
   	object_CID,
   	object_type,
   	insert_DTS,
   	prior_header_CID,
   	header_CID

FROM
   header_table

WHERE object_type = "peer_table_entry"

ORDER BY

	insert_DTS DESC
;

-- name: select_all_headers
SELECT
 	version,
   	object_CID,
   	object_type,
   	insert_DTS,
   	prior_header_CID,
   	header_CID

FROM
   header_table

;

-- name: select_network_name^
SELECT
   	network_name

FROM
   network_table

;




-- name: select_want_list_entry_by_key^
select peer_ID, object_CID, insert_DTS, last_update_DTS, insert_update_delta, source_peer_type
from want_list_table
where peer_ID = :peer_ID and object_CID = :object_CID
