def is_loc_max_or_end(index,lista):
    if index==0:
        return False
    if index==len(lista)-1:
        return False
    if lista[index]>lista[index-1] and lista[index]>lista[index+1]:
        return True
    return False
