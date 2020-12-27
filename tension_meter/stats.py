def show_results(codes):
    print('\n\n==========================\nResponses by status code:\n')
    for code, count in codes.items():
        print(f'{code}: {count} times\n==========================\n')
