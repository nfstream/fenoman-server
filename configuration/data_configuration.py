#TEST_DATAFRAME = '../../data/comnet14-flows-labeled.csv'
TEST_DATAFRAME = './data/X_scaled-labeled.csv'
DROP_VARIABLES = ['id']
TARGET_VARIABLE = 'application_name'
TRAIN_VALIDATION_SPLIT = 0.2

# X_scaled has only 1 column that needs to be dropped
"""DROP_VARIABLES = ['id', 'application_category_name', 'application_is_guessed', 'application_confidence',
                  'requested_server_name', 'client_fingerprint', 'server_fingerprint', 'user_agent', 'content_type',
                  'src_ip', 'src_mac', 'dst_ip', 'dst_mac', 'src_oui', 'dst_oui', 'ip_version', 'vlan_id', 'tunnel_id',
                  'src_port', 'dst_port',
                  'splt_direction', 'splt_ps', 'splt_piat_ms']"""