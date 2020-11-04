def get_cs_with_support_from_occurrences(dictionary_candidate_set: {}, number_of_subjects: int) -> {}:       # 'cs' stands for 'candidate set'
    candidate_set_with_support = {}
    for key, value in dictionary_candidate_set.items():
        support = len(value['occurred_in']) / number_of_subjects
        candidate_set_with_support[key] = {'support': support}
    return candidate_set_with_support


def get_initial_cs(dictionary_dataset: {}) -> {}:                                   # 'cs' stands for 'candidate set'
    candidate_set = {}
    for key, sequence in dictionary_dataset.items():
        for subtuple in sequence:
            for tuple_elem in subtuple:
                if tuple_elem not in candidate_set.keys():
                    candidate_set[tuple_elem] = {'occurred_in': [key]}
                else:
                    if key not in candidate_set[tuple_elem]['occurred_in']:
                        candidate_set[tuple_elem]['occurred_in'].append(key)
    number_of_subjects = len(dictionary_dataset.keys())
    return get_cs_with_support_from_occurrences(candidate_set, number_of_subjects)


def main():
    """ dataset's elements are in format:
        subject_id: [(sequence_element,), (sequence_element, sequence_element, sequence_element), ... ]
    """
    dataset = {
        "1": [('A',), ('A',)],
        "2": [('A',), ('B',), ('C', 'E')],
        "3": [('A', 'E')],
        "4": [('A',), ('C', 'D', 'E'), ('A',)],
        "5": [('A',)]
    }

    min_sup = 0.25

    initial_candidate_set = get_initial_cs(dataset)
    print(initial_candidate_set)


if __name__ == '__main__':
    main()
