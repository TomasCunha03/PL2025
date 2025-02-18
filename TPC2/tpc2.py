import sys
import re

def extract_composers(lines):
    composer_pattern = re.compile(r'[^;]+;".*?";\d{4};[^;]+;([^;]+);')
    composers = []

    for line in lines:
        match = composer_pattern.search(line)
        if match:
            composers.append(match.group(1))

    return sorted(composers)

def works_by_period(lines):
    period_pattern = re.compile(r'[^;]+;".*?";\d{4};([^;]+);[^;]+;')
    period_distribution = {}

    for line in lines:
        match = period_pattern.search(line)
        if match:
            period = match.group(1)
            period_distribution[period] = period_distribution.get(period, 0) + 1

    return period_distribution

def period_to_titles(lines):
    title_pattern = re.compile(r'([^;]+);".*?";\d{4};([^;]+);[^;]+;')
    period_titles = {}

    for line in lines:
        match = title_pattern.search(line)
        if match:
            title = match.group(1)
            period = match.group(2)
            if period not in period_titles:
                period_titles[period] = []
            period_titles[period].append(title)

    for period in period_titles:
        period_titles[period] = sorted(period_titles[period])

    return period_titles

def process_csv(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    records = []
    temp_line = ""

    for line in lines[1:]:
        line = line.strip()
        if temp_line:
            temp_line += " " + line
        else:
            temp_line = line

        if re.search(r';O\d+$', temp_line):
            records.append(temp_line)
            temp_line = ""

    return records

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use: python music_processor.py C:/Users/tomas/Ambiente de Trabalho/PL2025")
        sys.exit(1)

    path = sys.argv[1]
    normalized_data = process_csv(path)

    print("1. lista ordenada de compositores:")
    print("2. distribuiçao de trabalhos por periodo:")
    print("3. dicionario com cada periodo associado a uma lista ordenada de titulos.")

    user_choice = input("escolhe: ")
    if user_choice == "1":
        composers = extract_composers(normalized_data)
        for composer in composers:
            print(composer)
    elif user_choice == "2":
        period_distribution = works_by_period(normalized_data)
        for period, count in period_distribution.items():
            print(f"{period}: {count}")
    elif user_choice == "3":
        period_titles = period_to_titles(normalized_data)
        for period, titles in period_titles.items():
            print(f"{period}: {titles}")
    else:
        print("invalido!")

