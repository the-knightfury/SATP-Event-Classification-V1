import requests
import json
import pandas as pd
import credentials

def get_id(url, project, folder):
    auth = requests.auth.HTTPBasicAuth(username=credentials.USERNAME, password=credentials.PASSWORD)
    params = {'project':project, 'owner': credentials.USERNAME, 'search':folder, 'page':'1', 'output':'csv'}
    response = requests.get(url, params=params, auth=auth)
    # json_data = json.loads(response.text)
    print(response.text)
    file = open("tagtog/id_content.txt", "w")
    file.write(response.text)
    file.close()


def read_text():
    with open('tagtog/id_content.txt') as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    content = [i.split(',')[0] for i in content]
    return content

# Getting the Is-Relevant label
def get_label(url, project, folder, id, label_list):
    auth = requests.auth.HTTPBasicAuth(username=credentials.USERNAME, password=credentials.PASSWORD)
    params = {'project': project, 'owner': credentials.USERNAME, 'search': folder, 'page': '1',
              'output': 'ann.json',
              'ids': id}
    response = requests.get(url, params=params, auth=auth)
    print(response.text)
    json_data = json.loads(response.text)
    print(json_data)
    label_list.append(json_data["metas"]['m_1']['value'])

# change to 9 and 1 for the Annotators one and master one should be 11 and 3
def text_process(text, id_list, country, year):
    for j in range(9):
        val = text.partition(' ')
        text = val[2]
        if j == 1:
            id_list.append(int(val[0]))
        if j == 7:
            country.append((val[0]))
        if j == 3:
            year.append(int(val[0]))
    return text

# Getting the text
def get_text(url,project, folder, id, text_list, id_list, country, year):

    auth = requests.auth.HTTPBasicAuth(username=credentials.USERNAME, password=credentials.PASSWORD)
    params = {'project': project, 'owner': credentials.USERNAME, 'search': folder, 'page': '1', 'output': 'text',
              'ids': id}
    response = requests.get(url, params=params, auth=auth)
    # print(response.text)
    if response.text:
        text_val = text_process(response.text, id_list, country, year)
        text_list.append(text_val)
    else:
        text_list.append(None)

# Get JSON file
def get_json(url, id, project):
    auth = requests.auth.HTTPBasicAuth(username=credentials.USERNAME, password=credentials.PASSWORD)
    params = {'project': project, 'owner': credentials.USERNAME, 'search': 'folder:pool/Practice', 'page': '1',
              'output': 'ann.json',
              'ids': id}
    response = requests.get(url, params=params, auth=auth)
    json_data = json.loads(response.text)

    return json_data

def get_target(data, class_id , particular_list, event_type, flag):
    size = len(data)
    tmp = []
    tmp_type = []
    for i in range(size):
        if data[i]['classId'] == class_id:
            size_val = len(data[i]['offsets'])
            for j in range(size_val):
                tmp.append(data[i]['offsets'][j]['text'])
            # change the name of the flag variable
            if flag != None:
                if flag in data[i]['fields'].keys():
                    tmp_type.append(data[i]['fields'][flag]['value'])
                else:
                    tmp_type.append("NotSpecified")
                    # tmp_type.append("MissingActionTypeLabel")


    if len(tmp) == 0:
        particular_list.append(None)
        if flag != None:
            event_type.append(None)
    else:
        particular_list.append(tmp)
        if flag != None:
            event_type.append(tmp_type)


def get_data(url, id, project , targets, texts, events, actors, types, id_list, dates, locations, sat_events, country, year, relevance):
    json = get_json(url, id, project)
    # print(json)
    # events = [is_relevant[0], source[1], target[2], action[3], action_type[4], location[5], date[6]]
    get_text(url, project, 'folder:pool/Practice', id, texts, id_list, country, year)
    if json["anncomplete"] == True and (sat_events[0] in json["metas"].keys()) and json["metas"][sat_events[0]]['value'] == True:
        relevance.append(True)
        #get_text(url, project, 'folder:pool', id, texts, id_list)
        data = json['entities']
        #print(data)

        # Target - 1
        class_id = sat_events[2]
        get_target(data, class_id, targets, types, None)

        # Action - 1
        class_id = sat_events[3]
        get_target(data, class_id, events, types, sat_events[4])
        #
        # # Source - 1
        class_id = sat_events[1]
        get_target(data, class_id, actors, types, None)

        # # Date - 1
        class_id = sat_events[6]
        get_target(data, class_id, dates, types, None)

        # # Location - 1
        class_id = sat_events[5]
        get_target(data, class_id, locations, types, None)

    else:
        relevance.append(False)
        targets.append(None)
        events.append(None)
        source.append(None)
        dates.append(None)
        locations.append(None)
        types.append(None)



tagtogAPIUrl = "https://www.tagtog.net/-api/documents/v1"
p_id = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9']
p = 'p9'
project = ['demo', 'satp_news_data_500_'+ p]
folder = ['folder:pool/Practice', 'folder:pool']
# [is_relevant, source, target, action, action_type, location, date]
events_p1 = ["m_19", "e_20", "e_26", "e_23", "f_16", "e_29", "e_32"]
events_p2 = ["m_1", "e_2", "e_8", "e_5", "f_17", "e_11", "e_14"]
events_p3 = ["m_1", "e_2", "e_8", "e_5", "f_17", "e_11", "e_14"]

# 1 - Karina
# 2 - Karla
# 3 - Jenniye
# 4 - Shahreen

text_list = []
id_list = []
label_list = []
target_list = []
source = []
action = []
type_list = []
dates = []
locations = []
country = []
year = []
relevance = []

get_id(tagtogAPIUrl, project[1], folder[1])
doc_id = read_text()
print(len(doc_id))
# get_data(tagtogAPIUrl, doc_id[4], project[1] , target_list, text_list, action, source, type_list, id_list, dates, locations, events_p2, country, year)
# print(text_list)

for i in range(1, len(doc_id)):
    id = doc_id[i]
    print(id)
    get_data(tagtogAPIUrl, id , project[1], target_list, text_list, action, source, type_list, id_list, dates,
             locations, events_p2, country, year, relevance)

print(country)
print(year)
dict = {'id':id_list, 'is_relevant':relevance, 'target':target_list, 'source': source, 'action':action, 'action_type' : type_list, 'location':locations, 'date':dates,'country':country, 'year':year, 'news':text_list}
df = pd.DataFrame(dict)
print(df)
df.to_csv('Data_TagTog_Annotated/'+p+'.csv', header=True, index=False)


###############################################################################################################################################
###############################################################################################################################################

# for i in range(len(doc_id)):
#     id = doc_id[i]
#     print(id)
#     get_label(tagtogAPIUrl, project[0], folder[0], id, label_list)
#     get_text(tagtogAPIUrl, project[0], folder[0], id, text_list, id_list)


# dict = {'id':id_list, 'master':label_list, 'news':text_list}
# df = pd.DataFrame(dict)
# df.to_csv('tagtog/data_csv/master.csv', header=True, index=False)

