# -*- coding: utf-8 -*-
'''
from user_portrait.global_config import db,es_user_profile,profile_index_name,profile_index_type
from user_portrait.info_consume.model import CityTopicCount,CityWeibos,ProvinceWeibos
import math
import json
#from socialconsume.global_config import db
#from socialconsume.model import CityTopicCount, CityWeibos
'''
import sys
import json
import math
reload(sys)
sys.path.append('../../')
from diffusion_prediction.global_config import index_event_analysis_results,type_event_analysis_results
from diffusion_prediction.global_utils import es_prediction as es
from diffusion_prediction.global_utils import es_user_portrait,profile_index_name,profile_index_type


Minute = 60
Fifteenminutes = 15 * Minute
Hour = 3600
SixHour = Hour * 6
Day = Hour * 24
MinInterval = Fifteenminutes

def _json_loads(weibos):
    try:
        return json.loads(weibos)
    except ValueError:
        if isinstance(weibos, unicode):
            return json.loads(json.dumps(weibos))
        else:
            return None

'''
def province_weibo_count(topic,start_ts,end_ts,unit=MinInterval):
    province = {}
    if (end_ts - start_ts < unit):
        upbound = long(math.ceil(end_ts / (unit * 1.0)) * unit)
        items = db.session.query(CityTopicCount).filter(CityTopicCount.end==upbound, \
                                                       CityTopicCount.topic==topic).all()
        # if item:
        #     print item[0]
        #     geo = _json_loads(item[0].ccount)
        #     print geo
    else:
        upbound = long(math.ceil(end_ts / (unit * 1.0)) * unit)

        lowbound = long((start_ts / unit) * unit)
        items = db.session.query(CityTopicCount).filter(CityTopicCount.end>lowbound, \
                                                         CityTopicCount.end<=upbound, \
                                                         CityTopicCount.topic==topic).all()
    count_dict = {}
    for item in items:          
        geo = _json_loads(item.ccount)
        print geo
        for province,city_dict in geo.iteritems():
            #count_dict[province] = city_dict
            for k,v in city_dict.iteritems():
                if k == 'total':
                    continue
                #print k.encode('utf8'),v
                try:
                    count_dict[province]['total'] += v
                except:
                    count_dict[province] = {'total':v}
                try:
                    count_dict[province][k] += v
                except:
                    count_dict[province][k] = v
            #jln  all citys without province
            # for k,v in city_dict.iteritems():
            #     print k.encode('utf8'),v
            #     if k == 'total':
            #         continue                
            #     try:
            #         count_dict[k] += v
            #     except:
            #         count_dict[k] = v

            # try:
            #     province_dict[k] += v['total']
            # except:
            #     province_dict[k] = v['total']
    #print province_dict
    results = sorted(count_dict.iteritems(),key=lambda x:x[1]['total'],reverse=True)
    #print results
    return results
'''

def province_weibo_count_es(topic,start_ts,end_ts,unit=MinInterval):

    geo_count_results = {}
    geo_results_dict = {}
    
    query_body = {
        'query':{
            'term':{'en_name':topic}
        }
    }

    es_results = es.search(index=index_event_analysis_results,doc_type=type_event_analysis_results,\
                            body=query_body)['hits']['hits']
    print 'len:::::::::',len(es_results)
    for es_result in es_results:
        geo_results = es_result['_source']['geo_results']
        geo_results_dict = json.loads(geo_results)
        
        #sort_ts_attr = geo_results_dict['sort_ts_attr']
        #repost_list = geo_results_dict['repost_list']
        geo_cityTopic_results = geo_results_dict['geo_cityTopic_results']
        geo_cityCount = geo_cityTopic_results['geo_cityCount']


    #print 'geo_cityTopic_results[]:::::::::::',geo_cityTopic_results['geo_cityCount']
    '''
    if (end_ts - start_ts < unit):
        upbound = long(math.ceil(end_ts / (unit * 1.0)) * unit)

        mtype_count_results[upbound] = {}

        for key,value in counts.iteritems():
            if key == upbound:
                for k,v in value.iteritems():
                    try:
                        mtype_count_results[upbound][k] += v
                    except:
                        mtype_count_results[upbound][k] = v

    else:
        upbound = long(math.ceil(end_ts / (unit * 1.0)) * unit)
        lowbound = long((start_ts / unit) * unit)
        interval = (upbound-lowbound)/unit
        for i in range(interval, 0, -1):    
            begin_ts = upbound - unit * i
            end_ts = begin_ts + unit
            mtype_count_results[end_ts] = {}
            
            for key,value in counts.iteritems():
                if key > begin_ts and key <= end_ts:
                    for k,v in value.iteritems():
                        try:
                            mtype_count_results[end_ts][k] += v
                        except:
                            mtype_count_results[end_ts][k] = v
    '''        
    #return  geo_count_results
    return geo_cityCount



def city_weibo_count(topic,start_ts,end_ts,province,unit=MinInterval):
    city = {}
    if (end_ts - start_ts < unit):
        upbound = long(math.ceil(end_ts / (unit * 1.0)) * unit)
        items = db.session.query(CityTopicCount).filter(CityTopicCount.end==upbound, \
                                                       CityTopicCount.topic==topic).all()
    else:
        upbound = long(math.ceil(end_ts / (unit * 1.0)) * unit)

        lowbound = long((start_ts / unit) * unit)
        items = db.session.query(CityTopicCount).filter(CityTopicCount.end>lowbound, \
                                                         CityTopicCount.end<=upbound, \
                                                         CityTopicCount.topic==topic).all()
    city_dict = {}
    for item in items:          
        geo = _json_loads(item.ccount)
        try:
            citys = geo[province]
            for k,v in geo[province].iteritems():
                try:
                    city_dict[k] += v
                except:
                    city_dict[k] = v
        except:
            continue            

    print city_dict
    results = sorted(city_dict.iteritems(),key=lambda x:x[1],reverse=True)
    #print results
    return results

