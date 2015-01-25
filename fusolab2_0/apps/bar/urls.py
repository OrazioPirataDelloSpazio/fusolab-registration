from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'addpurchasedproduct/$', 'bar.views.addpurchasedproduct', name='addpurchasedproduct'),
    url(r'deletereceipt/(?P<receiptid>\d+)/$', 'bar.views.deletereceipt'),
    url(r'smallbalance/(?P<balance_type>\w+)/$', 'bar.views.bar_smallbalance_form', name='bar_small_form'),
    url(r'balance/(?P<balance_type>\w+)/$', 'bar.views.bar_balance_form', name='bar_form'),
    url(r'csv','bar.csv_tool.create_resume', name='create_resume'),
    url(r'^guida_bar/$', TemplateView.as_view(template_name='bar/guida.html'), name='bar_guide'),
    url(r'^price_list/$', 'bar.views.price_list', name='bar_price_list'),
    url(r'^poll_price_list/$', 'bar.views.poll_price_list', name='bar_poll_price_list'),
    url(r'$', 'bar.views.barcash', name='barcash'),

)

