#!/usr/bin/env python
# -*- coding:utf-8 -*-




# Canvas Page name.
FACEBOOK_CANVAS_NAME = 'ojo-ticket'

# A random token for use with the Real-time API.
FACEBOOK_REALTIME_VERIFY_TOKEN = 'RANDOM TOKEN'

# The external URL this application is available at where the Real-time API will
# send it's pings.
EXTERNAL_HREF = 'https:u//ojo-ticket.appspot.com/'

# Facebook User IDs of admins. The poor mans admin system.
ADMIN_USER_IDS = ['100002448856234']

UL_DEPARTEMENT = {'ACT':u'Actuariat\
', 'AEE':u'Admin. et éval. en éducation\
', 'ADM':u'Administration\
', 'ADS':u'Administration scolaire\
', 'APR':u'Affaires publ. et représ. int.\
', 'AGC':u'Agroéconomie\
', 'AGF':u'Agroforesterie\
', 'AGN':u'Agronomie\
', 'ALL':u'Allemand\
', 'AME':u'Aménagement du territoire\
', 'ANM':u'Anatomie\
', 'ANG':u'Anglais\
', 'ANL':u'Anglais (langue)\
', 'ANT':u'Anthropologie\
', 'ARA':u'Arabe\
', 'ARL':u'Archéologie\
', 'ARC':u'Architecture\
', 'GAD':u'Archivistique\
', 'ARD':u'Art dramatique\
', 'ANI':u'Art et science de l\'animation\
', 'ART':u'Arts\
', 'ARV':u'Arts visuels\
', 'ASR':u'Assurances\
', 'BCM':u'Biochimie\
', 'BCX':u'Biochimie médicale\
', 'BIF':u'Bio-informatique\
', 'BIO':u'Biologie\
', 'BMO':u'Biologie cell. et moléculaire\
', 'BVG':u'Biologie végétale\
', 'BPH':u'Biophotonique\
', 'CAT':u'Catéchése\
', 'CHM':u'Chimie\
', 'CHN':u'Chinois\
', 'CIN':u'Cinéma\
', 'COM':u'Communication\
', 'CTB':u'Comptabilité\
', 'CNS':u'Consommation\
', 'CSO':u'Counseling et orientation\
', 'CRL':u'Création littéraire\
', 'CRI':u'Criminologie\
', 'DES':u'Design graphique\
', 'DDU':u'Développement durable\
', 'DVE':u'Développement économique\
', 'DRI':u'Développement rural intégré\
', 'DID':u'Didactique\
', 'DRT':u'Droit\
', 'ERU':u'Économie rurale\
', 'ECN':u'Économique\
', 'EDC':u'Éducation\
', 'EPS':u'Éducation physique\
', 'ENP':u'Enseignement préscol. et prim.\
', 'ENS':u'Enseignement secondaire\
', 'EER':u'Ens. en éthique et cult. rel.\
', 'ENT':u'Entrepreneuriat\
', 'ENV':u'Environnement\
', 'EPM':u'Épidémiologie\
', 'EGN':u'Ergonomie\
', 'ERG':u'Ergothérapie\
', 'ESP':u'Espagnol\
', 'ESG':u'Espagnol (langue)\
', 'ETH':u'Éthique\
', 'EFN':u'Ethn. francoph. en Am. du N.\
', 'ETN':u'Ethnologie\
', 'EAN':u'Études anciennes\
', 'FEM':u'Études féministes\
', 'ETI':u'Études internationales\
', 'PTR':u'Études patrimoniales\
', 'GPL':u'Études pluridisciplinaires\
', 'EXD':u'Examen de doctorat\
', 'FOR':u'Foresterie\
', 'FIS':u'Formation interdisc. en santé\
', 'FPT':u'Formation prof. et technique\
', 'FRN':u'Français\
', 'FLE':u'Français lang. étr. ou seconde\
', 'FLS':u'Français langue seconde\
', 'GNT':u'Génétique\
', 'GAA':u'Génie agroalimentaire\
', 'GAE':u'Génie agroenvironnemental\
', 'GAL':u'Génie alimentaire\
', 'GCH':u'Génie chimique\
', 'GCI':u'Génie civil\
', 'GPG':u'Génie de la plasturgie\
', 'GEX':u'Génie des eaux\
', 'GEL':u'Génie électrique\
', 'GSC':u'Génie et sciences\
', 'GGL':u'Génie géologique\
', 'GIN':u'Génie industriel\
', 'GIF':u'Génie informatique\
', 'GLO':u'Génie logiciel\
', 'GMC':u'Génie mécanique\
', 'GML':u'Génie métallurgique\
', 'GMN':u'Génie minier\
', 'GPH':u'Génie physique\
', 'GGR':u'Géographie\
', 'GLG':u'Géologie\
', 'GMT':u'Géomatique\
', 'GSO':u'Gestion des opérations\
', 'GRH':u'Gestion des ress. humaines\
', 'GSE':u'Gestion économique\
', 'GSF':u'Gestion financière\
', 'GIE':u'Gestion internationale\
', 'GUI':u'Gest. urbaine et immobilière\
', 'GRC':u'Grec\
', 'HST':u'Histoire\
', 'HAR':u'Histoire de l\'art\
', 'HTL':u'Histologie\
', 'IFT':u'Informatique\
', 'IDI':u'Interv. en déficience intell.\
', 'IED':u'Intervention éducative\
', 'ITL':u'Italien\
', 'JAP':u'Japonais\
', 'JOU':u'Journalisme\
', 'KIN':u'Kinésiologie\
', 'LMO':u'Langues modernes\
', 'LOA':u'Langues orientales anciennes\
', 'LAT':u'Latin\
', 'LNG':u'Linguistique\
', 'LIT':u'Littérature\
', 'MNG':u'Management\
', 'MRK':u'Marketing\
', 'MAT':u'Mathématiques\
', 'MED':u'Médecine\
', 'MDD':u'Médecine dentaire\
', 'MDX':u'Médecine expérimentale\
', 'MEV':u'Mesure et évaluation\
', 'MQT':u'Méthodes quantitatives\
', 'MET':u'Méthodologie\
', 'MCB':u'Microbiologie\
', 'MSL':u'Muséologie\
', 'MUS':u'Musique\
', 'NRB':u'Neurobiologie\
', 'NUT':u'Nutrition\
', 'OCE':u'Océanographie\
', 'OPV':u'Optique et santé de la vue\
', 'ORT':u'Orthophonie\
', 'PST':u'Pastorale\
', 'PAT':u'Pathologie\
', 'PUN':u'Pédagogie universitaire\
', 'PHA':u'Pharmacie\
', 'PHC':u'Pharmacologie\
', 'PHI':u'Philosophie\
', 'PHS':u'Physiologie\
', 'PHT':u'Physiothérapie\
', 'PHY':u'Physique\
', 'PLG':u'Phytologie\
', 'PFP':u'Planif. financière personnelle\
', 'POR':u'Portugais\
', 'PSA':u'Psychiatrie\
', 'PSE':u'Psychoéducation\
', 'PSY':u'Psychologie\
', 'PPG':u'Psychopédagogie\
', 'RLT':u'Relations industrielles\
', 'RUS':u'Russe\
', 'SAT':u'Santé au travail\
', 'SAC':u'Santé communautaire\
', 'POL':u'Science politique\
', 'SAN':u'Sciences animales\
', 'SBM':u'Sciences biomédicales\
', 'SCR':u'Sciences des religions\
', 'SBO':u'Sciences du bois\
', 'SCG':u'Sciences géomatiques\
', 'SIN':u'Sciences infirmiéres\
', 'STA':u'Sciences, technologie aliments\
', 'SVS':u'Service social\
', 'SOC':u'Sociologie\
', 'SLS':u'Sols\
', 'STT':u'Statistique\
', 'SIO':u'Système information organisat.\
', 'TEN':u'Technologie éducative\
', 'THT':u'Théâtre\
', 'THL':u'Théologie\
', 'TCF':u'Thérapie conjug. et familiale\
', 'TRE':u'Thése, recherche, mémoire\
', 'TXM':u'Toxicomanie\
', 'TRD':u'Traduction\
', 'TED':u'Troubles envahissants du dév.\
'}
