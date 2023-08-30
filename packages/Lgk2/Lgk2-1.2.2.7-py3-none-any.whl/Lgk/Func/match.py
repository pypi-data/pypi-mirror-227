def detect(args="", value="", percent=80):
    matching_count = sum(1 for a, v in zip(args, value) if a == v)
    min_matching_count = max(len(args), len(value)) * (percent / 100)
    
    return matching_count >= min_matching_count


def match(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)
    
    matrix = [[0] * (len_str2 + 1) for _ in range(len_str1 + 1)]
    
    for i in range(len_str1 + 1):
        for j in range(len_str2 + 1):
            if i == 0 or j == 0:
                matrix[i][j] = 0
            elif str1[i - 1] == str2[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1] + 1
            else:
                matrix[i][j] = max(matrix[i - 1][j], matrix[i][j - 1])
    
    return matrix[len_str1][len_str2] / max(len_str1, len_str2)


