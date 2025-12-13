with open('input.txt', 'r') as f:
    data = [range(int(r.split('-')[0]), int(r.split('-')[1]) + 1) for r in f.read().split(',')]

print(data)

sum_of_invalid_ids = 0

for r in data:
    for id_to_check in r:
        if (len_id_to_check := (len(str_id_to_check := (str(id_to_check))))) % 2:
            continue
        if str_id_to_check[:len_id_to_check//2] == str_id_to_check[len_id_to_check//2:]:
            sum_of_invalid_ids += id_to_check


print(sum_of_invalid_ids)

sum_of_invalid_ids = 0

for r in data:
    for id_to_check in r:
        len_id_to_check = len(str_id_to_check := (str(id_to_check)))
        for teiler in range(2, len_id_to_check + 1):
            if len_id_to_check % teiler:
                continue
            chunk_size = len_id_to_check // teiler
            different_chunks = {str_id_to_check[i:i+chunk_size] for i in range(0, len_id_to_check, chunk_size)}
            if len(different_chunks) == 1:
                sum_of_invalid_ids += id_to_check
                break


print(sum_of_invalid_ids)