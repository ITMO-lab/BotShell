import pkgutil
search_path = ['.']
all_modules = [x[1] for x in pkgutil.iter_modules(path=search_path)]
print(all_modules)
