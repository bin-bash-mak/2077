import itertools
from typing import List, Generator


def merge_sequences(sequences: List[List[str]]) -> List[str]:
    """Merge a list of sequences into a single sequence.

    If two consecutive sequences have matching elements at the junction,
    it ensures that the duplicate is not repeated in the merged result.

    Args:
        sequences (List[List[str]]): A list of sequences to merge.

    Returns:
        List[str]: The merged sequence.
    """
    if not sequences:
        return []
    result: List[str] = sequences[0].copy()
    for arr in sequences[1:]:
        if arr and result and result[-1] == arr[0]:
            result.extend(arr[1:])
        else:
            result.extend(arr)
    return result


def generate_merged_combinations(
    sequences: List[List[str]], buffer_size: int
) -> Generator[List[str], None, None]:
    """Generate all possible combinations of sequences by merging them.

    Args:
        sequences (List[List[str]]): A list of sequences to combine.
        buffer_size (int): The maximum length of the merged sequence.

    Yields:
        List[str]: A merged sequence of the given sequences.
    """
    for number_of_sequences in range(len(sequences), 0, -1):
        for permutation in itertools.permutations(sequences, number_of_sequences):
            if len(merged := merge_sequences(permutation)) <= buffer_size:
                yield merged


def check_solution(
    matrix: List[List[str]],
    path: List[str],
    buffer_size: int,
    moves: List[tuple[int, int]] = None,
):
    """Check if a given path is a valid solution for a given matrix.

    Args:
        matrix (List[List[str]]): The matrix to check the path against.
        path (List[str]): The path to check.
        buffer_size (int): The size of the buffer.
        moves (List[tuple[int, int]], optional): The moves made so far. Defaults to None.

    Returns:
        List[tuple[int, int]]: The moves that lead to the solution if it is valid, None otherwise.
    """
    if moves is None:
        moves = []

    if len(moves) == len(path):
        return moves

    if len(moves) > len(path):
        return None

    is_row = len(moves) % 2 == 0

    current = 0 if len(moves) == 0 else moves[-1][0 if is_row else 1]
    # value of indeces taken

    taken = [i[0 if not is_row else 1] for i in moves]

    ps = matrix[current] if is_row else [i[current] for i in matrix]

    for i, c in enumerate(ps):
        if i not in taken and c == path[len(moves)]:
            t = moves.copy()
            t.append([current, i] if is_row else [i, current])
            if s := check_solution(matrix, path, buffer_size, moves=t):
                return s


def solve(matrix: List[List[str]], sequences: List[List[str]], buffer_size: int):
    """Solve the puzzle by finding a path in the matrix that matches one of the given sequences.

    Args:
        matrix (List[List[str]]): The matrix to search in.
        sequences (List[List[str]]): The sequences to search for.
        buffer_size (int): The size of the buffer.

    Returns:
        List[tuple[int, int]]: The moves that lead to a solution if one exists, None otherwise.
    """
    for perm in generate_merged_combinations(sequences, buffer_size):
        print(perm)
        if s := check_solution(matrix, perm, buffer_size):
            return s


if __name__ == "__main__":
    sequences = [["55", "BD", "1C"], ["7A", "55", "1C"], ["1C", "E9", "7A"]]
    sequences.reverse()
    matrix = [
        ["55", "FF", "1C", "BD", "1C", "BD", "7A"],
        ["7A", "BD", "55", "55", "55", "1C", "55"],
        ["55", "BD", "BD", "55", "FF", "1C", "55"],
        ["7A", "E9", "FF", "55", "55", "1C", "FF"],
        ["7A", "7A", "55", "1C", "FF", "55", "1C"],
        ["BD", "55", "55", "7A", "1C", "BD", "55"],
        ["1C", "55", "55", "1C", "BD", "1C", "7A"],
    ]
    buffer_size: int = 8
    print(solve(matrix, sequences, buffer_size))
