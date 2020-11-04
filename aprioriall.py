from itertools import combinations

def conver_init_dataset_dict_to_list(initial_dataset_dict: {}) -> []:
    list_dataset = []
    for sublist in initial_dataset_dict.keys():
        list_dataset.append(sublist)
    return list_dataset


def get_cs_with_support_from_occurrences(candidate_set_list: [], number_of_subjects: int) -> []:       # 'cs' stands for 'candidate set'
    candidate_set_with_support = []
    for cs_tuple in candidate_set_list:
        support = len(cs_tuple[1]) / number_of_subjects
        candidate_set_with_support.append((cs_tuple[0], support))
    return candidate_set_with_support


def get_initial_cs(dataset: []) -> []:                                   # 'cs' stands for 'candidate set'
    candidate_set = []
    unique_sequence_elements = {}
    unique_element_index = 0
    for subject_data in dataset:
        sequence = subject_data[1]
        for subtuple in sequence:
            for tuple_elem in subtuple:
                subject_id = subject_data[0]
                if tuple_elem not in unique_sequence_elements.keys():
                    unique_sequence_elements[tuple_elem] = unique_element_index
                    unique_element_index += 1
                    element_with_list_of_occurrences = (tuple_elem, [subject_id])
                    candidate_set.append(element_with_list_of_occurrences)
                else:
                    index = unique_sequence_elements[tuple_elem]
                    if subject_id not in candidate_set[index][1]:
                        candidate_set[index][1].append(subject_id)
    number_of_subjects = len(dataset)
    return get_cs_with_support_from_occurrences(candidate_set, number_of_subjects)


def get_frequent_set(candidate_sets: [], min_support: int) -> {}:
    frequent_sets = []
    for cs in candidate_sets:
        if cs[1] >= min_support:
            frequent_sets.append((cs[0], cs[1]))
    return frequent_sets


def get_elements_in_order(input_set: []) -> []:
    list_of_elements = []
    for element in input_set:
        list_of_elements.append(element[0])
    return list_of_elements


def create_candidate_set(original_dataset: [], freqeunt_sets: [], cs_seq_size: int):
    list_of_elements = get_elements_in_order(freqeunt_sets)
    all_combinations = combinations(list_of_elements, cs_seq_size)
    candidate_set = []
    number_of_subjects = len(original_dataset)
    for elem in list(all_combinations):
        occurrences = get_occurrences_of_sequence(original_dataset, elem)
        candidate_set.append((elem, occurrences/number_of_subjects))
    return candidate_set


def get_occurrences_of_sequence(original_dataset: [], checked_sequence: ()) -> []:
    len_checked_sequence = len(checked_sequence)
    occurrences = 0
    for subject_data in original_dataset:
        sequences = subject_data[1]
        for seq in sequences:
            if len(seq) >= len_checked_sequence:
                index = 0
                for element in seq:
                    if element == checked_sequence[index]:
                        index += 1
                if index == len_checked_sequence:       # the sequence has been found
                    occurrences += 1
                    break
    return occurrences


def main():
    """ dataset's elements are tuples, where first index of tuple is id of subject (e.g. id of client), and second index
    is list of sequences, where each sequence is a tuple.
        Example of one line (record for one subject)
        (subject_id, [(sequence_element,), (sequence_element, sequence_element, sequence_element), ... ])
    """
    dataset = [
                ("1", [('A',), ('A',)]),
                ("2", [('A',), ('B',), ('C', 'E')]),
                ("3", [('A', 'E')]),
                ("4", [('A',), ('C', 'D', 'E'), ('A',)]),
                ("5", [('A',)])
    ]

    min_sup = 0.25

    initial_candidate_set = get_initial_cs(dataset)
    print(initial_candidate_set)
    fs_1 = get_frequent_set(initial_candidate_set, min_sup)
    print(fs_1)
    cs_2 = create_candidate_set(dataset, fs_1, 2)
    print(cs_2)

if __name__ == '__main__':
    main()
