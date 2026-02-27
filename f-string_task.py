def format_number(num):
    return f"{f'{num:,.3f}'.replace(',', ' ').replace('.', ' .'):*^30}"

print(format_number(123488482390.28174))