import sys
import csv
import SimpleITK as sitk
import pathlib

names = [
    "Abel^Randi",
    "Ahmed^Sehrrish",
    "Alasa^Esther",
    "Aluqdah^Fahima",
    "Assali^Said",
    "Awolu^Oluwatomilola",
    "BLAND^ANA^C",
    "Baran^Christina",
    "Baraniuk^Svetlana",
    "Batchelder^Stephen",
    "Begala^Grace",
    "Blaylock^Ashlyn",
    "Bowen^Spencer",
    "Brawner^Emily",
    "Cantu^Jorge",
    "Carr^Adam",
    "Chan^Katrina",
    "Chavez^Megan",
    "Coleman^Reed",
    "Dang^Hy",
    "Diaz^David",
    "Diaz^Samuel",
    "Dutschmann^Elle",
    "Espinoza^Alejandra",
    "Estimbo^Carlos",
    "Farhoud^Fatmeh",
    "Farrar^Jioia",
    "Fessler^Emily",
    "Franco^Jonathan",
    "Garza^Daphne",
    "Gleckler^Stephen",
    "Gutierrez^Ramon",
    "Hall^Domanique",
    "Hernandez^Ian",
    "Hojabri^Arhalan",
    "Hudzietz^Sophie",
    "Jarratt^Darby",
    "Jimenez^Enrique",
    "Kennedy^Jacob",
    "Kermanshahani^Shaya",
    "Khan^Mafaz",
    "Kotarba^Rylee",
    "Krolczyk^Erica",
    "Land^Jamaine",
    "Liggett^Max",
    "Lopez^Carlos",
    "Lopez^Celene",
    "Lopez^Jesse",
    "Luna^Carreno^Andrew",
    "Maddox^Joshua",
    "Theall^Mark",
    "Mark^Ethen",
    "Marshburn^Saige",
    "Martinez^Roland",
    "Mickelson^Garrett",
    "Mollai^Isabella",
    "Moreno^Ana",
    "Navas^Santiago",
    "Neidhardt^Lance",
    "Nguyen^Alexandria",
    "Nguyen^Adam",
    "Nowak^Julia",
    "OBERG^JOHN",
    "Ortega^Marina",
    "Perez^Sofia",
    "Pollard^Holli",
    "Powell^John",
    "Price^Emily^D",
    "Pylate^Kara",
    "Quintero^Andrew",
    "Razo^Victoria",
    "Reisig^John",
    "Rendon^Chelsea",
    "Ritter^Sophie",
    "Roach^Kristiana",
    "Roberts^Sarah",
    "Rodriguez^Stephanie",
    "ROSS^LISA^MARIE",
    "Ryan^Edwin",
    "Guerroro-Sanche^Jennifer",
    "Sapon^Sarah",
    "Schuster^Sarah",
    "Scott^Orynthea",
    "Shields^Sheryl",
    "Sloan^Keyandria",
    "Smith^Britton",
    "Thornsberry^Anna",
    "Trujillo^Jordan",
    "Vanarsdale^Brooks^R",
    "Vasquez^Darlene",
    "Vasquez^Emily^Michell",
    "Ventura^Patrick",
    "Walker^Catherine",
    "Woll^Leora",
    "Yanes^Abner",
    "Zeller^Santiago",
    "Zuniga^Jorge^A",
    "Arambula^Lauren ",
    "Azua^Sofia ",
    "Stevens^Wyatt",
    "Tran^My",
    "Perry^Owen",
]

result = {}
p = pathlib.Path('X:')
with open('temp.csv', 'w') as sys.stdout:
    for file in p.glob('**/0000.dcm'):

        try:
            file_reader = sitk.ImageFileReader()
            file_reader.SetImageIO('GDCMImageIO')
            file_reader.SetFileName(str(file))
            file_reader.LoadPrivateTagsOn()
            file_reader.ReadImageInformation()
            info = {k: file_reader.GetMetaData(k) for k in file_reader.GetMetaDataKeys()}
        except:
            continue

        if '0010|0010' in info:
            
            name = info['0010|0010'].strip()
            race = ''
            if '0010|2160' in info:
                race = info['0010|2160'].strip()

            print(f'{name},{race},{file}')

            if name and race:
                if name in result:
                    if race != result[name]:
                        print(f"* check {name}")
                elif name in names:
                    result[name] = race


with open('result.csv', 'w', newline='') as f:
    csv.writer(f).writerows(result.items())

