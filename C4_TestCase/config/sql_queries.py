# sql_queries.py
#查询商机编号
GET_OPPORTUNITY_NUM_QUERY = "SELECT opportunity_num FROM opportunity.g_opportunity WHERE opportunity_name LIKE %s"
