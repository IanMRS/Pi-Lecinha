def count_date_occurrences(input_dict):
    date_count = {}
    
    for key, date_list in input_dict.items():
        for dates in date_list:
            for date in dates:
                if date in date_count:
                    date_count[date] += 1
                else:
                    date_count[date] = 1
    
    result_dict = {}
    for date, count in date_count.items():
        if count in result_dict:
            result_dict[count].append(date)
        else:
            result_dict[count] = [date]
    
    return result_dict

# Example usage
input_dict = {
    1: [['20231107', '20231108', '20231109', '20231110', '20231111', '20231112', '20231113', '20231114', '20231115', '20231116', '20231117', '20231118', '20231119', '20231120', '20231121', '20231122']],
    2: [['20231107', '20231108', '20231109', '20231110', '20231111', '20231112', '20231113', '20231114', '20231115', '20231116', '20231117', '20231118', '20231119', '20231120', '20231121', '20231122']],
    # Add more keys as needed
}

result = count_date_occurrences(input_dict)
print(result)
