from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from pprint import pprint
import json


def get_matched_name(name :str, name_type: str, data = list()):
    """This function takes a string as input and returns 
    the maximum matching string extracted from `data`.
    
    `data` contains whole JSON file, saved globaly.

    Args:
        name (str): The name of the procedure
        name_type (str): Wather name is city or day

    Returns:
        _type_: `None` if the matching proportion is less than 60,
                    Otherwise, the `str` name with the maximum matching ratio.
    """

    if name_type == "city":
        # Reading the Cities files as list
        with open("CitiesList490.txt", encoding='UTF-8') as file:
            for val in file.readlines():
                data.append(val.strip())
    else:
        # Reading the Days files as list
        with open("DaysList.txt", encoding='UTF-8') as file:
            for val in file.readlines():
                data.append(val.strip())
    
    
    if name == None:   return None, 0
    
    # Finding the only one string with maximum matching ratio and 
    # its matching ratio all available strings
    sentence, matching_ratio = process.extractOne(name, data, scorer=fuzz.token_sort_ratio)
    
    if matching_ratio >= 60:
        return sentence, matching_ratio
    else:
        print("Got word:", sentence, matching_ratio)
        # return None
        return sentence, matching_ratio


if __name__ == "__main__":
    print(get_matched_name("سومو", "day"))
    print(get_matched_name("passport", "day"))

    # str_list = ['Joe Biden', 'Joseph Biden', 'Joseph R Biden']

    # match_ratios = process.extract('joe r biden', str_list, scorer=fuzz.token_sort_ratio)
    # print(match_ratios)

    # best_match = process.extractOne('', str_list, scorer=fuzz.token_sort_ratio)
    # print(best_match)

