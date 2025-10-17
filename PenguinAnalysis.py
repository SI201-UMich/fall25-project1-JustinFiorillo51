# Justin Fiorillo
# 77117441
# haoranlu@umich.edu
# collaborators: ChatGPT helped me form some of the functions 
import csv
import os
import unittest

def loadPenguins(f):
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, f)
    # use this 'full_path' variable as the file that you open
    penguins = {}
    with open(full_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            penguins[row[""]] = {
                "species": row["species"],
                "island": row["island"],
                "sex": row["sex"] if row["sex"] != "NA" else None,
                "bill_length_mm": row["bill_length_mm"],
                "bill_depth_mm": row["bill_depth_mm"],
                "flipper_length_mm": row["flipper_length_mm"],
                "body_mass_g": row["body_mass_g"],
                "year": row["year"]
            }
    return penguins

def highSpeciesCt(penguins):
    """Returns dict of {island: most common species}"""
    species_counts = {}

    for penguin in penguins.values():
        island = penguin["island"]
        species = penguin["species"]
        if island == "" or species == "":
            continue
        if island not in species_counts:
            species_counts[island] = []

        species_counts[island].append(species)

    popSpecies = {}
    for island in species_counts:
        sp_list = species_counts[island]
        total = len(sp_list)
        counts = {}
        for sp in sp_list:
            counts[sp] = counts.get(sp, 0) + 1

        most_common = None
        most_count = 0
        for sp in counts:
            if counts[sp] > most_count:
                most_common = sp
                most_count = counts[sp]

        percent = round((most_count / total) * 100, 1)
        popSpecies[island] = (most_common, percent)
    return popSpecies

def sexCt(penguins, popSpecies):
    """Returns dict {island: predominant sex of most common species}"""
    sexCount = {}
    for island in popSpecies:
        species, percent = popSpecies[island]
        counts = {}
        for penguin in penguins.values():
            if penguin["island"] == island and penguin["species"] == species:
                sex = penguin["sex"]
                if sex and sex != "NA": 
                    counts[sex] = counts.get(sex, 0) + 1
        if counts:
            max_sex = None
            max_count = 0
            for s in counts:
                if counts[s] > max_count:
                    max_sex = s
                    max_count = counts[s]
            sexCount[island] = max_sex
        else:
            sexCount[island] = None

    return sexCount

def generateReport(popSpecies, sexCount, out_file="penguin_report.txt"):
    """Writes results to a text file"""
    with open(out_file, "w") as f:
        f.write("Penguin Analysis Report\n")
        f.write("=======================\n\n")

        for island in popSpecies:
            species, percent = popSpecies[island]
            sex = sexCount[island]
            f.write("Island: " + island + "\n")
            f.write("  Most common species: " + species + " (" + str(percent) + "%)\n")
            f.write("  Predominant sex: " + str(sex) + "\n\n")

class Penguins(unittest.TestCase):
    def main():
        penguins = loadPenguins("penguins.csv")
        popSpecies = highSpeciesCt(penguins)
        sexCount = sexCt(penguins, popSpecies)
        generateReport(popSpecies, sexCount)

    if __name__ == "__main__":
        main()
    
    def setUp(self):
        self.fake_penguins = {
            "1": {"species": "Adelie", "island": "Torgersen", "sex": "male"},
            "2": {"species": "Adelie", "island": "Torgersen", "sex": "female"},
            "3": {"species": "Adelie", "island": "Torgersen", "sex": "female"},
            "4": {"species": "Gentoo", "island": "Biscoe", "sex": "male"},
            "5": {"species": "Gentoo", "island": "Biscoe", "sex": "male"},
            "6": {"species": "Chinstrap", "island": "Dream", "sex": None}
        }
    def test_highSpeciesCt_normal(self):
        result = highSpeciesCt(self.fake_penguins)
        self.assertEqual(result["Torgersen"][0], "Adelie")

    def test_highSpeciesCt_percent(self):
        result = highSpeciesCt(self.fake_penguins)
        species, percent = result["Torgersen"]
        self.assertAlmostEqual(percent, 100.0) 

    def test_highSpeciesCt_edge_empty(self):
        result = highSpeciesCt({})
        self.assertEqual(result, {})

    def test_highSpeciesCt_edge_missing_data(self):
        bad_data = {"1": {"species": "", "island": "", "sex": "male"}}
        result = highSpeciesCt(bad_data)
        self.assertEqual(result, {})

    def test_sexCt_normal(self):
        popSpecies = {"Torgersen": ("Adelie", 100.0)}
        result = sexCt(self.fake_penguins, popSpecies)
        self.assertEqual(result["Torgersen"], "female")  

    def test_sexCt_multiple_islands(self):
        popSpecies = {
            "Torgersen": ("Adelie", 100.0),
            "Biscoe": ("Gentoo", 100.0)
        }
        result = sexCt(self.fake_penguins, popSpecies)
        self.assertEqual(result["Biscoe"], "male")

    def test_sexCt_edge_no_sex_data(self):
        popSpecies = {"Dream": ("Chinstrap", 100.0)}
        result = sexCt(self.fake_penguins, popSpecies)
        self.assertIsNone(result["Dream"])

    def test_sexCt_edge_empty(self):
        result = sexCt({}, {})
        self.assertEqual(result, {})
