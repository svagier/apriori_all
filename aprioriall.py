from itertools import combinations, product


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
                    element_with_list_of_occurrences = ((tuple_elem,), [subject_id])
                    candidate_set.append(element_with_list_of_occurrences)
                else:
                    index = unique_sequence_elements[tuple_elem]
                    if subject_id not in candidate_set[index][1]:
                        candidate_set[index][1].append(subject_id)
    number_of_subjects = len(dataset)
    return get_cs_with_support_from_occurrences(candidate_set, number_of_subjects)


def get_frequent_set(candidate_sets: [], min_support: float) -> {}:
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
    all_comb = list(all_combinations)
    for elem in all_comb:
        candidate = concat_tuples(elem)
        occurrences = get_occurrences_of_sequence(original_dataset, candidate)
        candidate_set.append((candidate, occurrences/number_of_subjects))
    return candidate_set


def concat_tuples(all_tuples: tuple) -> tuple:
    new_tuple = ()
    for elem in all_tuples:
        new_tuple += elem
    return new_tuple


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


def map_frequent_sets(frequent_datasets: []) -> []:
    mapped = []
    mapping_id = 1
    for frequent_set in frequent_datasets:
        for frequent_sequence in frequent_set:
            # (sequence, support, mapping_id)
            mapped.append((frequent_sequence[0], frequent_sequence[1], mapping_id))
            mapping_id += 1
    return mapped


def get_transformed_original_dataset(dataset: [], mapped_frequent_sets: []) -> []:
    transformed = []
    for record in dataset:
        transactions = record[1]
        all_transaction_combinations = []
        for sequence in transactions:
            sequence_list = [x for x, in sequence]
            sequence_combinations = []
            for x in range(1, len(sequence_list) + 1):
                sequence_combinations += list(combinations(sequence_list, x))
            all_transaction_combinations.append(sequence_combinations)
        transformed.append(map_transformed_sequence(all_transaction_combinations, mapped_frequent_sets))
    return transformed


def map_transformed_sequence(potential_sequences: [], mapped_frequent_sequences: []) -> []:
    final_sequences = []
    for list_of_sequences in potential_sequences:
        transformed_sequence = ()
        for seq in list_of_sequences:
            for elem in mapped_frequent_sequences:
                if elem[0] == seq:
                    transformed_sequence += (elem[2],)
        if len(transformed_sequence):
            final_sequences.append(transformed_sequence)
    return final_sequences


def sequencing_create_candidate_set(transformed_original_dataset:[], mapped_frequent_sequences: [], cs_seq_size: int) -> []:
    frequent_sequences_list = [x[2] for x in mapped_frequent_sequences]
    print("frequent_sequences_list", frequent_sequences_list)
    all_combinations_with_repeat = list(product(frequent_sequences_list, repeat=cs_seq_size))
    print("All combinations with repeat", all_combinations_with_repeat)
    print("transformed roiginal", transformed_original_dataset)
    sequencing_cs = []
    number_of_subjects = len(transformed_original_dataset)
    for combination in all_combinations_with_repeat:
        print("--------- checked ombination -----", combination)
        number_of_occurrences = 0
        for record in transformed_original_dataset:
            index = 0
            print("record", record)
            for sequence in record:
                print("sequence", sequence)
                for elem in sequence:
                    print("elem:", elem)
                    if combination[index] == elem:
                        index += 1
                        break
                if index == len(combination):
                    number_of_occurrences += 1
                    break
        sequencing_cs.append((combination, number_of_occurrences/number_of_subjects))
    return sequencing_cs


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

    # dataset = [
    #     ("105", [(30,), (90,)]),
    #     ("106", [(10, 20), (30,), (40, 60, 70)]),
    #     ("200", [(30, 50, 70)]),
    #     ("220", [(30,), (40, 60), (90,)]),
    #     ("300", [(90,)]),
    # ]

    min_sup = 0.25

    print("Original dataset:\n", dataset)

    initial_candidate_set = get_initial_cs(dataset)
    print("\nInitial candidate set:", initial_candidate_set)
    fs_1 = get_frequent_set(initial_candidate_set, min_sup)
    print("\nFrequent set 1: ", fs_1)
    cs_2 = create_candidate_set(dataset, fs_1, 2)
    print("\nCandidate set 2: ", cs_2)
    fs_2 = get_frequent_set(cs_2, min_sup)
    print("\nFrequent set 2: ", fs_2)
    all_frequent_sets = [fs_1, fs_2]
    mapped_frequent_sets = map_frequent_sets(all_frequent_sets)
    print("Mapped frequent sets", mapped_frequent_sets)
    transformed_original_dataset = get_transformed_original_dataset(dataset, mapped_frequent_sets)
    print("Transformed original dataset:", transformed_original_dataset)
    sequencing_cs_2 = sequencing_create_candidate_set(transformed_original_dataset, mapped_frequent_sets, 2)
    print("Sequenced candidate set 2:", sequencing_cs_2)


if __name__ == '__main__':
    main()
