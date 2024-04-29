from django.shortcuts import render

# Create your views here.

from .models import Brand, Tech, Shoe

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_brands = Brand.objects.all().count()
    num_shoes = Shoe.objects.all().count()
    num_tech = Tech.objects.all().count()


    context = {
        'num_brands': num_brands,
        'num_shoes': num_shoes,
        'num_tech': num_tech,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic

class ShoeListView(generic.ListView):
    model = Shoe
    context_object_name = 'shoe_list'

class ShoeDetailView(generic.DetailView):
    model = Shoe
    
class BrandListView(generic.ListView):
    model = Brand
    context_object_name = 'brand_list'

class BrandDetailView(generic.DetailView):
    model = Brand

from django.views import generic
from django.db import connection
from django.shortcuts import render
from .forms import Report
import os
from django.conf import settings
import sqlite3


class Reports(generic.TemplateView):
    template_name = 'report_view.html'  # Updated template name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = Report(self.request.GET or None)
        context['form'] = form
        context['result'] = None
        return context

    def post(self, request, *args, **kwargs):
        form = Report(request.POST)
        result = None

        if form.is_valid():
            shoe_name = form.cleaned_data['shoe_name']
            brand_name = form.cleaned_data['brand_name']
            lockdown_q = int(form.cleaned_data['lockdown_q'])
            traction_q = int(form.cleaned_data['traction_q'])
            comfort_q = int(form.cleaned_data['comfort_q'])
            looks_q = int(form.cleaned_data['looks_q'])

            sql_query = """
                SELECT *
                FROM catalog_shoe s INNER JOIN catalog_brand b ON s.brand_id = b.id INNER JOIN catalog_shoe_tech t ON s.id = t.shoe_id
                WHERE s.name LIKE ?
                    AND b.name LIKE ?
                    AND s.lockdown >= ?
                    AND s.traction >= ?
                    AND s.comfort >= ?
                    AND s.looks >= ?
                """
            parameters = [shoe_name, brand_name, lockdown_q, traction_q, comfort_q, looks_q]

            db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_query, parameters)
                result = cursor.fetchall()

        context = self.get_context_data(**kwargs)
        context['form'] = form
        context['result'] = result

        return render(request, self.template_name, context)
import logging
logger = logging.getLogger()
import sqlite3
from django.shortcuts import render
from django.db.models import Avg

def report_results(request):
    if request.method == 'POST':
        form = Report(request.POST)
        if form.is_valid():
            shoe_name = form.cleaned_data['shoe_name']
            brand_name = form.cleaned_data['brand_name']
            lockdown_q = int(form.cleaned_data['lockdown_q'])
            traction_q = int(form.cleaned_data['traction_q'])
            comfort_q = int(form.cleaned_data['comfort_q'])
            looks_q = int(form.cleaned_data['looks_q'])

            db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()

                # Execute the query and fetch the results
                sql_query = """
                    SELECT s.name, b.name, s.lockdown, s.traction, s.comfort, s.looks, tech.name
                    FROM catalog_shoe s
                    INNER JOIN catalog_brand b ON s.brand_id = b.id
                    INNER JOIN catalog_shoe_tech t ON s.id = t.shoe_id
                    INNER JOIN catalog_tech tech ON t.tech_id = tech.techId
                    WHERE s.name LIKE ?
                        AND b.name LIKE ?
                        AND s.lockdown >= ?
                        AND s.traction >= ?
                        AND s.comfort >= ?
                        AND s.looks >= ?
                """
                parameters = (
                    f"%{shoe_name}%",
                    f"%{brand_name}%",
                    lockdown_q, traction_q, comfort_q, looks_q
                )
                cursor.execute(sql_query, parameters)
                result = cursor.fetchall()

                # Calculate the column averages
                avg_query = """
                    SELECT
                        AVG(s.lockdown) AS avg_lockdown,
                        AVG(s.traction) AS avg_traction,
                        AVG(s.comfort) AS avg_comfort,
                        AVG(s.looks) AS avg_looks
                    FROM catalog_shoe s
                    INNER JOIN catalog_brand b ON s.brand_id = b.id
                    INNER JOIN catalog_shoe_tech t ON s.id = t.shoe_id
                    WHERE s.lockdown >= ?
                        AND s.traction >= ?
                        AND s.comfort >= ?
                        AND s.looks >= ?
                """
                cursor.execute(avg_query, (lockdown_q, traction_q, comfort_q, looks_q))
                averages = cursor.fetchone()

            context = {
                'form': form,
                'result': result,
                'averages': averages,
            }
            return render(request, 'report_results.html', context)
    else:
        form = Report()

    return render(request, 'report_form.html', {'form': form})

from django.shortcuts import get_object_or_404
from .models import Brand, Shoe

def brand_detail_view(request, brand_id):
    print("Entering brand_detail_view")

    brand_temp = get_object_or_404(Brand, brandId=brand_id)
    related_shoes = Shoe.objects.filter(brand=brand_temp)
    print(related_shoes)
    context = {
        'brand': brand_temp,
        'related_shoes': related_shoes,
    }

    return render(request, 'brand_detail.html', context)
