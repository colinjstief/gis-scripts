patcher( !CLASS_NAME! , !Impervious! , !Low_Vegetation! , !Forest! , !Barren! , !Water! )

def patcher(original, imp, low, forest, bar, wat):
  if wat == 1:
    return 1
  elif bar == 1:
    return 6
  elif forest == 1:
    return 3
  elif low == 1:
    return 5
  elif imp == 1:
    return 8
  else:
    if original == "Low Vegetation" or original == "Tilled Field" or original == "Extra Vegetation":
      return 5
    elif original == "Forest":
	  return 3
	elif original == "Impervious":
	  return 8
	else:
	  return 99 