# ============================================================
#  PhytoSense — AI Chatbot Route (Rule-Based, No API Key)
#  backend/routes/chat.py
# ============================================================

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import re

chat_bp = Blueprint("chat", __name__)

KNOWLEDGE = {
    "tomato blight|late blight|tomato late": {
        "title": "Tomato Late Blight",
        "body": "Cause: Fungus Phytophthora infestans\n\nSymptoms:\n- Dark brown water-soaked spots on leaves\n- White fuzzy growth under leaves in humid weather\n- Stems turn black, fruit develops brown rot\n\nTreatment:\n- Remove and destroy all infected parts immediately\n- Apply copper-based fungicide every 7-10 days\n- Use Mancozeb or Chlorothalonil spray\n\nPrevention:\n- Avoid overhead watering\n- Plant resistant varieties\n- Ensure good air circulation\n- Rotate crops every year"
    },
    "tomato early blight|early blight": {
        "title": "Tomato Early Blight",
        "body": "Cause: Fungus Alternaria solani\n\nSymptoms:\n- Dark brown spots with concentric rings (target pattern)\n- Yellow area around spots\n- Lower leaves affected first\n\nTreatment:\n- Remove affected lower leaves\n- Apply Mancozeb, Azoxystrobin, or Copper fungicide\n- Spray every 7-14 days\n\nPrevention:\n- Mulch soil to prevent soil splash\n- Water at base of plant\n- Crop rotation every season"
    },
    "tomato leaf mold|leaf mold": {
        "title": "Tomato Leaf Mold",
        "body": "Cause: Fungus Passalora fulva\n\nSymptoms:\n- Yellow patches on upper leaf surface\n- Olive-green mold on underside of leaves\n- Leaves curl and dry up\n\nTreatment:\n- Improve ventilation\n- Apply Chlorothalonil or Mancozeb\n- Remove severely infected leaves\n\nPrevention:\n- Keep humidity below 85%\n- Space plants for airflow"
    },
    "septoria|septoria leaf": {
        "title": "Septoria Leaf Spot",
        "body": "Cause: Fungus Septoria lycopersici\n\nSymptoms:\n- Small circular spots with dark border and light center\n- Tiny black dots inside spots\n- Starts on lower leaves\n\nTreatment:\n- Remove infected leaves\n- Apply Mancozeb or Chlorothalonil\n\nPrevention:\n- Avoid wetting foliage\n- Crop rotation\n- Remove plant debris after harvest"
    },
    "spider mite|two.spotted": {
        "title": "Spider Mites",
        "body": "Cause: Tetranychus urticae (pest)\n\nSymptoms:\n- Tiny yellow/white stippling on leaves\n- Fine webbing on undersides\n- Leaves turn bronze and drop\n\nTreatment:\n- Spray strong water jet to dislodge mites\n- Apply neem oil or insecticidal soap\n- Use miticide: Abamectin\n\nPrevention:\n- Keep plants well watered\n- Introduce predatory mites\n- Avoid dusty conditions"
    },
    "yellow leaf curl|curl virus|ylcv": {
        "title": "Tomato Yellow Leaf Curl Virus",
        "body": "Cause: Virus spread by whiteflies\n\nSymptoms:\n- Leaves curl upward and turn yellow\n- Stunted plant growth\n- Reduced fruit set\n\nTreatment:\n- No cure - remove and destroy infected plants\n- Control whiteflies with yellow sticky traps\n- Apply systemic insecticide\n\nPrevention:\n- Use resistant TY varieties\n- Reflective mulch repels whiteflies\n- Install insect-proof netting"
    },
    "mosaic virus|tomato mosaic": {
        "title": "Tomato Mosaic Virus",
        "body": "Cause: Tobacco/Tomato Mosaic Virus\n\nSymptoms:\n- Mottled light/dark green pattern on leaves\n- Leaves distorted\n- Stunted growth\n\nTreatment:\n- No cure - remove infected plants\n- Disinfect tools with soap\n\nPrevention:\n- Use certified virus-free seeds\n- Control aphids\n- Wash hands before handling plants"
    },
    "target spot": {
        "title": "Target Spot",
        "body": "Cause: Fungus Corynespora cassiicola\n\nSymptoms:\n- Brown spots with concentric rings\n- Spots merge causing large dead areas\n\nTreatment:\n- Apply Azoxystrobin or Boscalid\n- Remove heavily infected leaves\n\nPrevention:\n- Improve air circulation\n- Avoid overhead irrigation"
    },
    "bacterial spot|bacterial": {
        "title": "Bacterial Spot",
        "body": "Cause: Xanthomonas bacteria\n\nSymptoms:\n- Small water-soaked spots on leaves\n- Spots turn brown with yellow halo\n- Raised scab-like spots on fruit\n\nTreatment:\n- Apply copper-based bactericide\n- Remove infected plant parts\n\nPrevention:\n- Use certified disease-free seed\n- Avoid overhead watering\n- Rotate crops every 2-3 years"
    },
    "potato blight|potato late|potato early": {
        "title": "Potato Blight",
        "body": "Cause: Fungus Phytophthora infestans\n\nSymptoms:\n- Dark water-soaked spots on leaves\n- White mold in wet weather\n- Tubers develop brown rot\n\nTreatment:\n- Apply Mancozeb or copper fungicide\n- Destroy all infected material\n\nPrevention:\n- Plant certified disease-free seed potatoes\n- Use resistant varieties\n- Avoid overhead irrigation"
    },
    "apple scab|scab": {
        "title": "Apple Scab",
        "body": "Cause: Fungus Venturia inaequalis\n\nSymptoms:\n- Olive-green to black spots on leaves\n- Scabby spots on fruit\n- Early leaf drop\n\nTreatment:\n- Apply Captan or Myclobutanil fungicide\n- Spray every 7-14 days in wet spring\n- Remove fallen leaves in autumn\n\nPrevention:\n- Plant resistant varieties\n- Prune for good air circulation"
    },
    "apple black rot|black rot": {
        "title": "Apple Black Rot",
        "body": "Cause: Fungus Botryosphaeria obtusa\n\nSymptoms:\n- Purple spots on leaves\n- Fruit rots from calyx, turns black\n- Cankers on branches\n\nTreatment:\n- Prune out all cankered wood\n- Apply Captan fungicide\n- Remove mummified fruit\n\nPrevention:\n- Remove dead wood promptly\n- Maintain tree vigor"
    },
    "cedar rust|cedar apple": {
        "title": "Cedar Apple Rust",
        "body": "Cause: Fungus Gymnosporangium juniperi-virginianae\n\nSymptoms:\n- Bright orange/yellow spots on leaves\n- Orange tube-like structures under leaves\n\nTreatment:\n- Apply Myclobutanil from pink bud stage\n- Spray every 7-10 days for 3-4 applications\n\nPrevention:\n- Remove nearby juniper/cedar trees\n- Apply protective fungicide in spring"
    },
    "grape black rot": {
        "title": "Grape Black Rot",
        "body": "Cause: Fungus Guignardia bidwellii\n\nSymptoms:\n- Brown circular lesions on leaves\n- Berries shrivel into black mummies\n\nTreatment:\n- Apply Mancozeb or Myclobutanil\n- Remove all mummified berries\n\nPrevention:\n- Prune for good air circulation\n- Apply protective fungicide from bud break"
    },
    "esca|black measles": {
        "title": "Grape Esca (Black Measles)",
        "body": "Cause: Complex of fungi\n\nSymptoms:\n- Tiger-stripe pattern on leaves\n- Black spots on berries\n- Dark wood streaking\n\nTreatment:\n- No complete cure\n- Remove severely affected vines\n- Paint pruning wounds with fungicide\n\nPrevention:\n- Protect pruning wounds immediately\n- Use clean pruning tools"
    },
    "gray leaf spot|cercospora corn": {
        "title": "Corn Gray Leaf Spot",
        "body": "Cause: Fungus Cercospora zeae-maydis\n\nSymptoms:\n- Long rectangular gray/tan lesions\n- Parallel to leaf veins\n\nTreatment:\n- Apply Azoxystrobin or Propiconazole at tasseling\n\nPrevention:\n- Plant resistant hybrids\n- Crop rotation\n- Bury infected residue with tillage"
    },
    "common rust|corn rust": {
        "title": "Corn Common Rust",
        "body": "Cause: Fungus Puccinia sorghi\n\nSymptoms:\n- Brick-red/brown pustules on both leaf surfaces\n- Leaves turn yellow severely\n\nTreatment:\n- Apply Azoxystrobin or Trifloxystrobin early\n\nPrevention:\n- Plant resistant hybrids\n- Early planting\n- Monitor fields regularly"
    },
    "northern leaf blight|nlb": {
        "title": "Northern Leaf Blight",
        "body": "Cause: Fungus Exserohilum turcicum\n\nSymptoms:\n- Long cigar-shaped gray-green lesions (1-6 inches)\n\nTreatment:\n- Apply Propiconazole before tasseling\n\nPrevention:\n- Plant resistant hybrids\n- Crop rotation\n- Residue management"
    },
    "powdery mildew|powdery": {
        "title": "Powdery Mildew",
        "body": "Cause: Various powdery mildew fungi\n\nSymptoms:\n- White powdery coating on leaf surfaces\n- Leaves curl and distort\n- Affects squash, cherry, grape, wheat\n\nTreatment:\n- Apply sulfur-based fungicide\n- Neem oil spray (organic)\n- Potassium bicarbonate spray\n\nPrevention:\n- Plant resistant varieties\n- Avoid excessive nitrogen\n- Ensure good air circulation"
    },
    "citrus greening|huanglongbing|hlb": {
        "title": "Citrus Greening (HLB)",
        "body": "Cause: Bacteria spread by psyllid insects\n\nSymptoms:\n- Asymmetric yellowing of leaves\n- Fruit stays green, tastes bitter\n- Stunted growth, twig dieback\n\nTreatment:\n- No cure - remove and destroy infected trees\n- Control Asian citrus psyllid\n\nPrevention:\n- Use certified disease-free stock\n- Monitor psyllid populations"
    },
    "irrigat|watering|drip": {
        "title": "Irrigation Best Practices",
        "body": "When to water:\n- Water in early morning to reduce disease\n- Check soil 2-3 inches deep before watering\n- Water when top 2 inches feel dry\n\nHow to water:\n- Drip irrigation is best - keeps foliage dry\n- Avoid overhead sprinklers\n- Water deeply but less frequently\n\nSigns of stress:\n- Underwatering: wilting, yellowing, leaf curl\n- Overwatering: yellowing, root rot, fungal disease\n\nTip: Mulch soil to retain moisture and reduce watering by 30-50%"
    },
    "fertiliz|nutrient|npk|nitrogen": {
        "title": "Fertilization Guide",
        "body": "NPK Basics:\n- N (Nitrogen) - leaf/stem growth, dark green color\n- P (Phosphorus) - root development, flowering\n- K (Potassium) - disease resistance, fruit quality\n\nDeficiency signs:\n- Yellow leaves = Nitrogen deficiency\n- Purple leaves = Phosphorus deficiency\n- Brown leaf edges = Potassium deficiency\n\nSchedule:\n- Before planting: compost + balanced NPK (10-10-10)\n- Vegetative stage: high nitrogen\n- Flowering/fruiting: reduce N, increase P and K\n\nOrganic options: compost, bone meal, wood ash"
    },
    "soil|ph|acidic|alkaline": {
        "title": "Soil Health Guide",
        "body": "Ideal pH for crops:\n- Tomato: 6.0-6.8\n- Potato: 5.0-6.0\n- Corn: 5.8-7.0\n- Apple: 6.0-7.0\n- Grape: 5.5-6.5\n\nAdjusting pH:\n- Too acidic (low pH): Add agricultural lime\n- Too alkaline (high pH): Add sulfur or acidic compost\n\nImproving soil:\n- Add compost every season\n- Use cover crops in off-season\n- Minimize tillage"
    },
    "pest|insect|aphid|whitefly|thrip|caterpillar|worm": {
        "title": "Common Crop Pests",
        "body": "Aphids:\n- Tiny soft insects on stem tips\n- Treatment: Neem oil, insecticidal soap, ladybugs\n\nWhiteflies:\n- White flying insects under leaves\n- Treatment: Yellow sticky traps, neem oil\n\nThrips:\n- Silver streaks on leaves\n- Treatment: Spinosad, blue sticky traps\n\nCaterpillars:\n- Chewed leaves, droppings visible\n- Treatment: Bt (Bacillus thuringiensis)\n\nGeneral IPM: Monitor regularly, use beneficial insects, try organic first"
    },
    "organic|natural|organic farming": {
        "title": "Organic Farming Tips",
        "body": "Organic Disease Control:\n- Copper-based fungicides (approved organic)\n- Neem oil - broad spectrum\n- Baking soda spray for powdery mildew\n- Compost tea spray\n\nOrganic Pest Control:\n- Neem oil repels most insects\n- Insecticidal soap for soft insects\n- Diatomaceous earth for crawlers\n- Companion planting (basil repels aphids)\n\nSoil Building:\n- Compost, vermicompost, green manure\n- Cover crops - clover fixes nitrogen\n- Crop rotation\n\nTip: Healthy soil = healthy plants = fewer disease problems"
    },
    "crop rotation|rotation": {
        "title": "Crop Rotation Guide",
        "body": "Why rotate crops?\n- Breaks pest and disease cycles\n- Improves soil health\n- Reduces pesticide need\n\n4-year rotation:\n- Year 1: Solanaceae (tomato, potato, pepper)\n- Year 2: Legumes (beans, peas) - fix nitrogen\n- Year 3: Brassicas (cabbage, broccoli)\n- Year 4: Root crops (carrot, onion)\n\nKey rules:\n- Never plant same family 2 years in a row\n- Rotate at least 3-4 years for disease-prone crops\n- Keep records of what you planted where"
    },
    "harvest|when to harvest|ripe": {
        "title": "Harvest Guide",
        "body": "When to harvest:\n- Tomato: Full color, slight give when pressed\n- Potato: Vines die back, skin set (does not rub off)\n- Corn: Silks turn brown, kernels milky when pierced\n- Apple: Full color, comes off easily with gentle twist\n- Grape: Sweet taste test, seeds turn brown\n- Pepper: Full size, firm\n\nGeneral tips:\n- Harvest in cool morning hours\n- Handle gently to avoid bruising\n- Do not wash before storage\n- Harvest regularly to promote more production"
    },
    "seed|germination|sowing|planting": {
        "title": "Seed and Planting Guide",
        "body": "Seed selection:\n- Always use certified disease-free seeds\n- Treat seeds with fungicide before sowing\n- Store in cool, dry, dark place\n\nGermination:\n- Tomato: 21-27C soil temperature\n- Corn: Minimum 10C soil temperature\n- Keep soil moist but not waterlogged\n\nTransplanting:\n- Harden off seedlings 7-10 days before\n- Transplant on cloudy day or evening\n- Water well immediately after\n\nSpacing:\n- Tomato: 45-60 cm between plants\n- Corn: 25-30 cm plants, 75 cm rows\n- Potato: 30 cm plants, 75 cm rows"
    },
    "yield|production|increase yield": {
        "title": "Improving Crop Yield",
        "body": "Top ways to increase yield:\n1. Soil health - add compost, test pH\n2. Proper spacing - crowded plants = low yield\n3. Timely fertilization - right nutrients at right stage\n4. Water management - consistent moisture\n5. Pest/disease control - early detection is key\n6. Pruning - remove suckers in tomato\n7. Pollination - hand pollinate if bees are scarce\n\nVariety selection:\n- Use high-yielding certified varieties\n- Disease-resistant varieties = less losses\n\nQuick wins:\n- Mulching increases yield 20-30%\n- Drip irrigation saves 40% water + better yield"
    },
    "weather|frost|drought|humidity": {
        "title": "Weather and Crop Management",
        "body": "Disease risk by weather:\n- High humidity + warm = Fungal disease risk\n- Cool + wet = Blight risk\n- Hot + dry = Spider mite risk\n- After rain: Inspect plants within 24-48 hours\n\nFrost protection:\n- Cover plants with cloth before frost\n- Water soil before frost (holds heat)\n- Use row covers or cold frames\n\nDrought management:\n- Mulch heavily to retain moisture\n- Water deeply once a week\n- Shade cloth reduces heat stress\n\nWind protection:\n- Stake tall plants\n- Use windbreaks for exposed fields"
    },
}

