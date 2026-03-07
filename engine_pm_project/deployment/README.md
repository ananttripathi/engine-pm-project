---
title: Engine Predictive Maintenance
emoji: 🔧
sdk: streamlit
sdk_version: "1.28.0"
app_file: app.py
pinned: false
---

# Engine Predictive Maintenance

Predict engine condition (**Normal** vs **Maintenance Required**) from sensor readings.  
Model is loaded from the [Hugging Face model hub](https://huggingface.co/ananttripathiak/engine-pm-model).

## Sensor inputs

- Engine RPM, Lub oil pressure, Fuel pressure, Coolant pressure  
- Lub oil temperature, Coolant temperature  

Enter values and click **Predict** to get the classification.
