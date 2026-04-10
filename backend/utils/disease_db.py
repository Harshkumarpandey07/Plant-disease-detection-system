
# ============================================================
#  PhytoSense — Disease Knowledge Base
#  backend/utils/disease_db.py
# ============================================================

DISEASE_DB = {
    "Apple — Apple Scab": {
        "scientific_name": "Venturia inaequalis",
        "crop": "Apple",
        "severity_class": "High",
        "description": (
            "Apple scab is the most economically important disease of apples worldwide. "
            "It causes significant fruit and leaf damage, reducing market value and tree vigor. "
            "The fungus overwinters in fallen leaves and releases spores in spring during wet periods."
        ),
        "symptoms": [
            "Olive-green velvety lesions on leaf undersides",
            "Lesions turn brown-black on upper leaf surface",
            "Dark scab lesions on fruit surface",
            "Cracked, distorted and deformed fruit",
            "Premature defoliation in severe cases",
        ],
        "causes": "Fungus overwinters in fallen leaves; ascospores released in spring during wet periods with temperatures 7-24 degrees C.",
        "organic_treatment": (
            "Apply sulfur-based fungicides (lime-sulfur or wettable sulfur) every 7 days. "
            "Remove and compost fallen leaves to reduce inoculum. "
            "Prune trees for better canopy airflow. "
            "Kaolin clay particle film reduces infection periods."
        ),
        "chemical_treatment": (
            "Captan 50% WP at 2-3 g/L. "
            "Myclobutanil 20% WP at 0.25 g/L. "
            "Trifloxystrobin 50% WG. "
            "Begin spray program at green tip stage and continue through cover spray."
        ),
        "prevention": (
            "Plant scab-resistant varieties such as Enterprise, Liberty or GoldRush. "
            "Ensure good orchard air drainage. "
            "Monitor apple scab infection models during spring. "
            "Avoid overhead irrigation during critical infection periods."
        ),
        "favorable_conditions": "Temperature 7-24 degrees C during wet periods, leaf wetness over 9 hours",
    },

    "Apple — Black Rot": {
        "scientific_name": "Botryosphaeria obtusa",
        "crop": "Apple",
        "severity_class": "High",
        "description": (
            "Black rot affects leaves, fruit and bark of apple trees. "
            "Infected fruit develops concentric rings of brown rot and eventually mummifies on the tree. "
            "The disease can also cause frogeye leaf spot and limb cankers."
        ),
        "symptoms": [
            "Circular purple spots on leaves with tan centers (frogeye leaf spot)",
            "Fruit rot beginning at the calyx end",
            "Concentric rings of brown and black on infected fruit",
            "Mummified black fruit remaining on tree",
            "Reddish brown cankers on limbs and trunk",
        ],
        "causes": "Fungal pathogen that overwinters in mummified fruit, dead wood, and bark cankers.",
        "organic_treatment": (
            "Remove all mummified fruit and dead wood. "
            "Apply copper-based fungicides during the growing season. "
            "Prune out cankered wood at least 15 cm below visible infection. "
            "Maintain tree vigor through balanced fertilization."
        ),
        "chemical_treatment": (
            "Captan 50% WP at 2.5 g/L. "
            "Thiophanate-methyl 70% WP at 1.5 g/L. "
            "Ziram 76% WDG as protectant spray. "
            "Apply from pink stage through harvest on 10-14 day schedule."
        ),
        "prevention": (
            "Remove and destroy all mummified fruit before budbreak. "
            "Prune dead and diseased wood annually. "
            "Avoid wounding trees during pruning. "
            "Plant resistant varieties where available."
        ),
        "favorable_conditions": "Warm temperatures 24-29 degrees C, wet weather during fruit development",
    },

    "Apple — Cedar Apple Rust": {
        "scientific_name": "Gymnosporangium juniperi-virginianae",
        "crop": "Apple",
        "severity_class": "Medium",
        "description": (
            "Cedar apple rust requires two hosts to complete its life cycle: apple and eastern red cedar. "
            "It causes bright orange spots on apple leaves and fruit, reducing photosynthesis and fruit quality."
        ),
        "symptoms": [
            "Bright orange-yellow spots on upper leaf surface",
            "Orange tube-like structures on leaf undersides",
            "Deformed and spotted fruit",
            "Premature leaf drop in severe infections",
            "Gelatinous orange spore masses on nearby cedar trees in spring",
        ],
        "causes": "Fungal rust pathogen alternating between apple and juniper/cedar hosts; spores spread by wind.",
        "organic_treatment": (
            "Remove nearby eastern red cedar trees within 1 km if feasible. "
            "Apply sulfur-based fungicides from pink stage through petal fall. "
            "Neem oil applications provide moderate suppression. "
            "Plant rust-resistant apple varieties."
        ),
        "chemical_treatment": (
            "Myclobutanil 20% WP at 0.25 g/L every 7-10 days. "
            "Propiconazole 25% EC at 0.5 ml/L. "
            "Triadimefon 25% WP at 1 g/L. "
            "Apply protectant sprays before and during wet periods in spring."
        ),
        "prevention": (
            "Plant rust-resistant apple varieties such as Liberty, Freedom or Redfree. "
            "Remove galls from nearby cedar trees in late winter before spore release. "
            "Avoid planting apples near eastern red cedar or juniper. "
            "Apply preventive fungicide program from tight cluster through cover."
        ),
        "favorable_conditions": "Cool wet spring weather, proximity to juniper or cedar hosts",
    },

    "Apple — Healthy": {
        "scientific_name": "N/A",
        "crop": "Apple",
        "severity_class": "None",
        "description": "This apple plant appears healthy with no visible signs of disease or stress.",
        "symptoms": ["No disease symptoms detected", "Normal leaf color and texture", "Healthy plant morphology"],
        "causes": "N/A",
        "organic_treatment": "Continue regular monitoring and preventive care.",
        "chemical_treatment": "No treatment required.",
        "prevention": (
            "Maintain regular scouting schedule. "
            "Continue good cultural practices: proper spacing, balanced nutrition, adequate irrigation. "
            "Apply preventive copper sprays during high-risk weather periods."
        ),
        "favorable_conditions": "N/A",
    },

    "Blueberry — Healthy": {
        "scientific_name": "N/A",
        "crop": "Blueberry",
        "severity_class": "None",
        "description": "This blueberry plant appears healthy with no visible signs of disease.",
        "symptoms": ["No disease symptoms detected", "Normal leaf color and growth"],
        "causes": "N/A",
        "organic_treatment": "Maintain soil pH at 4.5-5.5 for optimal health.",
        "chemical_treatment": "No treatment required.",
        "prevention": "Regular monitoring, maintain acidic soil pH, adequate drainage.",
        "favorable_conditions": "N/A",
    },

    "Cherry — Powdery Mildew": {
        "scientific_name": "Podosphaera clandestina",
        "crop": "Cherry",
        "severity_class": "Medium",
        "description": (
            "Powdery mildew of cherry affects leaves, shoots and fruit. "
            "It appears as a white powdery coating and can cause significant defoliation and fruit russeting."
        ),
        "symptoms": [
            "White powdery coating on leaf surfaces",
            "Distorted and cupped young leaves",
            "Russeting and cracking of fruit skin",
            "Stunted shoot growth",
            "Premature defoliation in severe cases",
        ],
        "causes": "Obligate fungal pathogen favoured by warm days, cool nights and moderate humidity without rainfall.",
        "organic_treatment": (
            "Apply sulfur-based fungicides every 7-10 days. "
            "Neem oil at 3 ml/L provides good suppression. "
            "Potassium bicarbonate solutions are effective. "
            "Improve air circulation through pruning."
        ),
        "chemical_treatment": (
            "Myclobutanil 20% WP at 0.25 g/L. "
            "Trifloxystrobin 25% WG at 0.2 g/L. "
            "Quinoxyfen 25% SC at 0.5 ml/L. "
            "Begin applications at first symptom appearance."
        ),
        "prevention": (
            "Plant resistant cherry varieties. "
            "Prune for good canopy airflow. "
            "Avoid excess nitrogen fertilization. "
            "Apply preventive sulfur during periods of moderate temperatures."
        ),
        "favorable_conditions": "Warm days 20-27 degrees C, cool nights, moderate humidity 50-70%",
    },

    "Cherry — Healthy": {
        "scientific_name": "N/A",
        "crop": "Cherry",
        "severity_class": "None",
        "description": "This cherry plant appears healthy with no visible signs of disease.",
        "symptoms": ["No disease symptoms detected", "Normal leaf color and growth"],
        "causes": "N/A",
        "organic_treatment": "Continue preventive copper applications during wet periods.",
        "chemical_treatment": "No treatment required.",
        "prevention": "Regular monitoring, proper pruning for airflow, balanced fertilization.",
        "favorable_conditions": "N/A",
    },

    "Corn — Cercospora Leaf Spot": {
        "scientific_name": "Cercospora zeae-maydis",
        "crop": "Corn",
        "severity_class": "Medium",
        "description": (
            "Gray leaf spot is one of the most yield-limiting diseases of corn worldwide. "
            "It thrives under conditions of high humidity and moderate temperatures, "
            "and can cause significant leaf area loss and yield reduction in susceptible hybrids."
        ),
        "symptoms": [
            "Rectangular tan to gray lesions parallel to leaf veins",
            "Lesions limited by leaf veins giving rectangular appearance",
            "Lesions turn gray as fungal sporulation occurs",
            "Severe cases cause complete leaf blighting",
            "Lower leaves affected first progressing upward",
        ],
        "causes": "Fungal pathogen that overwinters in crop residue; favoured by prolonged leaf wetness and warm temperatures.",
        "organic_treatment": (
            "Crop rotation away from corn for at least one season. "
            "Tillage to bury infected residue reduces inoculum. "
            "Plant resistant hybrids as primary management strategy. "
            "Ensure adequate potassium nutrition."
        ),
        "chemical_treatment": (
            "Azoxystrobin 23% SC at 1 ml/L. "
            "Pyraclostrobin 25% EC at 0.8 ml/L. "
            "Propiconazole 25% EC at 1 ml/L. "
            "Apply at VT to R1 growth stage when disease threshold is reached."
        ),
        "prevention": (
            "Plant gray leaf spot resistant hybrids. "
            "Rotate with non-corn crops for 1-2 seasons. "
            "Avoid minimum tillage in high-risk fields. "
            "Scout regularly from V8 stage onward."
        ),
        "favorable_conditions": "Temperature 22-30 degrees C, relative humidity above 90%, prolonged dew periods",
    },

    "Corn — Common Rust": {
        "scientific_name": "Puccinia sorghi",
        "crop": "Corn",
        "severity_class": "Medium",
        "description": (
            "Common rust produces powdery orange-brown pustules on both leaf surfaces. "
            "Severe infections can cause significant yield loss especially in susceptible hybrids. "
            "Wind-dispersed spores spread rapidly across fields and regions."
        ),
        "symptoms": [
            "Cinnamon-brown powdery pustules on both leaf surfaces",
            "Pustules elongated and scattered across leaves",
            "Pustules turn black at maturity as teliospores form",
            "Heavy infection causes leaf yellowing and death",
            "Reduced ear fill in severe cases",
        ],
        "causes": "Obligate fungal pathogen; wind-dispersed urediniospores from southern overwintering regions.",
        "organic_treatment": (
            "Plant resistant hybrid varieties as primary strategy. "
            "Crop rotation to reduce local inoculum buildup. "
            "Adequate potassium fertilization reduces severity. "
            "Early planting to escape peak rust pressure periods."
        ),
        "chemical_treatment": (
            "Propiconazole 25% EC at 1 ml/L when pustules first appear. "
            "Azoxystrobin 23% SC at 1 ml/L. "
            "Trifloxystrobin 25% WG at 0.2 g/L. "
            "Apply at V8 stage or when disease threshold of 5% infected plants is reached."
        ),
        "prevention": (
            "Use certified rust-resistant hybrids with Rp1D or Rp3 gene resistance. "
            "Avoid excessive nitrogen that promotes lush susceptible growth. "
            "Monitor weather for warm humid conditions favoring rust spread. "
            "Early planting before inoculum levels peak."
        ),
        "favorable_conditions": "Temperature 16-23 degrees C, high humidity, cloudy weather",
    },

    "Corn — Northern Leaf Blight": {
        "scientific_name": "Exserohilum turcicum",
        "crop": "Corn",
        "severity_class": "High",
        "description": (
            "Northern leaf blight is a major foliar disease of corn causing large cigar-shaped lesions. "
            "Severe epidemics can reduce yield by 30-50% in susceptible hybrids under favorable conditions."
        ),
        "symptoms": [
            "Long cigar-shaped gray-green to tan lesions 2.5-15 cm long",
            "Lesions may have wavy or irregular margins",
            "Dark green water-soaked borders on young lesions",
            "Lesions coalesce causing extensive blighting",
            "Lower leaves affected first progressing upward",
        ],
        "causes": "Fungal pathogen overwinters in corn residue; conidia spread by wind and rain splash.",
        "organic_treatment": (
            "Rotate with non-corn crops for one to two seasons. "
            "Deep tillage to bury infected residue. "
            "Plant resistant hybrids with Ht gene resistance. "
            "Ensure balanced crop nutrition."
        ),
        "chemical_treatment": (
            "Azoxystrobin plus propiconazole premix at label rate. "
            "Pyraclostrobin 25% EC at 0.8 ml/L. "
            "Tebuconazole 250 EC at 0.5 ml/L. "
            "Apply preventively at tasseling when disease pressure is anticipated."
        ),
        "prevention": (
            "Plant hybrids with Ht1, Ht2 or HtN resistance genes. "
            "Rotate crops to reduce residue-borne inoculum. "
            "Avoid fields with history of severe NLB. "
            "Scout from V8 onward especially after prolonged wet periods."
        ),
        "favorable_conditions": "Temperature 18-27 degrees C, heavy dew or rain, high humidity",
    },

    "Corn — Healthy": {
        "scientific_name": "N/A",
        "crop": "Corn",
        "severity_class": "None",
        "description": "This corn plant appears healthy with no visible signs of disease.",
        "symptoms": ["No disease symptoms detected", "Normal leaf color and growth"],
        "causes": "N/A",
        "organic_treatment": "Maintain balanced nutrition and adequate moisture.",
        "chemical_treatment": "No treatment required.",
        "prevention": "Regular scouting, balanced fertilization, proper plant spacing.",
        "favorable_conditions": "N/A",
    },

    "Grape — Black Rot": {
        "scientific_name": "Guignardia bidwellii",
        "crop": "Grape",
        "severity_class": "High",
        "description": (
            "Black rot is the most serious fungal disease of grapes in humid climates. "
            "It can destroy 80-100% of the crop if left untreated. "
            "The pathogen overwinters in mummified berries and infected canes."
        ),
        "symptoms": [
            "Circular tan lesions with dark brown margins on leaves",
            "Black pycnidia visible as tiny dots in lesion center",
            "Young berries turn brown then black and shriveled",
            "Infected berries become hard mummies remaining on vine",
            "Cankers on woody canes and tendrils",
        ],
        "causes": "Fungal pathogen overwinters in mummified berries; infects all green tissue during wet periods.",
        "organic_treatment": (
            "Remove and destroy all mummified berries and infected canes. "
            "Copper-based fungicide applications from budbreak. "
            "Improve canopy airflow through proper training and leaf removal. "
            "Ensure good drainage and avoid low-lying poorly ventilated sites."
        ),
        "chemical_treatment": (
            "Myclobutanil 20% WP at 0.25 g/L. "
            "Tebuconazole 250 EC at 0.5 ml/L. "
            "Captan 50% WP plus sulfur as protectant. "
            "Apply from budbreak through veraison on 7-14 day schedule."
        ),
        "prevention": (
            "Site selection with good air drainage. "
            "Train vines for open well-ventilated canopy. "
            "Scout early in spring for first lesions. "
            "Remove all mummified berries before budbreak."
        ),
        "favorable_conditions": "Temperature 15-30 degrees C, wet weather, relative humidity above 90%",
    },

    "Grape — Esca Black Measles": {
        "scientific_name": "Phaeomoniella chlamydospora",
        "crop": "Grape",
        "severity_class": "High",
        "description": (
            "Esca is a complex grapevine trunk disease caused by multiple fungal pathogens. "
            "It causes internal wood decay, foliar symptoms and sudden vine collapse. "
            "It is considered one of the most economically devastating grapevine diseases worldwide."
        ),
        "symptoms": [
            "Interveinal chlorosis and necrosis creating tiger stripe pattern on leaves",
            "Dark streaking of wood when cut in cross-section",
            "Sudden wilting and death of entire shoots in summer",
            "Shriveled berries with dark spots",
            "Slow progressive decline of vine over multiple seasons",
        ],
        "causes": "Complex of fungal pathogens infecting through pruning wounds; favoured by drought stress.",
        "organic_treatment": (
            "Protect pruning wounds with wound sealant or fungicide paint immediately after cutting. "
            "Remove and destroy severely affected vines. "
            "Minimize pruning wound size. "
            "Improve vine vigor through balanced nutrition and irrigation."
        ),
        "chemical_treatment": (
            "Thiophanate-methyl 70% WP as wound protectant paste. "
            "Trichoderma-based biological wound protectants. "
            "No fully curative systemic treatments are currently available. "
            "Focus on prevention through wound management."
        ),
        "prevention": (
            "Apply wound protectant to all pruning cuts within 24 hours. "
            "Prune during dry weather to reduce infection risk. "
            "Use double pruning technique to delay final cuts. "
            "Remove and burn infected wood promptly."
        ),
        "favorable_conditions": "Pruning wounds during wet weather, drought-stressed vines",
    },

    "Grape — Leaf Blight": {
        "scientific_name": "Isariopsis clavispora",
        "crop": "Grape",
        "severity_class": "Medium",
        "description": (
            "Grape leaf blight causes dark angular lesions on leaves and can lead to significant defoliation. "
            "Severe infections reduce photosynthetic capacity and weaken vines."
        ),
        "symptoms": [
            "Dark brown angular lesions on leaves",
            "Lesions limited by leaf veins",
            "Grayish fungal sporulation on lesion surface",
            "Premature defoliation",
            "Reduced fruit quality in severe cases",
        ],
        "causes": "Fungal pathogen favoured by warm wet conditions during the growing season.",
        "organic_treatment": (
            "Remove infected leaves and improve canopy airflow. "
            "Apply copper-based fungicides preventively. "
            "Ensure good vine training for air circulation. "
            "Avoid overhead irrigation."
        ),
        "chemical_treatment": (
            "Mancozeb 75% WP at 2.5 g/L every 10-14 days. "
            "Chlorothalonil 75% WP at 2 g/L. "
            "Copper oxychloride 50% WP at 2 g/L. "
            "Apply protectant fungicides before infection periods."
        ),
        "prevention": (
            "Maintain open canopy through shoot positioning and leaf removal. "
            "Avoid excessive nitrogen fertilization. "
            "Use drip irrigation rather than overhead. "
            "Scout regularly from shoot emergence onward."
        ),
        "favorable_conditions": "Warm temperatures 20-28 degrees C, high humidity, frequent rainfall",
    },

    "Grape — Healthy": {
        "scientific_name": "N/A",
        "crop": "Grape",
        "severity_class": "None",
        "description": "This grapevine appears healthy with no visible signs of disease.",
        "symptoms": ["No disease symptoms detected", "Normal leaf color and vine growth"],
        "causes": "N/A",
        "organic_treatment": "Continue preventive copper and sulfur program.",
        "chemical_treatment": "No treatment required.",
        "prevention": "Regular canopy management, preventive spray program, wound protection at pruning.",
        "favorable_conditions": "N/A",
    },

    "Orange — Citrus Greening": {
        "scientific_name": "Candidatus Liberibacter asiaticus",
        "crop": "Orange",
        "severity_class": "High",
        "description": (
            "Citrus greening also known as Huanglongbing is the most devastating citrus disease worldwide. "
            "There is currently no cure and infected trees must be removed. "
            "It is spread by the Asian citrus psyllid insect vector."
        ),
        "symptoms": [
            "Asymmetric blotchy mottling of leaves",
            "Yellow shoot called blotchy mottle",
            "Small lopsided bitter fruit that fail to color properly",
            "Fruit drop before maturity",
            "Tree decline and death within years of infection",
        ],
        "causes": "Bacterial pathogen transmitted by Asian citrus psyllid insect; no cure currently exists.",
        "organic_treatment": (
            "Remove and destroy infected trees immediately to prevent spread. "
            "Control psyllid vector with horticultural oil sprays. "
            "Release biological control agents for psyllid management. "
            "Maintain tree nutrition to slow decline in mildly affected trees."
        ),
        "chemical_treatment": (
            "Imidacloprid systemic insecticide for psyllid vector control. "
            "Drenching applications of thermotherapy show experimental promise. "
            "Penicillin trunk injections may temporarily suppress symptoms. "
            "No fully effective curative treatment currently available."
        ),
        "prevention": (
            "Use certified disease-free nursery stock only. "
            "Implement strict psyllid monitoring and control program. "
            "Quarantine measures to prevent movement of infected plant material. "
            "Plant windbreaks to reduce psyllid movement into orchards."
        ),
        "favorable_conditions": "Presence of Asian citrus psyllid, warm tropical and subtropical climates",
    },

    "Peach — Bacterial Spot": {
        "scientific_name": "Xanthomonas arboricola pv. pruni",
        "crop": "Peach",
        "severity_class": "High",
        "description": (
            "Bacterial spot is one of the most common and destructive diseases of peach. "
            "It causes lesions on fruit, leaves and twigs, significantly reducing marketable yield."
        ),
        "symptoms": [
            "Small water-soaked spots on leaves turning brown with yellow halos",
            "Shot-hole appearance as lesion centers fall out",
            "Deep sunken pits on fruit surface",
            "Severe defoliation in wet years",
            "Twig cankers and dieback",
        ],
        "causes": "Bacterial pathogen spread by rain splash and wind during wet periods; enters through stomata.",
        "organic_treatment": (
            "Apply copper hydroxide sprays from shuck split through harvest. "
            "Avoid overhead irrigation to reduce leaf wetness. "
            "Remove severely infected twigs during dormant pruning. "
            "Maintain good tree vigor through balanced nutrition."
        ),
        "chemical_treatment": (
            "Copper hydroxide 77% WDG at 2 g/L every 5-7 days during wet periods. "
            "Oxytetracycline 17% SP at petal fall and shuck split. "
            "Kasugamycin 3% SL for systemic bactericidal action. "
            "Alternate copper with non-copper bactericides to prevent resistance."
        ),
        "prevention": (
            "Plant resistant or tolerant peach varieties. "
            "Avoid sites with poor air drainage. "
            "Use drip irrigation to minimize leaf wetness. "
            "Apply dormant copper sprays to reduce overwintering inoculum."
        ),
        "favorable_conditions": "Temperature 24-30 degrees C, rain or overhead irrigation, high humidity",
    },

    "Peach — Healthy": {
        "scientific_name": "N/A",
        "crop": "Peach",
        "severity_class": "None",
        "description": "This peach tree appears healthy with no visible signs of disease.",
        "symptoms": ["No disease symptoms detected", "Normal leaf color and fruit development"],
        "causes": "N/A",
        "organic_treatment": "Continue preventive copper spray program.",
        "chemical_treatment": "No treatment required.",
        "prevention": "Regular monitoring, copper dormant sprays, balanced nutrition.",
        "favorable_conditions": "N/A",
    },

    "Pepper — Bacterial Spot": {
        "scientific_name": "Xanthomonas euvesicatoria",
        "crop": "Pepper",
        "severity_class": "Medium",
        "description": (
            "Bacterial spot of pepper causes leaf lesions, defoliation and fruit blemishes "
            "that significantly reduce marketable yield and plant vigor."
        ),
        "symptoms": [
            "Small water-soaked spots on leaves with yellow halos",
            "Spots enlarge and turn brown with irregular margins",
            "Severe defoliation leaving fruit exposed to sunscald",
            "Raised scab-like lesions on green fruit",
            "Sunken water-soaked lesions on ripe fruit",
        ],
        "causes": "Bacterial pathogen spread by rain splash, contaminated tools and infected transplants.",
        "organic_treatment": (
            "Copper hydroxide 77% WDG at 2 g/L every 5-7 days. "
            "Use certified pathogen-free seed and transplants. "
            "Avoid working in fields when foliage is wet. "
            "Remove and destroy heavily infected plant material."
        ),
        "chemical_treatment": (
            "Copper oxychloride plus Mancozeb combination. "
            "Kasugamycin 3% SL for systemic bactericidal action. "
            "Streptomycin sulfate 200 ppm in early disease stages only. "
            "Alternate copper with non-copper bactericides to prevent resistance."
        ),
        "prevention": (
            "Use certified disease-free seeds treated with hot water at 50 degrees C for 25 minutes. "
            "2-year rotation with non-solanaceous crops. "
            "Drip irrigation instead of overhead. "
            "Disinfect tools with 10% bleach solution between plants."
        ),
        "favorable_conditions": "Temperature 24-30 degrees C, high humidity, frequent rain or overhead irrigation",
    },

    "Pepper — Healthy": {
        "scientific_name": "N/A",
        "crop": "Pepper",
        "severity_class": "None",
        "description": "This pepper plant appears healthy with no visible signs of disease.",
        "symptoms": ["No disease symptoms detected", "Normal leaf color and fruit development"],
        "causes": "N/A",
        "organic_treatment": "Continue preventive copper applications during wet periods.",
        "chemical_treatment": "No treatment required.",
        "prevention": "Regular monitoring, drip irrigation, crop rotation.",
        "favorable_conditions": "N/A",
    },

    "Potato — Early Blight": {
        "scientific_name": "Alternaria solani",
        "crop": "Potato",
        "severity_class": "Medium",
        "description": (
            "Early blight is a common fungal disease of potato appearing as characteristic "
            "dark concentric ring lesions on older leaves. It reduces photosynthetic area "
            "and can severely impact yield if not managed."
        ),
        "symptoms": [
            "Circular dark-brown spots on lower leaves first",
            "Concentric ring target-board pattern inside spots",
            "Yellow chlorotic halo surrounding lesions",
            "Premature defoliation starting from plant base",
            "Lesions on stems and tubers in severe cases",
        ],
        "causes": "Fungus Alternaria solani favoured by warm days 24-29 degrees C, cool nights and high humidity.",
        "organic_treatment": (
            "Apply neem oil at 3 ml/L every 5-7 days from early vegetative stage. "
            "Copper-based fungicides such as copper oxychloride 50% WP. "
            "Remove and destroy infected lower leaves. "
            "Maintain adequate plant nutrition as nitrogen deficiency increases susceptibility."
        ),
        "chemical_treatment": (
            "Chlorothalonil 75% WP at 2.0 g/L every 7 days. "
            "Azoxystrobin 23% SC at 1 ml/L for systemic action. "
            "Propiconazole 25% EC at 1 ml/L. "
            "Apply protectant fungicides preventively before symptoms appear."
        ),
        "prevention": (
            "Use certified disease-free seed tubers. "
            "Practice 3-year crop rotation with non-host crops. "
            "Maintain proper plant nutrition especially potassium. "
            "Avoid drought stress through consistent irrigation. "
            "Destroy crop debris after harvest."
        ),
        "favorable_conditions": "Warm days 24-29 degrees C, cool nights, intermittent rainfall",
    },

    "Potato — Late Blight": {
        "scientific_name": "Phytophthora infestans",
        "crop": "Potato",
        "severity_class": "High",
        "description": (
            "Late blight is the most destructive disease of potato and was responsible for the "
            "Irish Potato Famine of the 1840s. It can destroy an entire field within days "
            "under favorable conditions if left untreated."
        ),
        "symptoms": [
            "Dark water-soaked lesions on leaves starting at margins",
            "White mold on undersides of leaves during humid nights",
            "Rapid yellowing and wilting of foliage",
            "Brown-black rot on stems",
            "Pink-brown firm rot on tubers",
        ],
        "causes": "Oomycete pathogen spread by wind-borne sporangia; thrives at 10-25 degrees C with humidity above 90%.",
        "organic_treatment": (
            "Remove and destroy infected plant material immediately. "
            "Apply copper hydroxide at 1.5-2.0 kg/ha every 5-7 days. "
            "Use Bordeaux mixture of 1:1 copper sulfate to lime. "
            "Ensure good drainage and improve air circulation by hilling."
        ),
        "chemical_treatment": (
            "Mancozeb 75% WP at 2.5 g/L every 7 days. "
            "Metalaxyl plus Mancozeb Ridomil Gold for systemic plus contact protection. "
            "Cymoxanil plus Mancozeb as an alternative. "
            "Rotate fungicide classes to prevent resistance buildup."
        ),
        "prevention": (
            "Plant certified disease-free seed tubers and resistant varieties. "
            "Avoid overhead irrigation and use drip instead. "
            "Space plants adequately for air movement. "
            "Scout fields weekly especially during cool wet periods. "
            "Destroy volunteer potato plants that may harbour the pathogen."
        ),
        "favorable_conditions": "Temperature 10-25 degrees C, humidity above 90%, rainfall or heavy dew",
    },

    "Potato — Healthy": {
        "scientific_name": "N/A",
        "crop": "Potato",
        "severity_class": "None",
        "description": "This potato plant appears healthy with no visible signs of disease.",
        "symptoms": ["No disease symptoms detected", "Normal leaf color and vine growth"],
        "causes": "N/A",
        "organic_treatment": "Continue preventive copper applications during wet periods.",
        "chemical_treatment": "No treatment required.",
        "prevention": "Use certified seed, crop rotation, regular scouting.",
        "favorable_conditions": "N/A",
    },

    "Raspberry — Healthy": {
        "scientific_name": "N/A",
        "crop": "Raspberry",
        "severity_class": "None",
        "description": "This raspberry plant appears healthy with no visible signs of disease.",
        "symptoms": ["No disease symptoms detected", "Normal cane and leaf development"],
        "causes": "N/A",
        "organic_treatment": "Maintain proper cane management and air circulation.",
        "chemical_treatment": "No treatment required.",
        "prevention": "Regular pruning, remove old canes, adequate spacing.",
        "favorable_conditions": "N/A",
    },

    "Soybean — Healthy": {
        "scientific_name": "N/A",
        "crop": "Soybean",
        "severity_class": "None",
        "description": "This soybean plant appears healthy with no visible signs of disease.",
        "symptoms": ["No disease symptoms detected", "Normal leaf color and pod development"],
        "causes": "N/A",
        "organic_treatment": "Maintain balanced nutrition and proper drainage.",
        "chemical_treatment": "No treatment required.",
        "prevention": "Crop rotation, certified seed, scouting from V2 stage.",
        "favorable_conditions": "N/A",
    },

    "Squash — Powdery Mildew": {
        "scientific_name": "Podosphaera xanthii",
        "crop": "Squash",
        "severity_class": "Medium",
        "description": (
            "Powdery mildew is the most common disease of cucurbit crops including squash. "
            "It causes a white powdery coating on leaf surfaces reducing photosynthesis "
            "and shortening the productive season."
        ),
        "symptoms": [
            "White powdery spots on upper and lower leaf surfaces",
            "Spots enlarge to cover entire leaf surface",
            "Yellow discoloration of affected leaves",
            "Premature leaf senescence and defoliation",
            "Reduced fruit size and quality",
        ],
        "causes": "Obligate fungal pathogen; favoured by warm dry days with cool nights and moderate humidity.",
        "organic_treatment": (
            "Apply potassium bicarbonate solution at 5 g/L every 7 days. "
            "Neem oil at 3 ml/L is effective when applied early. "
            "Sulfur-based fungicides every 7-10 days. "
            "Remove severely infected leaves to reduce inoculum."
        ),
        "chemical_treatment": (
            "Myclobutanil 20% WP at 0.25 g/L. "
            "Azoxystrobin 23% SC at 1 ml/L. "
            "Quinoxyfen 25% SC at 0.5 ml/L. "
            "Begin applications at first sign of disease."
        ),
        "prevention": (
            "Plant resistant squash varieties where available. "
            "Ensure adequate plant spacing for airflow. "
            "Avoid excessive nitrogen fertilization. "
            "Apply preventive sulfur during warm weather."
        ),
        "favorable_conditions": "Warm dry days 20-27 degrees C, cool nights, moderate humidity 50-70%",
    },

    "Strawberry — Leaf Scorch": {
        "scientific_name": "Diplocarpon earlianum",
        "crop": "Strawberry",
        "severity_class": "Medium",
        "description": (
            "Leaf scorch is a common fungal disease of strawberries causing purple spots "
            "that coalesce to give a scorched appearance to leaves. It weakens plants "
            "and reduces fruit yield and quality."
        ),
        "symptoms": [
            "Small dark purple spots on upper leaf surface",
            "Spots enlarge and coalesce giving scorched appearance",
            "Purple to brown lesions with gray centers",
            "Severe cases cause complete leaf browning",
            "Reduced runner production and plant vigor",
        ],
        "causes": "Fungal pathogen favoured by wet conditions; overwinters in infected leaves.",
        "organic_treatment": (
            "Remove and destroy infected leaves and plant debris. "
            "Apply copper-based fungicides preventively. "
            "Improve air circulation by removing excess runners. "
            "Avoid overhead irrigation."
        ),
        "chemical_treatment": (
            "Captan 50% WP at 2 g/L every 7-10 days. "
            "Myclobutanil 20% WP at 0.25 g/L. "
            "Azoxystrobin 23% SC at 1 ml/L. "
            "Apply from early spring through harvest."
        ),
        "prevention": (
            "Plant certified disease-free transplants. "
            "Use drip irrigation to minimize leaf wetness. "
            "Remove and destroy old foliage after harvest. "
            "Rotate strawberry beds every 3-4 years."
        ),
        "favorable_conditions": "Cool wet spring weather, overhead irrigation, dense plant canopy",
    },

    "Strawberry — Healthy": {
        "scientific_name": "N/A",
        "crop": "Strawberry",
        "severity_class": "None",
        "description": "This strawberry plant appears healthy with no visible signs of disease.",
        "symptoms": ["No disease symptoms detected", "Normal leaf color and runner production"],
        "causes": "N/A",
        "organic_treatment": "Continue preventive copper applications during wet periods.",
        "chemical_treatment": "No treatment required.",
        "prevention": "Regular monitoring, drip irrigation, remove old foliage.",
        "favorable_conditions": "N/A",
    },

    "Tomato — Bacterial Spot": {
        "scientific_name": "Xanthomonas vesicatoria",
        "crop": "Tomato",
        "severity_class": "Medium",
        "description": (
            "Bacterial spot causes significant defoliation and fruit blemishes in tomato, "
            "reducing marketability and plant yield. It spreads rapidly in warm wet conditions "
            "and can devastate crops if not managed early."
        ),
        "symptoms": [
            "Small water-soaked greasy spots on leaves",
            "Spots enlarge with yellow halo turning brown",
            "Spots turn brown and angular limited by leaf veins",
            "Severe defoliation in wet weather",
            "Raised scab-like lesions on green fruit",
        ],
        "causes": "Bacterial pathogen spread by rain splash, wind-driven rain, insects and contaminated tools.",
        "organic_treatment": (
            "Copper hydroxide 77% WDG at 2 g/L every 5-7 days. "
            "Avoid working in fields when foliage is wet. "
            "Remove and destroy heavily infected plant material. "
            "Use certified pathogen-free transplants."
        ),
        "chemical_treatment": (
            "Copper oxychloride plus Mancozeb combination spray. "
            "Streptomycin sulfate 200 ppm in early stages only. "
            "Kasugamycin 3% SL for systemic bactericidal action. "
            "Alternate copper with non-copper bactericides to prevent resistance."
        ),
        "prevention": (
            "Use certified disease-free seeds treated with hot water at 50 degrees C for 25 minutes. "
            "Drip irrigation instead of overhead to avoid leaf wetness. "
            "2-year crop rotation with non-solanaceous crops. "
            "Disinfect tools with bleach solution between plants."
        ),
        "favorable_conditions": "Temperature 24-30 degrees C, high humidity, frequent rain or overhead irrigation",
    },

    "Tomato — Early Blight": {
        "scientific_name": "Alternaria solani",
        "crop": "Tomato",
        "severity_class": "Medium",
        "description": (
            "Early blight is a very common fungal disease of tomato causing distinctive "
            "concentric ring lesions on older leaves. Severe infections cause significant "
            "defoliation and fruit rot."
        ),
        "symptoms": [
            "Dark brown circular spots with concentric rings on older leaves",
            "Yellow halo surrounding lesions",
            "Lesions enlarge and coalesce causing leaf yellowing",
            "Premature defoliation starting from lower leaves",
            "Dark leathery lesions at stem end of fruit",
        ],
        "causes": "Fungal pathogen favoured by warm humid conditions; spreads by wind and rain splash.",
        "organic_treatment": (
            "Neem oil at 3 ml/L every 5-7 days. "
            "Copper oxychloride 50% WP at 2 g/L. "
            "Remove and destroy infected lower leaves. "
            "Maintain adequate nitrogen nutrition."
        ),
        "chemical_treatment": (
            "Chlorothalonil 75% WP at 2 g/L every 7 days. "
            "Azoxystrobin 23% SC at 1 ml/L. "
            "Difenoconazole 25% EC at 0.5 ml/L. "
            "Apply preventively from transplanting onward."
        ),
        "prevention": (
            "Use certified disease-free transplants. "
            "Stake plants to improve air circulation. "
            "Apply mulch to reduce soil splash. "
            "Practice crop rotation with non-solanaceous crops."
        ),
        "favorable_conditions": "Warm days 24-29 degrees C, high humidity, wet foliage",
    },

    "Tomato — Late Blight": {
        "scientific_name": "Phytophthora infestans",
        "crop": "Tomato",
        "severity_class": "High",
        "description": (
            "Late blight is one of the most destructive diseases of tomato. "
            "It thrives in cool wet conditions and can destroy an entire field within days "
            "if left untreated. The same pathogen causes late blight in potato."
        ),
        "symptoms": [
            "Dark water-soaked lesions on leaves",
            "White mold on undersides of leaves during humid nights",
            "Rapid yellowing and wilting of foliage",
            "Brown-black rot on stems and petioles",
            "Firm brown rot on fruit",
        ],
        "causes": "Oomycete pathogen spread by wind-borne sporangia; thrives at 10-25 degrees C with humidity above 90%.",
        "organic_treatment": (
            "Remove and destroy infected plant material immediately. "
            "Apply copper hydroxide at 1.5-2.0 kg/ha every 5-7 days. "
            "Use Bordeaux mixture of 1:1 copper sulfate to lime. "
            "Ensure good drainage and improve air circulation by pruning."
        ),
        "chemical_treatment": (
            "Mancozeb 75% WP at 2.5 g/L water every 7 days. "
            "Metalaxyl plus Mancozeb Ridomil Gold for systemic plus contact protection. "
            "Cymoxanil plus Mancozeb as an alternative. "
            "Rotate fungicide classes to prevent resistance buildup."
        ),
        "prevention": (
            "Plant certified disease-free seeds and resistant varieties such as Mountain Magic. "
            "Avoid overhead irrigation and use drip instead. "
            "Space plants adequately for air movement. "
            "Scout fields weekly especially during cool wet periods. "
            "Destroy volunteer potato plants nearby."
        ),
        "favorable_conditions": "Temperature 10-25 degrees C, humidity above 90%, rainfall or heavy dew",
    },

    "Tomato — Leaf Mold": {
        "scientific_name": "Passalora fulva",
        "crop": "Tomato",
        "severity_class": "Medium",
        "description": (
            "Leaf mold is primarily a disease of greenhouse tomatoes but also affects "
            "field crops in humid conditions. It causes significant yield losses through "
            "defoliation and reduced photosynthesis."
        ),
        "symptoms": [
            "Pale green to yellow spots on upper leaf surface",
            "Olive-green to brown velvety mold on lower leaf surface",
            "Leaves curl and dry out as infection progresses",
            "Severe defoliation in greenhouse conditions",
            "Fruit infection causing dark leathery rot at blossom end",
        ],
        "causes": "Fungal pathogen favoured by high humidity above 85% and moderate temperatures.",
        "organic_treatment": (
            "Improve greenhouse ventilation to reduce humidity. "
            "Apply copper-based fungicides preventively. "
            "Remove infected leaves promptly. "
            "Reduce plant density to improve airflow."
        ),
        "chemical_treatment": (
            "Chlorothalonil 75% WP at 2 g/L. "
            "Mancozeb 75% WP at 2.5 g/L. "
            "Difenoconazole 25% EC at 0.5 ml/L. "
            "Apply on 7-day intervals during high-risk periods."
        ),
        "prevention": (
            "Maintain greenhouse humidity below 85% through ventilation. "
            "Use resistant tomato varieties where available. "
            "Avoid overhead watering especially in evenings. "
            "Stake and prune plants to maximize airflow."
        ),
        "favorable_conditions": "High humidity above 85%, temperature 21-24 degrees C, poor ventilation",
    },

    "Tomato — Septoria Leaf Spot": {
        "scientific_name": "Septoria lycopersici",
        "crop": "Tomato",
        "severity_class": "Medium",
        "description": (
            "Septoria leaf spot is one of the most common foliar diseases of tomato. "
            "It can cause complete defoliation of lower leaves and progresses rapidly "
            "up the plant under warm wet conditions."
        ),
        "symptoms": [
            "Small circular spots with dark brown borders and light gray centers",
            "Tiny black pycnidia visible in lesion centers",
            "Spots first appear on lower leaves",
            "Rapid defoliation progressing upward",
            "Fruit rarely infected directly",
        ],
        "causes": "Fungal pathogen that overwinters in infected crop debris; spread by rain splash and tools.",
        "organic_treatment": (
            "Remove infected lower leaves immediately. "
            "Apply copper-based fungicides preventively. "
            "Mulch around plants to reduce soil splash. "
            "Avoid working among wet plants."
        ),
        "chemical_treatment": (
            "Chlorothalonil 75% WP at 2 g/L every 7-10 days. "
            "Mancozeb 75% WP at 2.5 g/L. "
            "Azoxystrobin 23% SC at 1 ml/L for systemic activity. "
            "Begin applications when first symptoms appear."
        ),
        "prevention": (
            "Use certified disease-free transplants. "
            "Stake and prune plants for airflow. "
            "Mulch to prevent soil splash. "
            "Rotate with non-solanaceous crops for 2-3 years. "
            "Remove and destroy crop debris after harvest."
        ),
        "favorable_conditions": "Warm temperatures 20-25 degrees C, wet conditions, dense canopy",
    },

    "Tomato — Spider Mites": {
        "scientific_name": "Tetranychus urticae",
        "crop": "Tomato",
        "severity_class": "Medium",
        "description": (
            "Two-spotted spider mite is a major pest of tomato causing stippling and bronzing "
            "of leaves. Severe infestations can cause complete defoliation and significant "
            "yield loss, especially under hot dry conditions."
        ),
        "symptoms": [
            "Fine stippling or bronzing of upper leaf surface",
            "Fine webbing on undersides of leaves and between leaflets",
            "Tiny moving dots visible on leaf undersides with hand lens",
            "Yellowing and premature leaf drop",
            "Stunted plant growth in severe infestations",
        ],
        "causes": "Arachnid pest; population explosions triggered by hot dry conditions and pesticide disruption of natural enemies.",
        "organic_treatment": (
            "Apply insecticidal soap at 5 ml/L every 5-7 days covering undersides of leaves. "
            "Neem oil at 3 ml/L disrupts mite development. "
            "Release predatory mites Phytoseiulus persimilis as biological control. "
            "Strong water sprays to knock mites off plants."
        ),
        "chemical_treatment": (
            "Abamectin 1.8% EC at 0.5 ml/L. "
            "Spiromesifen 22.9% SC at 0.75 ml/L. "
            "Bifenazate 43% SC at 1 ml/L. "
            "Rotate acaricide classes to prevent resistance."
        ),
        "prevention": (
            "Avoid broad-spectrum insecticides that kill natural enemies. "
            "Maintain adequate irrigation to reduce plant stress. "
            "Monitor regularly with hand lens from transplanting. "
            "Remove heavily infested plant parts promptly."
        ),
        "favorable_conditions": "Hot dry conditions above 28 degrees C, low humidity, drought-stressed plants",
    },

    "Tomato — Target Spot": {
        "scientific_name": "Corynespora cassiicola",
        "crop": "Tomato",
        "severity_class": "Medium",
        "description": (
            "Target spot affects all above-ground parts of tomato plants causing "
            "characteristic concentric ring lesions. It can cause severe defoliation "
            "and fruit spotting reducing marketable yield."
        ),
        "symptoms": [
            "Brown circular lesions with concentric rings on leaves",
            "Water-soaked appearance on young lesions",
            "Dark brown spots with yellow halos on fruit",
            "Defoliation of lower leaves progressing upward",
            "Stem lesions in severe cases",
        ],
        "causes": "Fungal pathogen favoured by warm humid conditions; spread by wind and rain splash.",
        "organic_treatment": (
            "Remove infected lower leaves promptly. "
            "Apply copper-based fungicides preventively. "
            "Improve air circulation through staking and pruning. "
            "Avoid overhead irrigation."
        ),
        "chemical_treatment": (
            "Chlorothalonil 75% WP at 2 g/L every 7-10 days. "
            "Azoxystrobin 23% SC at 1 ml/L. "
            "Boscalid 50% WG at 0.5 g/L. "
            "Apply from early vegetative stage through harvest."
        ),
        "prevention": (
            "Use resistant tomato varieties where available. "
            "Stake plants for good airflow. "
            "Practice crop rotation. "
            "Remove crop debris after harvest."
        ),
        "favorable_conditions": "Temperature 20-30 degrees C, high humidity, wet foliage periods",
    },

    "Tomato — Yellow Leaf Curl Virus": {
        "scientific_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "crop": "Tomato",
        "severity_class": "High",
        "description": (
            "Tomato yellow leaf curl virus is one of the most devastating viral diseases of tomato worldwide. "
            "Transmitted by whitefly, it causes severe stunting and yield loss. "
            "There is no cure once plants are infected."
        ),
        "symptoms": [
            "Upward curling and cupping of young leaves",
            "Interveinal yellowing and chlorosis of leaves",
            "Severe stunting of plant growth",
            "Flower drop leading to greatly reduced fruit set",
            "Small misshapen fruit on infected plants",
        ],
        "causes": "Begomovirus transmitted by silverleaf whitefly Bemisia tabaci; no cure once infected.",
        "organic_treatment": (
            "Remove and destroy infected plants immediately to reduce virus spread. "
            "Control whitefly vector with reflective mulches and yellow sticky traps. "
            "Apply insecticidal soap to suppress whitefly populations. "
            "Release whitefly parasitoids Encarsia formosa as biological control."
        ),
        "chemical_treatment": (
            "Imidacloprid 70% WS as soil drench or seed treatment for whitefly control. "
            "Thiamethoxam 25% WG for vector management. "
            "Spirotetramat 15% OD for whitefly nymph control. "
            "No curative treatments exist for the virus itself."
        ),
        "prevention": (
            "Plant TYLCV-resistant tomato varieties. "
            "Use insect-proof net houses for transplant production. "
            "Install reflective mulch to repel whiteflies. "
            "Scout regularly and remove infected plants immediately. "
            "Avoid planting near infected fields."
        ),
        "favorable_conditions": "Warm dry conditions favoring whitefly populations, temperature 25-35 degrees C",
    },

    "Tomato — Mosaic Virus": {
        "scientific_name": "Tomato Mosaic Virus (ToMV)",
        "crop": "Tomato",
        "severity_class": "High",
        "description": (
            "Tomato mosaic virus causes mosaic patterns, distortion and stunting of tomato plants. "
            "It is highly stable and easily transmitted mechanically through contact and tools. "
            "There is no cure for infected plants."
        ),
        "symptoms": [
            "Light and dark green mosaic mottling pattern on leaves",
            "Leaf distortion and shoestring appearance of leaflets",
            "Stunted plant growth",
            "Reduced fruit set and misshapen fruit",
            "Internal browning of fruit in severe cases",
        ],
        "causes": "Tobamovirus transmitted mechanically through contact, tools, and infected seed; extremely stable in soil.",
        "organic_treatment": (
            "Remove and destroy infected plants immediately. "
            "Disinfect tools with 10% trisodium phosphate or bleach solution. "
            "Wash hands thoroughly before handling plants. "
            "Do not smoke near plants as tobacco products carry related viruses."
        ),
        "chemical_treatment": (
            "No curative chemical treatments exist for viral infections. "
            "Focus entirely on prevention and sanitation measures. "
            "Mild strain cross-protection is used in some commercial operations."
        ),
        "prevention": (
            "Use certified virus-free seed. "
            "Plant ToMV-resistant varieties with Tm-2 resistance gene. "
            "Disinfect all tools and equipment before use. "
            "Remove and destroy infected plants immediately. "
            "Avoid handling plants after using tobacco products."
        ),
        "favorable_conditions": "Spreads rapidly in any condition through mechanical contact and tools",
    },

    "Tomato — Healthy": {
        "scientific_name": "N/A",
        "crop": "Tomato",
        "severity_class": "None",
        "description": "This tomato plant appears healthy with no signs of disease or pest damage.",
        "symptoms": ["No disease symptoms detected", "Normal leaf color and texture", "Healthy plant morphology"],
        "causes": "N/A",
        "organic_treatment": "Continue regular monitoring and preventive care.",
        "chemical_treatment": "No treatment required.",
        "prevention": (
            "Maintain regular scouting schedule. "
            "Continue good cultural practices including proper spacing, drip irrigation and balanced nutrition. "
            "Apply preventive copper sprays during high-risk weather periods."
        ),
        "favorable_conditions": "N/A",
    },
}


def get_disease_info(disease_name: str) -> dict:
    """Fuzzy lookup — tries exact match then partial match."""
    if disease_name in DISEASE_DB:
        return DISEASE_DB[disease_name]
    lower = disease_name.lower()
    for key, val in DISEASE_DB.items():
        if lower in key.lower() or key.lower() in lower:
            return val
    return {
        "scientific_name":    "Unknown",
        "crop":               disease_name.split(" — ")[0] if " — " in disease_name else "Unknown",
        "severity_class":     "Unknown",
        "description":        f"Detailed information for {disease_name} is being added to the database.",
        "symptoms":           ["Consult a local agricultural expert for this disease."],
        "causes":             "Consult local extension services.",
        "organic_treatment":  "Consult local extension services.",
        "chemical_treatment": "Consult local extension services.",
        "prevention":         "Maintain good agricultural practices and regular field scouting.",
        "favorable_conditions": "Varies",
    }


def get_all_diseases() -> list:
    return [
        {"name": k, "crop": v["crop"], "severity_class": v["severity_class"]}
        for k, v in DISEASE_DB.items()
    ]