SUGGESTIONS_BY_TOPIC = {
    "tomato": ["Tomato early blight", "Tomato mosaic virus", "Septoria leaf spot", "Spider mites on tomato"],
    "potato": ["Potato blight treatment", "Crop rotation for potato", "When to harvest potato"],
    "apple": ["Apple scab treatment", "Apple black rot control", "Cedar apple rust prevention"],
    "grape": ["Grape black rot", "Esca grape disease", "Organic grape treatment"],
    "corn": ["Gray leaf spot corn", "Corn common rust", "Northern leaf blight"],
    "disease": ["Powdery mildew treatment", "Bacterial spot control", "Organic disease control"],
    "farm": ["Crop rotation guide", "Irrigation best practices", "How to increase yield", "Organic farming tips"],
}


def get_suggestions(topic="farm"):
    for key in SUGGESTIONS_BY_TOPIC:
        if key in topic:
            return SUGGESTIONS_BY_TOPIC[key][:3]
    return SUGGESTIONS_BY_TOPIC["farm"][:3]


def get_response(message):
    msg = message.lower().strip()

    for pattern, response in KNOWLEDGE.items():
        keywords = pattern.split("|")
        if any(re.search(kw, msg) for kw in keywords):
            topic = keywords[0].split()[0] if keywords else "farm"
            return {
                "reply": f"**{response['title']}**\n\n{response['body']}",
                "suggestions": get_suggestions(topic),
            }

    if any(w in msg for w in ["hello", "hi", "hey", "namaste", "good morning", "good evening", "start"]):
        return {
            "reply": "Hello! Welcome to PhytoSense Assistant!\n\nI can help you with:\n- Disease identification and treatment\n- Crop management and irrigation\n- Pest control and prevention\n- Soil health and fertilization\n- Harvesting and yield improvement\n\nWhat would you like to know about your crops today?",
            "suggestions": ["Tomato late blight treatment", "Organic farming tips", "Crop rotation guide", "Pest control methods"],
        }

    if any(w in msg for w in ["thank", "thanks", "thank you"]):
        return {
            "reply": "You are welcome! Happy farming! Feel free to ask anything else about your crops.",
            "suggestions": ["Disease treatment guide", "Irrigation tips", "Fertilization guide"],
        }

    if any(w in msg for w in ["yellow", "yellowing", "pale leaves"]):
        return {
            "reply": "Yellowing Leaves - Possible Causes:\n\n1. Nitrogen deficiency - oldest leaves yellow first\n   Fix: Apply nitrogen fertilizer\n\n2. Overwatering - roots cannot absorb nutrients\n   Fix: Reduce watering, improve drainage\n\n3. Viral disease - mosaic yellow/green pattern\n   Fix: Remove infected plants\n\n4. Iron deficiency - young leaves yellow, veins stay green\n   Fix: Apply chelated iron\n\nBest approach: Upload a photo to the Leaf Scanner for accurate diagnosis!",
            "suggestions": ["Nitrogen fertilizer guide", "Overwatering signs", "Viral disease treatment"],
        }

    if any(w in msg for w in ["brown spot", "brown spots", "spots on leaves"]):
        return {
            "reply": "Brown Spots - Common Causes:\n\n1. Fungal disease (most common)\n   - Early blight, Septoria, Target spot\n   - Apply: Mancozeb or Copper fungicide\n\n2. Bacterial disease\n   - Water-soaked spots turning brown\n   - Apply: Copper bactericide\n\n3. Sunscald\n   - White/brown on sun-exposed side\n   - Fix: Provide partial shade\n\n4. Calcium deficiency\n   - Blossom end rot in tomato\n   - Fix: Apply calcium foliar spray\n\nUpload a photo to the Leaf Scanner for accurate identification!",
            "suggestions": ["Early blight treatment", "Bacterial spot control", "Calcium deficiency fix"],
        }

    if any(w in msg for w in ["white powder", "white coating", "powdery", "white stuff on leaves"]):
        return {
            "reply": "White Coating on Leaves = Powdery Mildew!\n\nTreatment:\n- Apply sulfur-based fungicide immediately\n- Neem oil spray (organic option)\n- Baking soda: 1 tsp per 1 liter water\n- Remove heavily infected leaves\n\nPrevention:\n- Improve air circulation between plants\n- Avoid evening watering\n- Plant resistant varieties",
            "suggestions": ["Powdery mildew prevention", "Organic fungicide options", "Neem oil usage"],
        }

    if any(w in msg for w in ["wilting", "wilt", "drooping", "falling over"]):
        return {
            "reply": "Wilting Plants - Causes and Solutions:\n\n1. Underwatering (most common)\n   - Water immediately, check soil daily\n\n2. Root rot (overwatering)\n   - Reduce water, improve drainage\n   - Apply fungicide drench\n\n3. Fusarium wilt (fungal)\n   - Brown streaking inside stem\n   - Remove infected plants, rotate crops\n\n4. Bacterial wilt\n   - Sudden collapse, slimy stem ooze\n   - Remove immediately, control beetles\n\n5. Heat stress\n   - Plants perk up in evening\n   - Mulch, shade cloth, morning watering",
            "suggestions": ["Fusarium wilt treatment", "Root rot prevention", "Heat stress management"],
        }

    if any(w in msg for w in ["help", "what can you do", "features", "how to use"]):
        return {
            "reply": "PhytoSense Assistant can help you with:\n\nDisease Identification:\nAsk about any plant disease by name or symptoms\n\nTreatment Advice:\nGet specific fungicide and bactericide recommendations\n\nPrevention Tips:\nLearn how to prevent diseases before they start\n\nCrop Management:\nIrrigation, fertilization, soil health, harvesting\n\nPest Control:\nIdentify and manage common crop pests\n\nTry asking:\n- How to treat tomato late blight?\n- What causes powdery mildew?\n- Best irrigation practice for corn\n- How to increase tomato yield?\n- Organic pest control methods",
            "suggestions": ["Tomato disease guide", "Crop rotation tips", "Organic farming", "Pest control"],
        }

    return {
        "reply": "I am not sure about that specific topic, but I can help you with:\n- Plant diseases: blight, rust, mold, spots, wilt\n- Crop management: irrigation, fertilization, soil\n- Pest control and organic farming\n- Harvesting and yield improvement\n\nTry asking something like:\n- How to treat tomato late blight?\n- What causes powdery mildew?\n- Best organic pest control?\n\nOr use the Leaf Scanner to upload a photo for instant disease detection!",
        "suggestions": ["Tomato disease guide", "Crop rotation tips", "Organic farming", "Pest control methods"],
    }


@chat_bp.route("/chat", methods=["POST"])
@jwt_required()
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "No message provided"}), 400
    response = get_response(message)
    return jsonify(response), 200
