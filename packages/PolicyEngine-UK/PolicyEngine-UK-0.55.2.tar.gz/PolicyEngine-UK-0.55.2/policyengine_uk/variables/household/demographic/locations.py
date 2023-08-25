from policyengine_uk.model_api import *


class BRMAName(Enum):
    ASHFORD = "Ashford"
    AYLESBURY = "Aylesbury"
    BARNSLEY = "Barnsley"
    BARROW_IN_FURNESS = "Barrow-in-Furness"
    BASINGSTOKE = "Basingstoke"
    BATH = "Bath"
    BEDFORD = "Bedford"
    BIRMINGHAM = "Birmingham"
    BLACK_COUNTRY = "Black Country"
    BLACKWATER_VALLEY = "Blackwater Valley"
    BOLTON_AND_BURY = "Bolton and Bury"
    BOURNEMOUTH = "Bournemouth"
    BRADFORD_SOUTH_DALES = "Bradford & South Dales"
    BRIGHTON_AND_HOVE = "Brighton and Hove"
    BRISTOL = "Bristol"
    BURY_ST_EDMUNDS = "Bury St Edmunds"
    CAMBRIDGE = "Cambridge"
    CANTERBURY = "Canterbury"
    CENTRAL_GREATER_MANCHESTER = "Central Greater Manchester"
    CENTRAL_LANCS = "Central Lancs"
    CENTRAL_LONDON = "Central London"
    CENTRAL_NORFOLK_NORWICH = "Central Norfolk & Norwich"
    CHELMSFORD = "Chelmsford"
    CHELTENHAM = "Cheltenham"
    CHERWELL_VALLEY = "Cherwell Valley"
    CHESTERFIELD = "Chesterfield"
    CHICHESTER = "Chichester"
    CHILTERNS = "Chilterns"
    COLCHESTER = "Colchester"
    COVENTRY = "Coventry"
    CRAWLEY_REIGATE = "Crawley & Reigate"
    DARLINGTON = "Darlington"
    DERBY = "Derby"
    DONCASTER = "Doncaster"
    DOVER_SHEPWAY = "Dover-Shepway"
    DURHAM = "Durham"
    EAST_CHESHIRE = "East Cheshire"
    EAST_LANCS = "East Lancs"
    EAST_THAMES_VALLEY = "East Thames Valley"
    EASTBOURNE = "Eastbourne"
    EASTERN_STAFFORDSHIRE = "Eastern Staffordshire"
    EXETER = "Exeter"
    FYLDE_COAST = "Fylde Coast"
    GLOUCESTER = "Gloucester"
    GRANTHAM_NEWARK = "Grantham & Newark"
    GREATER_LIVERPOOL = "Greater Liverpool"
    GRIMSBY = "Grimsby"
    GUILDFORD = "Guildford"
    HALIFAX = "Halifax"
    HARLOW_STORTFORD = "Harlow & Stortford"
    HARROGATE = "Harrogate"
    HEREFORDSHIRE = "Herefordshire"
    HIGH_WEALD = "High Weald"
    HULL_EAST_RIDING = "Hull & East Riding"
    HUNTINGDON = "Huntingdon"
    INNER_EAST_LONDON = "Inner East London"
    INNER_NORTH_LONDON = "Inner North London"
    INNER_SOUTH_EAST_LONDON = "Inner South East London"
    INNER_SOUTH_WEST_LONDON = "Inner South West London"
    INNER_WEST_LONDON = "Inner West London"
    IPSWICH = "Ipswich"
    ISLE_OF_WIGHT = "Isle of Wight"
    KENDAL = "Kendal"
    KERNOW_WEST = "Kernow West"
    KINGS_LYNN = "Kings Lynn"
    KIRKLEES = "Kirklees"
    LANCASTER = "Lancaster"
    LEEDS = "Leeds"
    LEICESTER = "Leicester"
    LINCOLN = "Lincoln"
    LINCOLNSHIRE_FENS = "Lincolnshire Fens"
    LOWESTOFT_GREAT_YARMOUTH = "Lowestoft & Great Yarmouth"
    LUTON = "Luton"
    MAIDSTONE = "Maidstone"
    MEDWAY_SWALE = "Medway & Swale"
    MENDIP = "Mendip"
    MID_EAST_DEVON = "Mid & East Devon"
    MID_WEST_DORSET = "Mid & West Dorset"
    MID_STAFFS = "Mid Staffs"
    MILTON_KEYNES = "Milton Keynes"
    NEWBURY = "Newbury"
    NORTH_CHESHIRE = "North Cheshire"
    NORTH_CORNWALL_DEVON_BORDERS = "North Cornwall & Devon Borders"
    NORTH_CUMBRIA = "North Cumbria"
    NORTH_DEVON = "North Devon"
    NORTH_NOTTINGHAM = "North Nottingham"
    NORTH_WEST_KENT = "North West Kent"
    NORTH_WEST_LONDON = "North West London"
    NORTHAMPTON = "Northampton"
    NORTHANTS_CENTRAL = "Northants Central"
    NORTHUMBERLAND = "Northumberland"
    NOTTINGHAM = "Nottingham"
    OLDHAM_ROCHDALE = "Oldham & Rochdale"
    OUTER_EAST_LONDON = "Outer East London"
    OUTER_NORTH_EAST_LONDON = "Outer North East London"
    OUTER_NORTH_LONDON = "Outer North London"
    OUTER_SOUTH_EAST_LONDON = "Outer South East London"
    OUTER_SOUTH_LONDON = "Outer South London"
    OUTER_SOUTH_WEST_LONDON = "Outer South West London"
    OUTER_WEST_LONDON = "Outer West London"
    OXFORD = "Oxford"
    PEAKS_DALES = "Peaks & Dales"
    PETERBOROUGH = "Peterborough"
    PLYMOUTH = "Plymouth"
    PORTSMOUTH = "Portsmouth"
    READING = "Reading"
    RICHMOND_HAMBLETON = "Richmond & Hambleton"
    ROTHERHAM = "Rotherham"
    RUGBY_EAST = "Rugby & East"
    SALISBURY = "Salisbury"
    SCARBOROUGH = "Scarborough"
    SCUNTHORPE = "Scunthorpe"
    SHEFFIELD = "Sheffield"
    SHROPSHIRE = "Shropshire"
    SOLIHULL = "Solihull"
    SOUTH_CHESHIRE = "South Cheshire"
    SOUTH_DEVON = "South Devon"
    SOUTH_EAST_HERTS = "South East Herts"
    SOUTH_WEST_ESSEX = "South West Essex"
    SOUTH_WEST_HERTS = "South West Herts"
    SOUTHAMPTON = "Southampton"
    SOUTHEND = "Southend"
    SOUTHERN_GREATER_MANCHESTER = "Southern Greater Manchester"
    SOUTHPORT = "Southport"
    ST_HELENS = "St Helens"
    STAFFORDSHIRE_NORTH = "Staffordshire North"
    STEVENAGE_NORTH_HERTS = "Stevenage & North Herts"
    SUNDERLAND = "Sunderland"
    SUSSEX_EAST = "Sussex East"
    SWINDON = "Swindon"
    TAMESIDE_GLOSSOP = "Tameside & Glossop"
    TAUNTON_WEST_SOMERSET = "Taunton & West Somerset"
    TEESSIDE = "Teesside"
    THANET = "Thanet"
    TYNESIDE = "Tyneside"
    WAKEFIELD = "Wakefield"
    WALTON = "Walton"
    WARWICKSHIRE_SOUTH = "Warwickshire South"
    WEST_CHESHIRE = "West Cheshire"
    WEST_CUMBRIA = "West Cumbria"
    WEST_PENNINE = "West Pennine"
    WEST_WILTSHIRE = "West Wiltshire"
    WESTON_S_MARE = "Weston-S-Mare"
    WIGAN = "Wigan"
    WINCHESTER = "Winchester"
    WIRRAL = "Wirral"
    WOLDS_AND_COAST = "Wolds and Coast"
    WORCESTER_NORTH = "Worcester North"
    WORCESTER_SOUTH = "Worcester South"
    WORTHING = "Worthing"
    YEOVIL = "Yeovil"
    YORK = "York"
    # Northern Ireland
    BELFAST = "Belfast"
    LOUGH_NEAGH_LOWER = "Lough Neagh Lower"
    LOUGH_NEAGH_UPPER = "Lough Neagh Upper"
    NORTH = "North (NI)"
    NORTH_WEST = "North West (NI)"
    SOUTH = "South (NI)"
    SOUTH_EAST = "South East (NI)"
    SOUTH_WEST = "South West (NI)"