def get_weibo_content_es(topic,start_ts,end_ts,province,sort_item='timestamp',unit=Fifteenminutes):
    
    weibo_dict = {}

    query_body = {
        'query':{
            'term':{'en_name':topic}
        }
    }

    es_results = es.search(index=index_event_analysis_results,doc_type=type_event_analysis_results,\
                            body=query_body)['hits']['hits']


    for es_result in es_results: 
        geo_results = es_result['_source']['geo_results']
        geo_results_dict = json.loads(geo_results)
        
        #sort_ts_attr = geo_results_dict['sort_ts_attr']
        #repost_list = geo_results_dict['repost_list']
        geo_cityTopic_results = geo_results_dict['geo_cityTopic_results']
        geo_weibos = geo_cityTopic_results['geo_weibos']

        #geo_weibos = _json_loads(geo_weibos)
    for end_ts,type_dict in geo_weibos.iteritems():
        for weibo_type,geo_weibo_list in type_dict.iteritems():
            for geo_weibo in geo_weibo_list:
                end_ts = geo_weibo[0]
                province_weibo = geo_weibo[1]
                city = geo_weibo[2]
                weibo = geo_weibo[3]
                #print 'weibo::::::::::::::::::',weibo
                if province_weibo == province:
                    weibo_content = {}
                    weibo_content['text'] = weibo['_source']['text'] 
                    weibo_content['uid'] = weibo['_source']['uid']
                    weibo_content['timestamp'] = weibo['_source']['timestamp']
                    weibo_content['sentiment'] = weibo['_source']['sentiment'] 
                    weibo_content['comment'] = weibo['_source']['comment']
                    weibo_content['retweeted'] = weibo['_source']['retweeted']
                    weibo_content['keywords'] = weibo['_source']['keywords_dict']
                    weibo_content['mid'] = weibo['_source']['mid']
                    try:
                        user = es_user_portrait.get(index=profile_index_name,doc_type=profile_index_type,id=weibo_content['uid'])['_source']
                        weibo_content['uname'] = user['nick_name']
                        weibo_content['photo_url'] = user['photo_url']
                    except:
                        weibo_content['uname'] = 'unknown'
                        weibo_content['photo_url'] = 'unknown'
                    weibo_dict[weibo_content['mid']] = weibo_content
    try:
        results = sorted(weibo_dict.items(),key=lambda x:x[1][sort_item],reverse=True)
    except:
        results = []
    #print results
    return results

'''
def get_weibo_content(topic,start_ts,end_ts,province,sort_item='timestamp',unit=Fifteenminutes):
    city = {}
    #print province.encode('utf8')
    # item = db.session.query(ProvinceWeibos).filter(ProvinceWeibos.end == 1468495800).all()
    # for i in item:
    #     print i.province.encode('utf8')  ###结果是unicode
    if (end_ts - start_ts < unit):
        upbound = long(math.ceil(end_ts / (unit * 1.0)) * unit)
        items = db.session.query(ProvinceWeibos).filter(ProvinceWeibos.end==upbound, \
                                                        ProvinceWeibos.province == province,\
                                                       ProvinceWeibos.topic==topic).all()
    else:
        upbound = long(math.ceil(end_ts / (unit * 1.0)) * unit)

        lowbound = long((start_ts / unit) * unit)
        items = db.session.query(ProvinceWeibos).filter(ProvinceWeibos.end>lowbound, \
                                                         ProvinceWeibos.end<=upbound, \
                                                        ProvinceWeibos.province == province,\
                                                         ProvinceWeibos.topic==topic).all()
    weibo_dict = {}
    for item in items: 
        weibo = _json_loads(item.weibos)
        #for weibo in weibos:
        weibo_content = {}
        weibo_content['text'] = weibo['_source']['text'] 
        weibo_content['uid'] = weibo['_source']['uid']
        weibo_content['timestamp'] = weibo['_source']['timestamp']
        weibo_content['sentiment'] = weibo['_source']['sentiment'] 
        weibo_content['comment'] = weibo['_source']['comment']
        weibo_content['retweeted'] = weibo['_source']['retweeted']
        weibo_content['keywords'] = weibo['_source']['keywords_dict']
        weibo_content['mid'] = weibo['_source']['mid']
        try:
            user = es_user_profile.get(index=profile_index_name,doc_type=profile_index_type,id=weibo_content['uid'])['_source']
            weibo_content['uname'] = user['nick_name']
            weibo_content['photo_url'] = user['photo_url']
        except:
            weibo_content['uname'] = 'unknown'
            weibo_content['photo_url'] = 'unknown'
        weibo_dict[weibo_content['mid']] = weibo_content
    results = sorted(weibo_dict.items(),key=lambda x:x[1][sort_item],reverse=True)
    #print results
    return results
'''

   
    #results = sorted(city_dict.iteritems(),key=lambda x:x[1],reverse=True)
    #print results
    #return results


if __name__ == '__main__':
    #all_weibo_count('aoyunhui',1468166400,1468170900)
    #get_weibo_content('aoyunhui',1468167300,1468167300,u'陕西')
    print get_weibo_content_es('mao_ze_dong_dan_chen_ji_nian_ri',1482681600,1483113600,u'北京',sort_item='timestamp',unit=Fifteenminutes)

    #province_weibo_count_es('mao_ze_dong_dan_chen_ji_nian_ri',1482681600,1483113600,unit=MinInterval)
