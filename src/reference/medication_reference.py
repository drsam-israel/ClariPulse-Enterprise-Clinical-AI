MEDICATION_REFERENCE = {

    "Metformin": {
        "drug_class": "Biguanide",
        "route": "Oral",
        "frequency": "Twice Daily",
        "default_dose": "500 mg",
    },

    "Insulin Glargine": {
        "drug_class": "Insulin",
        "route": "Subcutaneous",
        "frequency": "Once Daily",
        "default_dose": "10 units",
    },

    "Amlodipine": {
        "drug_class": "Calcium Channel Blocker",
        "route": "Oral",
        "frequency": "Once Daily",
        "default_dose": "5 mg",
    },

    "Lisinopril": {
        "drug_class": "ACE Inhibitor",
        "route": "Oral",
        "frequency": "Once Daily",
        "default_dose": "10 mg",
    },

    "Losartan": {
        "drug_class": "Angiotensin Receptor Blocker",
        "route": "Oral",
        "frequency": "Once Daily",
        "default_dose": "50 mg",
    },

    "Furosemide": {
        "drug_class": "Loop Diuretic",
        "route": "Oral",
        "frequency": "Once Daily",
        "default_dose": "40 mg",
    },

    "Atorvastatin": {
        "drug_class": "Statin",
        "route": "Oral",
        "frequency": "Nightly",
        "default_dose": "40 mg",
    },

    "Aspirin": {
        "drug_class": "Antiplatelet",
        "route": "Oral",
        "frequency": "Once Daily",
        "default_dose": "81 mg",
    },

    "Salbutamol": {
        "drug_class": "Bronchodilator",
        "route": "Inhalation",
        "frequency": "As Needed",
        "default_dose": "2 puffs",
    },

    "Budesonide": {
        "drug_class": "Inhaled Corticosteroid",
        "route": "Inhalation",
        "frequency": "Twice Daily",
        "default_dose": "200 mcg",
    },

    "Omeprazole": {
        "drug_class": "Proton Pump Inhibitor",
        "route": "Oral",
        "frequency": "Once Daily",
        "default_dose": "20 mg",
    },

    "Paracetamol": {
        "drug_class": "Analgesic",
        "route": "Oral",
        "frequency": "As Needed",
        "default_dose": "1 g",
    },

    "Enoxaparin": {
        "drug_class": "Anticoagulant",
        "route": "Subcutaneous",
        "frequency": "Once Daily",
        "default_dose": "40 mg",
    },

    "Ceftriaxone": {
        "drug_class": "Cephalosporin Antibiotic",
        "route": "Intravenous",
        "frequency": "Once Daily",
        "default_dose": "1 g",
    },

    "Vancomycin": {
        "drug_class": "Glycopeptide Antibiotic",
        "route": "Intravenous",
        "frequency": "Every 12 Hours",
        "default_dose": "1 g",
    },

    "Piperacillin-Tazobactam": {
        "drug_class": "Broad-Spectrum Antibiotic",
        "route": "Intravenous",
        "frequency": "Every 8 Hours",
        "default_dose": "4.5 g",
    },

}
DIAGNOSIS_TO_MEDICATION = {
    "E11.9": ["Metformin"],
    "I10": ["Amlodipine", "Lisinopril"],
    "N18.3": ["Losartan"],
    "I50.9": ["Furosemide"],
    "J44.9": ["Salbutamol", "Budesonide"],
    "A41.9": ["Piperacillin-Tazobactam", "Vancomycin"],
    "K21.9": ["Omeprazole"],
    "C34.9": ["Paracetamol"],
    "I21.9": ["Aspirin", "Atorvastatin"],
    "I63.9": ["Aspirin", "Atorvastatin"],
    "N39.0": ["Ceftriaxone"],
}