class LocalAuthority(Enum):
    ABERDEEN_CITY = "Aberdeen City"
    ABERDEENSHIRE = "Aberdeenshire"
    ADUR = "Adur"
    ALLERDALE = "Allerdale"
    AMBER_VALLEY = "Amber Valley"
    ANGUS = "Angus"
    ANTRIM_AND_NEWTOWNABBEY = "Antrim and Newtownabbey"
    ARDS_AND_NORTH_DOWN = "Ards and North Down"
    ARGYLL_AND_BUTE = "Argyll and Bute"
    ARMAGH_CITY_BANBRIDGE_AND_CRAIGAVON = (
        "Armagh City, Banbridge and Craigavon"
    )
    ARUN = "Arun"
    ASHFIELD = "Ashfield"
    ASHFORD = "Ashford"
    BABERGH = "Babergh"
    BARKING_AND_DAGENHAM = "Barking and Dagenham"
    BARNET = "Barnet"
    BARNSLEY = "Barnsley"
    BARROW_IN_FURNESS = "Barrow-in-Furness"
    BASILDON = "Basildon"
    BASINGSTOKE_AND_DEANE = "Basingstoke and Deane"
    BASSETLAW = "Bassetlaw"
    BATH_AND_NORTH_EAST_SOMERSET = "Bath and North East Somerset"
    BEDFORD = "Bedford"
    BELFAST = "Belfast"
    BEXLEY = "Bexley"
    BIRMINGHAM = "Birmingham"
    BLABY = "Blaby"
    BLACKBURN_WITH_DARWEN = "Blackburn with Darwen"
    BLACKPOOL = "Blackpool"
    BLAENAU_GWENT = "Blaenau Gwent"
    BOLSOVER = "Bolsover"
    BOLTON = "Bolton"
    BOSTON = "Boston"
    BOURNEMOUTH_CHRISTCHURCH_AND_POOLE = "Bournemouth, Christchurch and Poole"
    BRACKNELL_FOREST = "Bracknell Forest"
    BRADFORD = "Bradford"
    BRAINTREE = "Braintree"
    BRECKLAND = "Breckland"
    BRENT = "Brent"
    BRENTWOOD = "Brentwood"
    BRIDGEND = "Bridgend"
    BRIGHTON_AND_HOVE = "Brighton and Hove"
    BRISTOL_CITY_OF = "Bristol, City of"
    BROADLAND = "Broadland"
    BROMLEY = "Bromley"
    BROMSGROVE = "Bromsgrove"
    BROXBOURNE = "Broxbourne"
    BROXTOWE = "Broxtowe"
    BUCKINGHAMSHIRE = "Buckinghamshire"
    BURNLEY = "Burnley"
    BURY = "Bury"
    CAERPHILLY = "Caerphilly"
    CALDERDALE = "Calderdale"
    CAMBRIDGE = "Cambridge"
    CAMDEN = "Camden"
    CANNOCK_CHASE = "Cannock Chase"
    CANTERBURY = "Canterbury"
    CARDIFF = "Cardiff"
    CARLISLE = "Carlisle"
    CARMARTHENSHIRE = "Carmarthenshire"
    CASTLE_POINT = "Castle Point"
    CAUSEWAY_COAST_AND_GLENS = "Causeway Coast and Glens"
    CENTRAL_BEDFORDSHIRE = "Central Bedfordshire"
    CEREDIGION = "Ceredigion"
    CHARNWOOD = "Charnwood"
    CHELMSFORD = "Chelmsford"
    CHELTENHAM = "Cheltenham"
    CHERWELL = "Cherwell"
    CHESHIRE_EAST = "Cheshire East"
    CHESHIRE_WEST_AND_CHESTER = "Cheshire West and Chester"
    CHESTERFIELD = "Chesterfield"
    CHICHESTER = "Chichester"
    CHORLEY = "Chorley"
    CITY_OF_EDINBURGH = "City of Edinburgh"
    CITY_OF_LONDON = "City of London"
    CLACKMANNANSHIRE = "Clackmannanshire"
    COLCHESTER = "Colchester"
    CONWY = "Conwy"
    COPELAND = "Copeland"
    CORBY = "Corby"
    CORNWALL = "Cornwall"
    COTSWOLD = "Cotswold"
    COUNTY_DURHAM = "County Durham"
    COVENTRY = "Coventry"
    CRAVEN = "Craven"
    CRAWLEY = "Crawley"
    CROYDON = "Croydon"
    DACORUM = "Dacorum"
    DARLINGTON = "Darlington"
    DARTFORD = "Dartford"
    DAVENTRY = "Daventry"
    DENBIGHSHIRE = "Denbighshire"
    DERBY = "Derby"
    DERBYSHIRE_DALES = "Derbyshire Dales"
    DERRY_CITY_AND_STRABANE = "Derry City and Strabane"
    DONCASTER = "Doncaster"
    DORSET = "Dorset"
    DOVER = "Dover"
    DUDLEY = "Dudley"
    DUMFRIES_AND_GALLOWAY = "Dumfries and Galloway"
    DUNDEE_CITY = "Dundee City"
    EALING = "Ealing"
    EAST_AYRSHIRE = "East Ayrshire"
    EAST_CAMBRIDGESHIRE = "East Cambridgeshire"
    EAST_DEVON = "East Devon"
    EAST_DUNBARTONSHIRE = "East Dunbartonshire"
    EAST_HAMPSHIRE = "East Hampshire"
    EAST_HERTFORDSHIRE = "East Hertfordshire"
    EAST_LINDSEY = "East Lindsey"
    EAST_LOTHIAN = "East Lothian"
    EAST_NORTHAMPTONSHIRE = "East Northamptonshire"
    EAST_RENFREWSHIRE = "East Renfrewshire"
    EAST_RIDING_OF_YORKSHIRE = "East Riding of Yorkshire"
    EAST_STAFFORDSHIRE = "East Staffordshire"
    EAST_SUFFOLK = "East Suffolk"
    EASTBOURNE = "Eastbourne"
    EASTLEIGH = "Eastleigh"
    EDEN = "Eden"
    ELMBRIDGE = "Elmbridge"
    ENFIELD = "Enfield"
    EPPING_FOREST = "Epping Forest"
    EPSOM_AND_EWELL = "Epsom and Ewell"
    EREWASH = "Erewash"
    EXETER = "Exeter"
    FALKIRK = "Falkirk"
    FAREHAM = "Fareham"
    FENLAND = "Fenland"
    FERMANAGH_AND_OMAGH = "Fermanagh and Omagh"
    FIFE = "Fife"
    FLINTSHIRE = "Flintshire"
    FOLKESTONE_AND_HYTHE = "Folkestone and Hythe"
    FOREST_OF_DEAN = "Forest of Dean"
    FYLDE = "Fylde"
    GATESHEAD = "Gateshead"
    GEDLING = "Gedling"
    GLASGOW_CITY = "Glasgow City"
    GLOUCESTER = "Gloucester"
    GOSPORT = "Gosport"
    GRAVESHAM = "Gravesham"
    GREAT_YARMOUTH = "Great Yarmouth"
    GREENWICH = "Greenwich"
    GUILDFORD = "Guildford"
    GWYNEDD = "Gwynedd"
    HACKNEY = "Hackney"
    HALTON = "Halton"
    HAMBLETON = "Hambleton"
    HAMMERSMITH_AND_FULHAM = "Hammersmith and Fulham"
    HARBOROUGH = "Harborough"
    HARINGEY = "Haringey"
    HARLOW = "Harlow"
    HARROGATE = "Harrogate"
    HARROW = "Harrow"
    HART = "Hart"
    HARTLEPOOL = "Hartlepool"
    HASTINGS = "Hastings"
    HAVANT = "Havant"
    HAVERING = "Havering"
    HEREFORDSHIRE_COUNTY_OF = "Herefordshire, County of"
    HERTSMERE = "Hertsmere"
    HIGH_PEAK = "High Peak"
    HIGHLAND = "Highland"
    HILLINGDON = "Hillingdon"
    HINCKLEY_AND_BOSWORTH = "Hinckley and Bosworth"
    HORSHAM = "Horsham"
    HOUNSLOW = "Hounslow"
    HUNTINGDONSHIRE = "Huntingdonshire"
    HYNDBURN = "Hyndburn"
    INVERCLYDE = "Inverclyde"
    IPSWICH = "Ipswich"
    ISLE_OF_ANGLESEY = "Isle of Anglesey"
    ISLE_OF_WIGHT = "Isle of Wight"
    ISLES_OF_SCILLY = "Isles of Scilly"
    ISLINGTON = "Islington"
    KENSINGTON_AND_CHELSEA = "Kensington and Chelsea"
    KETTERING = "Kettering"
    KINGS_LYNN_AND_WEST_NORFOLK = "King's Lynn and West Norfolk"
    KINGSTON_UPON_HULL_CITY_OF = "Kingston upon Hull, City of"
    KINGSTON_UPON_THAMES = "Kingston upon Thames"
    KIRKLEES = "Kirklees"
    KNOWSLEY = "Knowsley"
    LAMBETH = "Lambeth"
    LANCASTER = "Lancaster"
    LEEDS = "Leeds"
    LEICESTER = "Leicester"
    LEWES = "Lewes"
    LEWISHAM = "Lewisham"
    LICHFIELD = "Lichfield"
    LINCOLN = "Lincoln"
    LISBURN_AND_CASTLEREAGH = "Lisburn and Castlereagh"
    LIVERPOOL = "Liverpool"
    LUTON = "Luton"
    MAIDSTONE = "Maidstone"
    MALDON = "Maldon"
    MALVERN_HILLS = "Malvern Hills"
    MANCHESTER = "Manchester"
    MANSFIELD = "Mansfield"
    MEDWAY = "Medway"
    MELTON = "Melton"
    MENDIP = "Mendip"
    MERTHYR_TYDFIL = "Merthyr Tydfil"
    MERTON = "Merton"
    MID_DEVON = "Mid Devon"
    MID_SUFFOLK = "Mid Suffolk"
    MID_SUSSEX = "Mid Sussex"
    MID_ULSTER = "Mid Ulster"
    MID_AND_EAST_ANTRIM = "Mid and East Antrim"
    MIDDLESBROUGH = "Middlesbrough"
    MIDLOTHIAN = "Midlothian"
    MILTON_KEYNES = "Milton Keynes"
    MOLE_VALLEY = "Mole Valley"
    MONMOUTHSHIRE = "Monmouthshire"
    MORAY = "Moray"
    NA_H_EILEANAN_SIAR = "Na h-Eileanan Siar"
    NEATH_PORT_TALBOT = "Neath Port Talbot"
    NEW_FOREST = "New Forest"
    NEWARK_AND_SHERWOOD = "Newark and Sherwood"
    NEWCASTLE_UPON_TYNE = "Newcastle upon Tyne"
    NEWCASTLE_UNDER_LYME = "Newcastle-under-Lyme"
    NEWHAM = "Newham"
    NEWPORT = "Newport"
    NEWRY_MOURNE_AND_DOWN = "Newry, Mourne and Down"
    NORTH_AYRSHIRE = "North Ayrshire"
    NORTH_DEVON = "North Devon"
    NORTH_EAST_DERBYSHIRE = "North East Derbyshire"
    NORTH_EAST_LINCOLNSHIRE = "North East Lincolnshire"
    NORTH_HERTFORDSHIRE = "North Hertfordshire"
    NORTH_KESTEVEN = "North Kesteven"
    NORTH_LANARKSHIRE = "North Lanarkshire"
    NORTH_LINCOLNSHIRE = "North Lincolnshire"
    NORTH_NORFOLK = "North Norfolk"
    NORTH_SOMERSET = "North Somerset"
    NORTH_TYNESIDE = "North Tyneside"
    NORTH_WARWICKSHIRE = "North Warwickshire"
    NORTH_WEST_LEICESTERSHIRE = "North West Leicestershire"
    NORTHAMPTON = "Northampton"
    NORTHUMBERLAND = "Northumberland"
    NORWICH = "Norwich"
    NOTTINGHAM = "Nottingham"
    NUNEATON_AND_BEDWORTH = "Nuneaton and Bedworth"
    OADBY_AND_WIGSTON = "Oadby and Wigston"
    OLDHAM = "Oldham"
    ORKNEY_ISLANDS = "Orkney Islands"
    OXFORD = "Oxford"
    PEMBROKESHIRE = "Pembrokeshire"
    PENDLE = "Pendle"
    PERTH_AND_KINROSS = "Perth and Kinross"
    PETERBOROUGH = "Peterborough"
    PLYMOUTH = "Plymouth"
    PORTSMOUTH = "Portsmouth"
    POWYS = "Powys"
    PRESTON = "Preston"
    READING = "Reading"
    REDBRIDGE = "Redbridge"
    REDCAR_AND_CLEVELAND = "Redcar and Cleveland"
    REDDITCH = "Redditch"
    REIGATE_AND_BANSTEAD = "Reigate and Banstead"
    RENFREWSHIRE = "Renfrewshire"
    RHONDDA_CYNON_TAF = "Rhondda Cynon Taf"
    RIBBLE_VALLEY = "Ribble Valley"
    RICHMOND_UPON_THAMES = "Richmond upon Thames"
    RICHMONDSHIRE = "Richmondshire"
    ROCHDALE = "Rochdale"
    ROCHFORD = "Rochford"
    ROSSENDALE = "Rossendale"
    ROTHER = "Rother"
    ROTHERHAM = "Rotherham"
    RUGBY = "Rugby"
    RUNNYMEDE = "Runnymede"
    RUSHCLIFFE = "Rushcliffe"
    RUSHMOOR = "Rushmoor"
    RUTLAND = "Rutland"
    RYEDALE = "Ryedale"
    SALFORD = "Salford"
    SANDWELL = "Sandwell"
    SCARBOROUGH = "Scarborough"
    SCOTTISH_BORDERS = "Scottish Borders"
    SEDGEMOOR = "Sedgemoor"
    SEFTON = "Sefton"
    SELBY = "Selby"
    SEVENOAKS = "Sevenoaks"
    SHEFFIELD = "Sheffield"
    SHETLAND_ISLANDS = "Shetland Islands"
    SHROPSHIRE = "Shropshire"
    SLOUGH = "Slough"
    SOLIHULL = "Solihull"
    SOMERSET_WEST_AND_TAUNTON = "Somerset West and Taunton"
    SOUTH_AYRSHIRE = "South Ayrshire"
    SOUTH_CAMBRIDGESHIRE = "South Cambridgeshire"
    SOUTH_DERBYSHIRE = "South Derbyshire"
    SOUTH_GLOUCESTERSHIRE = "South Gloucestershire"
    SOUTH_HAMS = "South Hams"
    SOUTH_HOLLAND = "South Holland"
    SOUTH_KESTEVEN = "South Kesteven"
    SOUTH_LAKELAND = "South Lakeland"
    SOUTH_LANARKSHIRE = "South Lanarkshire"
    SOUTH_NORFOLK = "South Norfolk"
    SOUTH_NORTHAMPTONSHIRE = "South Northamptonshire"
    SOUTH_OXFORDSHIRE = "South Oxfordshire"
    SOUTH_RIBBLE = "South Ribble"
    SOUTH_SOMERSET = "South Somerset"
    SOUTH_STAFFORDSHIRE = "South Staffordshire"
    SOUTH_TYNESIDE = "South Tyneside"
    SOUTHAMPTON = "Southampton"
    SOUTHEND_ON_SEA = "Southend-on-Sea"
    SOUTHWARK = "Southwark"
    SPELTHORNE = "Spelthorne"
    ST_ALBANS = "St Albans"
    ST_HELENS = "St. Helens"
    STAFFORD = "Stafford"
    STAFFORDSHIRE_MOORLANDS = "Staffordshire Moorlands"
    STEVENAGE = "Stevenage"
    STIRLING = "Stirling"
    STOCKPORT = "Stockport"
    STOCKTON_ON_TEES = "Stockton-on-Tees"
    STOKE_ON_TRENT = "Stoke-on-Trent"
    STRATFORD_ON_AVON = "Stratford-on-Avon"
    STROUD = "Stroud"
    SUNDERLAND = "Sunderland"
    SURREY_HEATH = "Surrey Heath"
    SUTTON = "Sutton"
    SWALE = "Swale"
    SWANSEA = "Swansea"
    SWINDON = "Swindon"
    TAMESIDE = "Tameside"
    TAMWORTH = "Tamworth"
    TANDRIDGE = "Tandridge"
    TEIGNBRIDGE = "Teignbridge"
    TELFORD_AND_WREKIN = "Telford and Wrekin"
    TENDRING = "Tendring"
    TEST_VALLEY = "Test Valley"
    TEWKESBURY = "Tewkesbury"
    THANET = "Thanet"
    THREE_RIVERS = "Three Rivers"
    THURROCK = "Thurrock"
    TONBRIDGE_AND_MALLING = "Tonbridge and Malling"
    TORBAY = "Torbay"
    TORFAEN = "Torfaen"
    TORRIDGE = "Torridge"
    TOWER_HAMLETS = "Tower Hamlets"
    TRAFFORD = "Trafford"
    TUNBRIDGE_WELLS = "Tunbridge Wells"
    UTTLESFORD = "Uttlesford"
    VALE_OF_GLAMORGAN = "Vale of Glamorgan"
    VALE_OF_WHITE_HORSE = "Vale of White Horse"
    WAKEFIELD = "Wakefield"
    WALSALL = "Walsall"
    WALTHAM_FOREST = "Waltham Forest"
    WANDSWORTH = "Wandsworth"
    WARRINGTON = "Warrington"
    WARWICK = "Warwick"
    WATFORD = "Watford"
    WAVERLEY = "Waverley"
    WEALDEN = "Wealden"
    WELLINGBOROUGH = "Wellingborough"
    WELWYN_HATFIELD = "Welwyn Hatfield"
    WEST_BERKSHIRE = "West Berkshire"
    WEST_DEVON = "West Devon"
    WEST_DUNBARTONSHIRE = "West Dunbartonshire"
    WEST_LANCASHIRE = "West Lancashire"
    WEST_LINDSEY = "West Lindsey"
    WEST_LOTHIAN = "West Lothian"
    WEST_OXFORDSHIRE = "West Oxfordshire"
    WEST_SUFFOLK = "West Suffolk"
    WESTMINSTER = "Westminster"
    WIGAN = "Wigan"
    WILTSHIRE = "Wiltshire"
    WINCHESTER = "Winchester"
    WINDSOR_AND_MAIDENHEAD = "Windsor and Maidenhead"
    WIRRAL = "Wirral"
    WOKING = "Woking"
    WOKINGHAM = "Wokingham"
    WOLVERHAMPTON = "Wolverhampton"
    WORCESTER = "Worcester"
    WORTHING = "Worthing"
    WREXHAM = "Wrexham"
    WYCHAVON = "Wychavon"
    WYRE = "Wyre"
    WYRE_FOREST = "Wyre Forest"
    YORK = "York"


class local_authority(Variable):
    value_type = Enum
    possible_values = LocalAuthority
    default_value = LocalAuthority.MAIDSTONE
    entity = Household
    label = "Local Authority"
    documentation = "The local authority for this household (this is often the same as your Broad Rental Market Area, but may differ)."
    definition_period = YEAR
