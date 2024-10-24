
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
	"source_peer_type"	TEXT
);

CREATE TABLE "network_table" (
	"network_name"	TEXT
);

-- name: insert_peer_row!
insert into peer_table (peer_ID, IPNS_name, origin_update_DTS, local_update_DTS, execution_platform, python_version,
		IPFS_agent, processing_status, agent, version)
values (:peer_ID, :IPNS_name, :origin_update_DTS, :local_update_DTS, :execution_platform, :python_version,
		:IPFS_agent, :processing_status, :agent, :version);

-- name: insert_header_row!
insert into header_table (version, object_CID, object_type, insert_DTS,
	 prior_header_CID, header_CID)
values (:version, :object_CID, :object_type, :insert_DTS,
	 :prior_header_CID, :header_CID);

-- name: insert_want_list_row!
insert into want_list_table (peer_ID, object_CID, insert_DTS, source_peer_type)
values (:peer_ID, :object_CID, :insert_DTS, :source_peer_type);

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

-- name: select_last_peer_table_entry_header^
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

-- name: select_remote_peers
SELECT
	peer_ID,
	IPNS_name,
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

WHERE processing_status = "NP"
