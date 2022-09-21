from django.shortcuts import render
from django.views.generic import TemplateView
import pandas as pd
import numpy as np
import pickle
from pickle import dump
from pickle import load
from django.conf import settings
import os
import json

def home(request):
    return render(request,template_name='forecast/home.html')


def predict(request):
    if request.method == 'POST':
        print(request.POST['days'])
        try:
            days = int(request.POST['days'])
                        
            # Loading the model we already created
            model=load(open(os.path.join(settings.BASE_DIR,'forecast/assets/hwf.sav'),'rb'))
            predictions=model.forecast(days)
            pred_df=pd.DataFrame({"Prediction":predictions})
            pred_df.insert(loc=0, column='Date', value=pred_df.index.strftime('%d/%m/%Y'))
            pred_df = pred_df.round(2)
            pred_df = pred_df.reset_index(drop=True)
            # parsing the DataFrame in json format.
            pred_df.index = np.arange(1, len(pred_df) + 1)
            json_records = pred_df.reset_index().to_json(orient ='records')
            data = []
            data = json.loads(json_records)
            return render(request,template_name='forecast/home.html',context={
                'column_names':['Number of Day','Date','Price'], 
                'data':data,
                'legend' : f'Gold Forecast for {days} days',
                'labels':pred_df['Date'].values,
                'values' : pred_df['Prediction'].values
                })
        except ValueError:
            error = "Please enter valid values"
            return render(request,template_name='forecast/home.html', context={'error':error})
    return render(request,template_name='forecast/home.html')

