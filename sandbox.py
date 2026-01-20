# def jank(arg1 = 'dumb', arg2 = 'dumber', arg3 = 'dumbest'):
#     print("Hello World!")

# # jank()

# # *args lets you pass as many args as you want
# def jank2(*args):
#     for arg in args:
#         print(arg)

# # jank2('dumb', 'dumber', 'dumbest')

# def flick_switch(words):
#     flag = True
#     output = []
    
#     for word in words:
#         if 'flick' in word:
#             output.append(not flag)
#             flag = not flag
#         else:
#             output.append(flag)
            
#     return output

#     # flick_switch(['wank', 'flick', 'jank', 'bank'])

# # removes everything including and after the "#" symbol
# def remove_url_anchor(url):
#   return url.split('#')[0]