import pandas as pd
import path
import SourceCode.utils as u


def convert_to_set(col):

    event_set = set()
    for i in col:
        event_set.add(i)
    return event_set

def probable_relevant_story(news, event_set, threshold):
    tokenized = news.split(" ")
    count = 0
    for t in tokenized:
        if t in event_set:
            count += 1
        if count >= threshold:
            return True
    return False


if __name__ == "__main__":

    source_data_path = path.MASTER
    event_path = path.TAGTOG_POST_ANNOTATION
    destination_data_path = path.TAGTOG_PRE_ANNOTATION

    action_file = path.ACTION
    source_file = path.FROM_2011To2015

    path_name = source_data_path + source_file
    action_path = event_path + action_file


    master_data = pd.read_csv(path_name, header=[0])
    master_data = u.remove_special_characters(master_data, 'news')

    actions = pd.read_csv(action_path, header=[0])
    actions_set = convert_to_set(actions.iloc[:, 0])


    # Step - 1 : Pull Out All the Probable relevant story
    master_data['Relevance'] = master_data['news'].apply(probable_relevant_story, args = (actions_set, 4))
    print(master_data[master_data['Relevance'] == True].shape)

    master_data.to_csv(destination_data_path+'master_2011to2015_probable_relevant_marked_data.csv', header=True, index=True, index_label='index')
