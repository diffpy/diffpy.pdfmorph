from matplotlib import rc_params_from_file

#this script is for printing the bg_mpl_stylesheet as a python dictionary.
bg_mpl_style = rc_params_from_file("bg_mpl_stylesheet", use_default_template=False)
print(dict(bg_mpl_style))