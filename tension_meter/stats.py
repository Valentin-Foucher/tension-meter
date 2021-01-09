def show_results(codes):
    """
    Callback called on user interruption
    :param codes: dict with code as key and the amount found as value
    """
    print('\n\n==========================\nResponses by status code:\n')
    for code, count in codes.items():
        print(f'{code}: {count} times\n==========================\n')
