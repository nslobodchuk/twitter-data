with open("output.csv") as output, open("output_first_1000_lines.csv", "w+") as output_1000:
    count = -1
    for line in output:
        count += 1
        if count >= 1000:
            break
        output_1000.write(line)
