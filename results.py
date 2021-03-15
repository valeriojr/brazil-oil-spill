import json
from pathlib import Path
import pandas


pandas.options.display.width = 0

results = []
for grid_search_result in Path('.').glob('*_result*.json'):
    results.extend(json.loads(grid_search_result.read_text()))

for result in results:
    result['val_accuracy'] = max(result['history']['val_accuracy'])
    if result['val_accuracy'] == result['history']['val_accuracy'][-1] and result['val_accuracy'] != result['history']['val_accuracy'][-2]:
        result['need_retraining'] = True
    else:
        result['need_retraining'] = False

df = pandas.DataFrame([{
    **r['params'],
    'val_accuracy': r['val_accuracy'],
    'need_retraining': r['need_retraining'],
} for r in results])

df = df.sort_values(by='val_accuracy', ascending=False)
top10 = df[:10]

df.to_csv('grid_search_results.csv', index=False)
