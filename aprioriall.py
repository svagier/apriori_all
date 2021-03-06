from itertools import combinations, product


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


def sequencing_create_initial_candidate_set(transformed_original_dataset: [], mapped_frequent_sequences: [], cs_seq_size: int) -> []:
    frequent_sequences_list = [x[2] for x in mapped_frequent_sequences]
    all_combinations_with_repeat = list(product(frequent_sequences_list, repeat=cs_seq_size))
    sequencing_cs = []
    number_of_subjects = len(transformed_original_dataset)
    for combination in all_combinations_with_repeat:
        number_of_occurrences = 0
        for record in transformed_original_dataset:
            index = 0
            for sequence in record:
                for elem in sequence:
                    if combination[index] == elem:
                        index += 1
                        break
                if index == len(combination):
                    number_of_occurrences += 1
                    break
        sequencing_cs.append((combination, number_of_occurrences/number_of_subjects))
    return sequencing_cs


def sequencing_get_frequent_set(sequencing_candidate_set: [], min_support: float) -> []:
    sequencing_fs = []
    for sequence_tuple in sequencing_candidate_set:
        if sequence_tuple[1] >= min_support:
            sequencing_fs.append(sequence_tuple)
    return sequencing_fs


def sequencing_create_candidate_set(transformed_original_dataset: [], previous_frequent_set: [], cs_seq_size: int) -> []:
    # get unique values from last positions from sequences in previous_frequent_set:
    last_position_values = []
    previous_frequent_set_sequences = []
    for seq in previous_frequent_set:
        previous_frequent_set_sequences.append(seq[0])
        if seq[0][cs_seq_size-2] not in last_position_values:
            last_position_values.append((seq[0][-1],))
    possibilities = []
    for seq in previous_frequent_set_sequences:
        for last_value in last_position_values:
            tup = seq + last_value
            possibilities.append(tup)
    sequencing_cs = []
    for possibility in possibilities:
        all_combinations = list(combinations(possibility, cs_seq_size-1))
        occurrences_in_previous_fs = 0
        for comb in all_combinations:
            if comb not in previous_frequent_set_sequences:
                break
            else:
                occurrences_in_previous_fs += 1
        if occurrences_in_previous_fs == cs_seq_size:
            sequencing_cs.append(possibility)

    number_of_subjects = len(transformed_original_dataset)
    sequencing_cs_with_sup = []
    # get support:
    for candidate in sequencing_cs:
        number_of_occurrences = 0
        for record in transformed_original_dataset:
            index = 0
            for sequence in record:
                for elem in sequence:
                    if candidate[index] == elem:
                        index += 1
                        break
                if index == len(candidate):
                    number_of_occurrences += 1
                    break
        sequencing_cs_with_sup.append((candidate, number_of_occurrences/number_of_subjects))

    return sequencing_cs_with_sup


def print_line_by_line(list_to_be_printed: []):
    if len(list_to_be_printed):
        for line in list_to_be_printed:
            print(line)
    else:
        print("Empty")


def apriori_all(dataset: [], min_sup: float):
    print("Original dataset:")
    print_line_by_line(dataset)
    candidate_set = get_initial_cs(dataset)
    print("\nInitial candidate set 1 (with support):")
    print_line_by_line(candidate_set)
    all_frequent_sets = []
    counter = 1
    while len(candidate_set):
        frequent_set = get_frequent_set(candidate_set, min_sup)
        print("\nFrequent set {} (with support):".format(counter))
        print_line_by_line(frequent_set)
        if len(frequent_set):
            all_frequent_sets.append(frequent_set)
            counter += 1
            candidate_set = create_candidate_set(dataset, frequent_set, counter)
            print("\nCandidate set {} (with support):".format(counter))
            print_line_by_line(candidate_set)
            if not len(candidate_set):
                counter -= 1        # this may happen only once
        else:
            break

    # Mapping:
    mapped_frequent_sets = map_frequent_sets(all_frequent_sets)
    print("\nMapped frequent sets (with support and new mapped value):")
    print_line_by_line(mapped_frequent_sets)

    # Transforming:
    transformed_original_dataset = get_transformed_original_dataset(dataset, mapped_frequent_sets)
    print("\nTransformed original dataset:")
    print_line_by_line(transformed_original_dataset)

    # Sequencing:
    sequencing_candidate_set = sequencing_create_initial_candidate_set(transformed_original_dataset, mapped_frequent_sets, counter)
    sequencing_frequent_set = ['initial_value (will be overwritten during first iteration']
    while len(sequencing_candidate_set) and len(sequencing_frequent_set):
        sequencing_frequent_set = sequencing_get_frequent_set(sequencing_candidate_set, min_sup)
        print("\nSequenced frequent set {} (with support):".format(counter))
        print_line_by_line(sequencing_frequent_set)
        if len(sequencing_frequent_set):
            counter += 1
            sequencing_candidate_set = sequencing_create_candidate_set(transformed_original_dataset, sequencing_frequent_set, 3)
            print("\nSequenced candidate set {} (with support):".format(counter))
            print_line_by_line(sequencing_candidate_set)
            if not len(sequencing_candidate_set):
                print("------ Sequenced candidate set {} is empty. Algorithm is ending. ------".format(counter))
                return
        else:
            print("------ Sequenced frequent set {} is empty. Algorithm is ending. ------".format(counter))
            return


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
    apriori_all(dataset, min_sup)


if __name__ == '__main__':
    main()
