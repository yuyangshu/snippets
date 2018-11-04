import pickle
import scipy.spatial
import matplotlib.pyplot as plt

suburbs = ['Alexandria', 'Ashfield', 'Auburn', 'Avalon Beach', 'Balgowlah', 'Balmain', 'Bankstown', 'Baulkham Hills', 'Bellevue Hill', 'Belmore', 'Bexley', 'Blacktown', 'Bondi', 'Bondi Beach', 'Botany', 'Burwood', 'Cabramatta', 'Camperdown', 'Campsie', 'Caringbah', 'Carlingford', 'Carlton', 'Castle Hill', 'Chatswood', 'Cherrybrook', 'Coogee', 'Cranebrook', 'Cremorne', 'Cronulla', 'Crows Nest', 'Darlinghurst', 'Dee Why', 'Drummoyne', 'Dulwich Hill', 'Earlwood', 'Eastwood', 'Elizabeth Bay', 'Engadine', 'Epping', 'Fairfield', 'Freshwater', 'Gladesville', 'Glebe', 'Glenmore Park', 'Glenwood', 'Granville', 'Greenacre', 'Greystanes', 'Guildford', 'Gymea', 'Haymarket', 'Homebush West', 'Hornsby', 'Hurstville', 'Ingleburn', 'Kellyville', 'Kellyville Ridge', 'Killara', 'Kingsford', 'Kirrawee', 'Kogarah', 'Lakemba', 'Lane Cove', 'Lane Cove North', 'Leichhardt', 'Lidcombe', 'Liverpool', 'Macquarie Fields', 'Manly', 'Maroubra', 'Marrickville', 'Marsfield', 'Mascot', 'Merrylands', 'Miranda', 'Mona Vale', 'Mortdale', 'Mosman', 'Mount Annan', 'Mount Druitt', 'Narrabeen', 'Neutral Bay', 'Newtown', 'North Parramatta', 'North Sydney', 'Northmead', 'Paddington', 'Padstow', 'Panania', 'Parramatta', 'Penrith', 'Penshurst', 'Potts Point', 'Prestons', 'Punchbowl', 'Pyrmont', 'Quakers Hill', 'Randwick', 'Redfern', 'Revesby', 'Rhodes', 'Rockdale', 'Rooty Hill', 'Rose Bay', 'Rozelle', 'Ryde', 'Sans Souci', 'Seven Hills', 'South Hurstville', 'St Clair', 'St Helens Park', 'St Ives', 'St Leonards', 'St Marys', 'Stanhope Gardens', 'Strathfield', 'Surry Hills', 'Sutherland', 'Sydney', 'Toongabbie', 'Turramurra', 'Wahroonga', 'Waterloo', 'Wentworth Point', 'West Pennant Hills', 'West Ryde', 'Westmead', 'Wiley Park', 'Winston Hills', 'Woollahra', 'Yagoona']

with open("suburbs_geolocations", 'rb') as f:
    dictionary = pickle.load(f)

coordinates = []
for item in suburbs:
    coordinates.append((dictionary[item][2], dictionary[item][1]))

voronoi = scipy.spatial.Voronoi(coordinates)

scipy.spatial.voronoi_plot_2d(voronoi)
plt.show()