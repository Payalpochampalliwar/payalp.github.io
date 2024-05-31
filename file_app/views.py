import pandas as pd
from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import DPDCount

def index(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            data = pd.read_excel(file.file)
            dpd_counts = data.groupby(['Cust State', 'DPD']).size().reset_index(name='count')
            dpd_counts['Cust State'] = dpd_counts['Cust State']
            dpd_counts = dpd_counts[['Cust State', 'DPD', 'count']]
            DPDCount.objects.bulk_create(dpd_counts.apply(lambda row: DPDCount(state=row['Cust State'], dpd=row['DPD'], count=row['count']), axis=1).tolist())
            return redirect('index')
    else:
        form = FileUploadForm()

    dpd_counts = DPDCount.objects.all()
    context = {'form': form, 'dpd_counts': dpd_counts}
    return render(request, 'index.html', context)