import argparse

# ----------------------------------------------------------------------------# 
# --------------------             Constants              --------------------# 
# ----------------------------------------------------------------------------# 

N_SPACES_TO_TAB = 4
SPACE_TAB = " " * N_SPACES_TO_TAB

# ----------------------------------------------------------------------------# 
# --------------------          Helper Functions          --------------------# 
# ----------------------------------------------------------------------------# 


def titleize(title: str):
    """ """
    return " ".join([token[0].upper() + token[1:] for token in title.split(" ")])


def create_section_text(section_title, n_width = 80):
    """ """

    assert n_width >= 40

    decorator ="# "
    blank_lines = decorator + "-" * (n_width - 4) + decorator

    inner_size = n_width - len(section_title) - 4
    bar_delta = inner_size - len(section_title) - 2

    n_bars = 20
    if bar_delta < 2 * n_bars:
        n_bars = max(1, bar_delta // 2)

    n_spaces = max(inner_size // 2 - n_bars, 1)
    bars = "-" * n_bars 
    spaces = " " * n_spaces
    odd_space = " " * (len(section_title) % 2)
    title_line = decorator + bars + spaces + titleize(section_title) + spaces + odd_space + bars + decorator

    return [blank_lines, title_line, blank_lines]

def write_code(code, filename):
    """ """
    with open(filename, "w") as file:
        file.write(code)


# ----------------------------------------------------------------------------# 
# ----------------           Pretty Core Functions            ----------------# 
# ----------------------------------------------------------------------------# 

def add_double_lines(new_code):
    """ """
    line = new_code[-1]

    double_line_start_tokens = ["def ", "class ", "if __name__ == '__main__':"]

    if any(line.startswith(token) for token in double_line_start_tokens):        
        non_empty_line_index = 2 # includes def statements
        while (new_code[-non_empty_line_index].strip() == ""):
            non_empty_line_index += 1

        non_empty_line_index -= 1
        new_code = new_code[:-non_empty_line_index] + ["", ""] + new_code[-1:]

    return new_code

def tabs_to_spaces(new_code):
    """ """
    if new_code[-1].startswith("\t"):
        n_tabs = new_code[-1].count("\t") - new_code[-1].lstrip("\t").count("\t")
        new_code[-1] = SPACE_TAB * n_tabs + new_code[-1].lstrip("\t")

    return new_code

def comment_after_function(new_code, ntabs=1):
    """ """
    prev_line, line = new_code[-2:]
    if prev_line.startswith("def ") and prev_line.endswith("):"):
        if not line.strip().startswith('"""'):
            new_code = new_code[:-2]
            new_code.extend([prev_line, SPACE_TAB * ntabs + '""" """', line])

    return new_code

def detect_open_function(new_code):
    """ """
    open_def = False
    for line in new_code:
        pass
    ## end function

def replace_sections(new_code):
    """ """
    line, new_code = new_code[-1], new_code[:-1]
    if line.lower().lstrip("# ").startswith("\section"):
        section_title = line.split("section", maxsplit=1)[1].strip()
        new_code.extend(create_section_text(section_title))
    else:
        new_code.append(line)

    if all(line_i.startswith("# -") for line_i in new_code[-3:]):
        section_title = new_code[-2].strip("# -")
        clean_section = create_section_text(section_title)
        new_code[-3:] = clean_section

    return new_code


#\section Pretty Up Core

def run_pretty_up_core(o_code):
    """ """

    new_code = ["", ""]
    for i, line in enumerate(o_code.split("\n")):
        new_code.append(line)
        new_code = replace_sections(new_code)
        new_code = comment_after_function(new_code)
        new_code = tabs_to_spaces(new_code)
        new_code = add_double_lines(new_code)

    return "\n".join(new_code).strip() + "\n"


def pretty_up(file_path: str):
    """ """
    assert file_path.endswith(".py")
    
    with open(file_path, "r") as file:
        original_code = file.read()

    new_code = run_pretty_up_core(original_code)
    write_code(new_code, file_path)


# ----------------------------------------------------------------------------# 
# --------------------                Main                --------------------# 
# ----------------------------------------------------------------------------# 


def get_arguments():
    """ """
    parser = argparse.ArgumentParser(prog='pretty-up-code', description='Makes code prettier')
    parser.add_argument('-i', "--input", dest='inputs', action="extend", nargs="+", type=str,
                        required=True, help="Input files")

    return parser.parse_args()


def main():
    """ """
    args = get_arguments()

    print("Making code pretty:")
    for input in args.inputs:
        print(f"\t - {input}")
        pretty_up(input)

if __name__ == '__main__':
    main()


# ----------------------------------------------------------------------------# 
# --------------------                End                 --------------------# 
# ----------------------------------------------------------------------------#
