from random import randint

# Starting 2018 to 2024 (7 years)
images_per_year = [77, 0, 0, 0, 0, 0, 0]

# 20 images per year (140 total)
chosen_per_year = 20

def get_random_image_index(year):
    year -= 2018

    if images_per_year[year] < chosen_per_year:
        print("Not enough images to satisfy method requirements")
        return

    to_select_from = list(range(1, images_per_year[year]))

    chosen = []
    while len(chosen) < chosen_per_year:
        random_image_index = to_select_from[randint(0, images_per_year[year] - 1)]

        if random_image_index not in chosen:
            chosen.append(random_image_index)
    
    chosen.sort()
    return chosen

images = get_random_image_index(2018)
print(images)
