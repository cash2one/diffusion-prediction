# -*-coding:utf-8-*-

ES_FLOW_TEXT_PORT = ["219.224.134.216:9201", "219.224.134.217:9201"]
ES_BE_RETWEET_PORT = ["219.224.134.216:9201", "219.224.134.217:9201"]
ES_PREDICTION_PORT = ["219.224.134.216:9202"]

REDIS_HOST = "219.224.134.213"
REDIS_PORT = "7371"

pre_flow_text = "flow_text_"
type_flow_text = "text"

index_be_retweet = "1225_be_retweet_1"
index_type_be_retweet = "user"

# the minimal prediction time
minimal_time_interval = 3600 

# the minimal prediction size
K = 12

# micro prediction data organization order
data_order = ["total_fans_number", "origin_weibo_number", "retweeted_weibo_number", "comment_weibo_number",\
        "positive_weibo_number", "neutral_weibo_number", "negetive_weibo_number", "origin_important_user_number", \
        "origin_important_user_retweet", "retweet_important_user_count", "retweet_important_user_retweet", \
        "total_count", "average_origin_imp_hour", "average_retweet_imp_hour"]

# prediction task manage index
index_manage_prediction_task = "manage_prediction_task"
type_manage_prediction_task = "prediction_task"


# detail prediction task
index_type_prediction_task = "micro_task"

# task_list scan text
task_scan_text = "task_scan_text"
type_macro_feature_result = "macro_feature_result"

